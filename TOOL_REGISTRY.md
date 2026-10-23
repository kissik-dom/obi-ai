# DOC 3: TOOL_REGISTRY.md - 620 Open-Source Tools (Categories A-K 50+ Each) & 920 Total Ecosystem Tools

## 1. ToolRecord Schema & Multi-Stage Lazy-Import Architecture

Every tool is typed via `ToolRecord` (`id`, `name`, `category`, `version`, `license`, `install_cmd`, `python_import`, `docker_image`, `api_endpoint`, `env_vars`, `dependencies`, `tabs_used_by`).
- **Open-Source Core Tools**: **620** (`>= 50` in every Category A-K + 56 Sovereign Core L).
- **Composio Enterprise Action Connectors**: **300** (60 packs x 5 typed actions).
- **Total Callable Tools**: **920**.
- **Anti-Junky Stacking Rule**: Heavy packages (`GHIDRA`, `FreeCAD`, `Blender`, `Wan 2.1`, `LTX-Video`, `MiniMax`, `SAM2`, `Demucs`) are lazy-imported inside functions only and isolated into Docker build stages `base -> security -> engineering -> images -> video -> messaging`.

## 2. Category Summary Matrix

| Category | Domain | Count | Docker Stage | Primary Tabs |
|---|---|---:|---|---|
| `A` | Video Editing | 51 | `video` | `video,images,social` |
| `B` | Translation & Dubbing | 51 | `video` | `research,news,social,video` |
| `C` | Messaging & Omnichannel | 50 | `messaging` | `agents,social,business,leads` |
| `D` | OSINT & Reconnaissance | 50 | `security` | `osint,leads,security,legal` |
| `E` | Web Scraping & CUA Browser Fleet | 55 | `base` | `web,leads,real_estate,research` |
| `F` | Deep Research & Knowledge Ingestion | 50 | `base` | `research,legal,finance,investments,news` |
| `G` | Security, WAF, SIEM, eBPF & Honeypot | 52 | `security` | `security,finance,investments,home` |
| `H` | Engineering, CAD, GHIDRA & Propulsion Research | 52 | `engineering` | `engineering,city,coding,real_estate` |
| `I` | Vocal Tuning, Stem Separation & Audio AI | 50 | `video` | `music,video` |
| `J` | Images, Photoreal Skin & Biometric Isolation | 53 | `images` | `images,fashion,social` |
| `K` | Video Generation, UGC, TV & Movies | 50 | `video` | `video,social,fashion` |
| `L` | Sovereign Infra, Hermes, Legal, Finance & GIS Core | 56 | `base` | `home,llm,agents,tasks,opensource,finance,city` |
| `M` | Composio Managed App Action Packs (60 x 5 actions) | 300 | `messaging` | `business,agents,opensource,social,leads` |

## 3. Complete Open-Source Tool Catalog (Categories A-L)

### Category A: Video Editing (51 Tools)

| # | Tool ID | Name | Category | Stage | Lazy Runner | Tabs |
|---:|---|---|---|---|---|---|
| 1 | `cat-a-01` | FFmpeg 6.1 CLI Master Encoder | `A` | `video` | `lazy_tool('cat-a-01')` | `video,images,social` |
| 2 | `cat-a-02` | Shotcut NLE | `A` | `video` | `lazy_tool('cat-a-02')` | `video,images,social` |
| 3 | `cat-a-03` | Kdenlive Studio | `A` | `video` | `lazy_tool('cat-a-03')` | `video,images,social` |
| 4 | `cat-a-04` | OpenShot Video Editor | `A` | `video` | `lazy_tool('cat-a-04')` | `video,images,social` |
| 5 | `cat-a-05` | Blender Video Sequence Editor | `A` | `video` | `lazy_tool('cat-a-05')` | `video,images,social` |
| 6 | `cat-a-06` | LosslessCut Trim Engine | `A` | `video` | `lazy_tool('cat-a-06')` | `video,images,social` |
| 7 | `cat-a-07` | Auto-Editor Silence Cutter | `A` | `video` | `lazy_tool('cat-a-07')` | `video,images,social` |
| 8 | `cat-a-08` | VapourSynth Frame Scripting | `A` | `video` | `lazy_tool('cat-a-08')` | `video,images,social` |
| 9 | `cat-a-09` | MoviePy Python Compositor | `A` | `video` | `lazy_tool('cat-a-09')` | `video,images,social` |
| 10 | `cat-a-10` | Manim Math Animation Engine | `A` | `video` | `lazy_tool('cat-a-10')` | `video,images,social` |
| 11 | `cat-a-11` | Olive 0.2 Node Compositor | `A` | `video` | `lazy_tool('cat-a-11')` | `video,images,social` |
| 12 | `cat-a-12` | Flowblade Linux NLE | `A` | `video` | `lazy_tool('cat-a-12')` | `video,images,social` |
| 13 | `cat-a-13` | Pitivi GES Editor | `A` | `video` | `lazy_tool('cat-a-13')` | `video,images,social` |
| 14 | `cat-a-14` | LiVES Realtime Video | `A` | `video` | `lazy_tool('cat-a-14')` | `video,images,social` |
| 15 | `cat-a-15` | Cinelerra-GG Broadcast NLE | `A` | `video` | `lazy_tool('cat-a-15')` | `video,images,social` |
| 16 | `cat-a-16` | Natron OpenFX Compositor | `A` | `video` | `lazy_tool('cat-a-16')` | `video,images,social` |
| 17 | `cat-a-17` | Remotion React Programmatic Video | `A` | `video` | `lazy_tool('cat-a-17')` | `video,images,social` |
| 18 | `cat-a-18` | FFmpeg.wasm Browser Transcoder | `A` | `video` | `lazy_tool('cat-a-18')` | `video,images,social` |
| 19 | `cat-a-19` | VidGear Async Video I/O | `A` | `video` | `lazy_tool('cat-a-19')` | `video,images,social` |
| 20 | `cat-a-20` | PySceneDetect Cut Detector | `A` | `video` | `lazy_tool('cat-a-20')` | `video,images,social` |
| 21 | `cat-a-21` | Whisper STT Subtitle Generator | `A` | `video` | `lazy_tool('cat-a-21')` | `video,images,social` |
| 22 | `cat-a-22` | WhisperX Word-Level Alignment | `A` | `video` | `lazy_tool('cat-a-22')` | `video,images,social` |
| 23 | `cat-a-23` | SeamlessM4T Dubbing Pipeline | `A` | `video` | `lazy_tool('cat-a-23')` | `video,images,social` |
| 24 | `cat-a-24` | NLLB-200 Subtitle Translator | `A` | `video` | `lazy_tool('cat-a-24')` | `video,images,social` |
| 25 | `cat-a-25` | Argos Translate Offline Subtitles | `A` | `video` | `lazy_tool('cat-a-25')` | `video,images,social` |
| 26 | `cat-a-26` | Decord GPU Video Loader | `A` | `video` | `lazy_tool('cat-a-26')` | `video,images,social` |
| 27 | `cat-a-27` | PyAV Libav Bindings | `A` | `video` | `lazy_tool('cat-a-27')` | `video,images,social` |
| 28 | `cat-a-28` | ImageIO-FFmpeg Streamer | `A` | `video` | `lazy_tool('cat-a-28')` | `video,images,social` |
| 29 | `cat-a-29` | AviSynth+ Frame Server | `A` | `video` | `lazy_tool('cat-a-29')` | `video,images,social` |
| 30 | `cat-a-30` | AviSynth Shader Pipeline | `A` | `video` | `lazy_tool('cat-a-30')` | `video,images,social` |
| 31 | `cat-a-31` | OpenCV Video I/O Pipeline | `A` | `video` | `lazy_tool('cat-a-31')` | `video,images,social` |
| 32 | `cat-a-32` | DaVinci Resolve Scripting Shim | `A` | `video` | `lazy_tool('cat-a-32')` | `video,images,social` |
| 33 | `cat-a-33` | Timecut Smooth Frame Capturer | `A` | `video` | `lazy_tool('cat-a-33')` | `video,images,social` |
| 34 | `cat-a-34` | FFprobe Stream Analyzer | `A` | `video` | `lazy_tool('cat-a-34')` | `video,images,social` |
| 35 | `cat-a-35` | MKVToolNix Container Remuxer | `A` | `video` | `lazy_tool('cat-a-35')` | `video,images,social` |
| 36 | `cat-a-36` | HandBrake CLI Batch Transcoder | `A` | `video` | `lazy_tool('cat-a-36')` | `video,images,social` |
| 37 | `cat-a-37` | Av1an Parallel AV1 Encoder | `A` | `video` | `lazy_tool('cat-a-37')` | `video,images,social` |
| 38 | `cat-a-38` | x264/x265 Mastering Codecs | `A` | `video` | `lazy_tool('cat-a-38')` | `video,images,social` |
| 39 | `cat-a-39` | NoiseTorch Realtime Denoiser | `A` | `video` | `lazy_tool('cat-a-39')` | `video,images,social` |
| 40 | `cat-a-40` | RNNoise Recurrent Audio Cleaner | `A` | `video` | `lazy_tool('cat-a-40')` | `video,images,social` |
| 41 | `cat-a-41` | Spleeter Video Stem Splitter | `A` | `video` | `lazy_tool('cat-a-41')` | `video,images,social` |
| 42 | `cat-a-42` | Demucs v4 Soundtrack Separator | `A` | `video` | `lazy_tool('cat-a-42')` | `video,images,social` |
| 43 | `cat-a-43` | RIFE 4x Frame Interpolation | `A` | `video` | `lazy_tool('cat-a-43')` | `video,images,social` |
| 44 | `cat-a-44` | ESRGAN Frame Upscaler | `A` | `video` | `lazy_tool('cat-a-44')` | `video,images,social` |
| 45 | `cat-a-45` | Real-ESRGAN Video Enhancer | `A` | `video` | `lazy_tool('cat-a-45')` | `video,images,social` |
| 46 | `cat-a-46` | DeOldify Archival Colorizer | `A` | `video` | `lazy_tool('cat-a-46')` | `video,images,social` |
| 47 | `cat-a-47` | DeScratch Film Restorer | `A` | `video` | `lazy_tool('cat-a-47')` | `video,images,social` |
| 48 | `cat-a-48` | ColorMancer LUT Grader | `A` | `video` | `lazy_tool('cat-a-48')` | `video,images,social` |
| 49 | `cat-a-49` | AutoSub CLI Captioner | `A` | `video` | `lazy_tool('cat-a-49')` | `video,images,social` |
| 50 | `cat-a-50` | SubSync Audio-Subtitle Aligner | `A` | `video` | `lazy_tool('cat-a-50')` | `video,images,social` |
| 51 | `cat-a-51` | Aegisub ASS Automation | `A` | `video` | `lazy_tool('cat-a-51')` | `video,images,social` |

### Category B: Translation & Dubbing (51 Tools)

