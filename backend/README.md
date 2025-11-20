# Rot Studio Backend (FastAPI + Diffusers)

This backend is designed to run on **Google Colab (free tier)** or any local GPU. It exposes a single `/stylize` endpoint that the React frontend calls to convert user-uploaded photos into stylized artwork using Stable Diffusion XL + style-specific LoRA adapters.

## Stack

- Python 3.10+
- FastAPI + Uvicorn
- HuggingFace Diffusers + LoRA adapters
- Torch with CUDA (Colab T4 / L4 is sufficient)
- Cloudflared (or Gradio share) for zero-cost tunneling

## Quickstart (Local GPU)

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## Zero-Cost Colab Deployment

1. Upload the `backend/` folder to Colab (or clone the repo).
2. Open `../notebooks/colab_backend.ipynb` in Colab and run the cells:
   - Installs dependencies
   - Downloads LoRA checkpoints the first time
   - Starts the FastAPI server via Uvicorn
   - Boots a free Cloudflare tunnel and prints the public URL
3. Copy the tunnel URL into the frontend `.env` (`VITE_API_BASE_URL`) and restart `npm run dev`.

## Environment Variables

| Name | Description | Default |
| --- | --- | --- |
| `SDXL_MODEL_ID` | HuggingFace repo id for the base model | `stabilityai/stable-diffusion-xl-base-1.0` |
| `SDXL_VAE_ID` | Optional improved VAE checkpoint | `madebyollin/sdxl-vae-fp16-fix` |

## API

### `POST /stylize`

Multipart body:

- `image`: file (PNG/JPG, < 12 MB)
- `style`: one of `ghibli`, `naruto`, `dragonball`, `picasso`, `davinci`
- `strength`: float (0.2 – 0.95) default `0.65`
- `guidance_scale`: float (3 – 12) default `7`
- `seed`: optional int for deterministic results

Response:

```json
{
  "style": "ghibli",
  "image_base64": "<base64 string>",
  "metadata": { "strength": 0.65, "guidance_scale": 7, "seed": 1234 }
}
```

## Adding New Styles

Edit `style_config.py` to append a `StylePreset` entry. Use a LoRA repo id from HuggingFace (all free) or leave it `None` for prompt-only styles.

