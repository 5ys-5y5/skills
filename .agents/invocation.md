# Discovery and invocation

The skills/SKILL.md entrypoint is a document index beside the bucket folders. It does not define a tool protocol. Every item uses skills/<bucket>/<name>/SKILL.md. Read only the selected item's document and references needed for the request. Downloading documents for a local cache does not require exposing every document to the model.

The invoking environment owns discovery, loading, authorization, and tool registration. Use its actual supported invocation method. Do not assume a tool named Skill, execute_skill, or verify_skill_result exists.

MCP usage documentation uses the same path structure but declares its dependency in its own document. Before applying it, establish that the invoking agent intends and is authorized to use that server and has a working connection to its tools. If not, describe the missing connection or use an available suitable tool; do not invent the server. Reading an MCP guide is not permission to install, launch, or reconfigure a server.

These are repository maintenance conventions, not a mandatory runtime schema. Agent-specific discovery metadata can be added only for an actual supported integration, without changing the portable domain instructions.
