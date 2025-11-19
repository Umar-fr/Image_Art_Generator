# Rot Studio - AI Art Style Transfer

End-to-end project for a 7th-semester B.Tech CSE (AI) submission. Users upload a photo, pick an art preset (Ghibli, Naruto, Dragon Ball, Picasso, Da Vinci, etc.), and get a stylized image generated on a zero-cost stack (React + Vite frontend, FastAPI + SDXL backend on Google Colab + Cloudflare Tunnel).

## Repository Layout

```
├── README.md
├── frontend/              # React + Vite app (upload UI, preset selector, downloader)
├── backend/               # FastAPI + Diffusers pipeline
├── notebooks/colab_backend.ipynb  # Reproducible Colab workflow
└── docs/architecture.md   # System design & infra plan
```

## Workflow Overview
1. **Frontend** (React) collects an image + preset, sends it to the backend, and displays the PNG output.
2. **Backend** (FastAPI) runs SDXL img2img with preset-specific prompts & LoRA adapters, returning a base64 string.
3. **Infrastructure** uses free services:
   - Google Colab GPU runtime for inference
   - Cloudflare tunnel to expose the FastAPI port
   - Netlify/Vercel/Cloudflare Pages for static frontend hosting
4. **Download** happens directly in the browser - no paid storage required.

See `docs/architecture.md` for deeper diagrams, data flow, and the one-day execution checklist.

## Frontend (React + Vite)

```bash
cd frontend
npm install
cp env.example .env.local   # or create manually
# set VITE_API_BASE_URL to the public tunnel URL (default http://127.0.0.1:8000)
npm run dev
# npm run build && npm run preview for a production bundle
```

Key files:

- `src/App.jsx`: main UI skeleton with upload, sliders, preset cards, and download button.
- `src/components/*`: presentational building blocks.
- `src/services/api.js`: `POST /stylize` helper with `FormData`.
- `src/data/stylePresets.js`: UI-friendly description of each style (must stay in sync with backend ids).

## Backend (FastAPI + Diffusers)

Local GPU quickstart:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Zero-cost Colab deployment:

1. Open `notebooks/colab_backend.ipynb` in Google Colab.
2. Upload (or git clone) this repo into `/content`.
3. Switch runtime to GPU, run cells top-to-bottom:
   - install dependencies
   - (optional) login to HuggingFace for gated LoRA checkpoints
   - start Uvicorn server
   - run Cloudflare tunnel and copy the public URL
4. Paste the printed URL into `frontend/.env` (`VITE_API_BASE_URL`), restart `npm run dev`, and test.

### API Contract

`POST /stylize`

| Field | Type | Notes |
| --- | --- | --- |
| `image` | file | PNG/JPG <= 12 MB |
| `style` | string | `ghibli`, `naruto`, `dragonball`, `picasso`, `davinci` |
| `strength` | float | 0.2 - 0.95, default 0.65 |
| `guidance_scale` | float | 3 - 12, default 7 |
| `seed` | int? | optional reproducibility |

Response:

```json
{
  "style": "ghibli",
  "image_base64": "data",
  "metadata": { "strength": 0.65, "guidance_scale": 7, "seed": 42 }
}
```

## Deployment (All Free)

| Layer | Service | Steps |
| --- | --- | --- |
| Frontend | Netlify/Vercel/Cloudflare Pages | Connect repo -> set build command `npm run build` -> output `dist`. |
| Backend | Google Colab + Cloudflare Tunnel | Run the notebook -> keep browser tab open during demos. |
| Domain | Optional custom domain | Point CNAME to Netlify/Vercel (still free). |

Tips:
- Run Colab notebook shortly before demo to avoid idle timeouts.
- Keep tunnel URL secret; disable the tunnel after showcasing.
- Capture demo screenshots for the project report.

## Project Report Checklist
- Source code (this repo)
- Architecture diagram + explanation (`docs/architecture.md`)
- Test evidence: include screenshots of each preset result, plus a health-check response.
- Deployment proof: Netlify/Vercel URL + Cloudflare tunnel log.
- Notebook: export executed Colab notebook (File > Download > .ipynb) for submission.

## How to run:
- `Local Machine`: git add . -> git commit -m "FIX" -> git push
- `Open google colab`: first paste this in the top cells: `!rm -rf /content/art-style-transfer` `!git clone https://github.com/Umar-fr/Image_Art_Generator /content/art-style-transfer` change thr runtime type to T4 GPU, and run all cells and copy the tunnel url and paste it to the local machine .env and push the code again.
- `Vercel`: Open vercel and paste the Tunnel url in environment variables and deploy the frontend.
