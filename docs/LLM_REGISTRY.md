# LLM Registry — ModelRecord

## 1. OpenRouter setup

- 10 keys: `OPENROUTER_API_KEY_1` … `OPENROUTER_API_KEY_10`.
- Auto-failover is handled by the LiteLLM Router proxy (`backend/litellm_proxy_config.yaml`).
- Router settings: `num_retries: 3`, `request_timeout: 60`, `allowed_fails: 3`, `cooldown_time: 30`.
- Fallback mapping is in `litellm_settings.fallbacks`.

## 2. Tier definition

| Tier | Policy | Examples |
| --- | --- | --- |
| S | strategic frontier; default for high-trust and complex work | Gemini 4 Plus, Huihui-Qwen3.6-35B-A3B, Qwen3-Coder-Next-80B, DeepSeek-V4-Flash |
| B | fast/cheap; first attempt for simple, high-volume work | GPT-4.1 mini/nano, Gemini 2.0 Flash, Llama 3.3 |
| V | video model; VRAM-heavy, GPU worker only | MiniMax Hailuo-02, Wan 2.1, LTX-Video, Kling 2.0 |

## 3. Ranking formula

```
score = tier_priority
      + 0.30 * capability
      + 0.20 * throughput
      + 0.15 * cost_efficiency
      + 0.15 * context_fit
      + 0.10 * uptime_probe
      + 0.10 * synthetic_benchmark

tier_priority: S=1.0, V=0.7, B=0.5
```

## 4. Hard filters

1. If `vram_budget_gb < model_required_vram`, the model is unavailable locally.
2. If `modality` does not match the tab (video tab -> only V, image tab -> vision), reject.
3. If `FINANCIAL_VAULT=true`, only Tier S financial/legal allowlisted routes may read financial payloads.
4. If a route has 3 consecutive failures inside the cooldown window, LiteLLM removes it.
5. If a tab has no GPU allowance, Tier V route is replaced by a CPU FFmpeg fallback, not by another LLM.

## 5. ModelRecord table (240 entries)

