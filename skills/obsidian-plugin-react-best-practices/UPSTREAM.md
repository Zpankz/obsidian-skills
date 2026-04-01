# Upstream source

This local skill vendors material from:
- Repository: `https://github.com/vercel-labs/agent-skills`
- Skill URL: `https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices`
- Imported from: `.tmp/vercel-agent-skills/skills/react-best-practices`

## Imported components
- Upstream umbrella skill from `SKILL.md`
- Compiled reference guide from `AGENTS.md`
- Rule files from `rules/`
- Repository metadata from `README.md`

## Local integration choices
- Renamed the local umbrella skill to `obsidian-plugin-react-best-practices`
- Added a focused derivative skill, `obsidian-plugin-react-performance`, for the client-heavy subset most relevant to Obsidian plugin interfaces
- Adapted the guidance so server-specific and Next.js-specific rules are applied only when the plugin repo actually uses those technologies
- Connected the family to shadcn/ui integration, accessibility, and the existing Obsidian plugin devkit
