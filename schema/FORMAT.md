# Agent-consumable skill format (v1)

Every distilled how-to becomes one or more JSON documents validating against `agent-skill.v1.json`.

Required fields:
- schema_version (1.0)
- id, name, goal
- prerequisites[]
- inputs[{name,type,description,required?}]
- outputs[{name,type,description}]
- constraints[]
- steps[{n, action, tool?, expect?}]

Optional: verification[], tags[], curriculum_ids[], source{}, domain, mcp_resource.

Publish path for MCP: `mcp-publish/skills/<id>.json` with URI `skill://<id>`.
