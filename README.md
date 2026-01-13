# Rot Studio - AI Art Style Transfer

This project allows users to upload a photo, pick an art style, and generate a stylized image using a CPU-optimized AI model. The application is built with a React + Vite frontend and a FastAPI backend, designed for a zero-cost deployment on Render.

## Repository Layout

```
├── README.md
├── frontend/              # React + Vite app
├── backend/               # FastAPI + Diffusers pipeline
└── render.yaml            # Deployment configuration for Render
```

## Deployment (All Free)

This project is optimized for a seamless, zero-cost deployment on Render and any static hosting provider like Netlify or Vercel.

### Backend (FastAPI on Render)

1.  **Create a Render Account**: Sign up at [render.com](https://render.com/).
2.  **Create a New Web Service**:
    *   Click the **New +** button and select **Web Service**.
    *   Connect your GitHub repository.
    *   Render will automatically detect the `render.yaml` file and configure the service.
    *   Choose a name for your service (e.g., `rot-pg-backend`).
    *   Select the **Free** plan.
    *   Click **Create Web Service**.
3.  **Get the Public URL**: After the initial build (which may take some time as it downloads the model), your service will be live at a public URL (e.g., `https://your-service-name.onrender.com`).

### Frontend (React on Netlify/Vercel)

1.  **Connect Your Repository**: Choose a static hosting provider and connect your repository.
2.  **Configure the Frontend**:
    *   Set the build command to `npm run build` and the output directory to `dist`.
    *   Add an environment variable named `VITE_API_BASE_URL` and set it to the public URL of your Render backend.
3.  **Deploy**: Deploy the frontend. Your application will now be live.

## API Contract

`POST /stylize`

| Field          | Type   | Notes                               |
| -------------- | ------ | ----------------------------------- |
| `image`        | file   | PNG/JPG <= 12 MB                    |
| `style`        | string | `cinematic`, `digital-art`          |
| `strength`     | float  | 0.0 - 1.0, default 0.5              |
| `guidance_scale` | float  | 0.0 - 1.0, default 0.0              |
| `seed`         | int?   | optional for reproducibility        |

Response:

```json
{
  "style": "cinematic",
  "image_base64": "data",
  "metadata": { "strength": 0.5, "guidance_scale": 0.0, "seed": 42 }
}
```
