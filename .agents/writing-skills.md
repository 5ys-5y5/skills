# Writing skills

Write the task knowledge that changes an agent's decisions. Each task folder contains SKILL.md with name and description frontmatter and concise instructions. Keep conditional details in relevant references inside that folder.

Follow https://agentskills.io/specification. Use valid YAML, including quoted or multiline strings when useful. Product metadata is optional. Reference bundled files relative to the skill directory and keep the folder usable when copied on its own. Do not require a catalog skill, proprietary activation command or consuming application's internal service path.

State inputs in domain terms: patient identifier, requested date, appointment, or desired action. Do not require application-specific JSON keys, secret reference formats, tenant IDs, provider endpoints, or invented execution tools. Use the access methods and permissions supplied by the invoking environment. Ask only for missing information needed for the task.

Keep domain distinctions that affect correctness: patient ownership, existing versus new records, requested versus completed actions, duplicate writes, and uncertain results. Do not replace these with a prescribed model or subagent orchestration.

Do not require an MCP server for a task that can use another available authorized browser or integration. An upstream MCP guide may require its particular server; label that dependency before offering the guide.

Preserve upstream instructions. Keep local prerequisite additions explicitly delimited and record both the original upstream hash and the resulting local hash in the owning folder's references/source.json. Verify that removing the declared addition restores the upstream bytes. Do not copy all tool schemas into a new first-party skill.