| # | Tool ID | Name | Category | Stage | Lazy Runner | Tabs |
|---:|---|---|---|---|---|---|
| 52 | `cat-b-01` | Whisper Large-v3 1.5B ASR | `B` | `video` | `lazy_tool('cat-b-01')` | `research,news,social,video` |
| 53 | `cat-b-02` | WhisperX Word-Level Aligner | `B` | `video` | `lazy_tool('cat-b-02')` | `research,news,social,video` |
| 54 | `cat-b-03` | SeamlessM4T v2 Large 2.3B | `B` | `video` | `lazy_tool('cat-b-03')` | `research,news,social,video` |
| 55 | `cat-b-04` | NLLB-200 3.3B 200-Language MT | `B` | `video` | `lazy_tool('cat-b-04')` | `research,news,social,video` |
| 56 | `cat-b-05` | Argos Translate Offline Engine | `B` | `video` | `lazy_tool('cat-b-05')` | `research,news,social,video` |
| 57 | `cat-b-06` | LibreTranslate Self-Hosted API | `B` | `video` | `lazy_tool('cat-b-06')` | `research,news,social,video` |
| 58 | `cat-b-07` | OPUS-MT 1000+ Language Pairs | `B` | `video` | `lazy_tool('cat-b-07')` | `research,news,social,video` |
| 59 | `cat-b-08` | MarianMT C++ Neural MT | `B` | `video` | `lazy_tool('cat-b-08')` | `research,news,social,video` |
| 60 | `cat-b-09` | EasyNMT Python Wrapper | `B` | `video` | `lazy_tool('cat-b-09')` | `research,news,social,video` |
| 61 | `cat-b-10` | Bergamot Browser WASM MT | `B` | `video` | `lazy_tool('cat-b-10')` | `research,news,social,video` |
| 62 | `cat-b-11` | Lingva Translate Privacy Proxy | `B` | `video` | `lazy_tool('cat-b-11')` | `research,news,social,video` |
| 63 | `cat-b-12` | Apertium Rule-Based MT | `B` | `video` | `lazy_tool('cat-b-12')` | `research,news,social,video` |
| 64 | `cat-b-13` | OpenNMT-py Sequence Engine | `B` | `video` | `lazy_tool('cat-b-13')` | `research,news,social,video` |
| 65 | `cat-b-14` | OpenNMT-tf Serving Runtime | `B` | `video` | `lazy_tool('cat-b-14')` | `research,news,social,video` |
| 66 | `cat-b-15` | Fairseq S2T Speech Translation | `B` | `video` | `lazy_tool('cat-b-15')` | `research,news,social,video` |
| 67 | `cat-b-16` | M2M100 1.2B Many-to-Many MT | `B` | `video` | `lazy_tool('cat-b-16')` | `research,news,social,video` |
| 68 | `cat-b-17` | MADLAD-400 400-Language T5 | `B` | `video` | `lazy_tool('cat-b-17')` | `research,news,social,video` |
| 69 | `cat-b-18` | FLORES-200 Quality Evaluator | `B` | `video` | `lazy_tool('cat-b-18')` | `research,news,social,video` |
| 70 | `cat-b-19` | Coqui XTTS v2 Cross-Lingual Dub | `B` | `video` | `lazy_tool('cat-b-19')` | `research,news,social,video` |
| 71 | `cat-b-20` | F5-TTS Cross-Lingual Flow | `B` | `video` | `lazy_tool('cat-b-20')` | `research,news,social,video` |
| 72 | `cat-b-21` | CosyVoice 2 Multilingual Stream | `B` | `video` | `lazy_tool('cat-b-21')` | `research,news,social,video` |
| 73 | `cat-b-22` | Seed-TTS Multilingual Prosody | `B` | `video` | `lazy_tool('cat-b-22')` | `research,news,social,video` |
| 74 | `cat-b-23` | RVC Cross-Language Timbre Lock | `B` | `video` | `lazy_tool('cat-b-23')` | `research,news,social,video` |
| 75 | `cat-b-24` | So-VITS-SVC 5.0 Pitch Dubber | `B` | `video` | `lazy_tool('cat-b-24')` | `research,news,social,video` |
| 76 | `cat-b-25` | Bark Multilingual Expressive TTS | `B` | `video` | `lazy_tool('cat-b-25')` | `research,news,social,video` |
| 77 | `cat-b-26` | Meta MMS 1100-Language Speech | `B` | `video` | `lazy_tool('cat-b-26')` | `research,news,social,video` |
| 78 | `cat-b-27` | Wav2Vec2 XLS-R Cross-Lingual | `B` | `video` | `lazy_tool('cat-b-27')` | `research,news,social,video` |
| 79 | `cat-b-28` | Whisper.cpp GGML Quantized ASR | `B` | `video` | `lazy_tool('cat-b-28')` | `research,news,social,video` |
| 80 | `cat-b-29` | Faster-Whisper CTranslate2 | `B` | `video` | `lazy_tool('cat-b-29')` | `research,news,social,video` |
| 81 | `cat-b-30` | Distil-Whisper Low-Latency ASR | `B` | `video` | `lazy_tool('cat-b-30')` | `research,news,social,video` |
| 82 | `cat-b-31` | NVIDIA Canary-1B Multilingual | `B` | `video` | `lazy_tool('cat-b-31')` | `research,news,social,video` |
| 83 | `cat-b-32` | NVIDIA Parakeet-TDT Transducer | `B` | `video` | `lazy_tool('cat-b-32')` | `research,news,social,video` |
| 84 | `cat-b-33` | NVIDIA NeMo Speech Toolkit | `B` | `video` | `lazy_tool('cat-b-33')` | `research,news,social,video` |
| 85 | `cat-b-34` | SpeechBrain All-in-One Audio | `B` | `video` | `lazy_tool('cat-b-34')` | `research,news,social,video` |
| 86 | `cat-b-35` | ESPnet End-to-End S2T | `B` | `video` | `lazy_tool('cat-b-35')` | `research,news,social,video` |
| 87 | `cat-b-36` | Maestro-U Unsupervised ASR | `B` | `video` | `lazy_tool('cat-b-36')` | `research,news,social,video` |
| 88 | `cat-b-37` | YT-Whisper Stream Transcriber | `B` | `video` | `lazy_tool('cat-b-37')` | `research,news,social,video` |
| 89 | `cat-b-38` | Lingvo Sequence Framework | `B` | `video` | `lazy_tool('cat-b-38')` | `research,news,social,video` |
| 90 | `cat-b-39` | TorchAudio Streaming Pipeline | `B` | `video` | `lazy_tool('cat-b-39')` | `research,news,social,video` |
| 91 | `cat-b-40` | HF Transformers Translation Pipeline | `B` | `video` | `lazy_tool('cat-b-40')` | `research,news,social,video` |
| 92 | `cat-b-41` | CTranslate2 INT8 Inference | `B` | `video` | `lazy_tool('cat-b-41')` | `research,news,social,video` |
| 93 | `cat-b-42` | FasterTransformer Decoder | `B` | `video` | `lazy_tool('cat-b-42')` | `research,news,social,video` |
| 94 | `cat-b-43` | TensorRT-LLM MT Engine | `B` | `video` | `lazy_tool('cat-b-43')` | `research,news,social,video` |
| 95 | `cat-b-44` | vLLM Multilingual Batch Server | `B` | `video` | `lazy_tool('cat-b-44')` | `research,news,social,video` |
| 96 | `cat-b-45` | LiteLLM Translation Router | `B` | `video` | `lazy_tool('cat-b-45')` | `research,news,social,video` |
| 97 | `cat-b-46` | OpenRouter Multi-Key MT Fallback | `B` | `video` | `lazy_tool('cat-b-46')` | `research,news,social,video` |
| 98 | `cat-b-47` | Domain Glossary Injector | `B` | `video` | `lazy_tool('cat-b-47')` | `research,news,social,video` |
| 99 | `cat-b-48` | Contextual Document-Level MT | `B` | `video` | `lazy_tool('cat-b-48')` | `research,news,social,video` |
| 100 | `cat-b-49` | Formality Register Controller | `B` | `video` | `lazy_tool('cat-b-49')` | `research,news,social,video` |
| 101 | `cat-b-50` | AnyAscii Unicode Transliterator | `B` | `video` | `lazy_tool('cat-b-50')` | `research,news,social,video` |
| 102 | `cat-b-51` | DeepMultilingual Punctuation Restorer | `B` | `video` | `lazy_tool('cat-b-51')` | `research,news,social,video` |

### Category C: Messaging & Omnichannel (50 Tools)

| # | Tool ID | Name | Category | Stage | Lazy Runner | Tabs |
|---:|---|---|---|---|---|---|
| 103 | `cat-c-01` | WAHA WhatsApp HTTP API | `C` | `messaging` | `lazy_tool('cat-c-01')` | `agents,social,business,leads` |
| 104 | `cat-c-02` | Baileys @whiskeysockets Multi-Device | `C` | `messaging` | `lazy_tool('cat-c-02')` | `agents,social,business,leads` |
| 105 | `cat-c-03` | whatsapp-web.js Headless Bridge | `C` | `messaging` | `lazy_tool('cat-c-03')` | `agents,social,business,leads` |
| 106 | `cat-c-04` | Evolution API v2 Omnichannel | `C` | `messaging` | `lazy_tool('cat-c-04')` | `agents,social,business,leads` |
| 107 | `cat-c-05` | WPPConnect WhatsApp Server | `C` | `messaging` | `lazy_tool('cat-c-05')` | `agents,social,business,leads` |
| 108 | `cat-c-06` | Venom-Bot Node WhatsApp | `C` | `messaging` | `lazy_tool('cat-c-06')` | `agents,social,business,leads` |
| 109 | `cat-c-07` | OpenWA Automate Toolkit | `C` | `messaging` | `lazy_tool('cat-c-07')` | `agents,social,business,leads` |
| 110 | `cat-c-08` | Chatwoot Omnichannel Inbox | `C` | `messaging` | `lazy_tool('cat-c-08')` | `agents,social,business,leads` |
| 111 | `cat-c-09` | Typebot Conversational Funnel Builder | `C` | `messaging` | `lazy_tool('cat-c-09')` | `agents,social,business,leads` |
| 112 | `cat-c-10` | Botpress v12 Visual Agent Studio | `C` | `messaging` | `lazy_tool('cat-c-10')` | `agents,social,business,leads` |
| 113 | `cat-c-11` | Rasa 3.x Open NLU Dialogue | `C` | `messaging` | `lazy_tool('cat-c-11')` | `agents,social,business,leads` |
| 114 | `cat-c-12` | Botkit Enterprise Connector | `C` | `messaging` | `lazy_tool('cat-c-12')` | `agents,social,business,leads` |
| 115 | `cat-c-13` | Hubot ChatOps Automation | `C` | `messaging` | `lazy_tool('cat-c-13')` | `agents,social,business,leads` |
| 116 | `cat-c-14` | Errbot Python Chat Daemon | `C` | `messaging` | `lazy_tool('cat-c-14')` | `agents,social,business,leads` |
| 117 | `cat-c-15` | Opsdroid Event-Driven Bot | `C` | `messaging` | `lazy_tool('cat-c-15')` | `agents,social,business,leads` |
| 118 | `cat-c-16` | BotMan Multi-Driver Framework | `C` | `messaging` | `lazy_tool('cat-c-16')` | `agents,social,business,leads` |
| 119 | `cat-c-17` | Mattermost Self-Hosted Team API | `C` | `messaging` | `lazy_tool('cat-c-17')` | `agents,social,business,leads` |
| 120 | `cat-c-18` | Rocket.Chat Sovereign Comms | `C` | `messaging` | `lazy_tool('cat-c-18')` | `agents,social,business,leads` |
| 121 | `cat-c-19` | Matrix Synapse Federated Homeserver | `C` | `messaging` | `lazy_tool('cat-c-19')` | `agents,social,business,leads` |
| 122 | `cat-c-20` | Element Matrix Bridge Suite | `C` | `messaging` | `lazy_tool('cat-c-20')` | `agents,social,business,leads` |
| 123 | `cat-c-21` | Telegram Bot API + MTProto | `C` | `messaging` | `lazy_tool('cat-c-21')` | `agents,social,business,leads` |
| 124 | `cat-c-22` | Telethon Async MTProto Client | `C` | `messaging` | `lazy_tool('cat-c-22')` | `agents,social,business,leads` |
| 125 | `cat-c-23` | Pyrogram Modern Telegram SDK | `C` | `messaging` | `lazy_tool('cat-c-23')` | `agents,social,business,leads` |
| 126 | `cat-c-24` | GramJS TypeScript MTProto | `C` | `messaging` | `lazy_tool('cat-c-24')` | `agents,social,business,leads` |
| 127 | `cat-c-25` | Discord.js v14 Gateway Bot | `C` | `messaging` | `lazy_tool('cat-c-25')` | `agents,social,business,leads` |
| 128 | `cat-c-26` | Slack Bolt Python/TS SDK | `C` | `messaging` | `lazy_tool('cat-c-26')` | `agents,social,business,leads` |
| 129 | `cat-c-27` | MS Teams Bot Framework Adapter | `C` | `messaging` | `lazy_tool('cat-c-27')` | `agents,social,business,leads` |
| 130 | `cat-c-28` | Wechaty Conversational SDK | `C` | `messaging` | `lazy_tool('cat-c-28')` | `agents,social,business,leads` |
| 131 | `cat-c-29` | LINE Messaging API SDK | `C` | `messaging` | `lazy_tool('cat-c-29')` | `agents,social,business,leads` |
| 132 | `cat-c-30` | Viber REST Bot Connector | `C` | `messaging` | `lazy_tool('cat-c-30')` | `agents,social,business,leads` |
| 133 | `cat-c-31` | signal-cli Encrypted Messenger | `C` | `messaging` | `lazy_tool('cat-c-31')` | `agents,social,business,leads` |
| 134 | `cat-c-32` | Session Oxen Onion Messenger | `C` | `messaging` | `lazy_tool('cat-c-32')` | `agents,social,business,leads` |
| 135 | `cat-c-33` | Instagram Graph API Business Reels Bridge | `C` | `messaging` | `lazy_tool('cat-c-33')` | `agents,social,business,leads` |
| 136 | `cat-c-34` | Meta Messenger Webhook SDK | `C` | `messaging` | `lazy_tool('cat-c-34')` | `agents,social,business,leads` |
| 137 | `cat-c-35` | Twilio Programmable Messaging Shim | `C` | `messaging` | `lazy_tool('cat-c-35')` | `agents,social,business,leads` |
| 138 | `cat-c-36` | Vonage Messages Dispatch Shim | `C` | `messaging` | `lazy_tool('cat-c-36')` | `agents,social,business,leads` |
| 139 | `cat-c-37` | Plivo SMS/Voice Trunk SDK | `C` | `messaging` | `lazy_tool('cat-c-37')` | `agents,social,business,leads` |
| 140 | `cat-c-38` | Gupshup WhatsApp Template Bridge | `C` | `messaging` | `lazy_tool('cat-c-38')` | `agents,social,business,leads` |
| 141 | `cat-c-39` | 360dialog Official WABA Shim | `C` | `messaging` | `lazy_tool('cat-c-39')` | `agents,social,business,leads` |
| 142 | `cat-c-40` | WATI Shared Inbox Adapter | `C` | `messaging` | `lazy_tool('cat-c-40')` | `agents,social,business,leads` |
| 143 | `cat-c-41` | Zoko Commerce WhatsApp Shim | `C` | `messaging` | `lazy_tool('cat-c-41')` | `agents,social,business,leads` |
| 144 | `cat-c-42` | Intercom Open Webhook Adapter | `C` | `messaging` | `lazy_tool('cat-c-42')` | `agents,social,business,leads` |
| 145 | `cat-c-43` | Zendesk Sunshine Conversations Shim | `C` | `messaging` | `lazy_tool('cat-c-43')` | `agents,social,business,leads` |
| 146 | `cat-c-44` | Crisp Livechat REST Bridge | `C` | `messaging` | `lazy_tool('cat-c-44')` | `agents,social,business,leads` |
| 147 | `cat-c-45` | Tawk.to Event Webhook Listener | `C` | `messaging` | `lazy_tool('cat-c-45')` | `agents,social,business,leads` |
| 148 | `cat-c-46` | LiveChat Agent SDK | `C` | `messaging` | `lazy_tool('cat-c-46')` | `agents,social,business,leads` |
| 149 | `cat-c-47` | Olark Transcript Webhook | `C` | `messaging` | `lazy_tool('cat-c-47')` | `agents,social,business,leads` |
| 150 | `cat-c-48` | Drift Playbook Open Shim | `C` | `messaging` | `lazy_tool('cat-c-48')` | `agents,social,business,leads` |
| 151 | `cat-c-49` | Freshchat Webhook Connector | `C` | `messaging` | `lazy_tool('cat-c-49')` | `agents,social,business,leads` |
| 152 | `cat-c-50` | HelpScout Mailbox Sync | `C` | `messaging` | `lazy_tool('cat-c-50')` | `agents,social,business,leads` |

### Category D: OSINT & Reconnaissance (50 Tools)

