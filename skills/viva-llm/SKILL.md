---
name: viva-llm
description: Use VIVA LLM for multi-provider chat, voice calls, terminal integration, assistants, skills, MCP tools, and agent mode inside Obsidian. Trigger when the user mentions VIVA LLM, voice chat, realtime voice, LLM providers in Obsidian, or vault-integrated AI chat.
---

# VIVA LLM Skill

This skill enables Claude Code to configure and use the VIVA LLM plugin — a multi-provider chat and voice interface embedded in Obsidian.

## Overview

VIVA LLM turns Obsidian into a multi-provider AI workstation. It supports text chat, realtime voice calls (OpenAI Realtime, Gemini Live), an integrated terminal, custom assistants, vault-aware tool calling, MCP server integration, screen capture, and agent mode with recursive tool execution.

## Supported Providers

| Provider | Default Model | Endpoint |
|----------|--------------|----------|
| OpenAI | `gpt-5-nano` | `https://api.openai.com/v1` |
| Gemini | `gemini-3.1-flash-live-preview` | `https://generativelanguage.googleapis.com/v1beta/openai` |
| Anthropic | `claude-3-7-sonnet-20250219` | `https://api.anthropic.com/v1` |
| xAI | `grok-4-fast-non-reasoning` | `https://api.x.ai/v1` |
| Mistral AI | `mixtral-8x7b` | `https://api.mistral.ai/v1` |
| DeepSeek | `deepseek-llm` | `https://api.deepseek.com/v1` |
| Ollama | `qwen3:0.6b` | `http://localhost:11434/v1` |
| Cohere | `command` | `https://api.cohere.ai/v1` |

## Commands

| Command ID | Name | Description |
|-----------|------|-------------|
| `choose-model-and-provider` | Choose model and provider | Switch active LLM provider and model |
| `complete-chat-response` | Complete chat response | Force completion of a streaming response |
| `open-voice-call` | Open voice call panel | Open the realtime voice interface |
| `open-integrated-terminal` | Open integrated terminal | Launch the built-in terminal pane |
| `speak-chat` | Speak chat | Read the latest response aloud via TTS |
| `edit-selection` | Edit selection | Apply LLM to the selected text |
| `send-active-note-context-to-terminal` | Send active note context to terminal | Pipe current note into the terminal session |
| `generate-title` | Generate title | Auto-generate a chat title |
| `analyze-conversation` | Analyze conversation | Run conversation analysis |
| `reverse-roles` | Reverse roles | Swap user/assistant roles |
| `create-terminal-graph-session` | Create terminal graph session | Open a graph-linked terminal |

## Key Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `endpoint` | number | `1` | Active provider index |
| `defaultmaxTokens` | number | `4096` | Max tokens per response |
| `agentMode` | boolean | `true` | Enable recursive tool-calling agent |
| `maxRecursionDepth` | number | `20` | Agent recursion limit |
| `useYAMLFrontMatter` | boolean | `true` | Read/write YAML frontmatter |
| `skillsFolder` | string | `_skills` | Vault folder for custom skills |
| `enableMcpTools` | boolean | `true` | Enable MCP tool servers |
| `enableScreenCapture` | boolean | `true` | Allow screen capture for vision |
| `screenCaptureFps` | number | `0.5` | Screen capture frame rate |
| `forceToolCalling` | boolean | `true` | Force tool use in responses |

### Voice / Realtime Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `realtimeModel` | string | `gpt-realtime-1.5` | OpenAI realtime model |
| `geminiLiveModel` | string | `gemini-3.1-flash-live-preview` | Gemini Live model |
| `realtimeVoice` | string | `cedar` | Voice for realtime sessions |
| `voiceIdleTimeout` | number | `10` | Seconds before voice auto-stops |
| `voiceBackendContextEnabled` | boolean | `true` | Send vault context during voice |
| `voiceBackendContextInterval` | number | `20` | Seconds between context pushes |

### MCP and Orchestrator Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `mcpAppHostEnabled` | boolean | `true` | MCP app-host mode |
| `mcpDynamicToolsEnabled` | boolean | `true` | Dynamic MCP tool discovery |
| `mcpDynamicToolLimit` | number | `128` | Max dynamic tools |
| `realtimeOrchestratorEnabled` | boolean | `true` | Voice orchestrator |
| `realtimeOrchestratorEndpoint` | string | `http://localhost:8317/v1` | Orchestrator endpoint |

## Assistants

VIVA LLM supports custom assistants — named personas with their own system prompt, model, and tool/skill configuration:

```json
{
  "id": "custom-id",
  "name": "My Assistant",
  "description": "A custom assistant for X",
  "systemPrompt": "You are...",
  "modelId": "gpt-5-nano",
  "enableTools": true,
  "enabledToolNames": [],
  "enabledSkillIds": [],
  "skillPreferences": {},
  "createdAt": 1700000000000,
  "updatedAt": 1700000000000
}
```

The default assistant is `"default"` and can be switched via `currentAssistantId`.

## Skills System

Skills live in the vault folder specified by `skillsFolder` (default `_skills`). Each skill is a markdown file the LLM loads as context. Skills can be enabled/disabled per assistant.

## Templates

Two template categories are available:

- **Selection templates** — applied to highlighted text (e.g., "Add emojis", "Auto complete 5 suggestions")
- **Chat templates** — full conversation starters

Templates can be configured via `selectionTemplates`, `chatTemplates`, and their command-palette variants `CMDselectionTemplates`, `CMDchatTemplates`.

## Message Format

Chat messages use a role-based format controlled by `messageRoleFormatter`:

```
# role: user
What is the mitral valve?

# role: assistant
The mitral valve is...
```

## Tool System

VIVA LLM exposes vault-aware tools to the LLM, grouped by classification. Tools can be individually enabled/disabled via `enabledToolClassifications`, `disabledToolNames`, and `toolAutoExecution`. Agent mode (`agentMode: true`) allows the LLM to chain tool calls up to `maxRecursionDepth`.

## Excalidraw Integration

Built-in Excalidraw server management:

| Setting | Default | Description |
|---------|---------|-------------|
| `excalidrawManagedStartupEnabled` | `true` | Auto-start Excalidraw servers |
| `excalidrawAutoRestart` | `true` | Restart on crash |
| `excalidrawMaxRestarts` | `3` | Max restart attempts |

## References

- Plugin manifest: `viva-llm` v2.0.2
- Caliber source: `/Users/mikhail/Obsidian/vivax/.obsidian/plugins/viva-llm/.caliber/summary.json`
