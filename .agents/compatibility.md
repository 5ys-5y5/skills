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

## Operational mapping revision (2026-10-15)

Added crm-ui-mapping and per-task UI mapping references for hospital workflows. Hospital test scenarios were moved to .agents/scenarios/hospital, outside the distributable skill directories. Runtime instructions apply to authorized actual CRM work and do not require a synthetic environment.

A separate agent read the current mapping, billing and appointment instructions and evaluated four supplied situations without service access: payment input versus balance display, search date versus appointment edit date, ambiguous Save buttons in a mapping-only request, and an authorized production lookup. Its decisions preserved record scope and action meaning, left unconfirmed mappings unresolved, did not authorize writes for mapping-only work, and did not require a synthetic environment for production reads. This is an instruction-behavior assessment, not a browser or CRM execution result.

## Mandatory prerequisite revision (2026-10-15)

Hospital now exposes one Agent Skills entrypoint, crm-ui-mapping. Five former independent task skills are deferred procedure resources under that skill. The repository has two discoverable skills including Chrome DevTools; Vercel skills@1.7.2 listed exactly those two.

Added a portable mapping/request/evidence JSON Schema, a blank profile template, per-workflow operation/input contracts and result schemas, and a stdin-only validator. Actual hospital XPath mappings, credentials and records remain caller-owned. The mapping/action/result phases distinguish missing mappings, per-action readiness and result shape. The validator checks declared evidence; a runtime must supply truthful browser observations and bind its tool dispatcher to the result for enforced action blocking.

Repository validation tests (12) and hospital gate tests (20) passed. Gate cases include missing XPath, wrong context, stale request evidence, repeated elements, incorrect semantics, missing input values, task input types, transitive prerequisites, cycles, scope roles, requested result bindings and extensible result fields. Independent document review identified direct-child bypass ambiguity and overbroad narrow-query requirements; the procedures now restate the gate and narrow queries use requested result bindings. Official skills-ref accepted both entrypoints, and the bundled JSON Schemas passed Draft 2020-12 schema checks. No actual CRM/browser action or custom runtime dispatcher integration was exercised.

## Mapping bootstrap correction (2026-10-15)

Corrected the circular prerequisite interpretation: missing mappings lead immediately to authorized CRM navigation, necessary authentication and XPath observation. Complete business-profile validation is not required for those preparation actions. Business record writes remain outside preparation. The skill explicitly permits equivalent document-based checks when Python execution is unavailable and distinguishes page-access failure from validation failure.

The bundled validator no longer imports jsonschema or requires third-party packages. It implements the keyword subset present in its bundled schemas, rejects unsupported keywords and does not claim to be a general JSON Schema engine. All hospital tests passed, including a Python -S subprocess with site packages disabled, malformed types and boolean-versus-number handling. Independent instruction review confirmed continuation into mapping without Python and truthful blocking when every authorized browser path fails. Actual CRM access and the user's ERR_BLOCKED_BY_CLIENT environment were not reproduced or modified.
