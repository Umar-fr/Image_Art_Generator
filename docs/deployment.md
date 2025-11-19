# Deployment Runbook (Zero Cost)

## Frontend (React + Vite)
1. `cd frontend`
2. `npm install`
3. `npm run build`
4. Deploy `dist/` to any static host:
   - **Netlify**: drag & drop folder or connect repo (build cmd `npm run build`, dir `dist`)
   - **Vercel**: import repo → Framework `Vite` → set `VITE_API_BASE_URL` env var
   - **Cloudflare Pages**: create project → set build cmd/output accordingly

## Backend (Google Colab + Cloudflare Tunnel)
1. Open `notebooks/colab_backend.ipynb` in Colab.
2. Upload repo to `/content`.
3. Switch runtime to GPU (T4).
4. Run cells:
   - verify path + GPU
   - install deps (`pip install -r backend/requirements.txt cloudflared`)
   - optional `huggingface_hub.login` for gated LoRAs
   - start `uvicorn app:app --host 0.0.0.0 --port 8000`
   - keep final `cloudflared tunnel --url http://127.0.0.1:8000` cell **running** and copy the public URL
5. Paste the `https://....trycloudflare.com` URL into the frontend `.env` → redeploy.

## Daily Usage Tips
- Colab sessions sleep after ~90 minutes of inactivity; keep the tab active during demos.
- Restart the server cell if you change `style_config.py`.
- Regenerate the Cloudflare tunnel URL whenever you restart to invalidate old links.

## Optional Enhancements
- Use [Gradio `launch(share=True)`](https://www.gradio.app/guides/share-your-app) in place of Cloudflare for simpler sharing.
- Mirror the backend on [fly.io free tier](https://fly.io) for 24/7 availability (requires minimal credit card verification but no spend).
- Cache generated images on the frontend with `IndexedDB` for offline viewing.

