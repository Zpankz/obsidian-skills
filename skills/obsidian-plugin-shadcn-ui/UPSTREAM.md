# Upstream source

This local skill vendors material from:
- Repository: `https://github.com/shadcn/ui`
- Skill URL: `https://skills.sh/shadcn/ui/shadcn`
- Imported from: `.tmp/shadcn-ui/skills/shadcn`

## Imported components
- Upstream umbrella skill from `SKILL.md`
- CLI reference from `cli.md`
- Theming and customization guidance from `customization.md`
- Rule files from `rules/`

## Local integration choices
- Renamed the local umbrella skill to `obsidian-plugin-shadcn-ui`
- Added focused local subskills `obsidian-plugin-shadcn-styling` and `obsidian-plugin-shadcn-composition`
- Adapted the guidance so it is only applied when an Obsidian plugin actually uses, or intentionally adopts, a React + Tailwind + shadcn stack
- Connected the family to the existing Obsidian plugin devkit, accessibility, styling, and React-performance skills
