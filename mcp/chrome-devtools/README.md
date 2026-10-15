# Chrome DevTools MCP — external server usage guide

This directory contains Google's official Chrome DevTools MCP skill document and references. It does not contain or provide a running MCP server.

Apply this guide only when the invoking agent intends and is authorized to use a connected Chrome DevTools MCP server. Check the actual tools available in that connection. A successful document load does not establish server availability. Do not invent tools or silently install, start, or configure a server to satisfy the guide. Treat setup as a separate authorized task when it is needed.

Once the connection is available, read [the official guide](SKILL.md). Read [tool reference](references/tool-reference.md) only for the tools needed for the task and [troubleshooting](references/troubleshooting.md) for relevant failures. Optional features in the full reference may not be enabled on the connected server.

The upstream SKILL.md is preserved verbatim, including its setup examples. Those examples are not instructions for this repository to auto-provision a server. The invoking agent applies its own execution policy and available configuration.

Source: ChromeDevTools/chrome-devtools-mcp, tag chrome-devtools-mcp-v1.10.1, commit e52c6b59b476c5e04d8dd9fd4bd017ba3b3d65df. Version and file hashes are recorded in [the source record](../../external-skills.lock.json). License: [Apache-2.0](references/LICENSE.txt).