| # | Tool ID | Name | Category | Stage | Lazy Runner | Tabs |
|---:|---|---|---|---|---|---|
| 153 | `cat-d-01` | SpiderFoot HX 200+ Recon Modules | `D` | `security` | `lazy_tool('cat-d-01')` | `osint,leads,security,legal` |
| 154 | `cat-d-02` | theHarvester Domain/Email Gatherer | `D` | `security` | `lazy_tool('cat-d-02')` | `osint,leads,security,legal` |
| 155 | `cat-d-03` | Maltego CE Entity Link Graph | `D` | `security` | `lazy_tool('cat-d-03')` | `osint,leads,security,legal` |
| 156 | `cat-d-04` | Recon-ng Modular Web Recon | `D` | `security` | `lazy_tool('cat-d-04')` | `osint,leads,security,legal` |
| 157 | `cat-d-05` | OSINT Framework Taxonomy Catalog | `D` | `security` | `lazy_tool('cat-d-05')` | `osint,leads,security,legal` |
| 158 | `cat-d-06` | OWASP Amass Subdomain Mapper | `D` | `security` | `lazy_tool('cat-d-06')` | `osint,leads,security,legal` |
| 159 | `cat-d-07` | Sublist3r Passive DNS Enumerator | `D` | `security` | `lazy_tool('cat-d-07')` | `osint,leads,security,legal` |
| 160 | `cat-d-08` | Photon High-Speed OSINT Crawler | `D` | `security` | `lazy_tool('cat-d-08')` | `osint,leads,security,legal` |
| 161 | `cat-d-09` | Sherlock 400-Site Username Hunter | `D` | `security` | `lazy_tool('cat-d-09')` | `osint,leads,security,legal` |
| 162 | `cat-d-10` | Social-Analyzer 1000+ Profile Matcher | `D` | `security` | `lazy_tool('cat-d-10')` | `osint,leads,security,legal` |
| 163 | `cat-d-11` | Twint Archival Timeline Parser | `D` | `security` | `lazy_tool('cat-d-11')` | `osint,leads,security,legal` |
| 164 | `cat-d-12` | Instaloader Public Profile Archiver | `D` | `security` | `lazy_tool('cat-d-12')` | `osint,leads,security,legal` |
| 165 | `cat-d-13` | snscrape Multi-Network Archiver | `D` | `security` | `lazy_tool('cat-d-13')` | `osint,leads,security,legal` |
| 166 | `cat-d-14` | GHunt Public Workspace Investigator | `D` | `security` | `lazy_tool('cat-d-14')` | `osint,leads,security,legal` |
| 167 | `cat-d-15` | Holehe Registered-Service Checker | `D` | `security` | `lazy_tool('cat-d-15')` | `osint,leads,security,legal` |
| 168 | `cat-d-16` | Maigret 3000-Site Handle Dossier | `D` | `security` | `lazy_tool('cat-d-16')` | `osint,leads,security,legal` |
| 169 | `cat-d-17` | WhatsMyName Web Identity Enumerator | `D` | `security` | `lazy_tool('cat-d-17')` | `osint,leads,security,legal` |
| 170 | `cat-d-18` | OnionSearch Tor Index Aggregator | `D` | `security` | `lazy_tool('cat-d-18')` | `osint,leads,security,legal` |
| 171 | `cat-d-19` | TorBot Darknet Link Grapher | `D` | `security` | `lazy_tool('cat-d-19')` | `osint,leads,security,legal` |
| 172 | `cat-d-20` | Photon Deep Asset Second-Pass | `D` | `security` | `lazy_tool('cat-d-20')` | `osint,leads,security,legal` |
| 173 | `cat-d-21` | Amass Intel ASN/CIDR Mapper | `D` | `security` | `lazy_tool('cat-d-21')` | `osint,leads,security,legal` |
| 174 | `cat-d-22` | Assetfinder Passive Subdomain Tool | `D` | `security` | `lazy_tool('cat-d-22')` | `osint,leads,security,legal` |
| 175 | `cat-d-23` | Findomain Certificate Transparency | `D` | `security` | `lazy_tool('cat-d-23')` | `osint,leads,security,legal` |
| 176 | `cat-d-24` | ProjectDiscovery Subfinder | `D` | `security` | `lazy_tool('cat-d-24')` | `osint,leads,security,legal` |
| 177 | `cat-d-25` | Gitleaks Secret Commit Scanner | `D` | `security` | `lazy_tool('cat-d-25')` | `osint,leads,security,legal` |
| 178 | `cat-d-26` | TruffleHog Verified Credential Detector | `D` | `security` | `lazy_tool('cat-d-26')` | `osint,leads,security,legal` |
| 179 | `cat-d-27` | Shodan Host Exposure API | `D` | `security` | `lazy_tool('cat-d-27')` | `osint,leads,security,legal` |
| 180 | `cat-d-28` | Censys Internet-Wide Cert Search | `D` | `security` | `lazy_tool('cat-d-28')` | `osint,leads,security,legal` |
| 181 | `cat-d-29` | Hunter.io Corporate Domain Verifier | `D` | `security` | `lazy_tool('cat-d-29')` | `osint,leads,security,legal` |
| 182 | `cat-d-30` | Clearbit Company Metadata Shim | `D` | `security` | `lazy_tool('cat-d-30')` | `osint,leads,security,legal` |
| 183 | `cat-d-31` | HaveIBeenPwned k-Anonymity Breach Check | `D` | `security` | `lazy_tool('cat-d-31')` | `osint,leads,security,legal` |
| 184 | `cat-d-32` | DeHashed Credential Exposure Audit | `D` | `security` | `lazy_tool('cat-d-32')` | `osint,leads,security,legal` |
| 185 | `cat-d-33` | IntelligenceX Archival Search | `D` | `security` | `lazy_tool('cat-d-33')` | `osint,leads,security,legal` |
| 186 | `cat-d-34` | SpiderFoot Headless CLI Runner | `D` | `security` | `lazy_tool('cat-d-34')` | `osint,leads,security,legal` |
| 187 | `cat-d-35` | Recon-ng Marketplace Sync | `D` | `security` | `lazy_tool('cat-d-35')` | `osint,leads,security,legal` |
| 188 | `cat-d-36` | SpiderSuite Web Security Crawler | `D` | `security` | `lazy_tool('cat-d-36')` | `osint,leads,security,legal` |
| 189 | `cat-d-37` | OSINTgram Authorized Account Auditor | `D` | `security` | `lazy_tool('cat-d-37')` | `osint,leads,security,legal` |
| 190 | `cat-d-38` | TikTok Public Metadata Collector | `D` | `security` | `lazy_tool('cat-d-38')` | `osint,leads,security,legal` |
| 191 | `cat-d-39` | YouTube Data & Caption OSINT | `D` | `security` | `lazy_tool('cat-d-39')` | `osint,leads,security,legal` |
| 192 | `cat-d-40` | LinkedInt Public Org Mapper | `D` | `security` | `lazy_tool('cat-d-40')` | `osint,leads,security,legal` |
| 193 | `cat-d-41` | CrossLinked Corporate Naming Enumerator | `D` | `security` | `lazy_tool('cat-d-41')` | `osint,leads,security,legal` |
| 194 | `cat-d-42` | PeopleDataLabs Enrichment Shim | `D` | `security` | `lazy_tool('cat-d-42')` | `osint,leads,security,legal` |
| 195 | `cat-d-43` | Pipl Identity Resolution Shim | `D` | `security` | `lazy_tool('cat-d-43')` | `osint,leads,security,legal` |
| 196 | `cat-d-44` | SocialScan Simultaneous Email/User Check | `D` | `security` | `lazy_tool('cat-d-44')` | `osint,leads,security,legal` |
| 197 | `cat-d-45` | EmailRep Reputation Scorer | `D` | `security` | `lazy_tool('cat-d-45')` | `osint,leads,security,legal` |
| 198 | `cat-d-46` | PhoneInfoga Carrier & Number OSINT | `D` | `security` | `lazy_tool('cat-d-46')` | `osint,leads,security,legal` |
| 199 | `cat-d-47` | NumVerify Telecom Prefix Validator | `D` | `security` | `lazy_tool('cat-d-47')` | `osint,leads,security,legal` |
| 200 | `cat-d-48` | TrueCallerPy Authorized Lookup Shim | `D` | `security` | `lazy_tool('cat-d-48')` | `osint,leads,security,legal` |
| 201 | `cat-d-49` | OSINT-SPY IP/Domain/BTC Analyzer | `D` | `security` | `lazy_tool('cat-d-49')` | `osint,leads,security,legal` |
| 202 | `cat-d-50` | DorkSearch Structured Query Builder | `D` | `security` | `lazy_tool('cat-d-50')` | `osint,leads,security,legal` |

### Category E: Web Scraping & CUA Browser Fleet (55 Tools)

| # | Tool ID | Name | Category | Stage | Lazy Runner | Tabs |
|---:|---|---|---|---|---|---|
| 203 | `cat-e-01` | Apify SDK Python Actor Runtime | `E` | `base` | `lazy_tool('cat-e-01')` | `web,leads,real_estate,research` |
| 204 | `cat-e-02` | Scrapy 2.11 Async Spider Engine | `E` | `base` | `lazy_tool('cat-e-02')` | `web,leads,real_estate,research` |
| 205 | `cat-e-03` | Playwright Python/Node 1.44 | `E` | `base` | `lazy_tool('cat-e-03')` | `web,leads,real_estate,research` |
| 206 | `cat-e-04` | Puppeteer 22 Chromium Automation | `E` | `base` | `lazy_tool('cat-e-04')` | `web,leads,real_estate,research` |
| 207 | `cat-e-05` | Selenium 4.21 Distributed Grid | `E` | `base` | `lazy_tool('cat-e-05')` | `web,leads,real_estate,research` |
| 208 | `cat-e-06` | BeautifulSoup4 + lxml Fast Parser | `E` | `base` | `lazy_tool('cat-e-06')` | `web,leads,real_estate,research` |
| 209 | `cat-e-07` | Pyppeteer Async CDP Driver | `E` | `base` | `lazy_tool('cat-e-07')` | `web,leads,real_estate,research` |
| 210 | `cat-e-08` | Crawlee Python 0.5 Adaptive Crawler | `E` | `base` | `lazy_tool('cat-e-08')` | `web,leads,real_estate,research` |
| 211 | `cat-e-09` | Crawlee Node 3.7 Browser Crawler | `E` | `base` | `lazy_tool('cat-e-09')` | `web,leads,real_estate,research` |
| 212 | `cat-e-10` | ScrapFly Open Stealth Adapter | `E` | `base` | `lazy_tool('cat-e-10')` | `web,leads,real_estate,research` |
| 213 | `cat-e-11` | Colly Lightning Go Scraper | `E` | `base` | `lazy_tool('cat-e-11')` | `web,leads,real_estate,research` |
| 214 | `cat-e-12` | Goutte PHP DOM Extractor | `E` | `base` | `lazy_tool('cat-e-12')` | `web,leads,real_estate,research` |
| 215 | `cat-e-13` | SimpleCrawler Node Event Spider | `E` | `base` | `lazy_tool('cat-e-13')` | `web,leads,real_estate,research` |
| 216 | `cat-e-14` | Node-Crawler Pool Worker | `E` | `base` | `lazy_tool('cat-e-14')` | `web,leads,real_estate,research` |
| 217 | `cat-e-15` | ScrapeGraphAI LLM-Guided Extractor | `E` | `base` | `lazy_tool('cat-e-15')` | `web,leads,real_estate,research` |
| 218 | `cat-e-16` | Browserless.io Self-Hosted Chrome Pool | `E` | `base` | `lazy_tool('cat-e-16')` | `web,leads,real_estate,research` |
| 219 | `cat-e-17` | HTTPX Async HTTP/2 Client | `E` | `base` | `lazy_tool('cat-e-17')` | `web,leads,real_estate,research` |
| 220 | `cat-e-18` | ProxyBroker Async Proxy Rotator | `E` | `base` | `lazy_tool('cat-e-18')` | `web,leads,real_estate,research` |
| 221 | `cat-e-19` | Playwright-Stealth Fingerprint Guard | `E` | `base` | `lazy_tool('cat-e-19')` | `web,leads,real_estate,research` |
| 222 | `cat-e-20` | Undetected-Chromedriver Patch | `E` | `base` | `lazy_tool('cat-e-20')` | `web,leads,real_estate,research` |
| 223 | `cat-e-21` | Cloudscraper Challenge Solver | `E` | `base` | `lazy_tool('cat-e-21')` | `web,leads,real_estate,research` |
| 224 | `cat-e-22` | curl_cffi BoringSSL/JA3 Impersonator | `E` | `base` | `lazy_tool('cat-e-22')` | `web,leads,real_estate,research` |
| 225 | `cat-e-23` | TLS-Client Go TLS Profile Wrapper | `E` | `base` | `lazy_tool('cat-e-23')` | `web,leads,real_estate,research` |
| 226 | `cat-e-24` | Scrapy-Redis Distributed Frontier | `E` | `base` | `lazy_tool('cat-e-24')` | `web,leads,real_estate,research` |
| 227 | `cat-e-25` | Frontera Large-Scale Crawl Frontier | `E` | `base` | `lazy_tool('cat-e-25')` | `web,leads,real_estate,research` |
| 228 | `cat-e-26` | Scrapy-Cluster Kafka Coordinator | `E` | `base` | `lazy_tool('cat-e-26')` | `web,leads,real_estate,research` |
| 229 | `cat-e-27` | Apache Kafka Crawl Event Bus | `E` | `base` | `lazy_tool('cat-e-27')` | `web,leads,real_estate,research` |
| 230 | `cat-e-28` | RabbitMQ Task Broker | `E` | `base` | `lazy_tool('cat-e-28')` | `web,leads,real_estate,research` |
| 231 | `cat-e-29` | RQ Redis Simple Job Queue | `E` | `base` | `lazy_tool('cat-e-29')` | `web,leads,real_estate,research` |
| 232 | `cat-e-30` | Celery Beat Periodic Crawl Scheduler | `E` | `base` | `lazy_tool('cat-e-30')` | `web,leads,real_estate,research` |
| 233 | `cat-e-31` | Dramatiq Reliable Actor Queue | `E` | `base` | `lazy_tool('cat-e-31')` | `web,leads,real_estate,research` |
| 234 | `cat-e-32` | SeleniumBase UC Mode Framework | `E` | `base` | `lazy_tool('cat-e-32')` | `web,leads,real_estate,research` |
| 235 | `cat-e-33` | Parker Structured Rule Extractor | `E` | `base` | `lazy_tool('cat-e-33')` | `web,leads,real_estate,research` |
| 236 | `cat-e-34` | Trafilatura Clean Article Extractor | `E` | `base` | `lazy_tool('cat-e-34')` | `web,leads,real_estate,research` |
| 237 | `cat-e-35` | Newspaper3k News Metadata Parser | `E` | `base` | `lazy_tool('cat-e-35')` | `web,leads,real_estate,research` |
| 238 | `cat-e-36` | Goose3 Main-Body Extractor | `E` | `base` | `lazy_tool('cat-e-36')` | `web,leads,real_estate,research` |
| 239 | `cat-e-37` | Readability.js Clean DOM Distiller | `E` | `base` | `lazy_tool('cat-e-37')` | `web,leads,real_estate,research` |
| 240 | `cat-e-38` | Mozilla Readability Reader View | `E` | `base` | `lazy_tool('cat-e-38')` | `web,leads,real_estate,research` |
| 241 | `cat-e-39` | Cheerio Fast jQuery-Core DOM | `E` | `base` | `lazy_tool('cat-e-39')` | `web,leads,real_estate,research` |
| 242 | `cat-e-40` | jsdom Standards DOM Emulator | `E` | `base` | `lazy_tool('cat-e-40')` | `web,leads,real_estate,research` |
| 243 | `cat-e-41` | Puppeteer-Extra-Plugin-Stealth | `E` | `base` | `lazy_tool('cat-e-41')` | `web,leads,real_estate,research` |
| 244 | `cat-e-42` | FingerprintSwitcher Viewport Manager | `E` | `base` | `lazy_tool('cat-e-42')` | `web,leads,real_estate,research` |
| 245 | `cat-e-43` | ProxyChain Local Auth Forwarder | `E` | `base` | `lazy_tool('cat-e-43')` | `web,leads,real_estate,research` |
| 246 | `cat-e-44` | Open Proxy List Health Validator | `E` | `base` | `lazy_tool('cat-e-44')` | `web,leads,real_estate,research` |
| 247 | `cat-e-45` | Enterprise Residential Proxy Shim | `E` | `base` | `lazy_tool('cat-e-45')` | `web,leads,real_estate,research` |
| 248 | `cat-e-46` | Rotating Geo-Proxy Session Manager | `E` | `base` | `lazy_tool('cat-e-46')` | `web,leads,real_estate,research` |
| 249 | `cat-e-47` | Scrapoxy Cloud Proxy Auto-Scaler | `E` | `base` | `lazy_tool('cat-e-47')` | `web,leads,real_estate,research` |
| 250 | `cat-e-48` | Smart Proxy Backoff Controller | `E` | `base` | `lazy_tool('cat-e-48')` | `web,leads,real_estate,research` |
| 251 | `cat-e-49` | Splash Lua Headless Renderer | `E` | `base` | `lazy_tool('cat-e-49')` | `web,leads,real_estate,research` |
| 252 | `cat-e-50` | Self-Hosted Scrapyd Cluster | `E` | `base` | `lazy_tool('cat-e-50')` | `web,leads,real_estate,research` |
| 253 | `cat-e-51` | Portia Visual Point-and-Click Scraper | `E` | `base` | `lazy_tool('cat-e-51')` | `web,leads,real_estate,research` |
| 254 | `cat-e-52` | RoboBrowser Lightweight Form Agent | `E` | `base` | `lazy_tool('cat-e-52')` | `web,leads,real_estate,research` |
| 255 | `cat-e-53` | MechanicalSoup Stateful Session Bot | `E` | `base` | `lazy_tool('cat-e-53')` | `web,leads,real_estate,research` |
| 256 | `cat-e-54` | Requests-HTML JS-Capable Client | `E` | `base` | `lazy_tool('cat-e-54')` | `web,leads,real_estate,research` |
| 257 | `cat-e-55` | PyQuery jQuery-Syntax XML/HTML | `E` | `base` | `lazy_tool('cat-e-55')` | `web,leads,real_estate,research` |

