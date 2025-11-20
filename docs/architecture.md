# Rot Studio – Architecture & Workflow

## Goal
Turn a user-provided portrait into stylized artwork (Ghibli, Naruto, Dragon Ball, Picasso, Da Vinci, etc.) using open-source diffusion checkpoints, entirely on zero-cost infrastructure (Colab GPU + free hosting).

## System Overview

```
User Browser ──▶ React/Vite App (static hosting) ──▶ FastAPI (Colab GPU)
      ▲                                                   │
      └────── Stylized PNG ◀────────────── Diffusers + LoRA pipeline
```

- **Frontend**: React + Vite single-page app. Handles uploads, preset selection, parameter sliders, progress states, downloads.
- **Backend**: FastAPI running inside Google Colab. Loads SDXL img2img pipeline + optional LoRA adapters per style. Exposes `/stylize`.
- **Tunneling**: Cloudflare tunnel exposes the Colab port to the internet for free. URL configured in the frontend `.env`.
- **Assets**: Everything stored client-side (base64). No persistent storage fees.

## Data Flow
1. User selects an image + preset in the React app.
2. The app sends a multipart `POST /stylize` request with the image + parameters.
3. FastAPI loads the preset, applies LoRA weights if configured, and runs SDXL img2img on GPU.
4. FastAPI returns a base64 PNG payload.
5. React displays the image and lets the user download (no backend storage needed).

## Frontend Anatomy
- `src/components/UploadZone`: drag-and-drop like uploader with live preview.
- `src/components/StyleSelector`: responsive cards for each preset.
- `src/components/ResultPane`: shows progress, errors, final image + download button.
- `src/services/api.js`: small fetch wrapper using `VITE_API_BASE_URL`.
- `src/data/stylePresets.js`: source of truth for UI presets (mirrors backend keys).

## Backend Anatomy
- `app.py`: FastAPI app with `/health` + `/stylize`.
  - Loads SDXL base + VAE.
  - Applies preset-specific LoRA adapters dynamically.
  - Streams PNG output back as base64.
- `style_config.py`: maps preset ids to prompts, negative prompts, LoRA repos, weights.
- `requirements.txt`: pinned versions for deterministic Colab installs.
- `notebooks/colab_backend.ipynb`: reproducible Colab workflow (install deps, start server, open tunnel).

## Zero-Cost Infrastructure Plan
| Component | Service | Notes |
| --- | --- | --- |
| Frontend hosting | Vercel / Netlify / Cloudflare Pages (free tier) | Static deploy via `npm run build`. |
| Backend compute | Google Colab Free GPU | Run the provided notebook; keep tab alive while demoing. |
| Public backend URL | Cloudflare Tunnel (free) | `cloudflared tunnel --url http://127.0.0.1:8000`. |
| Assets/storage | Browser memory | Download handled client-side, no cloud storage. |

## One-Day Execution Checklist
1. **AM** – Clone repo, run `npm install`, start Vite dev server.
2. **AM** – Open Colab notebook, install backend deps, verify `/health`.
3. **Midday** – Connect Cloudflare tunnel, paste URL into `frontend/.env`.
4. **Afternoon** – Polish UI, test each preset, capture screenshots.
5. **Evening** – Deploy frontend (Vercel/Netlify) + prepare presentation/report.

## Extending Accuracy
- Plug in additional LoRA adapters by editing `style_config.py`.
- Use ControlNet for pose preservation (add ControlNet weights via Diffusers).
- Cache prompts & parameters per user for reproducibility (localStorage).
- Experiment with `InstantID` or `IP-Adapter` to preserve identity more faithfully.

