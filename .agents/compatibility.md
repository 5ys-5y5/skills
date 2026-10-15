# Compatibility evidence

Checked on 2026-10-15. This is a verification record, not a runtime API or a dependency inventory.

## Repository checks

- `scripts/validate-skills.py`: 6 skills, 4 source files and 25 local links passed.
- `scripts/validate-skills.py --packaging`: optional product packaging also passed.
- `scripts/test-validation.py`: 12 tests passed, including acceptance without product files, quoted and multiline YAML, standard field constraints, and rejection of escaping skill references.
- The document index is `skills/README.md`. It is not advertised as a skill.

## Independent readers

Used the official Agent Skills `skills-ref` implementation at commit `69ef37e9424c0a7ea9dd2293b559e43ec8176379`, with Python 3.14 in a temporary environment. Its `validate`, `read-properties` API and `to-prompt` API accepted all 6 skill directories.

Copied the 6 complete skill folders to a temporary flat `skills/<name>` layout, removed their `agents/` UI metadata, and included no plugin manifests. SHA-256 comparison confirmed that each `SKILL.md` remained identical to its repository source. The official reference implementation again validated and read all 6 folders and generated their catalog entries.

Vercel `skills@1.7.2` found all 6 skills with `add <local-path> --list`, both in this repository and in the temporary folders without product configuration. No installation was performed. These checks demonstrate file discovery and metadata interoperability, not model activation or actual tool execution.

## Pending runtime verification

- External skill → custom runtime: the runtime repository/edit target has not been confirmed. No custom runtime behavior has been verified or changed.
- Local skill → another runtime with model activation and resource reads: a read-only synthetic Claude Code test was rejected by automatic approval review before execution because it could send private skill content to the external Claude service. User authorization for that transfer is required before retrying.
- CRM/MCP task execution: not performed; the required test service, tools and permissions were not provisioned by this work.

For later runtime tests, record the runtime version, external skill's exact source commit and hashes, discovery output, initial metadata disclosure, model-selected and user-selected activation, resource-read trace, missing-tool behavior, and observed task result. Report file checks, model behavior and real service execution separately.
