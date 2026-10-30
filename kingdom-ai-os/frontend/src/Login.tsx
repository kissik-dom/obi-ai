import { FormEvent, ReactNode, useEffect, useState } from 'react';
import { KeyRound, LockKeyhole, ShieldCheck, Smartphone } from 'lucide-react';

type Status = { enabled: boolean; configured: boolean; authenticated: boolean; two_factor: boolean };

async function post(path: string, body: unknown) {
  const r = await fetch('/api/v1/auth' + path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', body: JSON.stringify(body) });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.detail ? (typeof data.detail === 'string' ? data.detail : 'Please check what you typed.') : `Error ${r.status}`);
  return data;
}

export async function signOut() {
  await fetch('/api/v1/auth/logout', { method: 'POST', credentials: 'same-origin' }).catch(() => {});
  window.location.reload();
}

export function Gate({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<Status | null>(null);
  const [step, setStep] = useState<'password' | 'code' | 'setup'>('password');
  const [password, setPassword] = useState('');
  const [code, setCode] = useState('');
  const [setupToken, setSetupToken] = useState('');
  const [setup, setSetup] = useState<{ secret: string; qr_svg: string } | null>(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const load = () => fetch('/api/v1/auth/status', { credentials: 'same-origin' }).then(r => r.json()).then(setStatus).catch(() => setStatus({ enabled: false, configured: false, authenticated: true, two_factor: false }));
  useEffect(() => {
    load();
    // Any 401 from the API (session expired) sends you back to the sign-in screen.
    const orig = window.fetch;
    window.fetch = async (...args) => {
      const res = await orig(...args);
      const url = typeof args[0] === 'string' ? args[0] : (args[0] as Request).url;
      if (res.status === 401 && url.includes('/api/') && !url.includes('/api/v1/auth/')) setStatus(s => s ? { ...s, authenticated: false } : s);
      return res;
    };
    return () => { window.fetch = orig; };
  }, []);

  async function submit(e: FormEvent) {
    e.preventDefault(); setError(''); setBusy(true);
    try {
      if (step === 'setup') {
        await post('/totp/confirm', { setup_token: setupToken, code });
        setPassword(''); setCode(''); await load(); return;
      }
      const r = await post('/login', { password, code: step === 'code' ? code : '' });
      if (r.ok) { setPassword(''); setCode(''); await load(); return; }
      if (r.code_required) { setStep('code'); return; }
      if (r.setup_required) {
        setSetupToken(r.setup_token);
        setSetup(await post('/totp/start', { setup_token: r.setup_token }));
        setStep('setup'); return;
      }
    } catch (err) { setError(err instanceof Error ? err.message : 'Something went wrong.'); setCode(''); }
    finally { setBusy(false); }
  }

  if (!status) return <div className="login-shell"><div className="login-card"><p className="login-sub">Loading…</p></div></div>;
  if (!status.enabled || status.authenticated) return <>{children}</>;
  if (!status.configured) return <div className="login-shell"><div className="login-card"><LockKeyhole size={28} /><h1>Locked</h1><p className="login-sub">Sign-in hasn't been set up on this server yet, so the workspace is locked for safety.</p></div></div>;

  return (
    <div className="login-shell">
      <form className="login-card" onSubmit={submit}>
        <div className="login-badge">{step === 'setup' ? <Smartphone size={22} /> : step === 'code' ? <ShieldCheck size={22} /> : <KeyRound size={22} />}</div>
        <h1>Kingdom AI OS</h1>
        {step === 'password' && <>
          <p className="login-sub">Sign in to your workspace.</p>
          <label className="login-label" htmlFor="pw">Password</label>
          <input id="pw" className="login-input" type="password" autoComplete="current-password" autoFocus value={password} onChange={e => setPassword(e.target.value)} />
        </>}
        {step === 'code' && <>
          <p className="login-sub">Open your authenticator app and type the 6-digit code for <b>Kingdom AI OS</b>.</p>
          <input className="login-input code" inputMode="numeric" autoComplete="one-time-code" autoFocus maxLength={7} placeholder="123 456" value={code} onChange={e => setCode(e.target.value)} />
        </>}
        {step === 'setup' && setup && <>
          <p className="login-sub"><b>One-time setup:</b> scan this with Google Authenticator, Microsoft Authenticator or Authy. From now on you'll need the password <i>and</i> the code from your phone.</p>
          {setup.qr_svg && <img className="login-qr" src={setup.qr_svg} alt="QR code for your authenticator app" />}
          <details className="login-manual"><summary>Can't scan? Type this key instead</summary><code>{setup.secret.match(/.{1,4}/g)?.join(' ')}</code></details>
          <label className="login-label" htmlFor="c">Then type the 6-digit code it shows</label>
          <input id="c" className="login-input code" inputMode="numeric" autoComplete="one-time-code" maxLength={7} placeholder="123 456" value={code} onChange={e => setCode(e.target.value)} />
        </>}
        {error && <p className="login-error" role="alert">{error}</p>}
        <button className="login-btn" disabled={busy || (step === 'password' ? !password : code.replace(/\D/g, '').length !== 6)}>{busy ? 'Checking…' : step === 'password' ? 'Continue' : step === 'setup' ? 'Turn on & sign in' : 'Sign in'}</button>
        {step !== 'password' && <button type="button" className="login-link" onClick={() => { setStep('password'); setCode(''); setError(''); }}>Back</button>}
        <p className="login-foot"><LockKeyhole size={12} /> 5 wrong tries locks sign-in for 15 minutes.</p>
      </form>
    </div>
  );
}