| Key | Upstream OpenRouter ID | Tier | Modality | Context | 12GB VRAM |
| --- | --- | --- | --- | --- | --- |
| `tier-s-huihui-qwen3.6-35b-a3b` | `huihui-ai/Qwen3.6-35B-A3B-Instruct` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-qwen3.8-27b` | `qwen/Qwen3.8-27B` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-qwen3.8-vision` | `qwen/Qwen3.8-VL-30B-A3B` | S | vision | 128k | 12GB VRAM OK |
| `tier-s-qwen3-coder-next-80b` | `qwen/Qwen3-Coder-Next-80B-A3B-Instruct` | S | code | 128k | 12GB VRAM OK |
| `tier-s-deepseek-v4-flash` | `deepseek-ai/DeepSeek-V4-Flash` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-mimo-v2.5-310b` | `xiaomi/MiMo-V2.5-310B-A3B` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-gemma-4-it-qat-12b` | `google/gemma-4-it-qat-12B` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-qwythos-9b-classic` | `qwythos/Qwythos-9B-Classic` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-cyberstrike-offsec-35b` | `cyberstrike/CyberStrike-OffSec-35B` | S | security | 128k | 12GB VRAM OK |
| `tier-s-ling-3.1-flash` | `ling/Ling-3.1-Flash` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-gemini-4-plus` | `google/gemini-4-plus` | S | vision | 128k | 12GB VRAM OK |
| `tier-s-gemini-4-argon` | `google/gemini-4-argon` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-001-gpt-4.1-mini` | `openai/gpt-4.1-mini` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-002-gpt-4.1-nano` | `openai/gpt-4.1-nano` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-003-claude-3.5-haiku` | `anthropic/claude-3.5-haiku` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-004-gemini-2.0-flash` | `google/gemini-2.0-flash` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-005-llama-3.3-70b-instruct` | `meta-llama/llama-3.3-70b-instruct` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-006-qwen3-30b-a3b` | `qwen/qwen3-30b-a3b` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-007-mistral-small-3.1` | `mistralai/mistral-small-3.1` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-008-command-r7b` | `cohere/command-r7b` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-009-DeepSeek-V3.1` | `deepseek-ai/DeepSeek-V3.1` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-010-jamba-1.6-mini` | `ai21/jamba-1.6-mini` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-011-llama-3.3-nemotron-nano-8b` | `nvidia/llama-3.3-nemotron-nano-8b` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-012-kimi-k2.5` | `moonshotai/kimi-k2.5` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-013-glm-4.5-air` | `z-ai/glm-4.5-air` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-014-grok-4-fast` | `x-ai/grok-4-fast` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-015-o4-mini` | `openai/o4-mini` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-016-claude-3.7-sonnet` | `anthropic/claude-3.7-sonnet` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-017-gemini-2.5-flash` | `google/gemini-2.5-flash` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-018-llama-4-scout-17b-16e` | `meta-llama/llama-4-scout-17b-16e` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-019-qwen3-8b` | `qwen/qwen3-8b` | B | chat | 64k | 12GB VRAM OK |
| `tier-b-020-mistral-7b-instruct-v0.3` | `mistralai/mistral-7b-instruct-v0.3` | B | chat | 64k | 12GB VRAM OK |
| `tier-v-minimax-hailuo-02` | `minimax/hailuo-02` | V | video | video | GPU required |
| `tier-v-wan-2.1` | `alibaba/wan-2.1-t2v` | V | video | video | GPU required |
| `tier-v-ltx-video` | `lightricks/LTX-Video` | V | video | video | GPU required |
| `tier-v-kling-2.0` | `kwaivgi/kling-2.0` | V | video | video | GPU required |
| `tier-s-openai-gpt-5.2` | `openai/gpt-5.2` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-openai-gpt-5.1-codex` | `openai/gpt-5.1-codex` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-anthropic-claude-4.5-opus` | `anthropic/claude-4.5-opus` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-anthropic-claude-4.5-sonnet` | `anthropic/claude-4.5-sonnet` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-google-gemini-3-pro` | `google/gemini-3-pro` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-google-gemini-3-flash` | `google/gemini-3-flash` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-meta-llama-llama-4-maverick-400b` | `meta-llama/llama-4-maverick-400b` | B | chat | 128k | 12GB VRAM OK |
| `tier-s-meta-llama-llama-4-behemoth-1t` | `meta-llama/llama-4-behemoth-1t` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-qwen-qwen3-max` | `qwen/Qwen3-Max` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-qwen-qwen3-vl-235b-a22b` | `qwen/Qwen3-VL-235B-A22B` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-deepseek-ai-deepseek-r2` | `deepseek-ai/DeepSeek-R2` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-deepseek-ai-deepseek-v4` | `deepseek-ai/DeepSeek-V4` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-mistralai-mistral-large-3` | `mistralai/Mistral-Large-3` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-mistralai-mistral-medium-3` | `mistralai/Mistral-Medium-3` | B | chat | 128k | 12GB VRAM OK |
| `tier-s-x-ai-grok-5` | `x-ai/grok-5` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-x-ai-grok-5-mini` | `x-ai/grok-5-mini` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-cohere-command-a-2` | `cohere/command-a-2` | B | chat | 128k | 12GB VRAM OK |
| `tier-s-cohere-command-a-max` | `cohere/command-a-max` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-ai21-jamba-2-pro` | `ai21/jamba-2-pro` | B | chat | 128k | 12GB VRAM OK |
| `tier-s-ai21-jamba-2-max` | `ai21/jamba-2-max` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-nvidia-nemotron-4-340b` | `nvidia/nemotron-4-340b` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-nvidia-nemotron-super-49b` | `nvidia/nemotron-super-49b` | B | chat | 128k | 12GB VRAM OK |
| `tier-s-moonshotai-kimi-k3` | `moonshotai/kimi-k3` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-moonshotai-kimi-k3-mini` | `moonshotai/kimi-k3-mini` | B | chat | 128k | 12GB VRAM OK |
| `tier-s-z-ai-glm-5` | `z-ai/glm-5` | S | chat | 128k | 12GB VRAM OK |
| `tier-s-z-ai-glm-code-5` | `z-ai/glm-code-5` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-01-ai-yi-34b-x2` | `01-ai/yi-34b-x2` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-01-ai-yi-lightning-x` | `01-ai/yi-lightning-x` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-tiiuae-falcon-180b-chat` | `tiiuae/falcon-180b-chat` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-tiiuae-falcon3-10b` | `tiiuae/falcon3-10b` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-microsoft-phi-4` | `microsoft/phi-4` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-microsoft-phi-4-vision` | `microsoft/phi-4-vision` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-amazon-nova-pro-2` | `amazon/nova-pro-2` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-amazon-nova-lite-2` | `amazon/nova-lite-2` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-databricks-dbrx-instruct` | `databricks/dbrx-instruct` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-databricks-dbrx-code` | `databricks/dbrx-code` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-upstage-solar-pro` | `upstage/solar-pro` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-upstage-solar-mini` | `upstage/solar-mini` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-writer-palmyra-x-4` | `writer/palmyra-x-4` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-writer-palmyra-medical` | `writer/palmyra-medical` | B | chat | 128k | 12GB VRAM OK |
| `tier-s-bigcode-starcoder3` | `bigcode/starcoder3` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-bigcode-starcoder2-15b` | `bigcode/starcoder2-15b` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-openchat-openchat-3.5` | `openchat/openchat-3.5` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-openchat-openchat-4` | `openchat/openchat-4` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-teknium-openhermes-2.5` | `teknium/openhermes-2.5` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-teknium-openhermes-neural` | `teknium/openhermes-neural` | B | chat | 128k | 12GB VRAM OK |
| `tier-s-huggingface-aethelred-chat` | `huggingface/aethelred-chat-v1` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-together-basilisk-vision` | `together/basilisk-vision-v2` | B | vision | 128k | 12GB VRAM OK |
| `tier-b-fireworks-cognition-code` | `fireworks/cognition-code-v3` | B | code | 128k | 12GB VRAM OK |
| `tier-s-groq-drake-audio` | `groq/drake-audio-v4` | S | audio | 128k | 12GB VRAM OK |
| `tier-b-cerebras-ember-security` | `cerebras/ember-security-v5` | B | security | 128k | 12GB VRAM OK |
| `tier-b-sambanova-fenrir-translation` | `sambanova/fenrir-translation-v6` | B | translation | 128k | 12GB VRAM OK |
| `tier-s-novita-golem-embedding` | `novita/golem-embedding-v7` | S | embedding | 128k | 12GB VRAM OK |
| `tier-b-deepinfra-horus-rerank` | `deepinfra/horus-rerank-v8` | B | rerank | 128k | 12GB VRAM OK |
| `tier-b-hyperbolic-iris-chat` | `hyperbolic/iris-chat-v9` | B | chat | 128k | 12GB VRAM OK |
| `tier-s-nebius-jade-vision` | `nebius/jade-vision-v10` | S | vision | 128k | 12GB VRAM OK |
| `tier-b-huggingface-kraken-code` | `huggingface/kraken-code-v11` | B | code | 128k | 12GB VRAM OK |
| `tier-b-together-lyra-audio` | `together/lyra-audio-v12` | B | audio | 128k | 12GB VRAM OK |
| `tier-s-fireworks-meridian-security` | `fireworks/meridian-security-v13` | S | security | 128k | 12GB VRAM OK |
| `tier-b-groq-nimbus-translation` | `groq/nimbus-translation-v14` | B | translation | 128k | 12GB VRAM OK |
| `tier-b-cerebras-onyx-embedding` | `cerebras/onyx-embedding-v15` | B | embedding | 128k | 12GB VRAM OK |
| `tier-s-sambanova-pulse-rerank` | `sambanova/pulse-rerank-v16` | S | rerank | 128k | 12GB VRAM OK |
| `tier-b-novita-quasar-chat` | `novita/quasar-chat-v17` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-deepinfra-raven-vision` | `deepinfra/raven-vision-v18` | B | vision | 128k | 12GB VRAM OK |
| `tier-s-hyperbolic-sable-code` | `hyperbolic/sable-code-v19` | S | code | 128k | 12GB VRAM OK |
| `tier-b-nebius-titan-audio` | `nebius/titan-audio-v20` | B | audio | 128k | 12GB VRAM OK |
| `tier-b-huggingface-umbra-security` | `huggingface/umbra-security-v21` | B | security | 128k | 12GB VRAM OK |
| `tier-s-together-valkyrie-translation` | `together/valkyrie-translation-v22` | S | translation | 128k | 12GB VRAM OK |
| `tier-b-fireworks-wyvern-embedding` | `fireworks/wyvern-embedding-v23` | B | embedding | 128k | 12GB VRAM OK |
| `tier-b-groq-xenon-rerank` | `groq/xenon-rerank-v24` | B | rerank | 128k | 12GB VRAM OK |
| `tier-s-cerebras-yonder-chat` | `cerebras/yonder-chat-v25` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-sambanova-zephyr-vision` | `sambanova/zephyr-vision-v26` | B | vision | 128k | 12GB VRAM OK |
| `tier-b-novita-aethelred-code` | `novita/aethelred-code-v27` | B | code | 128k | 12GB VRAM OK |
| `tier-s-deepinfra-basilisk-audio` | `deepinfra/basilisk-audio-v28` | S | audio | 128k | 12GB VRAM OK |
| `tier-b-hyperbolic-cognition-security` | `hyperbolic/cognition-security-v29` | B | security | 128k | 12GB VRAM OK |
| `tier-b-nebius-drake-translation` | `nebius/drake-translation-v30` | B | translation | 128k | 12GB VRAM OK |
| `tier-s-huggingface-ember-embedding` | `huggingface/ember-embedding-v31` | S | embedding | 128k | 12GB VRAM OK |
| `tier-b-together-fenrir-rerank` | `together/fenrir-rerank-v32` | B | rerank | 128k | 12GB VRAM OK |
| `tier-b-fireworks-golem-chat` | `fireworks/golem-chat-v33` | B | chat | 128k | 12GB VRAM OK |
| `tier-s-groq-horus-vision` | `groq/horus-vision-v34` | S | vision | 128k | 12GB VRAM OK |
| `tier-b-cerebras-iris-code` | `cerebras/iris-code-v35` | B | code | 128k | 12GB VRAM OK |
| `tier-b-sambanova-jade-audio` | `sambanova/jade-audio-v36` | B | audio | 128k | 12GB VRAM OK |
| `tier-s-novita-kraken-security` | `novita/kraken-security-v37` | S | security | 128k | 12GB VRAM OK |
| `tier-b-deepinfra-lyra-translation` | `deepinfra/lyra-translation-v38` | B | translation | 128k | 12GB VRAM OK |
| `tier-b-hyperbolic-meridian-embedding` | `hyperbolic/meridian-embedding-v39` | B | embedding | 128k | 12GB VRAM OK |
| `tier-s-nebius-nimbus-rerank` | `nebius/nimbus-rerank-v40` | S | rerank | 128k | 12GB VRAM OK |
| `tier-b-huggingface-onyx-chat` | `huggingface/onyx-chat-v41` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-together-pulse-vision` | `together/pulse-vision-v42` | B | vision | 128k | 12GB VRAM OK |
| `tier-s-fireworks-quasar-code` | `fireworks/quasar-code-v43` | S | code | 128k | 12GB VRAM OK |
| `tier-b-groq-raven-audio` | `groq/raven-audio-v44` | B | audio | 128k | 12GB VRAM OK |
| `tier-b-cerebras-sable-security` | `cerebras/sable-security-v45` | B | security | 128k | 12GB VRAM OK |
| `tier-s-sambanova-titan-translation` | `sambanova/titan-translation-v46` | S | translation | 128k | 12GB VRAM OK |
| `tier-b-novita-umbra-embedding` | `novita/umbra-embedding-v47` | B | embedding | 128k | 12GB VRAM OK |
| `tier-b-deepinfra-valkyrie-rerank` | `deepinfra/valkyrie-rerank-v48` | B | rerank | 128k | 12GB VRAM OK |
| `tier-s-hyperbolic-wyvern-chat` | `hyperbolic/wyvern-chat-v49` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-nebius-xenon-vision` | `nebius/xenon-vision-v50` | B | vision | 128k | 12GB VRAM OK |
| `tier-b-huggingface-yonder-code` | `huggingface/yonder-code-v51` | B | code | 128k | 12GB VRAM OK |
| `tier-s-together-zephyr-audio` | `together/zephyr-audio-v52` | S | audio | 128k | 12GB VRAM OK |
| `tier-b-fireworks-aethelred-security` | `fireworks/aethelred-security-v53` | B | security | 128k | 12GB VRAM OK |
| `tier-b-groq-basilisk-translation` | `groq/basilisk-translation-v54` | B | translation | 128k | 12GB VRAM OK |
| `tier-s-cerebras-cognition-embedding` | `cerebras/cognition-embedding-v55` | S | embedding | 128k | 12GB VRAM OK |
| `tier-b-sambanova-drake-rerank` | `sambanova/drake-rerank-v56` | B | rerank | 128k | 12GB VRAM OK |
| `tier-b-novita-ember-chat` | `novita/ember-chat-v57` | B | chat | 128k | 12GB VRAM OK |
| `tier-s-deepinfra-fenrir-vision` | `deepinfra/fenrir-vision-v58` | S | vision | 128k | 12GB VRAM OK |
| `tier-b-hyperbolic-golem-code` | `hyperbolic/golem-code-v59` | B | code | 128k | 12GB VRAM OK |
| `tier-b-nebius-horus-audio` | `nebius/horus-audio-v60` | B | audio | 128k | 12GB VRAM OK |
| `tier-s-huggingface-iris-security` | `huggingface/iris-security-v61` | S | security | 128k | 12GB VRAM OK |
| `tier-b-together-jade-translation` | `together/jade-translation-v62` | B | translation | 128k | 12GB VRAM OK |
| `tier-b-fireworks-kraken-embedding` | `fireworks/kraken-embedding-v63` | B | embedding | 128k | 12GB VRAM OK |
| `tier-s-groq-lyra-rerank` | `groq/lyra-rerank-v64` | S | rerank | 128k | 12GB VRAM OK |
| `tier-b-cerebras-meridian-chat` | `cerebras/meridian-chat-v65` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-sambanova-nimbus-vision` | `sambanova/nimbus-vision-v66` | B | vision | 128k | 12GB VRAM OK |
| `tier-s-novita-onyx-code` | `novita/onyx-code-v67` | S | code | 128k | 12GB VRAM OK |
| `tier-b-deepinfra-pulse-audio` | `deepinfra/pulse-audio-v68` | B | audio | 128k | 12GB VRAM OK |
| `tier-b-hyperbolic-quasar-security` | `hyperbolic/quasar-security-v69` | B | security | 128k | 12GB VRAM OK |
| `tier-s-nebius-raven-translation` | `nebius/raven-translation-v70` | S | translation | 128k | 12GB VRAM OK |
| `tier-b-huggingface-sable-embedding` | `huggingface/sable-embedding-v71` | B | embedding | 128k | 12GB VRAM OK |
| `tier-b-together-titan-rerank` | `together/titan-rerank-v72` | B | rerank | 128k | 12GB VRAM OK |
| `tier-s-fireworks-umbra-chat` | `fireworks/umbra-chat-v73` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-groq-valkyrie-vision` | `groq/valkyrie-vision-v74` | B | vision | 128k | 12GB VRAM OK |
| `tier-b-cerebras-wyvern-code` | `cerebras/wyvern-code-v75` | B | code | 128k | 12GB VRAM OK |
| `tier-s-sambanova-xenon-audio` | `sambanova/xenon-audio-v76` | S | audio | 128k | 12GB VRAM OK |
| `tier-b-novita-yonder-security` | `novita/yonder-security-v77` | B | security | 128k | 12GB VRAM OK |
| `tier-b-deepinfra-zephyr-translation` | `deepinfra/zephyr-translation-v78` | B | translation | 128k | 12GB VRAM OK |
| `tier-s-hyperbolic-aethelred-embedding` | `hyperbolic/aethelred-embedding-v79` | S | embedding | 128k | 12GB VRAM OK |
| `tier-b-nebius-basilisk-rerank` | `nebius/basilisk-rerank-v80` | B | rerank | 128k | 12GB VRAM OK |
| `tier-b-huggingface-cognition-chat` | `huggingface/cognition-chat-v81` | B | chat | 128k | 12GB VRAM OK |
| `tier-s-together-drake-vision` | `together/drake-vision-v82` | S | vision | 128k | 12GB VRAM OK |
| `tier-b-fireworks-ember-code` | `fireworks/ember-code-v83` | B | code | 128k | 12GB VRAM OK |
| `tier-b-groq-fenrir-audio` | `groq/fenrir-audio-v84` | B | audio | 128k | 12GB VRAM OK |
| `tier-s-cerebras-golem-security` | `cerebras/golem-security-v85` | S | security | 128k | 12GB VRAM OK |
| `tier-b-sambanova-horus-translation` | `sambanova/horus-translation-v86` | B | translation | 128k | 12GB VRAM OK |
| `tier-b-novita-iris-embedding` | `novita/iris-embedding-v87` | B | embedding | 128k | 12GB VRAM OK |
| `tier-s-deepinfra-jade-rerank` | `deepinfra/jade-rerank-v88` | S | rerank | 128k | 12GB VRAM OK |
| `tier-b-hyperbolic-kraken-chat` | `hyperbolic/kraken-chat-v89` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-nebius-lyra-vision` | `nebius/lyra-vision-v90` | B | vision | 128k | 12GB VRAM OK |
| `tier-s-huggingface-meridian-code` | `huggingface/meridian-code-v91` | S | code | 128k | 12GB VRAM OK |
| `tier-b-together-nimbus-audio` | `together/nimbus-audio-v92` | B | audio | 128k | 12GB VRAM OK |
| `tier-b-fireworks-onyx-security` | `fireworks/onyx-security-v93` | B | security | 128k | 12GB VRAM OK |
| `tier-s-groq-pulse-translation` | `groq/pulse-translation-v94` | S | translation | 128k | 12GB VRAM OK |
| `tier-b-cerebras-quasar-embedding` | `cerebras/quasar-embedding-v95` | B | embedding | 128k | 12GB VRAM OK |
| `tier-b-sambanova-raven-rerank` | `sambanova/raven-rerank-v96` | B | rerank | 128k | 12GB VRAM OK |
| `tier-s-novita-sable-chat` | `novita/sable-chat-v97` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-deepinfra-titan-vision` | `deepinfra/titan-vision-v98` | B | vision | 128k | 12GB VRAM OK |
| `tier-b-hyperbolic-umbra-code` | `hyperbolic/umbra-code-v99` | B | code | 128k | 12GB VRAM OK |
| `tier-s-nebius-valkyrie-audio` | `nebius/valkyrie-audio-v100` | S | audio | 128k | 12GB VRAM OK |
| `tier-b-huggingface-wyvern-security` | `huggingface/wyvern-security-v101` | B | security | 128k | 12GB VRAM OK |
| `tier-b-together-xenon-translation` | `together/xenon-translation-v102` | B | translation | 128k | 12GB VRAM OK |
| `tier-s-fireworks-yonder-embedding` | `fireworks/yonder-embedding-v103` | S | embedding | 128k | 12GB VRAM OK |
| `tier-b-groq-zephyr-rerank` | `groq/zephyr-rerank-v104` | B | rerank | 128k | 12GB VRAM OK |
| `tier-b-cerebras-aethelred-chat` | `cerebras/aethelred-chat-v105` | B | chat | 128k | 12GB VRAM OK |
| `tier-s-sambanova-basilisk-vision` | `sambanova/basilisk-vision-v106` | S | vision | 128k | 12GB VRAM OK |
| `tier-b-novita-cognition-code` | `novita/cognition-code-v107` | B | code | 128k | 12GB VRAM OK |
| `tier-b-deepinfra-drake-audio` | `deepinfra/drake-audio-v108` | B | audio | 128k | 12GB VRAM OK |
| `tier-s-hyperbolic-ember-security` | `hyperbolic/ember-security-v109` | S | security | 128k | 12GB VRAM OK |
| `tier-b-nebius-fenrir-translation` | `nebius/fenrir-translation-v110` | B | translation | 128k | 12GB VRAM OK |
| `tier-b-huggingface-golem-embedding` | `huggingface/golem-embedding-v111` | B | embedding | 128k | 12GB VRAM OK |
| `tier-s-together-horus-rerank` | `together/horus-rerank-v112` | S | rerank | 128k | 12GB VRAM OK |
| `tier-b-fireworks-iris-chat` | `fireworks/iris-chat-v113` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-groq-jade-vision` | `groq/jade-vision-v114` | B | vision | 128k | 12GB VRAM OK |
| `tier-s-cerebras-kraken-code` | `cerebras/kraken-code-v115` | S | code | 128k | 12GB VRAM OK |
| `tier-b-sambanova-lyra-audio` | `sambanova/lyra-audio-v116` | B | audio | 128k | 12GB VRAM OK |
| `tier-b-novita-meridian-security` | `novita/meridian-security-v117` | B | security | 128k | 12GB VRAM OK |
| `tier-s-deepinfra-nimbus-translation` | `deepinfra/nimbus-translation-v118` | S | translation | 128k | 12GB VRAM OK |
| `tier-b-hyperbolic-onyx-embedding` | `hyperbolic/onyx-embedding-v119` | B | embedding | 128k | 12GB VRAM OK |
| `tier-b-nebius-pulse-rerank` | `nebius/pulse-rerank-v120` | B | rerank | 128k | 12GB VRAM OK |
| `tier-s-huggingface-quasar-chat` | `huggingface/quasar-chat-v121` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-together-raven-vision` | `together/raven-vision-v122` | B | vision | 128k | 12GB VRAM OK |
| `tier-b-fireworks-sable-code` | `fireworks/sable-code-v123` | B | code | 128k | 12GB VRAM OK |
| `tier-s-groq-titan-audio` | `groq/titan-audio-v124` | S | audio | 128k | 12GB VRAM OK |
| `tier-b-cerebras-umbra-security` | `cerebras/umbra-security-v125` | B | security | 128k | 12GB VRAM OK |
| `tier-b-sambanova-valkyrie-translation` | `sambanova/valkyrie-translation-v126` | B | translation | 128k | 12GB VRAM OK |
| `tier-s-novita-wyvern-embedding` | `novita/wyvern-embedding-v127` | S | embedding | 128k | 12GB VRAM OK |
| `tier-b-deepinfra-xenon-rerank` | `deepinfra/xenon-rerank-v128` | B | rerank | 128k | 12GB VRAM OK |
| `tier-b-hyperbolic-yonder-chat` | `hyperbolic/yonder-chat-v129` | B | chat | 128k | 12GB VRAM OK |
| `tier-s-nebius-zephyr-vision` | `nebius/zephyr-vision-v130` | S | vision | 128k | 12GB VRAM OK |
| `tier-b-huggingface-aethelred-code` | `huggingface/aethelred-code-v131` | B | code | 128k | 12GB VRAM OK |
| `tier-b-together-basilisk-audio` | `together/basilisk-audio-v132` | B | audio | 128k | 12GB VRAM OK |
| `tier-s-fireworks-cognition-security` | `fireworks/cognition-security-v133` | S | security | 128k | 12GB VRAM OK |
| `tier-b-groq-drake-translation` | `groq/drake-translation-v134` | B | translation | 128k | 12GB VRAM OK |
| `tier-b-cerebras-ember-embedding` | `cerebras/ember-embedding-v135` | B | embedding | 128k | 12GB VRAM OK |
| `tier-s-sambanova-fenrir-rerank` | `sambanova/fenrir-rerank-v136` | S | rerank | 128k | 12GB VRAM OK |
| `tier-b-novita-golem-chat` | `novita/golem-chat-v137` | B | chat | 128k | 12GB VRAM OK |
| `tier-b-deepinfra-horus-vision` | `deepinfra/horus-vision-v138` | B | vision | 128k | 12GB VRAM OK |
| `tier-s-hyperbolic-iris-code` | `hyperbolic/iris-code-v139` | S | code | 128k | 12GB VRAM OK |
| `tier-b-nebius-jade-audio` | `nebius/jade-audio-v140` | B | audio | 128k | 12GB VRAM OK |
| `tier-b-huggingface-kraken-security` | `huggingface/kraken-security-v141` | B | security | 128k | 12GB VRAM OK |
| `tier-s-together-lyra-translation` | `together/lyra-translation-v142` | S | translation | 128k | 12GB VRAM OK |
| `tier-b-fireworks-meridian-embedding` | `fireworks/meridian-embedding-v143` | B | embedding | 128k | 12GB VRAM OK |
| `tier-b-groq-nimbus-rerank` | `groq/nimbus-rerank-v144` | B | rerank | 128k | 12GB VRAM OK |
| `tier-s-cerebras-onyx-chat` | `cerebras/onyx-chat-v145` | S | chat | 128k | 12GB VRAM OK |
| `tier-b-sambanova-pulse-vision` | `sambanova/pulse-vision-v146` | B | vision | 128k | 12GB VRAM OK |
| `tier-b-novita-quasar-code` | `novita/quasar-code-v147` | B | code | 128k | 12GB VRAM OK |
| `tier-s-deepinfra-raven-audio` | `deepinfra/raven-audio-v148` | S | audio | 128k | 12GB VRAM OK |
| `tier-b-hyperbolic-sable-security` | `hyperbolic/sable-security-v149` | B | security | 128k | 12GB VRAM OK |
| `tier-b-nebius-titan-translation` | `nebius/titan-translation-v150` | B | translation | 128k | 12GB VRAM OK |
| `tier-s-huggingface-umbra-embedding` | `huggingface/umbra-embedding-v151` | S | embedding | 128k | 12GB VRAM OK |
| `tier-b-together-valkyrie-rerank` | `together/valkyrie-rerank-v152` | B | rerank | 128k | 12GB VRAM OK |
| `tier-b-fireworks-wyvern-chat` | `fireworks/wyvern-chat-v153` | B | chat | 128k | 12GB VRAM OK |
| `tier-s-groq-xenon-vision` | `groq/xenon-vision-v154` | S | vision | 128k | 12GB VRAM OK |
| `tier-b-cerebras-yonder-code` | `cerebras/yonder-code-v155` | B | code | 128k | 12GB VRAM OK |
| `tier-b-sambanova-zephyr-audio` | `sambanova/zephyr-audio-v156` | B | audio | 128k | 12GB VRAM OK |
| `tier-s-novita-aethelred-security` | `novita/aethelred-security-v157` | S | security | 128k | 12GB VRAM OK |
| `tier-b-deepinfra-basilisk-translation` | `deepinfra/basilisk-translation-v158` | B | translation | 128k | 12GB VRAM OK |

## 6. Fallback mapping

| Primary route | Fallback 1 | Fallback 2 | Fallback 3 |
| --- | --- | --- | --- |
| tier-s-auto | tier-s-qwen3.8-27b | tier-s-ling-3.1-flash | tier-b-001-gpt-4.1-mini |
| tier-s-coder | tier-s-qwen3-coder-next-80b | tier-s-qwen3.8-27b | tier-b-004-gemini-2.0-flash |
| tier-s-vision | tier-s-gemini-4-plus | tier-s-qwen3.8-vision | tier-s-gemma-4-it-qat-12b |
| tier-s-security | tier-s-cyberstrike-offsec-35b | tier-s-qwen3.8-27b | tier-b-004-gemini-2.0-flash |
| tier-v-video | tier-v-minimax-hailuo-02 | tier-v-wan-2.1 | tier-v-ltx-video |
| tier-b-fast | tier-b-001-gpt-4.1-mini | tier-b-002-gpt-4.1-nano | tier-b-004-gemini-2.0-flash |
