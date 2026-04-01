# Upstream source

This local skill family vendors material from:
- Repository: `https://github.com/gapmiss/obsidian-plugin-skill`
- Imported from: `.tmp/obsidian-plugin-skill`

## Imported components
- Upstream umbrella skill from `.agents/skills/obsidian/SKILL.md`
- Reference files from `.agents/skills/obsidian/reference/`
- Boilerplate generator from `tools/create-plugin.js`
- Command guidance from `.claude/commands/create-plugin.md` and `.claude/commands/obsidian.md` was used as source context for the local integration design

## Local integration choices
- Kept the canonical local umbrella name as `obsidian-plugin-dev`
- Split major upstream references into independently invokable namespaced skills such as `obsidian-plugin-accessibility` and `obsidian-plugin-submission`
- Added a dedicated `obsidian-plugin-boilerplate` skill so scaffolding can be invoked directly without loading the full rule set first
- Retained the umbrella skill's bundled reference files and local tool copy for progressive disclosure
