# Model verification protocol

The model registry is a candidate list, not a list of working models. A display name is not a provider ID. A successful `/models` catalog response only proves that the provider returned a catalog; it does not prove that every listed model can be invoked by this account.

## Available controls

- `GET /api/v1/system/provider-models?provider=openrouter`, `provider=fireworks`, or `provider=huggingface`: fetch the provider's current model catalog using server-side credentials.
- `POST /api/v1/system/model-probe`: sends one short, explicit test request. The caller must set `confirm_provider_cost=true`. The request may consume credits.
- `scripts/probe_models.py`: dry-run by default; `--execute` tests only candidate records that already have a supported provider and an exact model ID, and checks that the ID is present in the live catalog first.
- `/api/v1/chat`: routes only records whose status is `VERIFIED` and which have an exact provider model ID. The record must also map to the allowlisted Fireworks, OpenRouter, or Hugging Face Inference Providers provider.

## What a single passing probe proves

Only that the endpoint returned a non-empty text response at that moment. Separate tests are required for context limits, long-output reliability, streaming, JSON/schema output, tool/function calling, vision, audio, rate limits, latency, cost, safety behavior, availability by region/account, and regression quality.

## Report generated in this package

`model-verification-report.json` is a dry-run report for the 101 candidate records. The current records have no verified exact provider model IDs, and this environment has no provider keys; therefore no real provider requests were made. A model must not be marked working based on this dry-run.


## Hugging Face catalog discovery

- `scripts/discover_hf_models.py` calls the Hugging Face Inference Providers router catalog at `https://router.huggingface.co/v1/models` using `HF_TOKEN` and writes a timestamped JSON catalog snapshot. It does **not** call every model or verify quality.
- `scripts/probe_models.py --execute` now supports `huggingface` provider mapping as well as Fireworks and OpenRouter. Only exact IDs already present in the candidate registry are considered; do not infer IDs from display names.
- The OpenAI-compatible Hugging Face router is for chat-completion workloads. Use the appropriate Hugging Face inference client/task endpoint for image generation, speech, embeddings, or other non-chat modalities.
- Provider catalog entries may be visible while account access, credits, provider availability, or a particular task still blocks a live inference call.

- `scripts/discover_provider_models.py --provider huggingface|openrouter|fireworks` writes a catalog snapshot without sending inference prompts. The manually triggered `Manual provider catalog discovery` workflow runs this for the selected provider and uploads a 7-day artifact. The workflow exposes only the selected provider's secret to its job.
