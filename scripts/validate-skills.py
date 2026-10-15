#!/usr/bin/env python3
"""Validate local documents, packaging and source records; no network calls."""
import hashlib
import argparse
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills'


def inside(base, relative):
    target = (base / relative).resolve()
    if not target.is_relative_to(base.resolve()) or not target.is_file():
        raise ValueError(f'Missing or escaping file: {base / relative}')
    return target


def validate_header(path):
    text = path.read_text(encoding='utf-8')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)', text, re.S)
    if not match or not match[2].strip():
        raise ValueError(f'Missing frontmatter or body: {path}')
    header = yaml.safe_load(match[1])
    if not isinstance(header, dict):
        raise ValueError(f'Frontmatter must be a YAML mapping: {path}')
    name, description = header.get('name'), header.get('description')
    if not isinstance(name, str) or not 1 <= len(name) <= 64 or not re.fullmatch(
            r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError(f'Invalid name: {path}')
    if name != path.parent.name:
        raise ValueError(f'Folder/name mismatch: {path}')
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        raise ValueError(f'Invalid description: {path}')
    if 'compatibility' in header:
        value = header['compatibility']
        if not isinstance(value, str) or not value.strip() or len(value) > 500:
            raise ValueError(f'Invalid compatibility: {path}')
    if 'metadata' in header:
        value = header['metadata']
        if not isinstance(value, dict) or not all(
                isinstance(k, str) and isinstance(v, str) for k, v in value.items()):
            raise ValueError(f'Invalid metadata: expected string-to-string mapping: {path}')
    for field in ('license', 'allowed-tools'):
        if field in header and not isinstance(header[field], str):
            raise ValueError(f'Invalid {field}: {path}')
    return name


def validate(packaging=False):
    names = set()
    skill_dirs = set()
    documents = sorted(SKILLS.rglob('SKILL.md'))
    if not documents:
        raise ValueError('No SKILL.md documents')
    for path in documents:
        name = validate_header(path)
        if name in names:
            raise ValueError(f'Duplicate name: {path}')
        names.add(name)
        if len(path.relative_to(SKILLS).parts) != 3:
            raise ValueError(f'Expected skills/<bucket>/<name>/SKILL.md: {path}')
        skill_dirs.add('./' + path.parent.relative_to(ROOT).as_posix())

    if packaging:
        validate_packaging(skill_dirs, documents)

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
        if any(part in ('.git', 'graft', 'node_modules', '.venv') for part in path.relative_to(ROOT).parts):
            continue
        # Imported references retain links to their original upstream tree.
        if path.name in ('tool-reference.md', 'troubleshooting.md'):
            continue
        for url in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if '://' in url or url.startswith('#'):
                continue
            base = path.parent if path.name == 'SKILL.md' else ROOT
            relative = url.split('#')[0] if base == path.parent else str(
                (path.parent / url.split('#')[0]).relative_to(ROOT))
            inside(base, relative)
            links += 1
    print(f'PASS: {len(documents)} standard skills, '
          f'{checked_sources} source files, {links} local links; packaging={packaging}')


def validate_packaging(skill_dirs, documents):
    """Product-specific checks, deliberately separate from portable skill validation."""
    for path in documents:
        metadata_path = path.parent / 'agents/openai.yaml'
        if not metadata_path.exists():
            continue
        metadata = yaml.safe_load(metadata_path.read_text(encoding='utf-8'))
        ui = metadata.get('interface', {}) if isinstance(metadata, dict) else {}
        title, summary = ui.get('display_name'), ui.get('short_description')
        if not isinstance(title, str) or not title.strip() or not isinstance(summary, str) or not 25 <= len(summary) <= 64:
            raise ValueError(f'Invalid UI metadata: {metadata_path}')
    plugin = json.loads(inside(ROOT, '.claude-plugin/plugin.json').read_text())
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', plugin['name']):
        raise ValueError('Invalid plugin name')
    if not re.fullmatch(r'\d+\.\d+\.\d+', plugin['version']):
        raise ValueError('Plugin version must be major.minor.patch')
    if set(plugin['skills']) != skill_dirs or len(plugin['skills']) != len(skill_dirs):
        raise ValueError('Plugin skill paths must match the task folders exactly (exclude the catalog)')
    marketplace = json.loads(inside(ROOT, '.claude-plugin/marketplace.json').read_text())
    entries = marketplace['plugins']
    if len(entries) != 1 or entries[0]['name'] != plugin['name'] or entries[0]['source'] != './':
        raise ValueError('Marketplace must reference the local plugin')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packaging', action='store_true', help='Also check optional product packaging')
    validate(packaging=parser.parse_args().packaging)
