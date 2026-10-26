# Vultr deployment

Obi AI runs as a regular Node.js production service and does not require Vercel.

## Requirements

- Ubuntu 22.04 or 24.04 VPS
- Docker Engine and Docker Compose plugin
- A DNS record pointing the app hostname to the Vultr server
- Provider secrets in `/opt/obi-ai/.env` (never commit this file)

## Deploy

```bash
sudo mkdir -p /opt/obi-ai
sudo chown "$USER":"$USER" /opt/obi-ai
git clone https://github.com/kissik-dom/obi-ai.git /opt/obi-ai
cd /opt/obi-ai
cp .env.example .env
nano .env

docker compose -f docker-compose.vultr.yml up -d --build
docker compose -f docker-compose.vultr.yml ps
curl http://127.0.0.1:3000/api/health
```

The service listens on port `3000`. Put Caddy or Nginx in front of it for HTTPS, and allow only SSH plus ports 80/443 in the Vultr firewall. Do not expose provider keys to the browser.

## Updating

```bash
cd /opt/obi-ai
git pull --ff-only origin main
docker compose -f docker-compose.vultr.yml up -d --build
```

The container has a health check at `/api/health` and restarts automatically after host or process failures.

## Automatic GitHub deployment

The repository includes `.github/workflows/deploy-vultr.yml`. The existing deployment setup uses these GitHub Actions credentials:

- `SERVER_HOST` — public IP or DNS name of the VPS; it may be a repository variable or secret
- `SSH_USERNAME` — SSH user, typically `root` or a deployment user
- `SSH_PRIVATE_KEY` — private OpenSSH key for that user, not a `.pub` or PuTTY `.ppk` file

The first manual deployment must create the server `.env` file in `/opt/obi-ai` or `$HOME/obi-ai`. After that, every push to `main` packages the commit, uploads it over SSH, rebuilds the container, and checks `/api/health`.