### Category F: Deep Research & Knowledge Ingestion (50 Tools)

| # | Tool ID | Name | Category | Stage | Lazy Runner | Tabs |
|---:|---|---|---|---|---|---|
| 258 | `cat-f-01` | Ling-3.1-Flash 1M Whole-Site Reader | `F` | `base` | `lazy_tool('cat-f-01')` | `research,legal,finance,investments,news` |
| 259 | `cat-f-02` | GLM-5.3 Flash Long-Context Synthesizer | `F` | `base` | `lazy_tool('cat-f-02')` | `research,legal,finance,investments,news` |
| 260 | `cat-f-03` | Qwen3.8-27B 2.19M Chain-of-Thought | `F` | `base` | `lazy_tool('cat-f-03')` | `research,legal,finance,investments,news` |
| 261 | `cat-f-04` | DeepSeek-V4-Flash Frontier Analyst | `F` | `base` | `lazy_tool('cat-f-04')` | `research,legal,finance,investments,news` |
| 262 | `cat-f-05` | MiMo-V2.5-310B Paper Corpus Engine | `F` | `base` | `lazy_tool('cat-f-05')` | `research,legal,finance,investments,news` |
| 263 | `cat-f-06` | Perplexica Self-Hosted AI Search | `F` | `base` | `lazy_tool('cat-f-06')` | `research,legal,finance,investments,news` |
| 264 | `cat-f-07` | Haystack 2.x Deepset RAG Pipelines | `F` | `base` | `lazy_tool('cat-f-07')` | `research,legal,finance,investments,news` |
| 265 | `cat-f-08` | LangChain 0.2 Runnable Graphs | `F` | `base` | `lazy_tool('cat-f-08')` | `research,legal,finance,investments,news` |
| 266 | `cat-f-09` | LlamaIndex 0.11 Property Graph RAG | `F` | `base` | `lazy_tool('cat-f-09')` | `research,legal,finance,investments,news` |
| 267 | `cat-f-10` | DSPy Stanford Prompt Compiler | `F` | `base` | `lazy_tool('cat-f-10')` | `research,legal,finance,investments,news` |
| 268 | `cat-f-11` | PaperQA2 High-Precision Citation QA | `F` | `base` | `lazy_tool('cat-f-11')` | `research,legal,finance,investments,news` |
| 269 | `cat-f-12` | Elicit Literature Matrix Shim | `F` | `base` | `lazy_tool('cat-f-12')` | `research,legal,finance,investments,news` |
| 270 | `cat-f-13` | Semantic Scholar 200M-Paper API | `F` | `base` | `lazy_tool('cat-f-13')` | `research,legal,finance,investments,news` |
| 271 | `cat-f-14` | arXiv 2.4M Preprint Bulk Harvester | `F` | `base` | `lazy_tool('cat-f-14')` | `research,legal,finance,investments,news` |
| 272 | `cat-f-15` | OpenAlex 250M Scholarly Graph | `F` | `base` | `lazy_tool('cat-f-15')` | `research,legal,finance,investments,news` |
| 273 | `cat-f-16` | Crossref DOI Citation Resolver | `F` | `base` | `lazy_tool('cat-f-16')` | `research,legal,finance,investments,news` |
| 274 | `cat-f-17` | PubMed NCBI E-Utilities Connector | `F` | `base` | `lazy_tool('cat-f-17')` | `research,legal,finance,investments,news` |
| 275 | `cat-f-18` | PubMed Central Open-Access XML | `F` | `base` | `lazy_tool('cat-f-18')` | `research,legal,finance,investments,news` |
| 276 | `cat-f-19` | CORE Global Open-Access Aggregator | `F` | `base` | `lazy_tool('cat-f-19')` | `research,legal,finance,investments,news` |
| 277 | `cat-f-20` | BASE Bielefeld Academic Search | `F` | `base` | `lazy_tool('cat-f-20')` | `research,legal,finance,investments,news` |
| 278 | `cat-f-21` | OpenReview Peer-Review Corpus | `F` | `base` | `lazy_tool('cat-f-21')` | `research,legal,finance,investments,news` |
| 279 | `cat-f-22` | Google Scholar SerpAPI Citation Shim | `F` | `base` | `lazy_tool('cat-f-22')` | `research,legal,finance,investments,news` |
| 280 | `cat-f-23` | Bing Web Search Grounding Shim | `F` | `base` | `lazy_tool('cat-f-23')` | `research,legal,finance,investments,news` |
| 281 | `cat-f-24` | Brave Independent Index Search API | `F` | `base` | `lazy_tool('cat-f-24')` | `research,legal,finance,investments,news` |
| 282 | `cat-f-25` | Tavily Agentic Research Search | `F` | `base` | `lazy_tool('cat-f-25')` | `research,legal,finance,investments,news` |
| 283 | `cat-f-26` | Exa.ai Neural Embeddings Web Search | `F` | `base` | `lazy_tool('cat-f-26')` | `research,legal,finance,investments,news` |
| 284 | `cat-f-27` | You.com RAG Web Snippet API | `F` | `base` | `lazy_tool('cat-f-27')` | `research,legal,finance,investments,news` |
| 285 | `cat-f-28` | Serper.dev Low-Latency SERP JSON | `F` | `base` | `lazy_tool('cat-f-28')` | `research,legal,finance,investments,news` |
| 286 | `cat-f-29` | SerpAPI Multi-Engine Structured Search | `F` | `base` | `lazy_tool('cat-f-29')` | `research,legal,finance,investments,news` |
| 287 | `cat-f-30` | SearXNG Self-Hosted Metasearch | `F` | `base` | `lazy_tool('cat-f-30')` | `research,legal,finance,investments,news` |
| 288 | `cat-f-31` | Whoogle Privacy Search Proxy | `F` | `base` | `lazy_tool('cat-f-31')` | `research,legal,finance,investments,news` |
| 289 | `cat-f-32` | Kagi Universal Summarizer Shim | `F` | `base` | `lazy_tool('cat-f-32')` | `research,legal,finance,investments,news` |
| 290 | `cat-f-33` | Marginalia Non-Commercial Web Index | `F` | `base` | `lazy_tool('cat-f-33')` | `research,legal,finance,investments,news` |
| 291 | `cat-f-34` | OpenScholar Citation-Verified LM | `F` | `base` | `lazy_tool('cat-f-34')` | `research,legal,finance,investments,news` |
| 292 | `cat-f-35` | Galactica Scientific Token Parser | `F` | `base` | `lazy_tool('cat-f-35')` | `research,legal,finance,investments,news` |
| 293 | `cat-f-36` | SciBERT Scientific Entity Tagger | `F` | `base` | `lazy_tool('cat-f-36')` | `research,legal,finance,investments,news` |
| 294 | `cat-f-37` | BioBERT Biomedical Literature NER | `F` | `base` | `lazy_tool('cat-f-37')` | `research,legal,finance,investments,news` |
| 295 | `cat-f-38` | Longformer Sparse-Attention Encoder | `F` | `base` | `lazy_tool('cat-f-38')` | `research,legal,finance,investments,news` |
| 296 | `cat-f-39` | BigBird Block-Sparse Document Encoder | `F` | `base` | `lazy_tool('cat-f-39')` | `research,legal,finance,investments,news` |
| 297 | `cat-f-40` | Unstructured.io Multi-Format Chunker | `F` | `base` | `lazy_tool('cat-f-40')` | `research,legal,finance,investments,news` |
| 298 | `cat-f-41` | LlamaParse Complex Table Extractor | `F` | `base` | `lazy_tool('cat-f-41')` | `research,legal,finance,investments,news` |
| 299 | `cat-f-42` | IBM Docling Layout-Aware PDF->MD | `F` | `base` | `lazy_tool('cat-f-42')` | `research,legal,finance,investments,news` |
| 300 | `cat-f-43` | Marker Fast GPU PDF-to-Markdown | `F` | `base` | `lazy_tool('cat-f-43')` | `research,legal,finance,investments,news` |
| 301 | `cat-f-44` | GROBID TEI-XML Scholarly PDF Parser | `F` | `base` | `lazy_tool('cat-f-44')` | `research,legal,finance,investments,news` |
| 302 | `cat-f-45` | PaddleOCR Multilingual Table OCR | `F` | `base` | `lazy_tool('cat-f-45')` | `research,legal,finance,investments,news` |
| 303 | `cat-f-46` | Tesseract 5 LSTM Document OCR | `F` | `base` | `lazy_tool('cat-f-46')` | `research,legal,finance,investments,news` |
| 304 | `cat-f-47` | LayoutParser Deep Document Segmentation | `F` | `base` | `lazy_tool('cat-f-47')` | `research,legal,finance,investments,news` |
| 305 | `cat-f-48` | MinerU PDF Formula/Table Extractor | `F` | `base` | `lazy_tool('cat-f-48')` | `research,legal,finance,investments,news` |
| 306 | `cat-f-49` | OpenTimestamps + IPFS Kubo Proof-of-Existence | `F` | `base` | `lazy_tool('cat-f-49')` | `research,legal,finance,investments,news` |
| 307 | `cat-f-50` | Qdrant 768d Hybrid Dense/Sparse Indexer | `F` | `base` | `lazy_tool('cat-f-50')` | `research,legal,finance,investments,news` |

### Category G: Security, WAF, SIEM, eBPF & Honeypot (52 Tools)

