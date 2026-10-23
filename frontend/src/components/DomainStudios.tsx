import { useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { apiClient } from "../lib/apiClient";
import type { IsolationMode } from "../types/api";
import { CopyButton } from "./CopyButton";

export function EngineeringStudio() {
  const [binaryName, setBinaryName] = useState("flight_controller_fw.elf");
  const [threadSpec, setThreadSpec] = useState("M3x10mm ISO 4762");
  const [driveFreq, setDriveFreq] = useState(36.4);

  const ghidraMut = useMutation({
    mutationFn: () => apiClient.analyzeGhidra(binaryName, "7f454c4602010100"),
  });
  const screwMut = useMutation({
    mutationFn: () => apiClient.generateFreeCadScrew(threadSpec, "Al 7075-T6", 8),
  });
  const propMut = useMutation({
    mutationFn: () => apiClient.simulatePropulsion("mach_effect_piezo_resonator", driveFreq),
  });

  return (
    <section className="mb-5 rounded border-2 border-orange-600 bg-white p-4">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2 border-b border-neutral-200 pb-2">
        <div>
          <h3 className="text-sm font-extrabold uppercase tracking-wide text-orange-600">
            Engineering Studio: Headless GHIDRA SRE, FreeCAD M3/M4 Torque & Propulsion FEM
          </h3>
          <p className="text-xs text-neutral-700">
            Primary LLMs: Qwen3-Coder-Next-80B (Priority 4) + Gemini-4-Argon-400B (Priority 15)
          </p>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <div className="rounded border border-neutral-300 p-3">
          <div className="mb-2 font-mono text-[11px] font-bold text-fuchsia-600">1. GHIDRA 11.2 P-CODE SRE</div>
          <input
            type="text"
            value={binaryName}
            onChange={(e) => setBinaryName(e.target.value)}
            className="mb-2 w-full rounded border border-neutral-300 px-2.5 py-1.5 text-xs"
          />
          <button
            type="button"
            onClick={() => ghidraMut.mutate()}
            className="w-full rounded bg-neutral-900 px-3 py-1.5 text-xs font-bold text-white hover:bg-neutral-800"
          >
            {ghidraMut.isPending ? "Decompiling..." : "Run Headless GHIDRA"}
          </button>
          {ghidraMut.data && (
            <div className="mt-2 space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="font-mono text-[11px] text-teal-700">{ghidraMut.data.engine}</span>
                <CopyButton value={ghidraMut.data.decompiled_c_preview} />
              </div>
              <pre className="overflow-x-auto rounded border border-neutral-200 bg-neutral-50 p-2 text-black">
                {ghidraMut.data.decompiled_c_preview}
              </pre>
            </div>
          )}
        </div>

        <div className="rounded border border-neutral-300 p-3">
          <div className="mb-2 font-mono text-[11px] font-bold text-teal-600">2. FREECAD / OPENSCAD ISO 4762</div>
          <select
            value={threadSpec}
            onChange={(e) => setThreadSpec(e.target.value)}
            className="mb-2 w-full rounded border border-neutral-300 bg-white px-2.5 py-1.5 text-xs"
          >
            <option value="M3x10mm ISO 4762">M3x10mm ISO 4762 (1.2 N-m)</option>
            <option value="M4x12mm ISO 4762">M4x12mm ISO 4762 (2.9 N-m)</option>
          </select>
          <button
            type="button"
            onClick={() => screwMut.mutate()}
            className="w-full rounded bg-teal-600 px-3 py-1.5 text-xs font-bold text-white hover:bg-teal-700"
          >
            {screwMut.isPending ? "Generating CAD..." : "Generate Screw Boss & BOM"}
          </button>
          {screwMut.data && (
            <div className="mt-2 space-y-1.5">
              <div className="flex items-center justify-between font-mono text-[11px]">
                <span>Torque: {screwMut.data.recommended_torque_nm} N-m</span>
                <CopyButton value={screwMut.data.openscad_script} />
              </div>
              <pre className="overflow-x-auto rounded border border-neutral-200 bg-neutral-50 p-2 text-black">
                {screwMut.data.openscad_script}
              </pre>
            </div>
          )}
        </div>

        <div className="rounded border border-neutral-300 p-3">
          <div className="mb-2 font-mono text-[11px] font-bold text-orange-600">3. NASA BPP / MACH-EFFECT FEM</div>
          <input
            type="number"
            step="0.1"
            value={driveFreq}
            onChange={(e) => setDriveFreq(Number(e.target.value))}
            className="mb-2 w-full rounded border border-neutral-300 px-2.5 py-1.5 text-xs"
          />
          <button
            type="button"
            onClick={() => propMut.mutate()}
            className="w-full rounded bg-orange-600 px-3 py-1.5 text-xs font-bold text-white hover:bg-orange-700"
          >
            {propMut.isPending ? "Solving FEM..." : "Run OpenFOAM + Elmer FEM"}
          </button>
          {propMut.data && (
            <div className="mt-2 rounded border border-neutral-200 bg-neutral-50 p-2 font-mono text-[11px]">
              <div>Q-Factor: {propMut.data.resonator_q_factor}</div>
              <div>Net Force: {propMut.data.predicted_net_force_micro_newtons} uN</div>
              <div>KiCad HV Clearance: {propMut.data.kicad_hv_clearance_mm} mm</div>
              <div>Status: {propMut.data.status}</div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

export function ImageDirectorStudio() {
  const [prompt, setPrompt] = useState("Editorial studio portrait with natural skin pores and balanced rim lighting");
  const [mode, setMode] = useState<IsolationMode>("combined_directors_cut");
  const [stoneFilter, setStoneFilter] = useState<"all" | "diamonds_only" | "rubies_only" | "emeralds_only">("all");
  const [batchCount, setBatchCount] = useState(24);

  const imgMut = useMutation({
    mutationFn: () =>
      apiClient.runImageConsistency({
        prompt,
        isolation_mode: mode,
        stone_filter: stoneFilter,
        batch_count: batchCount,
      }),
  });

  return (
    <section className="mb-5 rounded border-2 border-fuchsia-600 bg-white p-4">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2 border-b border-neutral-200 pb-2">
        <div>
          <h3 className="text-sm font-extrabold uppercase tracking-wide text-fuchsia-600">
            7-Subagent Biometric Director&apos;s Cut & Zero-Bleed Isolation (Up to 1,000 Parallel GPU Pics)
          </h3>
          <p className="text-xs text-neutral-700">
            Model: gemma-4-it-qat-12b (Priority 8) + FLUX.1-dev + RealVisXL V5 + SAM2 + DINOv2 Pose-Only
          </p>
        </div>
      </div>

      <div className="grid gap-3 md:grid-cols-4">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="rounded border border-neutral-300 px-3 py-1.5 text-xs md:col-span-2"
        />
        <select
          value={mode}
          onChange={(e) => setMode(e.target.value as IsolationMode)}
          className="rounded border border-neutral-300 bg-white px-2.5 py-1.5 text-xs"
        >
          <option value="combined_directors_cut">Combined Director&apos;s Cut (7 Subagents)</option>
          <option value="face_only_biometric">Face Only (Biometric Lock)</option>
          <option value="hair_only">Hair Only (Zero Skin Bleed)</option>
          <option value="jewelry_only">Jewelry Only (Stone Isolation)</option>
          <option value="clothes_only">Clothes Only (Garment Transfer)</option>
          <option value="background_only">Background Only (Depth Relight)</option>
        </select>
        <div className="flex gap-2">
          <select
            value={stoneFilter}
            onChange={(e) =>
              setStoneFilter(e.target.value as "all" | "diamonds_only" | "rubies_only" | "emeralds_only")
            }
            className="w-1/2 rounded border border-neutral-300 bg-white px-2 py-1.5 text-xs"
          >
            <option value="all">All Stones</option>
            <option value="diamonds_only">Diamonds Only</option>
            <option value="rubies_only">Rubies Only</option>
            <option value="emeralds_only">Emeralds Only</option>
          </select>
          <input
            type="number"
            min={1}
            max={1000}
            value={batchCount}
            onChange={(e) => setBatchCount(Number(e.target.value))}
            className="w-1/2 rounded border border-neutral-300 px-2 py-1.5 text-xs"
          />
        </div>
      </div>

      <div className="mt-3 flex items-center gap-3">
        <button
          type="button"
          onClick={() => imgMut.mutate()}
          className="rounded bg-fuchsia-600 px-4 py-1.5 text-xs font-bold text-white hover:bg-fuchsia-700"
        >
          {imgMut.isPending ? "Rendering Batch..." : `Deliver Unified ${batchCount}-Image Batch`}
        </button>
        <button
          type="button"
          onClick={() => {
            setBatchCount(1000);
            window.setTimeout(() => imgMut.mutate(), 20);
          }}
          className="rounded border border-neutral-900 bg-white px-3 py-1.5 font-mono text-[11px] font-bold text-black hover:bg-neutral-100"
        >
          200x5 = 1,000-Pic GPU Stress Batch
        </button>
      </div>

      {imgMut.data && (
        <div className="mt-3 rounded border border-neutral-200 bg-neutral-50 p-3 font-mono text-[11px]">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <span>
              Sandbox: <strong>{imgMut.data.sandbox_id}</strong> | Cosine Face Lock:{" "}
              <strong>{imgMut.data.face_cosine_similarity}</strong> | Workers:{" "}
              <strong>{imgMut.data.gpu_workers_allocated}</strong>
            </span>
            <CopyButton value={imgMut.data.unified_zip_uri} label="COPY ZIP URI" />
          </div>
          <div className="mt-1 text-teal-800">{imgMut.data.unified_zip_uri}</div>
        </div>
      )}
    </section>
  );
}

export function VideoStitchStudio() {
  const [prompt, setPrompt] = useState("Multi-character investigative thriller with locked biometric continuity");
  const [durationSec, setDurationSec] = useState(7200);
  const [modelId, setModelId] = useState("minimax-hailuo-02");

  const vidMut = useMutation({
    mutationFn: () =>
      apiClient.runVideoStitch({
        prompt,
        target_duration_seconds: durationSec,
        clip_duration_seconds: 30,
        parallel_workers: 60,
        primary_video_model: modelId,
      }),
  });

  return (
    <section className="mb-5 rounded border-2 border-teal-600 bg-white p-4">
      <h3 className="text-sm font-extrabold uppercase tracking-wide text-teal-600">
        600-Clip Parallel Video / UGC / Cinema Stitcher (FFmpeg 6.1 + MoviePy + WhisperX)
      </h3>
      <div className="mt-3 grid gap-3 md:grid-cols-4">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="rounded border border-neutral-300 px-3 py-1.5 text-xs md:col-span-2"
        />
        <select
          value={modelId}
          onChange={(e) => setModelId(e.target.value)}
          className="rounded border border-neutral-300 bg-white px-2.5 py-1.5 text-xs"
        >
          <option value="minimax-hailuo-02">MiniMax Hailuo-02 (#1 UGC Physics)</option>
          <option value="wan-2.1-14b">Wan 2.1 14B (Photoreal Skin)</option>
          <option value="ltx-video-13b">LTX-Video 13B (10x Parallel Speed)</option>
          <option value="kling-2.0-director">Kling 2.0 Director</option>
        </select>
        <select
          value={durationSec}
          onChange={(e) => setDurationSec(Number(e.target.value))}
          className="rounded border border-neutral-300 bg-white px-2.5 py-1.5 text-xs"
        >
          <option value={300}>5 Minutes (10 x 30s clips)</option>
          <option value={7200}>2 Hours (240 x 30s clips)</option>
          <option value={18000}>5 Hours (600 x 30s clips)</option>
        </select>
      </div>
      <div className="mt-3">
        <button
          type="button"
          onClick={() => vidMut.mutate()}
          className="rounded bg-teal-600 px-4 py-1.5 text-xs font-bold text-white hover:bg-teal-700"
        >
          {vidMut.isPending ? "Stitching Clips..." : "Render & Stitch Into Single MP4"}
        </button>
      </div>
      {vidMut.data && (
        <div className="mt-3 flex flex-wrap items-center justify-between gap-2 rounded border border-neutral-200 bg-neutral-50 p-3 font-mono text-[11px]">
          <span>
            Clips Stitched: {vidMut.data.total_clips_planned} | Speedup: {vidMut.data.parallel_speedup_factor}x | MP4:{" "}
            {vidMut.data.final_single_mp4_uri}
          </span>
          <CopyButton value={vidMut.data.final_single_mp4_uri} label="COPY MP4 URI" />
        </div>
      )}
    </section>
  );
}

export function VocalTuningStudio() {
  const [title, setTitle] = useState("Sovereign AnthemSession");
  const [keyScale, setKeyScale] = useState("C Minor");
  const [stems, setStems] = useState<2 | 4 | 5>(4);

  const vocalMut = useMutation({
    mutationFn: () =>
      apiClient.runVocalTuning({
        track_title: title,
        key_scale: keyScale,
        retune_speed_ms: 8,
        stems,
        include_808_kit: true,
      }),
  });

  return (
    <section className="mb-5 rounded border-2 border-fuchsia-600 bg-white p-4">
      <h3 className="text-sm font-extrabold uppercase tracking-wide text-fuchsia-600">
        Vocal Tuning & 94-Sample Free 808 Studio (Demucs v4 + Spleeter + GSnap + MAutoPitch + Graillon 2 + RVC)
      </h3>
      <div className="mt-3 grid gap-3 md:grid-cols-4">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="rounded border border-neutral-300 px-3 py-1.5 text-xs"
        />
        <input
          type="text"
          value={keyScale}
          onChange={(e) => setKeyScale(e.target.value)}
          className="rounded border border-neutral-300 px-3 py-1.5 text-xs"
        />
        <select
          value={stems}
          onChange={(e) => setStems(Number(e.target.value) as 2 | 4 | 5)}
          className="rounded border border-neutral-300 bg-white px-2.5 py-1.5 text-xs"
        >
          <option value={2}>2 Stems (Vocals + Instrumental)</option>
          <option value={4}>4 Stems (Vocals, Drums/808, Bass, Other)</option>
          <option value={5}>5 Stems (Vocals, Drums/808, Bass, Piano, Other)</option>
        </select>
        <button
          type="button"
          onClick={() => vocalMut.mutate()}
          className="rounded bg-fuchsia-600 px-4 py-1.5 text-xs font-bold text-white hover:bg-fuchsia-700"
        >
          {vocalMut.isPending ? "Mastering..." : "Isolate, Tune & Master WAV"}
        </button>
      </div>
      {vocalMut.data && (
        <div className="mt-3 flex flex-wrap items-center justify-between gap-2 rounded border border-neutral-200 bg-neutral-50 p-3 font-mono text-[11px]">
          <span>
            Master WAV: {vocalMut.data.mastered_wav_uri} | 808 Samples Loaded:{" "}
            {vocalMut.data.eight_oh_eight_samples_available}
          </span>
          <CopyButton value={vocalMut.data.mastered_wav_uri} label="COPY WAV URI" />
        </div>
      )}
    </section>
  );
}

export function SecurityKycStudio() {
  const [consentChecked, setConsentChecked] = useState(false);
  const [holder, setHolder] = useState("Sovereign Operator");

  const attemptsQuery = useQuery({
    queryKey: ["security-attempts"],
    queryFn: apiClient.getSecurityAttempts,
  });

  const kycMut = useMutation({
    mutationFn: () => apiClient.optInBiometric(consentChecked, holder),
  });

  const passportMut = useMutation({
    mutationFn: () => apiClient.issuePassport(holder, "global-tabs-1-28"),
  });

  return (
    <section className="mb-5 rounded border-2 border-orange-600 bg-white p-4">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2 border-b border-neutral-200 pb-2">
        <div>
          <h3 className="text-sm font-extrabold uppercase tracking-wide text-orange-600">
            8-Layer Zero-Trust Perimeter, Cowrie Honeypot Audit & BIPA/GDPR Opt-In VideoKYC
          </h3>
          <p className="text-xs text-neutral-700">
            CrowdSec WAF, Wazuh SIEM, Suricata IDS, Falco + Tetragon eBPF, Vault HSM (10 req/s), WireGuard, Cowrie
          </p>
        </div>
        <a
          href="/api/security/audit/export"
          target="_blank"
          rel="noreferrer"
          className="rounded border border-amber-600 bg-amber-400 px-3 py-1.5 font-mono text-[11px] font-bold text-black hover:bg-amber-500"
        >
          EXPORT POLICE AUDIT PDF
        </a>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded border border-neutral-300 p-3">
          <div className="mb-2 font-mono text-[11px] font-bold text-teal-700">
            EXPLICIT OPT-IN BIOMETRIC VIDEOKYC & OMNIVIDENS PASSPORT
          </div>
          <input
            type="text"
            value={holder}
            onChange={(e) => setHolder(e.target.value)}
            className="mb-2 w-full rounded border border-neutral-300 px-2.5 py-1.5 text-xs"
          />
          <label className="mb-2 flex items-start gap-2 text-xs text-neutral-800">
            <input
              type="checkbox"
              checked={consentChecked}
              onChange={(e) => setConsentChecked(e.target.checked)}
              className="mt-0.5"
            />
            <span>
              I explicitly consent under BIPA and GDPR to encrypted Vault HSM VideoKYC enrollment (auto-purged in 30
              days).
            </span>
          </label>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => kycMut.mutate()}
              className="rounded bg-teal-600 px-3 py-1.5 text-xs font-bold text-white hover:bg-teal-700"
            >
              Verify VideoKYC
            </button>
            <button
              type="button"
              onClick={() => passportMut.mutate()}
              className="rounded bg-fuchsia-600 px-3 py-1.5 text-xs font-bold text-white hover:bg-fuchsia-700"
            >
              Issue OMNIVIDENS QR Seal
            </button>
          </div>
          {kycMut.data && (
            <div className="mt-2 rounded border border-neutral-200 bg-neutral-50 p-2 font-mono text-[11px]">
              Verified: {String(kycMut.data.verified)} | Vault Key: {kycMut.data.vault_hsm_key_id} |{" "}
              {kycMut.data.legal_notice}
            </div>
          )}
          {passportMut.data && (
            <div className="mt-2 flex items-center justify-between rounded border border-neutral-200 bg-neutral-50 p-2 font-mono text-[11px]">
              <span>
                {passportMut.data.passport_id} | {passportMut.data.qr_payload}
              </span>
              <CopyButton value={passportMut.data.qr_payload} />
            </div>
          )}
        </div>

        <div className="rounded border border-neutral-300 p-3">
          <div className="mb-2 font-mono text-[11px] font-bold text-orange-700">
            COWRIE HONEYPOT & WAF TELEMETRY ({attemptsQuery.data?.attempts.length ?? 0} EVENTS)
          </div>
          <div className="max-h-40 space-y-1.5 overflow-y-auto font-mono text-[11px]">
            {(attemptsQuery.data?.attempts ?? []).length === 0 ? (
              <div className="text-neutral-600">No external decoy probes logged yet.</div>
            ) : (
              attemptsQuery.data?.attempts.map((a) => (
                <div key={a.attempt_id} className="rounded border border-neutral-200 bg-neutral-50 p-2">
                  <div>
                    <strong>{a.path}</strong> | IP: {a.ip} | {a.asn} | {a.vultr_location}
                  </div>
                  <div className="text-neutral-600">
                    Cowrie TTY: {a.honeypot_recording_id} | JA3: {a.ja3}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
