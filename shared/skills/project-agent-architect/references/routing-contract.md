# Repository Routing Contract

Read this reference only after repository evidence admits at least one Repository-Specific Profile. Global-only bootstrap needs no routing schema.

## Owned files

- `AGENTS.md` contains one managed span bounded by `<!-- routing:start -->` and `<!-- routing:end -->`. Preserve every byte outside that span.
- `routing.toml` declares context pointers, routes, and metadata for Repository-Specific Profiles.
- `.codex/agents/<name>.toml` pins each executable profile's exact assignment.

Model, skill, and tool availability is environment evidence, not repository policy. Record it in a temporary observations file outside the proposal and pass it to validation with `--observations <path>`.

## `routing.toml`

```toml
context_pointers = ["CONTEXT.md"]

[[routes]]
trigger = "recurring task class recognizable before work starts"
profile = "repository-profile"

[[profiles]]
name = "repository-profile"
access_requirement = "read-only"
responsibility = "One concise repository-specific responsibility."
skills = ["observed-skill"]
tools = ["observed-tool"]
```

Every route names an existing profile. Every profile name matches one `.codex/agents/<name>.toml`. `access_requirement` is exactly `read-only` or `workspace-write` and matches the agent's sandbox.

## Temporary observations

```toml
models = ["gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.6-sol"]
unavailable_models = []
skills = ["observed-skill"]
tools = ["observed-tool"]
```

Record only observed identities. An absent model remains unverifiable; a model belongs in `unavailable_models` only when current evidence confirms it is unavailable. The observations file is validation input and is not added to the repository.

## `.codex/agents/<name>.toml`

```toml
name = "repository-profile"
description = "Narrow trigger and responsibility."
model = "gpt-5.6-terra"
model_reasoning_effort = "medium"
sandbox_mode = "read-only"
developer_instructions = "Repository-specific delta only."
```

The values for `model`, `model_reasoning_effort`, and `sandbox_mode` are explicit. Skills and tools live in `routing.toml`; repository-specific instructions contain only the local delta while global policy and engineering methodology remain in their existing authorities.

## Validation result

- `FAIL` blocks application and must be fixed.
- `WARN` is fixed, accepted, or explicitly deferred before completion.
- `PASS` means the structure and observed references are valid; the orchestrator still owns routing judgment.