| # | Tool ID | Name | Category | Stage | Lazy Runner | Tabs |
|---:|---|---|---|---|---|---|
| 308 | `cat-g-01` | CrowdSec 100k Collaborative Behavioral WAF | `G` | `security` | `lazy_tool('cat-g-01')` | `security,finance,investments,home` |
| 309 | `cat-g-02` | Wazuh 4.8 SIEM + FIM + XDR | `G` | `security` | `lazy_tool('cat-g-02')` | `security,finance,investments,home` |
| 310 | `cat-g-03` | Suricata 7 100Gbps IDS/IPS | `G` | `security` | `lazy_tool('cat-g-03')` | `security,finance,investments,home` |
| 311 | `cat-g-04` | Falco eBPF Syscall Anomaly Monitor | `G` | `security` | `lazy_tool('cat-g-04')` | `security,finance,investments,home` |
| 312 | `cat-g-05` | Tetragon Cilium eBPF Policy Enforcement | `G` | `security` | `lazy_tool('cat-g-05')` | `security,finance,investments,home` |
| 313 | `cat-g-06` | Aqua Tracee 200+ eBPF Forensics | `G` | `security` | `lazy_tool('cat-g-06')` | `security,finance,investments,home` |
| 314 | `cat-g-07` | KubeArmor eBPF + LSM Container Block | `G` | `security` | `lazy_tool('cat-g-07')` | `security,finance,investments,home` |
| 315 | `cat-g-08` | Aya Rust + BCC Python Custom kprobe Sensor | `G` | `security` | `lazy_tool('cat-g-08')` | `security,finance,investments,home` |
| 316 | `cat-g-09` | HashiCorp Vault 1.15 HSM Transit Engine | `G` | `security` | `lazy_tool('cat-g-09')` | `security,finance,investments,home` |
| 317 | `cat-g-10` | WireGuard Zero Trust mTLS Mesh | `G` | `security` | `lazy_tool('cat-g-10')` | `security,finance,investments,home` |
| 318 | `cat-g-11` | Cowrie SSH/HTTP Honeypot + Police PDF Exporter | `G` | `security` | `lazy_tool('cat-g-11')` | `security,finance,investments,home` |
| 319 | `cat-g-12` | Thinkst Canarytokens Tripwire Generator | `G` | `security` | `lazy_tool('cat-g-12')` | `security,finance,investments,home` |
| 320 | `cat-g-13` | ModSecurity v3 + OWASP CRS 4.2 | `G` | `security` | `lazy_tool('cat-g-13')` | `security,finance,investments,home` |
| 321 | `cat-g-14` | Zeek 6 Network Security Monitor | `G` | `security` | `lazy_tool('cat-g-14')` | `security,finance,investments,home` |
| 322 | `cat-g-15` | Osquery 5.12 SQL Endpoint Telemetry | `G` | `security` | `lazy_tool('cat-g-15')` | `security,finance,investments,home` |
| 323 | `cat-g-16` | Velociraptor DFIR Endpoint Hunt | `G` | `security` | `lazy_tool('cat-g-16')` | `security,finance,investments,home` |
| 324 | `cat-g-17` | Loki + Promtail + Prometheus + Grafana Stack | `G` | `security` | `lazy_tool('cat-g-17')` | `security,finance,investments,home` |
| 325 | `cat-g-18` | Watchtower + Keel Zero-Downtime Self-Healing | `G` | `security` | `lazy_tool('cat-g-18')` | `security,finance,investments,home` |
| 326 | `cat-g-19` | OpenHands + SWE-agent Autonomous Patch Engine | `G` | `security` | `lazy_tool('cat-g-19')` | `security,finance,investments,home` |
| 327 | `cat-g-20` | Aider Git-Native Security Patcher | `G` | `security` | `lazy_tool('cat-g-20')` | `security,finance,investments,home` |
| 328 | `cat-g-21` | CompreFace facial_enrolled + FIDO2 WebAuthn VideoKYC | `G` | `security` | `lazy_tool('cat-g-21')` | `security,finance,investments,home` |
| 329 | `cat-g-22` | Authelia Forward-Auth 2FA Portal | `G` | `security` | `lazy_tool('cat-g-22')` | `security,finance,investments,home` |
| 330 | `cat-g-23` | Authentik Sovereign IdP & OIDC | `G` | `security` | `lazy_tool('cat-g-23')` | `security,finance,investments,home` |
| 331 | `cat-g-24` | Keycloak Enterprise Federation | `G` | `security` | `lazy_tool('cat-g-24')` | `security,finance,investments,home` |
| 332 | `cat-g-25` | Ory Kratos Cloud-Native Identity | `G` | `security` | `lazy_tool('cat-g-25')` | `security,finance,investments,home` |
| 333 | `cat-g-26` | Cerbos Stateless Fine-Grained AuthZ | `G` | `security` | `lazy_tool('cat-g-26')` | `security,finance,investments,home` |
| 334 | `cat-g-27` | Open Policy Agent (OPA) Gatekeeper | `G` | `security` | `lazy_tool('cat-g-27')` | `security,finance,investments,home` |
| 335 | `cat-g-28` | Kyverno Kubernetes Policy Engine | `G` | `security` | `lazy_tool('cat-g-28')` | `security,finance,investments,home` |
| 336 | `cat-g-29` | Aqua Trivy Container/FS Vulnerability Scanner | `G` | `security` | `lazy_tool('cat-g-29')` | `security,finance,investments,home` |
| 337 | `cat-g-30` | Anchore Grype + Syft Cyclonedx SBOM | `G` | `security` | `lazy_tool('cat-g-30')` | `security,finance,investments,home` |
| 338 | `cat-g-31` | Quay Clair Static Layer Analyzer | `G` | `security` | `lazy_tool('cat-g-31')` | `security,finance,investments,home` |
| 339 | `cat-g-32` | Harbor Signed Artifact Registry | `G` | `security` | `lazy_tool('cat-g-32')` | `security,finance,investments,home` |
| 340 | `cat-g-33` | Notary v2 TUF Content Trust | `G` | `security` | `lazy_tool('cat-g-33')` | `security,finance,investments,home` |
| 341 | `cat-g-34` | Sigstore Cosign Keyless Provenance | `G` | `security` | `lazy_tool('cat-g-34')` | `security,finance,investments,home` |
| 342 | `cat-g-35` | Falco Talon Automated Threat Responder | `G` | `security` | `lazy_tool('cat-g-35')` | `security,finance,investments,home` |
| 343 | `cat-g-36` | CrowdSec Nginx/Traefik/Cloudflare Bouncer | `G` | `security` | `lazy_tool('cat-g-36')` | `security,finance,investments,home` |
| 344 | `cat-g-37` | Wazuh Active-Response Firewall Blocker | `G` | `security` | `lazy_tool('cat-g-37')` | `security,finance,investments,home` |
| 345 | `cat-g-38` | Suricata-Update ET Open Rule Refresher | `G` | `security` | `lazy_tool('cat-g-38')` | `security,finance,investments,home` |
| 346 | `cat-g-39` | Snort 3 Packet Inspection Engine | `G` | `security` | `lazy_tool('cat-g-39')` | `security,finance,investments,home` |
| 347 | `cat-g-40` | pfSense Perimeter Firewall Configurator | `G` | `security` | `lazy_tool('cat-g-40')` | `security,finance,investments,home` |
| 348 | `cat-g-41` | OPNsense API Firewall Bridge | `G` | `security` | `lazy_tool('cat-g-41')` | `security,finance,investments,home` |
| 349 | `cat-g-42` | CrowdSec Cyber Threat Intelligence Feed | `G` | `security` | `lazy_tool('cat-g-42')` | `security,finance,investments,home` |
| 350 | `cat-g-43` | MISP Threat Sharing Platform | `G` | `security` | `lazy_tool('cat-g-43')` | `security,finance,investments,home` |
| 351 | `cat-g-44` | TheHive + Cortex Incident Response | `G` | `security` | `lazy_tool('cat-g-44')` | `security,finance,investments,home` |
| 352 | `cat-g-45` | Shuffle Open-Source SOAR Workflows | `G` | `security` | `lazy_tool('cat-g-45')` | `security,finance,investments,home` |
| 353 | `cat-g-46` | Wazuh ML Sandbox Anomaly Trainer | `G` | `security` | `lazy_tool('cat-g-46')` | `security,finance,investments,home` |
| 354 | `cat-g-47` | Vault PKI Short-Lived mTLS Rotator | `G` | `security` | `lazy_tool('cat-g-47')` | `security,finance,investments,home` |
| 355 | `cat-g-48` | WireGuard Portal Peer Provisioner | `G` | `security` | `lazy_tool('cat-g-48')` | `security,finance,investments,home` |
| 356 | `cat-g-49` | Headscale Self-Hosted Tailnet Control | `G` | `security` | `lazy_tool('cat-g-49')` | `security,finance,investments,home` |
| 357 | `cat-g-50` | NetBird Zero-Trust P2P Overlay | `G` | `security` | `lazy_tool('cat-g-50')` | `security,finance,investments,home` |
| 358 | `cat-g-51` | Self-Hosted Mesh Relay Node | `G` | `security` | `lazy_tool('cat-g-51')` | `security,finance,investments,home` |
| 359 | `cat-g-52` | ZeroTier Virtual L2 Encrypted Switch | `G` | `security` | `lazy_tool('cat-g-52')` | `security,finance,investments,home` |

### Category H: Engineering, CAD, GHIDRA & Propulsion Research (52 Tools)

| # | Tool ID | Name | Category | Stage | Lazy Runner | Tabs |
|---:|---|---|---|---|---|---|
| 360 | `cat-h-01` | GHIDRA 11.2 NSA SRE Decompiler + P-Code + Ghidrathon | `H` | `engineering` | `lazy_tool('cat-h-01')` | `engineering,city,coding,real_estate` |
| 361 | `cat-h-02` | Binary Ninja Cloud HLIL/MLIL/LLIL Shim | `H` | `engineering` | `lazy_tool('cat-h-02')` | `engineering,city,coding,real_estate` |
| 362 | `cat-h-03` | Radare2 + Cutter + r2pipe Scripting | `H` | `engineering` | `lazy_tool('cat-h-03')` | `engineering,city,coding,real_estate` |
| 363 | `cat-h-04` | angr 9.2 Symbolic Execution Suite | `H` | `engineering` | `lazy_tool('cat-h-04')` | `engineering,city,coding,real_estate` |
| 364 | `cat-h-05` | FreeCAD 0.22 Parametric FEM + TechDraw | `H` | `engineering` | `lazy_tool('cat-h-05')` | `engineering,city,coding,real_estate` |
| 365 | `cat-h-06` | OpenSCAD 2024 Programmatic CSG CAD | `H` | `engineering` | `lazy_tool('cat-h-06')` | `engineering,city,coding,real_estate` |
| 366 | `cat-h-07` | Blender 4.0 Geometry Nodes & Cycles | `H` | `engineering` | `lazy_tool('cat-h-07')` | `engineering,city,coding,real_estate` |
| 367 | `cat-h-08` | KiCad 8 Schematic + 3D Multilayer PCB | `H` | `engineering` | `lazy_tool('cat-h-08')` | `engineering,city,coding,real_estate` |
| 368 | `cat-h-09` | OpenCascade 7.7 + CadQuery 2.4 Python BREP | `H` | `engineering` | `lazy_tool('cat-h-09')` | `engineering,city,coding,real_estate` |
| 369 | `cat-h-10` | OpenFOAM 12 Computational Fluid Dynamics | `H` | `engineering` | `lazy_tool('cat-h-10')` | `engineering,city,coding,real_estate` |
| 370 | `cat-h-11` | CalculiX 2.20 Structural/Thermal FEA | `H` | `engineering` | `lazy_tool('cat-h-11')` | `engineering,city,coding,real_estate` |
| 371 | `cat-h-12` | PrusaSlicer 2.8 Headless G-Code Engine | `H` | `engineering` | `lazy_tool('cat-h-12')` | `engineering,city,coding,real_estate` |
| 372 | `cat-h-13` | OpenCV 4.9 Metrology & Vision Inspection | `H` | `engineering` | `lazy_tool('cat-h-13')` | `engineering,city,coding,real_estate` |
| 373 | `cat-h-14` | IfcOpenShell 0.7 OpenBIM IFC4 Toolkit | `H` | `engineering` | `lazy_tool('cat-h-14')` | `engineering,city,coding,real_estate` |
| 374 | `cat-h-15` | OpenBOM + InvenTree Fastener/Torque BOM | `H` | `engineering` | `lazy_tool('cat-h-15')` | `engineering,city,coding,real_estate` |
| 375 | `cat-h-16` | DocAssemble + LaTeX Patent Drawing Generator | `H` | `engineering` | `lazy_tool('cat-h-16')` | `engineering,city,coding,real_estate` |
| 376 | `cat-h-17` | NASA Breakthrough Propulsion Physics Archive | `H` | `engineering` | `lazy_tool('cat-h-17')` | `engineering,city,coding,real_estate` |
| 377 | `cat-h-18` | Woodward Mach-Effect Thruster Sim Notebook | `H` | `engineering` | `lazy_tool('cat-h-18')` | `engineering,city,coding,real_estate` |
| 378 | `cat-h-19` | Superconducting Rotating-Disk Gravity Model | `H` | `engineering` | `lazy_tool('cat-h-19')` | `engineering,city,coding,real_estate` |
| 379 | `cat-h-20` | Biefeld-Brown Electrohydrodynamic Lifter FEM | `H` | `engineering` | `lazy_tool('cat-h-20')` | `engineering,city,coding,real_estate` |
| 380 | `cat-h-21` | Asymmetric RF Resonant Cavity Maxwell Solver | `H` | `engineering` | `lazy_tool('cat-h-21')` | `engineering,city,coding,real_estate` |
| 381 | `cat-h-22` | Quantum Vacuum Fluctuation Casimir Simulator | `H` | `engineering` | `lazy_tool('cat-h-22')` | `engineering,city,coding,real_estate` |
| 382 | `cat-h-23` | Elmer FEM 9 Multiphysics Electromagnetics | `H` | `engineering` | `lazy_tool('cat-h-23')` | `engineering,city,coding,real_estate` |
| 383 | `cat-h-24` | KiCad High-Voltage Creepage/Clearance DRC | `H` | `engineering` | `lazy_tool('cat-h-24')` | `engineering,city,coding,real_estate` |
| 384 | `cat-h-25` | LTspice XVII SPICE Circuit Batch Runner | `H` | `engineering` | `lazy_tool('cat-h-25')` | `engineering,city,coding,real_estate` |
| 385 | `cat-h-26` | NASA OpenMDAO 3.33 Multidisciplinary Optimizer | `H` | `engineering` | `lazy_tool('cat-h-26')` | `engineering,city,coding,real_estate` |
| 386 | `cat-h-27` | Gmsh 4.12 3D Finite-Element Mesher | `H` | `engineering` | `lazy_tool('cat-h-27')` | `engineering,city,coding,real_estate` |
| 387 | `cat-h-28` | Netgen Tetrahedral Mesh Generator | `H` | `engineering` | `lazy_tool('cat-h-28')` | `engineering,city,coding,real_estate` |
| 388 | `cat-h-29` | CalculiX CrunchiX Nonlinear Solver | `H` | `engineering` | `lazy_tool('cat-h-29')` | `engineering,city,coding,real_estate` |
| 389 | `cat-h-30` | Salome-Meca Pre/Post CAE Platform | `H` | `engineering` | `lazy_tool('cat-h-30')` | `engineering,city,coding,real_estate` |
| 390 | `cat-h-31` | Code_Aster Thermomechanical Solver | `H` | `engineering` | `lazy_tool('cat-h-31')` | `engineering,city,coding,real_estate` |
| 391 | `cat-h-32` | NASA OpenVSP Parametric Aircraft Geometry | `H` | `engineering` | `lazy_tool('cat-h-32')` | `engineering,city,coding,real_estate` |
| 392 | `cat-h-33` | SU2 Stanford Aerospace CFD Suite | `H` | `engineering` | `lazy_tool('cat-h-33')` | `engineering,city,coding,real_estate` |
| 393 | `cat-h-34` | ParaView Scientific Volume Visualizer | `H` | `engineering` | `lazy_tool('cat-h-34')` | `engineering,city,coding,real_estate` |
| 394 | `cat-h-35` | FreeCAD Fasteners ISO/DIN Screw Workbench | `H` | `engineering` | `lazy_tool('cat-h-35')` | `engineering,city,coding,real_estate` |
| 395 | `cat-h-36` | FreeCAD A2plus Kinematic Assembly | `H` | `engineering` | `lazy_tool('cat-h-36')` | `engineering,city,coding,real_estate` |
| 396 | `cat-h-37` | FreeCAD Assembly4 LCS Parametric Links | `H` | `engineering` | `lazy_tool('cat-h-37')` | `engineering,city,coding,real_estate` |
| 397 | `cat-h-38` | FreeCAD CfdOF OpenFOAM Workbench | `H` | `engineering` | `lazy_tool('cat-h-38')` | `engineering,city,coding,real_estate` |
| 398 | `cat-h-39` | FreeCAD FEM Gmsh/CalculiX Workbench | `H` | `engineering` | `lazy_tool('cat-h-39')` | `engineering,city,coding,real_estate` |
| 399 | `cat-h-40` | OpenSCAD BOSL2 Precision Gear/Thread Lib | `H` | `engineering` | `lazy_tool('cat-h-40')` | `engineering,city,coding,real_estate` |
| 400 | `cat-h-41` | KiCad RF Microstrip & Impedance Tools | `H` | `engineering` | `lazy_tool('cat-h-41')` | `engineering,city,coding,real_estate` |
| 401 | `cat-h-42` | KiKit Automated PCB Panelization | `H` | `engineering` | `lazy_tool('cat-h-42')` | `engineering,city,coding,real_estate` |
| 402 | `cat-h-43` | KiCad JLCPCB BOM/CPL Fabrication Exporter | `H` | `engineering` | `lazy_tool('cat-h-43')` | `engineering,city,coding,real_estate` |
| 403 | `cat-h-44` | Octopart + Findchips Live Component Sourcing | `H` | `engineering` | `lazy_tool('cat-h-44')` | `engineering,city,coding,real_estate` |
| 404 | `cat-h-45` | SnapEDA Footprint & Symbol Importer | `H` | `engineering` | `lazy_tool('cat-h-45')` | `engineering,city,coding,real_estate` |
| 405 | `cat-h-46` | UltraLibrarian CAD Model Connector | `H` | `engineering` | `lazy_tool('cat-h-46')` | `engineering,city,coding,real_estate` |
| 406 | `cat-h-47` | SamacSys Component Loader | `H` | `engineering` | `lazy_tool('cat-h-47')` | `engineering,city,coding,real_estate` |
| 407 | `cat-h-48` | Library.io Parametric PCB Generator | `H` | `engineering` | `lazy_tool('cat-h-48')` | `engineering,city,coding,real_estate` |
| 408 | `cat-h-49` | KiCad Symbol & Footprint Validator | `H` | `engineering` | `lazy_tool('cat-h-49')` | `engineering,city,coding,real_estate` |
| 409 | `cat-h-50` | Pcbnew Python Board Automation | `H` | `engineering` | `lazy_tool('cat-h-50')` | `engineering,city,coding,real_estate` |
| 410 | `cat-h-51` | Gerbv Gerber RS-274X Layer Verifier | `H` | `engineering` | `lazy_tool('cat-h-51')` | `engineering,city,coding,real_estate` |
| 411 | `cat-h-52` | UltiMaker Cura 5.8 CuraEngine + OctoPrint API | `H` | `engineering` | `lazy_tool('cat-h-52')` | `engineering,city,coding,real_estate` |

