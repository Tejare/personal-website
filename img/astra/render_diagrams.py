"""Rebuild the site's editable SVG diagrams (Python standard library only)."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GREEN, MUTED, AMBER, BLUE = '#7ee787', '#a2afbf', '#edc777', '#90bcfa'


def start(height, title, description):
    return [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs>
  <linearGradient id="bg" x2="1" y2="1"><stop stop-color="#18222e"/><stop offset="1" stop-color="#10161e"/></linearGradient>
  <linearGradient id="card" x2="1" y2="1"><stop stop-color="#202c39"/><stop offset="1" stop-color="#19232f"/></linearGradient>
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M1 1 8 5 1 9" fill="none" stroke="{GREEN}" stroke-width="1.6"/></marker>
  <marker id="return" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1 8 5 1 9" fill="none" stroke="{BLUE}" stroke-width="1.6"/></marker>
</defs>
<style>text{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;fill:#e5edf5}}.mono{{font-family:'SF Mono',Menlo,Consolas,monospace;letter-spacing:1px}}</style>
<rect width="840" height="{height}" rx="22" fill="url(#bg)"/>
''']


def text(p, x, y, content, size=18, color=None, weight=None, mono=False):
    attrs = f' style="fill:{color}"' if color else ''
    attrs += f' font-weight="{weight}"' if weight else ''
    attrs += ' class="mono"' if mono else ''
    p.append(f'<text x="{x}" y="{y}" font-size="{size}"{attrs}>{escape(content)}</text>')


def box(p, x, y, w, h, fill='url(#card)', stroke='#344251', radius=14):
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>')


def line(p, d, color=GREEN, dashed=False, arrow=True):
    marker = 'return' if color == BLUE else 'arrow'
    p.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round"' + (' stroke-dasharray="5 7"' if dashed else '') + (f' marker-end="url(#{marker})"' if arrow else '') + '/>')


def save(name, p):
    (ROOT / name).write_text('\n'.join(p) + '\n</svg>\n')


def pipeline():
    p = start(1340, 'From idea to verified detection', 'Seeder turns pentest runs, CVE advisories, threat intel, coverage gaps, incident retros and manual ideas into candidate detections. Tuner, Herald, Warden and Porter prepare each rule. Human approval precedes shipping, and maintainer review precedes production. Sentry verifies deployed rules. Mechanism failures and recalls return to Tuner; overlaps pause for a human.')
    text(p, 40, 44, '01 / DETECTION LIFECYCLE', 14, GREEN, mono=True)
    text(p, 40, 86, 'From idea to verified detection', 32, weight=600)
    text(p, 40, 117, 'Every promotion carries evidence. Every failure has a return path.', 18, MUTED)
    box(p, 96, 150, 704, 760, '#131c26', '#344251', 18)
    text(p, 118, 180, 'FACTORY', 13, GREEN, mono=True)
    text(p, 500, 180, 'No production repository credential', 15, MUTED)
    # Station 000: seeders feed the line.
    seeders = ['Manual ideas', 'Pentest runs', 'CVE advisories', 'Threat intel', 'Coverage gaps', 'Incident retros']
    for i, label in enumerate(seeders):
        x = 123 + i * 113
        box(p, x, 212, 100, 34, stroke='#47765b', radius=17)
        p.append(f'<text x="{x+50}" y="234" font-size="11.5" text-anchor="middle" style="fill:#c5d1dd">{escape(label)}</text>')
        line(p, f'M{x+50} 250 V286')
    box(p, 118, 290, 660, 80)
    text(p, 136, 319, '000', 14, GREEN, mono=True)
    text(p, 188, 321, 'Seeder', 25, weight=600)
    text(p, 136, 352, 'Each signal becomes a one-line idea: titled, deduped, ranked, queued', 16, MUTED)
    p.append(f'<text x="760" y="320" font-size="13" text-anchor="end" style="fill:{GREEN}" class="mono">IDEA INTAKE</text>')
    line(p, 'M294 374 V402')
    text(p, 310, 394, 'proposed', 13, GREEN, mono=True)
    p.append('<g transform="translate(0,150)">')
    rows = [
        (256, '001', 'Tuner', 'Draft + backtest on real telemetry', 'VOLUME GATE', 'Within the alert budget', 'ready_for_review'),
        (376, '002', 'Herald', 'Review by a different model family', 'ADVERSARIAL REVIEW', 'Intent questions → human', 'reviewed'),
        (496, '003', 'Warden', 'Compare with the deployed-rule index', 'DUPLICATE GATE', 'Overlap → pause for a human', 'passed'),
        (616, '004', 'Porter', 'Deposit the approved rule in the outbox', 'HUMAN GATE 1', 'Approve before shipping', 'shipped'),
    ]
    for y, number, name, subtitle, note, detail, stage in rows:
        box(p, 118, y, 354, 87)
        text(p, 136, y+29, number, 14, GREEN, mono=True)
        text(p, 188, y+31, name, 25, weight=600)
        text(p, 136, y+62, subtitle, 16, MUTED)
        text(p, 500, y+30, note, 13, AMBER if number == '004' else GREEN, mono=True)
        text(p, 500, y+59, detail, 17, AMBER if number == '004' else MUTED)
        line(p, f'M294 {y+87} V{y+116}')
        text(p, 310, y+108, stage, 13, GREEN, mono=True)
    # Keep return paths in a dedicated gutter, clear of labels and cards.
    line(p, 'M118 419 H72 V300 H115', BLUE, True)
    text(p, 500, 450, 'Broken mechanism → Tuner', 16, BLUE)
    box(p, 118, 783, 660, 68, '#29271f', '#74633e')
    text(p, 138, 809, 'HUMAN GATE 2', 13, AMBER, mono=True)
    text(p, 138, 835, 'Pull agent opens a merge request; maintainer reviews + merges.', 17)
    line(p, 'M294 736 V780')
    line(p, 'M294 851 V883')
    box(p, 118, 887, 354, 72, '#182e29', '#47765b')
    text(p, 138, 917, 'Production', 25, weight=600)
    text(p, 138, 942, 'Rule deployed through the protected branch', 15, MUTED)
    text(p, 500, 920, 'LIVE', 13, GREEN, mono=True)
    text(p, 500, 946, 'Independent deployment boundary', 16, MUTED)
    line(p, 'M294 959 V990')
    box(p, 118, 994, 354, 87)
    text(p, 136, 1023, '005', 14, GREEN, mono=True)
    text(p, 188, 1025, 'Sentry', 25, weight=600)
    text(p, 136, 1056, 'Daily liveness checks + mutation replay', 16, MUTED)
    text(p, 500, 1024, 'CONTINUOUS VERIFICATION', 13, GREEN, mono=True)
    text(p, 500, 1053, 'Prove the deployed rule still fires', 17, MUTED)
    line(p, 'M118 1038 H48 V300 H115', BLUE, True)
    line(p, 'M118 817 H48', BLUE, True, False)
    line(p, 'M40 1130 H72', BLUE, True, False)
    text(p, 86, 1136, 'RECALL / Failed verification or reviewer rejection returns to Tuner.', 16, BLUE)
    text(p, 86, 1161, 'Evidence becomes the next work order; the rule traverses the line again.', 16, MUTED)
    p.append('</g>')
    save('fig1_pipeline.svg', p)


def credentials():
    p = start(1080, 'Separate credentials. Explicit human control.', 'Four separate access boundaries: factory, outbox, pull agent and production repository. Factory can write only to the outbox. The pull agent holds outbox read access and the repository credential but cannot merge. Two human gates control shipping and merging.')
    text(p, 40, 44, '02 / CREDENTIAL BOUNDARIES', 14, GREEN, mono=True)
    text(p, 40, 86, 'Separate credentials. Human control.', 32, weight=600)
    text(p, 40, 117, 'Four access boundaries. No principal can author and land a rule alone.', 18, MUTED)
    rows = [
        (156, '01', 'Factory', 'Porter writes the approved rule', 'HUMAN GATE 1', 'Pre-ship approval', 'No production repository credential', AMBER),
        (370, '02', 'Outbox', 'An isolated handoff for rule artifacts', 'SCOPED STORAGE', 'Rule files + status', 'This boundary contains only the outbox', GREEN),
        (584, '03', 'Pull agent', 'Operated by a separate team', 'TWO CREDENTIALS', 'Outbox read + repository access', 'Can create a branch and merge request; cannot merge', BLUE),
        (798, '04', 'Production repository', 'Protected branch', 'HUMAN GATE 2', 'Maintainer review + merge', 'Branch protection enforces the final approval', AMBER),
    ]
    for y, number, name, subtitle, note, detail, footer, accent in rows:
        box(p, 76, y, 724, 148)
        p.append(f'<rect x="76" y="{y+20}" width="3" height="108" rx="1.5" fill="{accent}"/>')
        text(p, 98, y+34, number, 15, accent, mono=True)
        text(p, 144, y+36, name, 26, weight=600)
        text(p, 98, y+68, subtitle, 18, MUTED)
        text(p, 490, y+33, note, 13, accent, mono=True)
        text(p, 490, y+65, detail, 16)
        line(p, f'M98 {y+91} H778', '#344251', False, False)
        text(p, 98, y+123, footer, 16, MUTED)
    for y, heading, detail in [
        (304, 'WRITE → OUTBOX ONLY', 'Factory credential is scoped to this handoff.'),
        (518, 'READ → OUTBOX ONLY', 'Pull agent retrieves artifacts with a read-only key.'),
        (732, 'CREATE BRANCH + MERGE REQUEST', 'Repository credential stays with the pull agent.'),
    ]:
        line(p, f'M160 {y} V{y+62}')
        text(p, 190, y+26, heading, 13, GREEN, mono=True)
        text(p, 190, y+49, detail, 16, MUTED)
    line(p, 'M76 873 H42 V230 H73', BLUE, True)
    text(p, 76, 1000, 'REJECTION RETURNS THE RULE TO THE FACTORY', 13, BLUE, mono=True)
    text(p, 76, 1028, 'Recall the outbox row, reset its stage, and attach reviewer feedback.', 17, MUTED)
    text(p, 76, 1053, 'The repaired rule updates the same merge request.', 17, MUTED)
    save('fig6_credentials.svg', p)


if __name__ == '__main__':
    pipeline()
    credentials()
