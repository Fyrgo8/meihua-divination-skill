# meihua-divination-skill

A public Codex skill for structured **Meihua Yishu** hexagram interpretation.

It treats a skill as a small service rather than a long prompt: the repo contains a routing contract, input/output contract, failure handling rules, deterministic helper scripts, and layered references for deeper execution.

## What This Skill Does

This skill is built for **conversation-triggered Meihua divination reading** when the user already has a formed hexagram or enough casting information.

It focuses on:

- structured Meihua Yishu readings
- step-by-step `full-reading` output
- quick judgment mode
- intake checking when the case is incomplete
- review mode for auditing an existing reading

It explicitly does **not** try to cover:

- Bazi / Four Pillars
- Ziwei
- full Liuyao NaJia systems
- generic fortune talk without a hexagram
- automatic casting from random raw inputs

## Current Reading Logic

The current skill uses these explicit defaults:

- `动卦为用，静卦为体`
- strength analysis must consider **both 月令 and 卦气**
- final strength judgment must land on **体相对用谁更强**
- external signs are high-weight validators, not automatic overrides

## Repository Structure

```text
meihua-divination/
├── SKILL.md
├── README.md
├── evals/
│   └── evals.json
├── references/
│   ├── modes.md
│   ├── output-contracts.md
│   └── workflow.md
├── resources/
│   └── case-input.example.json
└── scripts/
    └── normalize_case_input.py
```

## Key Files

- `SKILL.md`
  The routing layer, input/output contract, execution flow, and failure handling.

- `references/workflow.md`
  The core Meihua interpretation workflow.

- `references/modes.md`
  Execution depth for `intake / quick-reading / full-reading / review`.

- `references/output-contracts.md`
  Fixed output templates so responses stay stable.

- `scripts/normalize_case_input.py`
  A deterministic helper that validates structured case input. It does **not** interpret the hexagram; it only normalizes data.

## Installation

### Option 1: install as a local Codex skill

Place the repo under your Codex skill directory:

```text
C:\Users\<your-user>\.codex\skills\meihua-divination
```

Restart Codex or open a new thread so the skill list is refreshed.

### Option 2: package as a `.skill`

If you already have the `skill-creator` helper installed, validate and package with:

```powershell
$env:PYTHONUTF8='1'
py -3 C:\Users\冯\.codex\skills\skill-creator\scripts\quick_validate.py C:\Users\冯\.codex\skills\meihua-divination
py -3 -m scripts.package_skill C:\Users\冯\.codex\skills\meihua-divination C:\Users\冯\.codex\skills\dist
```

## Example Trigger

```text
问工作变动：上坤下乾，初爻动，泰之升，未月。按梅花易数完整断一下。
```

Expected behavior:

- route into `full-reading`
- determine body/use with `动卦为用，静卦为体`
- analyze relation, strength, movement, transformed hexagram, mutual hexagram, external signs, and fallback checks
- output a structured reading instead of free-form mystical slogans

## Design Notes

This repo follows a “skill as microservice” approach:

- route precisely
- keep the main contract thin
- push deterministic work into scripts
- keep interpretation logic layered in references
- make failure modes explicit instead of hiding them in prompt prose

## Status

Current state:

- local Codex skill structure complete
- validation passes with UTF-8 mode enabled on Windows
- includes minimal eval prompts for trigger testing

## License

No license file is attached yet. Add one before broad redistribution if you want explicit reuse permissions.
