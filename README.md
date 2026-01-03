# Rot Studio - AI Art Style Transfer

End-to-end project for a 7th-semester B.Tech CSE (AI) submission. Users upload a photo, pick an art preset (Ghibli, Naruto, Dragon Ball, Picasso, Da Vinci, etc.), and get a stylized image generated on a zero-cost stack (React + Vite frontend, FastAPI + SDXL backend on Hugging Face Spaces).

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

Hugging Face Spaces Deployment (Free GPU):

1. **Create a Hugging Face Account**: If you don't have one, sign up at [huggingface.co](https://huggingface.co/).
2. **Create a New Space**:
   - Go to your profile and click **New Space**.
   - Give it a name (e.g., `rot-studio-backend`).
   - Select **Docker** as the Space SDK.
   - Choose the **NVIDIA T4 Small** hardware for a free GPU.
   - Under **Space secrets**, add a secret named `HUGGING_FACE_HUB_TOKEN` with your Hugging Face Hub token as the value. This is needed for downloading models.
   - Click **Create Space**.
3. **Push the Backend to the Space**:
   - The repository will be created empty. Follow the instructions on the Space page to clone it, then copy the contents of the `backend/` directory (`app.py`, `requirements.txt`, etc.) into the root of your new Space repository and push.
   - Make sure the `backend/` directory contains `app.py`, `requirements.txt`, `style_config.py`, and the new `README.md` with the Hugging Face metadata.
4. **Get the Public URL**: Once the build is complete, the Space will have a public URL (e.g., `https://<your-username>-<space-name>.hf.space`). This is your new backend endpoint.
5. **Update the Frontend**:
   - In the `frontend/` directory, update the `.env.local` file with the new URL:
     ```
     VITE_API_BASE_URL=https://<your-username>-<space-name>.hf.space
     ```
   - Re-deploy your frontend.

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

## Project Report Checklist
- Source code (this repo)
- Architecture diagram + explanation (`docs/architecture.md`)
- Test evidence: include screenshots of each preset result, plus a health-check response.
- Deployment proof: Netlify/Vercel URL + your Hugging Face Space URL.
- Notebook: export executed Colab notebook (File > Download > .ipynb) for submission (if you still need it for your report).
