# Discovery and invocation

The skills/README.md index is a document index beside the bucket folders, not a skill or a tool protocol. Every actual skill uses skills/<bucket>/<name>/SKILL.md. Follow the public Agent Skills specification for frontmatter and bundled resources. The bucket layout is a repository convention, not a requirement imposed on consuming runtimes or external skills.

Clients initially disclose names and descriptions. Activate selected instructions through model choice or explicit user request, then load required resources relative to the skill root. No proprietary command or metadata is required. Follow the public client implementation guide; the invoking environment owns its actual APIs, storage, authentication and tool registration.

The invoking environment owns discovery, loading, authorization, and tool registration. Use its actual supported invocation method. Do not assume a tool named Skill, execute_skill, or verify_skill_result exists.

MCP usage documentation uses the same path structure but declares its dependency in its own document. Before applying it, establish that the invoking agent intends and is authorized to use that server and has a working connection to its tools. If not, describe the missing connection or use an available suitable tool; do not invent the server. Reading an MCP guide is not permission to install, launch, or reconfigure a server.

These are repository maintenance conventions, not a mandatory runtime schema. Agent-specific discovery metadata can be added only for an actual supported integration, without changing the portable domain instructions.

The optional Claude-compatible plugin manifest in .claude-plugin/plugin.json registers task folders for supported plugin hosts. Do not register the README index as a task or duplicate the list in another inventory. Product packaging is checked separately with --packaging. It is not a prerequisite for standard discovery, loading or validation. The marketplace does not provide MCP servers.

An optional agents/openai.yaml may provide product UI metadata. Standard clients may ignore it. It must never be required to read a skill or its resources. Do not infer explicit-only invocation from sensitive writes, or add dependencies with guessed tool identifiers. Report missing execution prerequisites instead of fabricating or silently installing them.
