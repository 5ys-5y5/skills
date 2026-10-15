# Upstream documentation updates

external-skills.lock.json records source repository, exact upstream commit, version, license, original file paths, and hashes. The recorded version describes the documents, not a server installed in every consuming environment.

1. Select an upstream release and resolve its exact commit. Fetch documentation and license files from that commit.
2. Compare the changes to the existing source records. Preserve upstream bytes and keep local prerequisite explanations outside the original documents.
3. Record new source metadata and file hashes. Explain changed server requirements or tool availability in the MCP directory's local README.
4. Leave consuming environments' credentials, configuration, permissions, and user-edited skills untouched. Each consumer chooses when to adopt a documentation version and how to match it to its own connected tools.
5. Keep a versioned source history so a prior document release can be restored. Updating these documents neither updates an MCP server nor deploys a consuming service.

First-party task files have their own versions and hashes. They describe portable domain work, not application configuration contracts. This repository has no automatic updater or scheduled monitor. Upstream @latest examples are source documentation, not automatic installation commands.
