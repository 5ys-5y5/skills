# Repository instructions

Maintain portable task knowledge. Read [.agents/writing-skills.md](.agents/writing-skills.md) before editing skill content and [.agents/invocation.md](.agents/invocation.md) before changing discovery or dependencies.

Do not define a consuming application's configuration keys, APIs, storage, authentication protocol, runtime graph, deployment, or cache policy here. The invoking agent resolves those details in its own environment.

Keep every item under skills/<bucket>/<name>/SKILL.md. The skills/README.md index and bucket README files link to these documents. Only actual skills use SKILL.md and must follow the public Agent Skills specification. Product-specific metadata and plugin packaging are optional and must not be prerequisites for reading a skill. Mark an MCP dependency in the owning document; do not create a separate mcp tree. A document does not provide an MCP server or authorize its installation.

Keep source versions and update instructions inside the owning folder. Do not create a second root lock or update inventory. Preserve upstream attribution and license; record local prerequisite notices as adaptations. Use scripts/list-skills.sh to derive the document paths and scripts/validate-skills.py to check local files without an external service.

Check local links, frontmatter, source hashes, and realistic task behavior after changes. Do not claim that document validation proves a successful real service execution. Do not add credentials or patient records.
