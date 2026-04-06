---
name: obsidian-ops
description: "Handle Obsidian project operations: builds, linting, version bumps, release prep, and environment troubleshooting. Trigger on build failures, release packaging, or ref syncing."
---

# Obsidian Operations Skill

Use this skill for the operational side of Obsidian projects, especially after implementation work is done and you need to verify builds, package artifacts, troubleshoot environments, or prepare a release.

## Related skills
- `obsidian-dev`
- `obsidian-plugin-dev`
- `obsidian-plugin-boilerplate`
- `obsidian-plugin-submission`

This skill covers the operational aspects of maintaining an Obsidian project, including build workflows, sync procedures, and release management.

## Purpose

To ensure reliable builds, consistent reference materials, and safe release processes while strictly following project policies.

## Scope

This skill covers:
- Build and lint workflows
- Syncing reference documentation from external sources
- Version management and release preparation
- Build and environment troubleshooting

## Core Rules

- **NEVER perform automatic git operations**: AI agents must never execute `git commit`, `git push`, or any command that automatically stages or commits changes without explicit user approval for each step.
- **Verify Build**: Always run a build/lint after significant changes to ensure compatibility.
- **Sync Status**: Keep `sync-status.json` updated when updating reference materials.

## Bundled Resources

- `references/build-workflow.md`: Standard build and development commands.
- `references/release-readiness.md`: Checklist for ensuring a project is ready for release.
- `references/sync-procedure.md`: How to pull updates from reference repositories.
- `references/versioning-releases.md`: Workflow for versioning and GitHub releases.
- `references/troubleshooting.md`: Common issues and their resolutions.
- `references/quick-reference.md`: One-page cheat sheet for common operations.
