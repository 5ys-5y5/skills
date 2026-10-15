#!/usr/bin/env python3
"""Validate local document paths and per-item source records; no network calls."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills'


def inside(base, relative):
    target = (base / relative).resolve()
    if not target.is_relative_to(base.resolve()) or not target.is_file():
        raise ValueError(f'Missing or escaping file: {base / relative}')
    return target


def validate():
    names = set()
    documents = sorted(SKILLS.rglob('SKILL.md'))
    if not documents:
        raise ValueError('No SKILL.md documents')
    for path in documents:
        text = path.read_text(encoding='utf-8')
        match = re.match(r'\A---\n(.*?)\n---\n(.+)', text, re.S)
        if not match:
            raise ValueError(f'Missing frontmatter or body: {path}')
        header = match[1]
        name = re.search(r'^name: ([a-z0-9]+(?:-[a-z0-9]+)*)$', header, re.M)
        description = re.search(r'^description: \S.+$', header, re.M)
        if not name or not description or name[1] in names:
            raise ValueError(f'Invalid or duplicate name/description: {path}')
        names.add(name[1])
        if path != SKILLS / 'SKILL.md' and name[1] != path.parent.name:
            raise ValueError(f'Folder/name mismatch: {path}')

    checked_sources = 0
    for record in SKILLS.rglob('references/source.json'):
        owner = record.parent.parent
        source = json.loads(record.read_text(encoding='utf-8'))
        for item in source['files']:
            path = inside(owner, item['path'])
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() != item['sha256']:
                raise ValueError(f'Source digest mismatch: {path}')
            if 'bytes' in item and len(data) != item['bytes']:
                raise ValueError(f'Source size mismatch: {path}')
            if 'upstreamSha256' in item:
                original, removed = re.subn(
                    rb'<!-- local-prerequisite:start -->.*?<!-- local-prerequisite:end -->\n\n',
                    b'', data, flags=re.S)
                if removed != 1 or hashlib.sha256(original).hexdigest() != item['upstreamSha256']:
                    raise ValueError(f'Upstream original changed beyond declared notice: {path}')
            checked_sources += 1

    links = 0
    for path in ROOT.rglob('*.md'):
        # Imported references retain links to their original upstream tree.
        if path.name in ('tool-reference.md', 'troubleshooting.md'):
            continue
        for url in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if '://' in url or url.startswith('#'):
                continue
            inside(ROOT, str((path.parent / url.split('#')[0]).relative_to(ROOT)))
            links += 1
    print(f'PASS: {len(documents)} documents, {checked_sources} source files, {links} local links')


if __name__ == '__main__':
    validate()
