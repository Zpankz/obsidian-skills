---
name: obsidian-plugin-boilerplate
description: Use this skill when starting a new Obsidian plugin or retrofitting an existing plugin repo with the missing boilerplate files. Covers guided setup, metadata validation, and the local create-plugin generator script derived from the upstream obsidian-plugin-skill project.
---

# Obsidian Plugin Boilerplate

Use this skill when the user wants to create a new Obsidian plugin, scaffold a clean TypeScript plugin structure, or validate core metadata before writing feature code.

## What this skill provides
- A local interactive generator at `tools/create-plugin.js`
- Guidance for choosing automated versus manual setup
- Manifest naming and description validation before code generation
- Boilerplate expectations that align with `obsidian-plugin-dev`

## Recommended workflow
1. Ask whether the user wants **automated setup** or **manual setup**.
2. For automated setup, run `node skills/obsidian-plugin-boilerplate/tools/create-plugin.js` from the repo root.
3. For manual setup, create the same baseline files explicitly: `manifest.json`, `src/main.ts`, `src/settings.ts`, `styles.css`, `package.json`, `tsconfig.json`, `esbuild.config.mjs`, `version-bump.mjs`, `versions.json`, `.gitignore`, and `LICENSE`.
4. After scaffolding, immediately apply `obsidian-plugin-dev`, `obsidian-plugin-ui-ux`, `obsidian-plugin-accessibility`, and `obsidian-plugin-submission` to keep the generated project review-ready.

## Interactive setup guidance
Present the user with two options:

### 1. Automated setup
- Run `node skills/obsidian-plugin-boilerplate/tools/create-plugin.js`
- The generator creates a minimal plugin skeleton with best-practice defaults
- It validates plugin name, id, description, author, and target directory interactively
- It detects existing projects and only adds missing files when possible

### 2. Manual setup
- Walk through each required file step by step
- Explain what each file does
- Keep the template free of leftover sample names and placeholder production logging
- Ensure the initial settings UI, CSS, and manifest all follow local plugin-development guidance

## Validation reminders
- Plugin id must not contain `obsidian` or end with `plugin`
- Plugin name must not contain `Obsidian` or end with `Plugin`
- Description must not start with formulaic text like `This plugin` and must end with punctuation
- UI copy should use sentence case
- Generated UI should be keyboard accessible and theme-aware from the start

## Related skills
- `obsidian-plugin-dev`
- `obsidian-plugin-ui-ux`
- `obsidian-plugin-accessibility`
- `obsidian-plugin-submission`
- `obsidian-dev`
- `obsidian-ops`