### Category I: Vocal Tuning, Stem Separation & Audio AI (50 Tools)

| # | Tool ID | Name | Category | Stage | Lazy Runner | Tabs |
|---:|---|---|---|---|---|---|
| 412 | `cat-i-01` | GSnap GVST Realtime Pitch Autotune | `I` | `video` | `lazy_tool('cat-i-01')` | `music,video` |
| 413 | `cat-i-02` | MAutoPitch Melda Formant-Preserving Tuner | `I` | `video` | `lazy_tool('cat-i-02')` | `music,video` |
| 414 | `cat-i-03` | Graillon 2 Auburn Live Vocal Pitch/Octaver | `I` | `video` | `lazy_tool('cat-i-03')` | `music,video` |
| 415 | `cat-i-04` | PitchProof Aegean Harmonizer Pedal | `I` | `video` | `lazy_tool('cat-i-04')` | `music,video` |
| 416 | `cat-i-05` | Open Formant-Shifter Vocal Processor | `I` | `video` | `lazy_tool('cat-i-05')` | `music,video` |
| 417 | `cat-i-06` | Voloco-Style Mobile Scale Quantizer | `I` | `video` | `lazy_tool('cat-i-06')` | `music,video` |
| 418 | `cat-i-07` | Realtime Low-Latency Scale Pitch Engine | `I` | `video` | `lazy_tool('cat-i-07')` | `music,video` |
| 419 | `cat-i-08` | Audacity 3.5 / Tenacity Batch Macro Runner | `I` | `video` | `lazy_tool('cat-i-08')` | `music,video` |
| 420 | `cat-i-09` | Ardour 8 Multitrack DAW Session Engine | `I` | `video` | `lazy_tool('cat-i-09')` | `music,video` |
| 421 | `cat-i-10` | ReaPlugs VST Chain Processor | `I` | `video` | `lazy_tool('cat-i-10')` | `music,video` |
| 422 | `cat-i-11` | Ocenaudio Spectral Editor Bridge | `I` | `video` | `lazy_tool('cat-i-11')` | `music,video` |
| 423 | `cat-i-12` | Spectral De-Click/De-Reverb Restoration Chain | `I` | `video` | `lazy_tool('cat-i-12')` | `music,video` |
| 424 | `cat-i-13` | Spleeter Deezer MIT 2/4/5-Stem Separator | `I` | `video` | `lazy_tool('cat-i-13')` | `music,video` |
| 425 | `cat-i-14` | Demucs v4 Hybrid Transformer SOTA Stems | `I` | `video` | `lazy_tool('cat-i-14')` | `music,video` |
| 426 | `cat-i-15` | RVC v2 + So-VITS-SVC 5.0 Voice Cloner | `I` | `video` | `lazy_tool('cat-i-15')` | `music,video` |
| 427 | `cat-i-16` | Applio RVC Studio Inference Pipeline | `I` | `video` | `lazy_tool('cat-i-16')` | `music,video` |
| 428 | `cat-i-17` | MyShell OpenVoice V2 Tone-Color Cloner | `I` | `video` | `lazy_tool('cat-i-17')` | `music,video` |
| 429 | `cat-i-18` | Seed-TTS Zero-Shot Prosody Transfer | `I` | `video` | `lazy_tool('cat-i-18')` | `music,video` |
| 430 | `cat-i-19` | F5-TTS Flow-Matching Singing/Speech | `I` | `video` | `lazy_tool('cat-i-19')` | `music,video` |
| 431 | `cat-i-20` | CosyVoice 2 Zero-Shot Instruction Voice | `I` | `video` | `lazy_tool('cat-i-20')` | `music,video` |
| 432 | `cat-i-21` | Free 808 Producer Kit (94 Tuned 808 Basses) | `I` | `video` | `lazy_tool('cat-i-21')` | `music,video` |
| 433 | `cat-i-22` | Meta MusicGen Small/Medium/Large/Melody | `I` | `video` | `lazy_tool('cat-i-22')` | `music,video` |
| 434 | `cat-i-23` | Stable Audio Open 44.1kHz Stereo Generator | `I` | `video` | `lazy_tool('cat-i-23')` | `music,video` |
| 435 | `cat-i-24` | Riffusion / RiffAUDIO Spectrogram Synth | `I` | `video` | `lazy_tool('cat-i-24')` | `music,video` |
| 436 | `cat-i-25` | Suno Prompt-to-Track Arrangement Shim | `I` | `video` | `lazy_tool('cat-i-25')` | `music,video` |
| 437 | `cat-i-26` | Udio Stem-Conditioned Mastering Shim | `I` | `video` | `lazy_tool('cat-i-26')` | `music,video` |
| 438 | `cat-i-27` | Aubio Onset, Tempo & Pitch Detector | `I` | `video` | `lazy_tool('cat-i-27')` | `music,video` |
| 439 | `cat-i-28` | librosa 0.11 Music Information Retrieval | `I` | `video` | `lazy_tool('cat-i-28')` | `music,video` |
| 440 | `cat-i-29` | Essentia MTG Audio Feature Extractor | `I` | `video` | `lazy_tool('cat-i-29')` | `music,video` |
| 441 | `cat-i-30` | TorchAudio GPU Spectrogram DSP | `I` | `video` | `lazy_tool('cat-i-30')` | `music,video` |
| 442 | `cat-i-31` | Spotify Pedalboard Studio VST3/AU Host | `I` | `video` | `lazy_tool('cat-i-31')` | `music,video` |
| 443 | `cat-i-32` | SoundFile Libsndfile Lossless I/O | `I` | `video` | `lazy_tool('cat-i-32')` | `music,video` |
| 444 | `cat-i-33` | Pydub High-Level Segment Crossfader | `I` | `video` | `lazy_tool('cat-i-33')` | `music,video` |
| 445 | `cat-i-34` | FFmpeg EBU R128 Loudness Normalizer | `I` | `video` | `lazy_tool('cat-i-34')` | `music,video` |
| 446 | `cat-i-35` | SoX Swiss-Army Resampler & Compander | `I` | `video` | `lazy_tool('cat-i-35')` | `music,video` |
| 447 | `cat-i-36` | Rubber Band Time-Stretch & Pitch-Shift | `I` | `video` | `lazy_tool('cat-i-36')` | `music,video` |
| 448 | `cat-i-37` | Praat Phonetics & Formant Analyzer | `I` | `video` | `lazy_tool('cat-i-37')` | `music,video` |
| 449 | `cat-i-38` | WORLD High-Quality Speech Vocoder | `I` | `video` | `lazy_tool('cat-i-38')` | `music,video` |
| 450 | `cat-i-39` | CREPE Deep Convolutional Pitch Tracker | `I` | `video` | `lazy_tool('cat-i-39')` | `music,video` |
| 451 | `cat-i-40` | PESTO Self-Supervised Pitch Estimator | `I` | `video` | `lazy_tool('cat-i-40')` | `music,video` |
| 452 | `cat-i-41` | Parselmouth Python Praat Bindings | `I` | `video` | `lazy_tool('cat-i-41')` | `music,video` |
| 453 | `cat-i-42` | RAVE IRCAM Realtime Variational Timbre | `I` | `video` | `lazy_tool('cat-i-42')` | `music,video` |
| 454 | `cat-i-43` | Google Magenta DDSP Differentiable Synth | `I` | `video` | `lazy_tool('cat-i-43')` | `music,video` |
| 455 | `cat-i-44` | NSynth Neural Wavetable Generator | `I` | `video` | `lazy_tool('cat-i-44')` | `music,video` |
| 456 | `cat-i-45` | Sonic Visualiser Annotation Exporter | `I` | `video` | `lazy_tool('cat-i-45')` | `music,video` |
| 457 | `cat-i-46` | Sonic Annotator Vamp Batch Runner | `I` | `video` | `lazy_tool('cat-i-46')` | `music,video` |
| 458 | `cat-i-47` | Spleeter Web Stem Workspace | `I` | `video` | `lazy_tool('cat-i-47')` | `music,video` |
| 459 | `cat-i-48` | Demucs Web Track Splitter | `I` | `video` | `lazy_tool('cat-i-48')` | `music,video` |
| 460 | `cat-i-49` | Ultimate Vocal Remover (UVR5) MDX-Net | `I` | `video` | `lazy_tool('cat-i-49')` | `music,video` |
| 461 | `cat-i-50` | MDX23 Ensemble Bleedless Vocal Isolator | `I` | `video` | `lazy_tool('cat-i-50')` | `music,video` |

### Category J: Images, Photoreal Skin & Biometric Isolation (53 Tools)

