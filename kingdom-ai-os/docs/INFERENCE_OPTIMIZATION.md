# Inference speed and quality optimization plan

Do not install every inference engine into the same production stack. Select per hardware and workload, then benchmark against a baseline.

## Candidate layers

- **vLLM:** high-throughput GPU model serving; evaluate batching, throughput, time-to-first-token, and concurrency.
- **SGLang:** serving/runtime option with prefix caching and optimization features; benchmark long repeated system prompts and multi-turn workloads.
- **llama.cpp:** local inference for supported quantized models and CPU/GPU mixes; useful when hardware constraints or local privacy dominate.
- **Ollama:** convenient local model runtime and API for development and local use; assess multi-user throughput before production.
- **LiteLLM:** provider routing/gateway layer, not a model speedup by itself; use for common interfaces, routing, fallbacks, and cost observability.
- **DSPy:** programmatic prompt/pipeline optimization; require a curated evaluation set and score improvement before accepting an optimized prompt.
- **Haystack / LlamaIndex:** retrieval and orchestration frameworks; use only when source-grounded retrieval materially improves a task.

## Optimization techniques to benchmark

1. Quantization (for example, a suitable 8-bit or 4-bit variant) against quality regression tests.
2. Continuous batching and concurrency limits for GPU inference.
3. Prefix/KV caching when prompts share stable system instructions or repeated document context.
4. Speculative decoding where supported and where a draft model actually improves end-to-end latency.
5. Prompt compression and retrieval of relevant passages instead of repeatedly sending entire archives.
6. Streaming output to reduce perceived latency; streaming is a UI/API capability and does not necessarily reduce total generation time.
7. Route tasks by capability and cost: a fast model for classification/extraction, a stronger model for complex reasoning, and vision-capable models for images.
8. Use structured output and tools only where required; unnecessary tool calls increase latency and failure modes.

## Acceptance criteria

Benchmark a fixed task set on the same hardware and prompts. Record model/provider/version, quantization, concurrency, time-to-first-token, tokens/sec, p50/p95 latency, error rate, cost per successful task, citation accuracy, task success, and safety regressions. Never mark a faster model as smarter without a task-specific quality evaluation. Keep a rollback path and the baseline configuration.

Official starting references:
- vLLM: https://docs.vllm.ai/
- SGLang: https://sgl-project.github.io/
- Playwright browser automation: https://playwright.dev/python/docs/intro
- Crawl4AI: https://docs.crawl4ai.com/
- Trafilatura extraction: https://trafilatura.readthedocs.io/en/latest/extraction-overview.html
- Scrapy: https://www.scrapy.org/
