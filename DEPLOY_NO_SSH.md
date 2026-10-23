# Deploy & Add Secrets With ZERO SSH (100% From Phone / Browser)

You do **not** need SSH, a terminal, or a Vultr API key. Everything works 100% from a web browser (including Safari on iPhone/iPad).

---

## 1. Where You Insert Secrets Now (Right Inside the App's Web UI!)

Whether you are using the **live Arena Preview right now** or after clicking deploy on Render / Railway / Vultr:

1. Open the Kingdom AI OS web app.
2. Click **`10. Settings`** on any tab.
3. At the top, in **"Browser Secret Vault (Zero SSH / Zero Terminal Needed)"**, paste:
   - `OPENROUTER_API_KEY_1` (`sk-or-v1-...` from [openrouter.ai/keys](https://openrouter.ai/keys))
   - *(Optional)* `OPENROUTER_API_KEY_2`, `OBLITERATUS_API_KEY`, or `COMPOSIO_API_KEY`
4. Click **`SEAL KEYS IN VAULT HSM`**.
   - Your key is immediately encrypted inside the server's **Vault HSM** seal and never displayed in plaintext again!

*(Do not paste API keys into Arena chat; paste them directly into that `10. Settings` Vault box or your hosting dashboard's Environment Variables screen.)*

---

## 2. Three 1-Click Browser Deploy Options (Zero SSH, Zero Terminal)

### Option 1: Railway.app (Fastest 2-Minute Phone/Browser Deploy from GitHub)
This repository now has a unified root `Dockerfile` and `railway.json` that deploys **both the White-Theme UI and FastAPI Backend together on one `https://...up.railway.app` URL**:
1. Open **[railway.app](https://railway.app)** in your browser and tap **Login with GitHub**.
2. Tap **New Project -> Deploy from GitHub repo** and pick **`kissik-dom/obi-ai`** (select branch `arena/41e9ebf0-obi-ai`, or merge the PR into `main` on GitHub first).
3. Tap the deployed service -> **Settings -> Networking -> Generate Domain**.
4. Tap **Variables** (or use `10. Settings` inside the app) to paste `OPENROUTER_API_KEY_1`. Done!

---

### Option 2: Render.com Blueprint (Auto-Generates Internal Secrets in Browser)
This repository includes `render.yaml`:
1. Open **[dashboard.render.com](https://dashboard.render.com)** in your browser and sign in with GitHub.
2. Tap **New + -> Blueprint** (or **Web Service**) and select **`kissik-dom/obi-ai`** (branch `arena/41e9ebf0-obi-ai` or `main`).
3. Render automatically generates `KINGDOM_INTERNAL_SECRET`, `LITELLM_MASTER_KEY`, and `VAULT_TOKEN` for you, and shows a web text box where you paste `OPENROUTER_API_KEY_1`.
4. Tap **Apply / Deploy** -> Render gives you a live `https://kingdom-ai-os.onrender.com` URL!

---

### Option 3: Vultr Web Dashboard Using Cloud-Init (Zero SSH!)
Even on **Vultr** (`my.vultr.com`), you never have to touch SSH:
1. Open **[my.vultr.com](https://my.vultr.com)** -> **Deploy + -> Deploy New Server** -> **Ubuntu 24.04 x64** (Cloud GPU or Cloud Compute).
2. Scroll down to **Additional Features -> Enable Cloud-Init User-Data** in the web page.
3. Copy and paste the contents of `vultr_cloud_init.yaml` into that browser box and tap **Deploy Now**.
4. Wait ~3-4 minutes while Vultr automatically installs Docker, clones `kissik-dom/obi-ai`, generates all internal passwords, and starts Kingdom AI OS.
5. Open `http://YOUR_VULTR_SERVER_IP:5173` in your browser -> tap **`10. Settings`** -> paste `OPENROUTER_API_KEY_1` into the **Browser Secret Vault** -> tap **`SEAL KEYS IN VAULT HSM`**. Zero SSH ever!
