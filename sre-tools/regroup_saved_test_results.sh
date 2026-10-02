#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(dirname "$script_dir")
cd "$repo_root"

report=${1:-demo/static/templates/docs_tests_2026.html}
if [[ ! -f "$report" ]]; then
    printf 'ERROR: saved test report not found: %s\n' "$report" >&2
    exit 2
fi

transcript=$(mktemp "${TMPDIR:-/tmp}/dairyfarm-saved-tests.XXXXXX")
metadata=$(mktemp "${TMPDIR:-/tmp}/dairyfarm-report-metadata.XXXXXX")
staged_report=$(mktemp "${report}.tmp.XXXXXX")
trap 'rm -f "$transcript" "$metadata" "$staged_report"' EXIT

python3 - "$report" "$transcript" "$metadata" <<'PY'
from html.parser import HTMLParser
from pathlib import Path
import re
import sys


class SavedReportParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.heading = []
        self.command = []
        self.transcript = []
        self.capture_heading = False
        self.capture_command = False
        self.capture_summary = False
        self.summary_section = False
        self.heading_level = 0
        self.section_heading = []
        self.summary = []
        self.pre_depth = 0
        self.code_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h1':
            self.capture_heading = True
            self.heading_level = 1
        elif tag == 'h2':
            self.heading_level = 2
            self.section_heading = []
        elif tag == 'p' and self.summary_section:
            self.capture_summary = True
        elif tag == 'pre':
            self.pre_depth += 1
        elif tag == 'code':
            self.code_depth += 1
            if self.pre_depth == 0:
                self.capture_command = True

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.capture_heading = False
        elif tag == 'h2':
            if ''.join(self.section_heading).strip() == 'Run summary':
                self.summary_section = True
            self.heading_level = 0
        elif tag == 'p' and self.capture_summary:
            self.capture_summary = False
            if self.summary:
                self.summary.append('\n')
        elif tag == 'pre' and self.pre_depth:
            self.pre_depth -= 1
            self.code_depth = 0
        elif tag == 'code' and self.code_depth:
            self.code_depth -= 1
            if self.pre_depth == 0:
                self.capture_command = False
            else:
                self.transcript.append('\n')

    def handle_data(self, data):
        if self.capture_heading:
            self.heading.append(data)
        if self.heading_level == 2:
            self.section_heading.append(data)
        if self.capture_command:
            self.command.append(data)
        if self.capture_summary:
            self.summary.append(data)
        if self.pre_depth and self.code_depth:
            self.transcript.append(data)


report_path, transcript_path, metadata_path = map(Path, sys.argv[1:])
parser = SavedReportParser()
parser.feed(report_path.read_text())
heading = ''.join(parser.heading).strip()
command = ''.join(parser.command).strip()
transcript = ''.join(parser.transcript)
summary_lines = [
    line.strip() for line in ''.join(parser.summary).splitlines()
    if re.match(r'^(Ran \d+ tests?(?: in |$)|OK(?: \(|$)|FAILED(?: \(|$)|NO TESTS RAN)',
                 line.strip())
]
summary_lines = list(dict.fromkeys(summary_lines))
transcript = re.sub(
    r'(?<!\n)(test_\w+ \([\w.]+\) \.\.\.)', r'\n\1', transcript
)

date_match = re.search(r'(\d{4}-\d{2}-\d{2})$', heading)
if not date_match:
    raise SystemExit('ERROR: cannot read run date from the saved report title.')
if not command:
    raise SystemExit('ERROR: cannot read the test command from the saved report.')
if not re.search(r'^\S+ \([\w.]+\) \.\.\.', transcript, re.MULTILINE):
    raise SystemExit('ERROR: no verbose test cases found in the saved report.')
test_rows = re.findall(r'^\S+ \([\w.]+\) \.\.\. (.+)$', transcript, re.MULTILINE)
if not any(line.startswith('Ran ') for line in summary_lines):
    summary_lines.insert(0, 'Ran {} tests'.format(len(test_rows)))
if not any(line.startswith(('OK', 'FAILED', 'NO TESTS RAN'))
           for line in summary_lines):
    if test_rows and all(result == 'ok' for result in test_rows):
        summary_lines.append('OK')
if summary_lines:
    transcript += '\n' + '\n'.join(summary_lines) + '\n'

transcript_path.write_text(transcript)
metadata_path.write_text('{}\n{}'.format(date_match.group(1), command))
PY

run_date=$(sed -n '1p' "$metadata")
command_text=$(sed -n '2p' "$metadata")
printf 'Regrouping saved test results from %s...\n' "$report"
sre-tools/run_and_publish_test_results.sh \
    --input "$transcript" \
    --output "$staged_report" \
    --run-date "$run_date" \
    --command "$command_text"

python3 - "$transcript" "$staged_report" <<'PY'
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

transcript = Path(sys.argv[1]).read_text()
report = Path(sys.argv[2]).read_text()


class ReportParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.pre_depth = 0
        self.code_depth = 0
        self.output = []

    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.pre_depth += 1
        elif tag == 'code' and self.pre_depth:
            self.code_depth += 1

    def handle_endtag(self, tag):
        if tag == 'pre' and self.pre_depth:
            self.pre_depth -= 1
        elif tag == 'code' and self.code_depth:
            self.code_depth -= 1
            self.output.append('\n')

    def handle_data(self, data):
        if self.pre_depth and self.code_depth:
            self.output.append(data)


parser = ReportParser()
parser.feed(report)
pattern = r'^\S+ \([\w.]+\) \.\.\.'
expected = re.findall(pattern, transcript, re.MULTILINE)
actual = re.findall(pattern, ''.join(parser.output), re.MULTILINE)
if not expected or actual != expected:
    raise SystemExit(
        'ERROR: grouped report verification failed; expected {} tests, '
        'found {}.'.format(len(expected), len(actual)))
print('Verified all {} saved test cases are present.'.format(len(actual)))
PY
chmod 644 "$staged_report"
mv "$staged_report" "$report"
printf 'Updated saved test report: %s\n' "$report"