| # | Tool ID | Name | Category | Stage | Lazy Runner | Tabs |
|---:|---|---|---|---|---|---|
| 462 | `cat-j-01` | FLUX.1-dev 12B BFL Rectified-Flow Photoreal | `J` | `images` | `lazy_tool('cat-j-01')` | `images,fashion,social` |
| 463 | `cat-j-02` | Juggernaut XL v9 Micro-Contrast Skin | `J` | `images` | `lazy_tool('cat-j-02')` | `images,fashion,social` |
| 464 | `cat-j-03` | RealVisXL V5 Tuned Light-Brown Skin & Hair | `J` | `images` | `lazy_tool('cat-j-03')` | `images,fashion,social` |
| 465 | `cat-j-04` | Meta SAM2 Image/Video Mask Segmenter | `J` | `images` | `lazy_tool('cat-j-04')` | `images,fashion,social` |
| 466 | `cat-j-05` | Meta DINOv2 Pose-Only Zero-Color-Bleed | `J` | `images` | `lazy_tool('cat-j-05')` | `images,fashion,social` |
| 467 | `cat-j-06` | IP-Adapter Reference Feature Injector | `J` | `images` | `lazy_tool('cat-j-06')` | `images,fashion,social` |
| 468 | `cat-j-07` | InstantID Zero-Shot Facial Landmarks Lock | `J` | `images` | `lazy_tool('cat-j-07')` | `images,fashion,social` |
| 469 | `cat-j-08` | PhotoMaker V2 Stacked ID Embedding | `J` | `images` | `lazy_tool('cat-j-08')` | `images,fashion,social` |
| 470 | `cat-j-09` | FaceChain Portrait Identity LoRA Pipeline | `J` | `images` | `lazy_tool('cat-j-09')` | `images,fashion,social` |
| 471 | `cat-j-10` | ConsistentID Multi-Character Scene Lock | `J` | `images` | `lazy_tool('cat-j-10')` | `images,fashion,social` |
| 472 | `cat-j-11` | ControlNet 1.1 Canny/Depth/Normal/Pose | `J` | `images` | `lazy_tool('cat-j-11')` | `images,fashion,social` |
| 473 | `cat-j-12` | T2I-Adapter Lightweight Spatial Guide | `J` | `images` | `lazy_tool('cat-j-12')` | `images,fashion,social` |
| 474 | `cat-j-13` | CompreFace Self-Hosted ArcFace Verification | `J` | `images` | `lazy_tool('cat-j-13')` | `images,fashion,social` |
| 475 | `cat-j-14` | GroundingDINO 1.5 Text-Prompted BBox | `J` | `images` | `lazy_tool('cat-j-14')` | `images,fashion,social` |
| 476 | `cat-j-15` | BiRefNet 2024 High-Res Hair/Jewelry Matting | `J` | `images` | `lazy_tool('cat-j-15')` | `images,fashion,social` |
| 477 | `cat-j-16` | LaMa Resolution-Robust Background Inpainter | `J` | `images` | `lazy_tool('cat-j-16')` | `images,fashion,social` |
| 478 | `cat-j-17` | GFPGAN 1.4 Blind Facial Restoration | `J` | `images` | `lazy_tool('cat-j-17')` | `images,fashion,social` |
| 479 | `cat-j-18` | CodeFormer Fidelity-Controllable Face Fix | `J` | `images` | `lazy_tool('cat-j-18')` | `images,fashion,social` |
| 480 | `cat-j-19` | Real-ESRGAN x4plus Photoreal Upscaler | `J` | `images` | `lazy_tool('cat-j-19')` | `images,fashion,social` |
| 481 | `cat-j-20` | SUPIR SDXL Photo-Realistic Restorer | `J` | `images` | `lazy_tool('cat-j-20')` | `images,fashion,social` |
| 482 | `cat-j-21` | Stable Diffusion XL 1.0 Base + Refiner | `J` | `images` | `lazy_tool('cat-j-21')` | `images,fashion,social` |
| 483 | `cat-j-22` | Stable Diffusion 1.5 / 2.1 Control Pipelines | `J` | `images` | `lazy_tool('cat-j-22')` | `images,fashion,social` |
| 484 | `cat-j-23` | LCM-LoRA 4-Step Interactive Preview | `J` | `images` | `lazy_tool('cat-j-23')` | `images,fashion,social` |
| 485 | `cat-j-24` | Hyper-SD Trajectory Segmented Sampler | `J` | `images` | `lazy_tool('cat-j-24')` | `images,fashion,social` |
| 486 | `cat-j-25` | AnimateDiff SD1.5 Turntable Preview | `J` | `images` | `lazy_tool('cat-j-25')` | `images,fashion,social` |
| 487 | `cat-j-26` | IP-Adapter-FaceID-PlusV2 Biometric Adapter | `J` | `images` | `lazy_tool('cat-j-26')` | `images,fashion,social` |
| 488 | `cat-j-27` | InsightFace buffalo_l 512d ArcFace Extractor | `J` | `images` | `lazy_tool('cat-j-27')` | `images,fashion,social` |
| 489 | `cat-j-28` | MediaPipe 468-Point 3D Face Mesh | `J` | `images` | `lazy_tool('cat-j-28')` | `images,fashion,social` |
| 490 | `cat-j-29` | OpenPose Full-Body/Hand Skeleton | `J` | `images` | `lazy_tool('cat-j-29')` | `images,fashion,social` |
| 491 | `cat-j-30` | DWPose Whole-Body Distillation Pose | `J` | `images` | `lazy_tool('cat-j-30')` | `images,fashion,social` |
| 492 | `cat-j-31` | YOLOv8-Seg Instance Mask Detector | `J` | `images` | `lazy_tool('cat-j-31')` | `images,fashion,social` |
| 493 | `cat-j-32` | YOLOv9 Programmable Gradient Detector | `J` | `images` | `lazy_tool('cat-j-32')` | `images,fashion,social` |
| 494 | `cat-j-33` | RT-DETR Transformer Object Detector | `J` | `images` | `lazy_tool('cat-j-33')` | `images,fashion,social` |
| 495 | `cat-j-34` | Grounded-SAM Prompt-to-Alpha Pipeline | `J` | `images` | `lazy_tool('cat-j-34')` | `images,fashion,social` |
| 496 | `cat-j-35` | BiRefNet-HR 2048px Studio Cutout | `J` | `images` | `lazy_tool('cat-j-35')` | `images,fashion,social` |
| 497 | `cat-j-36` | U2-Net Salient Object Matting | `J` | `images` | `lazy_tool('cat-j-36')` | `images,fashion,social` |
| 498 | `cat-j-37` | IS-Net Dichotomous High-Detail Cutout | `J` | `images` | `lazy_tool('cat-j-37')` | `images,fashion,social` |
| 499 | `cat-j-38` | MODNet Trimap-Free Portrait Matting | `J` | `images` | `lazy_tool('cat-j-38')` | `images,fashion,social` |
| 500 | `cat-j-39` | PP-Matting Human Hair Alpha Engine | `J` | `images` | `lazy_tool('cat-j-39')` | `images,fashion,social` |
| 501 | `cat-j-40` | Rembg CLI/Python Background Remover | `J` | `images` | `lazy_tool('cat-j-40')` | `images,fashion,social` |
| 502 | `cat-j-41` | CarveKit Collar/Jewelry Edge Refiner | `J` | `images` | `lazy_tool('cat-j-41')` | `images,fashion,social` |
| 503 | `cat-j-42` | CLIPSeg Zero-Shot Mask Predictor | `J` | `images` | `lazy_tool('cat-j-42')` | `images,fashion,social` |
| 504 | `cat-j-43` | CLIP Interrogator Prompt Reverse-Engineer | `J` | `images` | `lazy_tool('cat-j-43')` | `images,fashion,social` |
| 505 | `cat-j-44` | BLIP-2 Visual Question & Captioning | `J` | `images` | `lazy_tool('cat-j-44')` | `images,fashion,social` |
| 506 | `cat-j-45` | LLaVA-Next High-Res Image Describer | `J` | `images` | `lazy_tool('cat-j-45')` | `images,fashion,social` |
| 507 | `cat-j-46` | Florence-2 Unified Vision Foundation | `J` | `images` | `lazy_tool('cat-j-46')` | `images,fashion,social` |
| 508 | `cat-j-47` | Kohya_ss LoRA/DreamBooth Trainer | `J` | `images` | `lazy_tool('cat-j-47')` | `images,fashion,social` |
| 509 | `cat-j-48` | OneTrainer Unified Diffusion Fine-Tuner | `J` | `images` | `lazy_tool('cat-j-48')` | `images,fashion,social` |
| 510 | `cat-j-49` | DreamBooth Subject-Driven Personalizer | `J` | `images` | `lazy_tool('cat-j-49')` | `images,fashion,social` |
| 511 | `cat-j-50` | PEFT LoRA Rank-Stabilized Adapter | `J` | `images` | `lazy_tool('cat-j-50')` | `images,fashion,social` |
| 512 | `cat-j-51` | LyCORIS LoHa/LoKr Texture Trainer | `J` | `images` | `lazy_tool('cat-j-51')` | `images,fashion,social` |
| 513 | `cat-j-52` | SDXL-Turbo Adversarial 1-Step Preview | `J` | `images` | `lazy_tool('cat-j-52')` | `images,fashion,social` |
| 514 | `cat-j-53` | SDXL-Lightning Progressive 4-Step Distill | `J` | `images` | `lazy_tool('cat-j-53')` | `images,fashion,social` |

### Category K: Video Generation, UGC, TV & Movies (50 Tools)

| # | Tool ID | Name | Category | Stage | Lazy Runner | Tabs |
|---:|---|---|---|---|---|---|
| 515 | `cat-k-01` | MiniMax Hailuo-02 720p/1080p UGC Realism | `K` | `video` | `lazy_tool('cat-k-01')` | `video,social,fashion` |
| 516 | `cat-k-02` | Wan 2.1 14B Realistic Skin & Motion | `K` | `video` | `lazy_tool('cat-k-02')` | `video,social,fashion` |
| 517 | `cat-k-03` | LTX-Video 13B Fastest 600-Clip Pipeline | `K` | `video` | `lazy_tool('cat-k-03')` | `video,social,fashion` |
| 518 | `cat-k-04` | Kling 2.0 3D Camera Trajectory Engine | `K` | `video` | `lazy_tool('cat-k-04')` | `video,social,fashion` |
| 519 | `cat-k-05` | Nex-N2-mini-35B 26-Shot Storyboarder | `K` | `video` | `lazy_tool('cat-k-05')` | `video,social,fashion` |
| 520 | `cat-k-06` | Qwen3.8-Vision 28B Camera Angle Selector | `K` | `video` | `lazy_tool('cat-k-06')` | `video,social,fashion` |
| 521 | `cat-k-07` | Qwythos-9B-Classic 5000-Char Video Prompt King | `K` | `video` | `lazy_tool('cat-k-07')` | `video,social,fashion` |
| 522 | `cat-k-08` | CogVideoX-5B Text/Image-to-Video | `K` | `video` | `lazy_tool('cat-k-08')` | `video,social,fashion` |
| 523 | `cat-k-09` | ModelScope DAMO Text-to-Video | `K` | `video` | `lazy_tool('cat-k-09')` | `video,social,fashion` |
| 524 | `cat-k-10` | AnimateDiff V3 Motion Director | `K` | `video` | `lazy_tool('cat-k-10')` | `video,social,fashion` |
| 525 | `cat-k-11` | Stable Video Diffusion 1.1 I2V | `K` | `video` | `lazy_tool('cat-k-11')` | `video,social,fashion` |
| 526 | `cat-k-12` | VideoCrafter2 High-Quality Open T2V | `K` | `video` | `lazy_tool('cat-k-12')` | `video,social,fashion` |
| 527 | `cat-k-13` | Open-Sora 1.2 Arbitrary-Aspect Video | `K` | `video` | `lazy_tool('cat-k-13')` | `video,social,fashion` |
| 528 | `cat-k-14` | Mora Multi-Agent Collaborative Video | `K` | `video` | `lazy_tool('cat-k-14')` | `video,social,fashion` |
| 529 | `cat-k-15` | Luma Dream Machine Keyframe Shim | `K` | `video` | `lazy_tool('cat-k-15')` | `video,social,fashion` |
| 530 | `cat-k-16` | Pika 1.0 Region-Modify Shim | `K` | `video` | `lazy_tool('cat-k-16')` | `video,social,fashion` |
| 531 | `cat-k-17` | Runway Gen-3 Alpha Motion-Brush Shim | `K` | `video` | `lazy_tool('cat-k-17')` | `video,social,fashion` |
| 532 | `cat-k-18` | Open DiT Long-Clip Sora-Class Shim | `K` | `video` | `lazy_tool('cat-k-18')` | `video,social,fashion` |
| 533 | `cat-k-19` | Hotshot-XL Consistent GIF/Clip Synth | `K` | `video` | `lazy_tool('cat-k-19')` | `video,social,fashion` |
| 534 | `cat-k-20` | Zeroscope V2 XL Watermark-Free 1024x576 | `K` | `video` | `lazy_tool('cat-k-20')` | `video,social,fashion` |
| 535 | `cat-k-21` | I2VGen-XL Cascaded Image-to-Video | `K` | `video` | `lazy_tool('cat-k-21')` | `video,social,fashion` |
| 536 | `cat-k-22` | DynamiCrafter Open-Domain Image Animator | `K` | `video` | `lazy_tool('cat-k-22')` | `video,social,fashion` |
| 537 | `cat-k-23` | MotionCtrl Unified Camera + Object Control | `K` | `video` | `lazy_tool('cat-k-23')` | `video,social,fashion` |
| 538 | `cat-k-24` | CameraCtrl Plucker-Ray Trajectory Guide | `K` | `video` | `lazy_tool('cat-k-24')` | `video,social,fashion` |
| 539 | `cat-k-25` | DragNUWA Trajectory-Guided Motion | `K` | `video` | `lazy_tool('cat-k-25')` | `video,social,fashion` |
| 540 | `cat-k-26` | AnimateAnyone Character Garment Consistency | `K` | `video` | `lazy_tool('cat-k-26')` | `video,social,fashion` |
| 541 | `cat-k-27` | MagicAnimate DensePose Temporal Human | `K` | `video` | `lazy_tool('cat-k-27')` | `video,social,fashion` |
| 542 | `cat-k-28` | Champ 3D SMPL Parametric Human Guide | `K` | `video` | `lazy_tool('cat-k-28')` | `video,social,fashion` |
| 543 | `cat-k-29` | MimicMotion Confidence-Aware Pose Video | `K` | `video` | `lazy_tool('cat-k-29')` | `video,social,fashion` |
| 544 | `cat-k-30` | First-Order Motion Model (FOMM) | `K` | `video` | `lazy_tool('cat-k-30')` | `video,social,fashion` |
| 545 | `cat-k-31` | Wav2Lip GAN Speech-to-Lip Aligner | `K` | `video` | `lazy_tool('cat-k-31')` | `video,social,fashion` |
| 546 | `cat-k-32` | SadTalker Stylized 3D Motion Coefficients | `K` | `video` | `lazy_tool('cat-k-32')` | `video,social,fashion` |
| 547 | `cat-k-33` | DreamTalk Emotional Talking Head | `K` | `video` | `lazy_tool('cat-k-33')` | `video,social,fashion` |
| 548 | `cat-k-34` | Alibaba EMO Expressive Audio Portrait | `K` | `video` | `lazy_tool('cat-k-34')` | `video,social,fashion` |
| 549 | `cat-k-35` | V-Express Conditional V-Kps Talking Head | `K` | `video` | `lazy_tool('cat-k-35')` | `video,social,fashion` |
| 550 | `cat-k-36` | LivePortrait Stitch-Ready Portrait Driver | `K` | `video` | `lazy_tool('cat-k-36')` | `video,social,fashion` |
| 551 | `cat-k-37` | Hallo Hierarchical Audio Visual Driven | `K` | `video` | `lazy_tool('cat-k-37')` | `video,social,fashion` |
| 552 | `cat-k-38` | EchoMimic Landmark+Audio Portrait | `K` | `video` | `lazy_tool('cat-k-38')` | `video,social,fashion` |
| 553 | `cat-k-39` | AniPortrait Audio2Mesh Character Driver | `K` | `video` | `lazy_tool('cat-k-39')` | `video,social,fashion` |
| 554 | `cat-k-40` | X-Portrait Expressive Identity Transfer | `K` | `video` | `lazy_tool('cat-k-40')` | `video,social,fashion` |
| 555 | `cat-k-41` | ToonCrafter Keyframe Interpolation | `K` | `video` | `lazy_tool('cat-k-41')` | `video,social,fashion` |
| 556 | `cat-k-42` | RIFE v4.15 60fps Smooth Interpolator | `K` | `video` | `lazy_tool('cat-k-42')` | `video,social,fashion` |
| 557 | `cat-k-43` | FILM Frame Interpolation Large Motion | `K` | `video` | `lazy_tool('cat-k-43')` | `video,social,fashion` |
| 558 | `cat-k-44` | Depth-Anything-V2 Temporal Video Depth | `K` | `video` | `lazy_tool('cat-k-44')` | `video,social,fashion` |
| 559 | `cat-k-45` | MiDaS v3.1 Monocular Depth Estimator | `K` | `video` | `lazy_tool('cat-k-45')` | `video,social,fashion` |
| 560 | `cat-k-46` | RAFT Dense All-Pairs Optical Flow | `K` | `video` | `lazy_tool('cat-k-46')` | `video,social,fashion` |
| 561 | `cat-k-47` | PWC-Net Pyramid Warping Optical Flow | `K` | `video` | `lazy_tool('cat-k-47')` | `video,social,fashion` |
| 562 | `cat-k-48` | Deforum Keyframed 3D Warp Sequencer | `K` | `video` | `lazy_tool('cat-k-48')` | `video,social,fashion` |
| 563 | `cat-k-49` | Parallax 2.5D Ken-Burns Depth Camera | `K` | `video` | `lazy_tool('cat-k-49')` | `video,social,fashion` |
| 564 | `cat-k-50` | Stable WarpFusion Optical-Flow Styler | `K` | `video` | `lazy_tool('cat-k-50')` | `video,social,fashion` |

