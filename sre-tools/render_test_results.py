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
TEST_RESULT_PATTERN = re.compile(
    r'^(?P<name>\S+) \((?P<class>[\w.]+)\) \.\.\. (?P<status>.+)$'
)
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
MODULE_TEST_TYPES = {
    'test_ai_assisted_dataset': 'Dataset integration',
    'test_api_views': 'REST API',
    'test_models': 'Models and database',
    'test_serializers': 'API serializers',
    'test_tenant_isolation': 'Tenant isolation',
    'test_ui_auth': 'Server-side UI authentication',
    'test_urls': 'URL routing',
    'test_user_api': 'REST API',
    'test_user_creation_tool': 'Management tool',
    'test_views': 'Server-rendered views',
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
        test_type = MODULE_TEST_TYPES.get(
            module_key, 'Application tests'
        )
        test_rows = []
        for line in lines:
            match = TEST_RESULT_PATTERN.match(line)
            if match:
                test_rows.append(match.groupdict())
        module_filter = _filter_key('suite', test_module)
        type_filter = _filter_key('type', test_type)
        area_filter = _filter_key('area', area_key)
        areas.setdefault(area_key, {
            'title': area_title,
            'filter': area_filter,
            'modules': [],
        })['modules'].append({
            'title': module_title,
            'filter': module_filter,
            'type': test_type,
            'type_filter': type_filter,
            'lines': lines,
            'tests': test_rows,
        })

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

    all_test_types = OrderedDict()
    area_links = []
    suite_links = []
    area_sections = []
    for area_key, area in areas.items():
        area_modules = area['modules']
        area_count = sum(len(module['tests']) for module in area_modules)
        area_links.append(_filter_button(area['filter'], area['title']))
        module_sections = []
        for module in area_modules:
            all_test_types.setdefault(
                module['type_filter'], module['type']
            )
            suite_links.append(
                _filter_button(
                    module['filter'],
                    '{} · {}'.format(area['title'], module['title']),
                )
            )
            module_template = (
                '      <section class="test-module" '
                'ng-show="testResultsFilter === \'all\' || '
                'testResultsFilter === \'{}\' || '
                'testResultsFilter === \'{}\' || '
                'testResultsFilter === \'{}\'">\n'
                '        <h4>{}</h4>\n'
                '        <p class="test-module-meta">'
                '{} · {} cases · {}</p>\n'
                '        <table class="test-case-table" '
                'ng-show="testResultsFilter !== \'all\'">\n'
                '          <thead><tr><th>Test case</th>'
                '<th>Test class</th><th>Result</th></tr></thead>\n'
                '          <tbody>\n{}\n'
                '          </tbody>\n'
                '        </table>\n'
                '        <details class="test-raw-output" '
                'ng-show="testResultsFilter !== \'all\'">\n'
                '          <summary>Raw output</summary>\n'
                '          <pre><code>{}</code></pre>\n'
                '        </details>\n'
                '      </section>'
            )
            module_sections.append(module_template.format(
                area['filter'],
                module['type_filter'],
                module['filter'],
                escape(module['title']),
                escape(module['type']),
                len(module['tests']),
                _test_counts(module['tests']),
                '\n'.join(
                    (
                        '            <tr><td>{}</td><td>{}</td>'
                        '<td class="test-status {}">{}</td></tr>'
                    ).format(
                        escape(test['name']),
                        escape(test['class']),
                        _status_class(test['status']),
                        escape(test['status']),
                    )
                    for test in module['tests']
                ),
                escape('\n'.join(module['lines'])),
            ))
        area_template = (
            '  <section class="test-area" '
            'ng-show="testResultsFilter === \'all\' || '
            'testResultsFilter === \'{}\' || {}">\n'
            '    <h3>{} — {} cases across {} suites</h3>\n{}\n'
            '  </section>'
        )
        area_sections.append(area_template.format(
            area['filter'],
            ' || '.join(
                "testResultsFilter === '{}'".format(filter_key)
                for module in area_modules
                for filter_key in (
                    module['type_filter'],
                    module['filter'],
                )
            ),
            escape(area['title']),
            area_count,
            len(area_modules),
            '\n'.join(module_sections),
        ))

    type_links = [
        _filter_button(filter_key, label)
        for filter_key, label in all_test_types.items()
    ]
    navigation = '''  <nav class="test-results-nav"
       aria-label="Test result filters">
    <div class="test-results-nav-row">
      <strong>View:</strong>
{}
    </div>
    <div class="test-results-nav-row">
      <strong>Test area:</strong>
{}
    </div>
    <div class="test-results-nav-row">
      <strong>Test type:</strong>
{}
    </div>
    <div class="test-results-nav-row">
      <strong>Test suite:</strong>
{}
    </div>
  </nav>'''.format(
        _filter_button('all', 'Dashboard'),
        '\n'.join(area_links),
        '\n'.join(type_links),
        '\n'.join(suite_links),
    )
    return (
        setup_section,
        '\n'.join(area_sections),
        '\n'.join(result_lines),
        navigation,
    )


def _filter_key(prefix, value):
    slug = re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')
    return '{}-{}'.format(prefix, slug)


def _filter_button(filter_key, label):
    return (
        '      <button type="button" '
        'ng-click="setTestResultsFilter(\'{}\')" '
        'ng-class="{{ active: testResultsFilter === \'{}\' }}">{}</button>'
    ).format(
        filter_key,
        filter_key,
        escape(label),
    )


def _status_class(status):
    if status == 'ok' or status.startswith(
        ('skipped', 'expected failure')
    ):
        return 'passed'
    return 'failed'


def _test_counts(tests):
    passed = sum(
        1 for test in tests if _status_class(test['status']) == 'passed'
    )
    skipped = sum(
        1 for test in tests if test['status'].startswith('skipped')
    )
    failed = len(tests) - passed - skipped
    return '{} passed · {} skipped · {} problems'.format(
        passed, skipped, failed
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--run-date', required=True)
    parser.add_argument('--command', required=True)
    args = parser.parse_args()

    transcript = args.input.read_text()
    setup, grouped_results, run_summary, navigation = (
        render_grouped_results(transcript)
    )
    command = escape(args.command)
    report = '''<div class="raw">
  <h1>Django Test Results — {run_date}</h1>
  <p>Command: <code>{command}</code></p>
  <h2>Test results dashboard</h2>
{navigation}
  <p class="test-results-help">Choose an area, test type, or suite to see its
  cases. The dashboard lists coverage and counts; filtered views show each
  case, class, and result.</p>
{setup}
{grouped_results}
  <h2>Run summary</h2>
{run_summary}
  <p><a href="#!/docs/tests/">Back to saved test runs</a></p>
</div>
'''.format(
        run_date=escape(args.run_date),
        command=command,
        navigation=navigation,
        setup=setup,
        grouped_results=grouped_results,
        run_summary=run_summary,
    )
    args.output.write_text(report)
    print('Saved test report to {}'.format(args.output))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
