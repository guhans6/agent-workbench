#!/usr/bin/env python3
"""Read-only structural checks and a temporary complete-bundle installation check."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile

SKILLS = ('to-tickets', 'implement', 'setup-matt-pocock-skills', 'matt-informed-engineering')
CONSUMERS = SKILLS[:3]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_links(file):
    text = file.read_text()
    for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', text):
        if target.startswith(('http:', 'https:', '#', 'mailto:')) or '<' in target:
            continue
        path = target.split('#', 1)[0]
        require((file.parent / path).exists(), f'{file}: missing reference {target}')


def check_bundle(root):
    for name in SKILLS:
        folder = root / 'skills' / name
        file = folder / 'SKILL.md'
        require(file.is_file(), f'missing skill: {file}')
        license_file = folder / 'LICENSE'
        require(license_file.is_file(), f'{folder}: missing MIT notice')
        notice = license_file.read_text()
        require('Copyright (c) 2026 Matt Pocock' in notice and 'MIT License' in notice, f'{folder}: incorrect license provenance')
        text = file.read_text()
        require(text.startswith('---\n'), f'{file}: missing frontmatter')
        metadata = text.split('---', 2)[1]
        require(re.search(r'^name: ' + re.escape(name) + r'$', metadata, re.M), f'{file}: incorrect name')
        if name in CONSUMERS:
            require('disable-model-invocation: true' in metadata, f'{file}: explicit invocation policy changed')
            require('../../workflows/validated-checkpoints.md' in text, f'{file}: missing checkpoint pointer')
        else:
            require('disable-model-invocation: true' not in metadata, f'{file}: advisor automatic reach disabled')
        for document in folder.rglob('*.md'):
            check_links(document)
    require((root / 'workflows/validated-checkpoints.md').is_file(), 'shared checkpoint protocol is missing')
    check_links(root / 'workflows/validated-checkpoints.md')


def check_repo(repo):
    check_bundle(repo / 'shared')
    manifest = json.loads((repo / 'shared/upstream/matt-pocock/local-adaptations.json').read_text())
    require({entry['skill'] for entry in manifest['adaptations']} == set(CONSUMERS), 'adaptation manifest must cover exactly the three upstream consumers')
    for entry in manifest['adaptations']:
        baseline = repo / entry['baseline']
        require(hashlib.sha256(baseline.read_bytes()).hexdigest() == entry['baseline_sha256'], f'{baseline}: upstream baseline checksum mismatch')
        require((repo / entry['local_file']).is_file(), f"missing adapted file: {entry['local_file']}")
        require((baseline.parent.parent / 'LICENSE').is_file(), f'{baseline}: missing upstream license')
        require((repo / entry['local_file']).parent.joinpath('LICENSE').read_bytes() == (baseline.parent.parent / 'LICENSE').read_bytes(), f'{baseline}: copied license differs')
    catalog = (repo / 'catalog/surfaces.yaml').read_text()
    table = (repo / 'catalog/skills.md').read_text()
    for name in SKILLS:
        require(len(re.findall(r'^\s+- name: "?' + re.escape(name) + r'"?\s*$', catalog, re.M)) == 1, f'{name}: expected one catalog entry')
        require('shared/skills/' + name + '/SKILL.md' in catalog, f'{name}: catalog path absent')
        require('`' + name + '`' in table, f'{name}: missing human catalog entry')
    for file in (repo / 'shared/workflows').glob('*checkpoint*.md'):
        check_links(file)
    check_links(repo / 'shared/workflows/skill-maintenance.md')
    with tempfile.TemporaryDirectory(prefix='workbench-checkpoint-install-') as temp:
        installation = Path(temp)
        for name in SKILLS:
            shutil.copytree(repo / 'shared/skills' / name, installation / 'skills' / name)
        # A single-folder style installation must fail, not pass with a dangling reference.
        try:
            check_bundle(installation)
        except ValueError:
            pass
        else:
            raise ValueError('incomplete installation incorrectly passed')
        (installation / 'workflows').mkdir()
        shutil.copyfile(repo / 'shared/workflows/validated-checkpoints.md', installation / 'workflows/validated-checkpoints.md')
        check_bundle(installation)
    print('PASS: metadata, local references, catalog entries, upstream baseline hashes/license, complete temporary installation, incomplete-install rejection')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--installation-root', type=Path, help='read-only check of an asset root containing skills/ and workflows/')
    args = parser.parse_args()
    if args.installation_root:
        check_bundle(args.installation_root.resolve())
        print('PASS: target bundle metadata and references (host loading and behavior untested)')
    else:
        check_repo(Path(__file__).resolve().parents[1])


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as error:
        raise SystemExit(f'FAIL: {error}')