### Category L: Sovereign Infrastructure, Hermes, Legal, Finance & GIS Core (56 Tools)

| # | Tool ID | Name | Category | Stage | Lazy Runner | Tabs |
|---:|---|---|---|---|---|---|
| 565 | `cat-l-01` | Qdrant 1.7.3 Vector Database (768d Cosine) | `L` | `base` | `lazy_tool('cat-l-01')` | `home,agents,tasks,opensource,finance,legal,city` |
| 566 | `cat-l-02` | MinIO S3 Object Storage (Atomic Temp-Rename) | `L` | `base` | `lazy_tool('cat-l-02')` | `home,agents,tasks,opensource,finance,legal,city` |
| 567 | `cat-l-03` | HashiCorp Vault 1.15 HSM Transit | `L` | `base` | `lazy_tool('cat-l-03')` | `home,agents,tasks,opensource,finance,legal,city` |
| 568 | `cat-l-04` | PostgreSQL 16 Relational Task Registry | `L` | `base` | `lazy_tool('cat-l-04')` | `home,agents,tasks,opensource,finance,legal,city` |
| 569 | `cat-l-05` | SQLAlchemy 2.0 + Alembic Migrations | `L` | `base` | `lazy_tool('cat-l-05')` | `home,agents,tasks,opensource,finance,legal,city` |
| 570 | `cat-l-06` | Redis 7 Queue & PubSub | `L` | `base` | `lazy_tool('cat-l-06')` | `home,agents,tasks,opensource,finance,legal,city` |
| 571 | `cat-l-07` | Celery 5.3.6 + Celery Beat + Flower | `L` | `base` | `lazy_tool('cat-l-07')` | `home,agents,tasks,opensource,finance,legal,city` |
| 572 | `cat-l-08` | trycua/cua Computer-Use Agent SDK | `L` | `base` | `lazy_tool('cat-l-08')` | `home,agents,tasks,opensource,finance,legal,city` |
| 573 | `cat-l-09` | trycua/boat 2000-Space Isolated Cloud Computers | `L` | `base` | `lazy_tool('cat-l-09')` | `home,agents,tasks,opensource,finance,legal,city` |
| 574 | `cat-l-10` | Hermes-Agent Autonomous Skill Runtime | `L` | `base` | `lazy_tool('cat-l-10')` | `home,agents,tasks,opensource,finance,legal,city` |
| 575 | `cat-l-11` | Hermes-Library Multi-Agent Memory | `L` | `base` | `lazy_tool('cat-l-11')` | `home,agents,tasks,opensource,finance,legal,city` |
| 576 | `cat-l-12` | Hermes-Tool-Use Structured Function Engine | `L` | `base` | `lazy_tool('cat-l-12')` | `home,agents,tasks,opensource,finance,legal,city` |
| 577 | `cat-l-13` | Obliteratus Never-Fail Multi-Provider Cascade | `L` | `base` | `lazy_tool('cat-l-13')` | `home,agents,tasks,opensource,finance,legal,city` |
| 578 | `cat-l-14` | Composio 250+ Managed OAuth Tool Router | `L` | `base` | `lazy_tool('cat-l-14')` | `home,agents,tasks,opensource,finance,legal,city` |
| 579 | `cat-l-15` | PyGithub Repository & PR Automation | `L` | `base` | `lazy_tool('cat-l-15')` | `home,agents,tasks,opensource,finance,legal,city` |
| 580 | `cat-l-16` | GitHub Actions CI/CD Runner Bridge | `L` | `base` | `lazy_tool('cat-l-16')` | `home,agents,tasks,opensource,finance,legal,city` |
| 581 | `cat-l-17` | Vultr v2 Cloud GPU Provisioner API | `L` | `base` | `lazy_tool('cat-l-17')` | `home,agents,tasks,opensource,finance,legal,city` |
| 582 | `cat-l-18` | OSMnx Street Network Graph Modeler | `L` | `base` | `lazy_tool('cat-l-18')` | `home,agents,tasks,opensource,finance,legal,city` |
| 583 | `cat-l-19` | GeoPandas Spatial DataFrame Engine | `L` | `base` | `lazy_tool('cat-l-19')` | `home,agents,tasks,opensource,finance,legal,city` |
| 584 | `cat-l-20` | QGIS Headless PyQGIS Cartography | `L` | `base` | `lazy_tool('cat-l-20')` | `home,agents,tasks,opensource,finance,legal,city` |
| 585 | `cat-l-21` | CityGML 3D Urban Digital Twin Parser | `L` | `base` | `lazy_tool('cat-l-21')` | `home,agents,tasks,opensource,finance,legal,city` |
| 586 | `cat-l-22` | CourtListener 10M+ Legal Opinion Search | `L` | `base` | `lazy_tool('cat-l-22')` | `home,agents,tasks,opensource,finance,legal,city` |
| 587 | `cat-l-23` | Harvard Caselaw Access Project Connector | `L` | `base` | `lazy_tool('cat-l-23')` | `home,agents,tasks,opensource,finance,legal,city` |
| 588 | `cat-l-24` | Legal-BERT Clause Risk Scorer | `L` | `base` | `lazy_tool('cat-l-24')` | `home,agents,tasks,opensource,finance,legal,city` |
| 589 | `cat-l-25` | LexNLP Contract Obligation Extractor | `L` | `base` | `lazy_tool('cat-l-25')` | `home,agents,tasks,opensource,finance,legal,city` |
| 590 | `cat-l-26` | Eyecite Legal Citation Parser | `L` | `base` | `lazy_tool('cat-l-26')` | `home,agents,tasks,opensource,finance,legal,city` |
| 591 | `cat-l-27` | Blackstone UK/Common-Law spaCy Pipeline | `L` | `base` | `lazy_tool('cat-l-27')` | `home,agents,tasks,opensource,finance,legal,city` |
| 592 | `cat-l-28` | Kissi Gazette Blockchain Legal Notice Publisher | `L` | `base` | `lazy_tool('cat-l-28')` | `home,agents,tasks,opensource,finance,legal,city` |
| 593 | `cat-l-29` | OpenTimestamps Bitcoin Header Notarizer | `L` | `base` | `lazy_tool('cat-l-29')` | `home,agents,tasks,opensource,finance,legal,city` |
| 594 | `cat-l-30` | IPFS Kubo Content-Addressed Archive | `L` | `base` | `lazy_tool('cat-l-30')` | `home,agents,tasks,opensource,finance,legal,city` |
| 595 | `cat-l-31` | Aave V3 Flash-Loan Testnet Simulator | `L` | `base` | `lazy_tool('cat-l-31')` | `home,agents,tasks,opensource,finance,legal,city` |
| 596 | `cat-l-32` | Uniswap V3/V4 Concentrated Liquidity Math | `L` | `base` | `lazy_tool('cat-l-32')` | `home,agents,tasks,opensource,finance,legal,city` |
| 597 | `cat-l-33` | CCXT 100+ Exchange Market Data Connector | `L` | `base` | `lazy_tool('cat-l-33')` | `home,agents,tasks,opensource,finance,legal,city` |
| 598 | `cat-l-34` | OpenBB Quantitative Terminal SDK | `L` | `base` | `lazy_tool('cat-l-34')` | `home,agents,tasks,opensource,finance,legal,city` |
| 599 | `cat-l-35` | Hummingbot Market-Making Strategy Engine | `L` | `base` | `lazy_tool('cat-l-35')` | `home,agents,tasks,opensource,finance,legal,city` |
| 600 | `cat-l-36` | Foundry Forge/Cast EVM Verification | `L` | `base` | `lazy_tool('cat-l-36')` | `home,agents,tasks,opensource,finance,legal,city` |
| 601 | `cat-l-37` | Hardhat Smart-Contract Test Suite | `L` | `base` | `lazy_tool('cat-l-37')` | `home,agents,tasks,opensource,finance,legal,city` |
| 602 | `cat-l-38` | QuantLib Fixed-Income & Derivatives Pricing | `L` | `base` | `lazy_tool('cat-l-38')` | `home,agents,tasks,opensource,finance,legal,city` |
| 603 | `cat-l-39` | Ghostfolio Self-Hosted Wealth Tracker | `L` | `base` | `lazy_tool('cat-l-39')` | `home,agents,tasks,opensource,finance,legal,city` |
| 604 | `cat-l-40` | WBRG Sovereign Dual-License Instrument Registry | `L` | `base` | `lazy_tool('cat-l-40')` | `home,agents,tasks,opensource,finance,legal,city` |
| 605 | `cat-l-41` | Repliers + ATTOM Real-Estate Valuation Shim | `L` | `base` | `lazy_tool('cat-l-41')` | `home,agents,tasks,opensource,finance,legal,city` |
| 606 | `cat-l-42` | LibreMLS + RESO Web API Property Sync | `L` | `base` | `lazy_tool('cat-l-42')` | `home,agents,tasks,opensource,finance,legal,city` |
| 607 | `cat-l-43` | EspoCRM Self-Hosted Deal Pipeline | `L` | `base` | `lazy_tool('cat-l-43')` | `home,agents,tasks,opensource,finance,legal,city` |
| 608 | `cat-l-44` | Listmonk Bounce-Retry Legal-Timestamp Mailer | `L` | `base` | `lazy_tool('cat-l-44')` | `home,agents,tasks,opensource,finance,legal,city` |
| 609 | `cat-l-45` | Postal + Haraka Self-Hosted SMTP | `L` | `base` | `lazy_tool('cat-l-45')` | `home,agents,tasks,opensource,finance,legal,city` |
| 610 | `cat-l-46` | FreePBX + Asterisk SIP Trunk Controller | `L` | `base` | `lazy_tool('cat-l-46')` | `home,agents,tasks,opensource,finance,legal,city` |
| 611 | `cat-l-47` | SignalWire + Jambonz Programmable Voice | `L` | `base` | `lazy_tool('cat-l-47')` | `home,agents,tasks,opensource,finance,legal,city` |
| 612 | `cat-l-48` | OpenSIPS + Kamailio High-CPS SIP Router | `L` | `base` | `lazy_tool('cat-l-48')` | `home,agents,tasks,opensource,finance,legal,city` |
| 613 | `cat-l-49` | Jitsi + LiveKit Sovereign WebRTC Rooms | `L` | `base` | `lazy_tool('cat-l-49')` | `home,agents,tasks,opensource,finance,legal,city` |
| 614 | `cat-l-50` | n8n + Windmill Self-Hosted Workflow DAGs | `L` | `base` | `lazy_tool('cat-l-50')` | `home,agents,tasks,opensource,finance,legal,city` |
| 615 | `cat-l-51` | MemGPT / Letta Tiered Agent Memory | `L` | `base` | `lazy_tool('cat-l-51')` | `home,agents,tasks,opensource,finance,legal,city` |
| 616 | `cat-l-52` | CrewAI + AutoGen + LangGraph Swarm Adapters | `L` | `base` | `lazy_tool('cat-l-52')` | `home,agents,tasks,opensource,finance,legal,city` |
| 617 | `cat-l-53` | Prometheus + Alertmanager + Grafana + Loki | `L` | `base` | `lazy_tool('cat-l-53')` | `home,agents,tasks,opensource,finance,legal,city` |
| 618 | `cat-l-54` | Watchtower + Keel Container Self-Healer | `L` | `base` | `lazy_tool('cat-l-54')` | `home,agents,tasks,opensource,finance,legal,city` |
| 619 | `cat-l-55` | Convex Optional Webhook State Sync Adapter | `L` | `base` | `lazy_tool('cat-l-55')` | `home,agents,tasks,opensource,finance,legal,city` |
| 620 | `cat-l-56` | BIPA/GDPR VideoKYC Consent Ledger | `L` | `base` | `lazy_tool('cat-l-56')` | `home,agents,tasks,opensource,finance,legal,city` |

### Category M: Composio 300 Managed Action Connectors (60 Packs x `list`, `get`, `create`, `update`, `webhook`)

`GitHub`, `GitLab`, `Bitbucket`, `Gmail`, `Google Calendar`, `Google Drive`, `Google Sheets`, `Google Docs`, `Notion`, `Linear`, `Slack`, `Discord`, `Jira`, `Confluence`, `Asana`, `Trello`, `ClickUp`, `Monday.com`, `Airtable`, `HubSpot`, `Salesforce`, `Pipedrive`, `Zoho CRM`, `Zendesk`, `Freshdesk`, `Intercom`, `Stripe`, `QuickBooks`, `Xero`, `Brex`, `Shopify`, `WooCommerce`, `Figma`, `Webflow`, `WordPress`, `Ghost`, `Medium`, `Substack`, `LinkedIn Pages`, `X/Twitter API`, `YouTube Studio`, `Instagram Business`, `TikTok Business`, `Meta Ads`, `Google Ads`, `PostHog`, `Mixpanel`, `Amplitude`, `Sentry`, `Datadog`, `PagerDuty`, `Opsgenie`, `Cloudflare`, `AWS S3`, `Vultr Cloud`, `DigitalOcean`, `Supabase`, `Neon Postgres`, `Snowflake`, `BigQuery`

