#!/usr/bin/env python3
"""Render a saved Django test-run transcript as an Angular static template.

Example:
    python sre-tools/render_test_results.py \
        --input /tmp/django-test-run.txt \
        --output demo/static/templates/docs_tests_2026.html \
        --run-date 2026-10-01 \
        --command "python manage.py test -v 2"
"""

import argparse
from collections import OrderedDict
from html import escape
from pathlib import Path
import re


TEST_CASE_PATTERN = re.compile(r'^\S+ \((?P<test_case>[\w.]+)\) \.\.\.')
RUN_SUMMARY_PATTERN = re.compile(
    r'^(Ran \d+ tests?(?: in |$)|OK(?: \(|$)|FAILED(?: \(|$)|NO TESTS RAN)'
)
AREA_TITLES = {
    'assets': 'Assets and inventory',
    'summary': 'Reporting',
    'demo': 'Application and contact',
}
MODULE_TITLES = {
    'test_ai_assisted_dataset': 'AI-assisted dataset',
    'test_api_views': 'API views',
    'test_models': 'Models',
    'test_serializers': 'Serializers',
    'test_tenant_isolation': 'Tenant isolation',
    'test_ui_auth': 'UI authentication',
    'test_urls': 'URL routing',
    'test_user_api': 'User API',
    'test_user_creation_tool': 'User creation',
    'test_views': 'Page views',
}


def group_transcript(transcript):
    setup = []
    summary = []
    modules = OrderedDict()
    active_module = None
    tests_started = False

    for line in transcript.splitlines():
        match = TEST_CASE_PATTERN.match(line)
        if match:
            test_module = match.group('test_case').rsplit('.', 1)[0]
            modules.setdefault(test_module, []).append(line)
            active_module = test_module
            tests_started = True
        elif RUN_SUMMARY_PATTERN.match(line):
            summary.append(line)
            active_module = None
        elif active_module:
            modules[active_module].append(line)
        elif tests_started:
            summary.append(line)
        else:
            setup.append(line)

    if not modules:
        raise ValueError(
            'No verbose Django test cases found in the input transcript.'
        )

    return setup, summary, modules


def render_grouped_results(transcript):
    setup, summary, modules = group_transcript(transcript)
    areas = OrderedDict()
    for test_module, lines in modules.items():
        parts = test_module.split('.')
        area_key = parts[0]
        area_title = AREA_TITLES.get(
            area_key, area_key.replace('_', ' ').title()
        )
        module_key = parts[-1]
        module_title = MODULE_TITLES.get(
            module_key, module_key.replace('_', ' ').title()
        )
        areas.setdefault(area_title, []).append(
            (module_title, lines, len([
                line for line in lines if TEST_CASE_PATTERN.match(line)
            ]))
        )

    result_lines = []
    for line in summary:
        if line.startswith('Ran '):
            result_lines.append(
                '<p><strong>{}</strong></p>'.format(escape(line))
            )
        elif line.startswith(('OK', 'FAILED', 'NO TESTS RAN')):
            result_lines.append(
                '<p><strong>{}</strong></p>'.format(escape(line))
            )
        elif line.strip():
            result_lines.append(
                '<pre><code>{}</code></pre>'.format(escape(line))
            )

    setup_section = ''
    if any(line.strip() for line in setup):
        setup_section = '''  <details class="test-setup">
    <summary>Test database and setup output</summary>
    <pre><code>{}</code></pre>
  </details>
'''.format(escape('\n'.join(setup)))

    area_sections = []
    for area_title, area_modules in areas.items():
        area_count = sum(count for _, _, count in area_modules)
        module_sections = []
        for module_title, lines, count in area_modules:
            module_sections.append('''    <details class="test-module">
      <summary>{} — {} tests</summary>
      <pre><code>{}</code></pre>
    </details>'''.format(
                escape(module_title),
                count,
                escape('\n'.join(lines)),
            ))
        area_sections.append('''  <details class="test-area">
    <summary>{} — {} tests across {} modules</summary>
{}
  </details>'''.format(
            escape(area_title),
            area_count,
            len(area_modules),
            '\n'.join(module_sections),
        ))

    return setup_section, '\n'.join(area_sections), '\n'.join(result_lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--run-date', required=True)
    parser.add_argument('--command', required=True)
    args = parser.parse_args()

    transcript = args.input.read_text()
    setup, grouped_results, run_summary = render_grouped_results(transcript)
    command = escape(args.command)
    report = '''<div class="raw">
  <h1>Django Test Results — {run_date}</h1>
  <p>Command: <code>{command}</code></p>
  <h2>Results by app and test module</h2>
{setup}
{grouped_results}
  <h2>Run summary</h2>
{run_summary}
  <p><a href="#!/docs/tests/">Back to saved test runs</a></p>
</div>
'''.format(
        run_date=escape(args.run_date),
        command=command,
        setup=setup,
        grouped_results=grouped_results,
        run_summary=run_summary,
    )
    args.output.write_text(report)
    print('Saved test report to {}'.format(args.output))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
