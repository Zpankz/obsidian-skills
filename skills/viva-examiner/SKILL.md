---
name: viva-examiner
description: Use Viva Examiner for real-time voice viva exams powered by Gemini Live. Trigger when the user mentions viva examiner, exam stations, CICM/ANZCA primary viva, voice examination, or drill deck.
---

# Viva Examiner Skill

This skill enables Claude Code to configure and interact with the Viva Examiner plugin — a real-time voice oral examination simulator for medical primary exams.

## Overview

Viva Examiner uses Gemini 3.1 Flash Live to conduct timed oral examination stations. It reads question stems from a drill-deck folder in the vault, runs 10-minute timed stations with real-time voice interaction, scores candidates on a 1–10 scale, and logs transcripts back to the vault.

**Desktop only** — requires microphone access for live voice interaction.

## Commands

| Command ID | Name | Description |
|-----------|------|-------------|
| `open-examiner` | Open examiner | Open the Viva Examiner panel |
| `random-station` | Start random station | Begin a randomly selected exam station |
| `pick-station` | Pick a station | Choose a specific station from the deck |

## Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `geminiApiKey` | string | `""` | Gemini API key |
| `model` | string | `gemini-3.1-flash-live-preview` | Gemini Live model |
| `voice` | string | `Orus` | Examiner voice |
| `stationDuration` | number | `600` | Station duration in seconds (10 min) |
| `autoTranscribe` | boolean | `true` | Auto-transcribe the session |
| `drillDeckPath` | string | `Limitless Lifelogs/VIVA Drill Deck` | Vault path to station stems |
| `logToVault` | boolean | `true` | Write transcripts/scores to vault |

## Drill Deck Structure

Station stems are stored as notes in the `drillDeckPath` folder. The plugin picks from these when running stations. Each note contains the opening stem and question cascade for one viva topic.

The default deck location is `Limitless Lifelogs/VIVA Drill Deck` with a default capacity of 26 stations.

## Examination Flow

1. **Open** — Use ribbon icon (stethoscope) or command `Open examiner`
2. **Select** — Pick a station or start random
3. **Examine** — Gemini Live conducts the 10-minute timed viva:
   - Reads the opening stem
   - Asks questions in logical cascade (basic recall → application)
   - Gives one redirect prompt if stuck, then moves on
   - Covers as many questions as possible in the time limit
4. **Score** — Pass (5–6), Good (7–8), Distinction (9–10)
5. **Feedback** — Structured: strengths, gaps, specific errors with correct answers
6. **Log** — Transcript and score saved to vault (when `logToVault` is enabled)

## Examiner Persona

The system prompt configures the examiner to:
- Speak clearly at moderate pace
- Use phrases like "Tell me about...", "Can you explain...", "What else?"
- Never reveal model answers during the station — only during feedback
- Always provide structured feedback after the station ends

## Exam Domains

Targets CICM and ANZCA Primary exam topics:
- Physiology
- Pharmacology
- Anatomy
- Physics
- Clinical application

## References

- Plugin manifest: `viva-examiner` v1.0.0
- Caliber source: `/Users/mikhail/Obsidian/vivax/.obsidian/plugins/viva-examiner/.caliber/summary.json`
