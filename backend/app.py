import base64
import io
import os
from typing import Optional

import torch
from diffusers import AutoPipelineForImage2Image
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from style_config import STYLE_PRESETS, list_presets

# Environment setup
MODEL_ID = os.getenv("MODEL_ID", "stabilityai/sdxl-turbo")
DEVICE = "cpu"
DTYPE = torch.float32

# FastAPI app setup
app = FastAPI(title="Rot PG API", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_pipeline():
    """Loads the image-to-image pipeline from Hugging Face."""
    pipe = AutoPipelineForImage2Image.from_pretrained(
        MODEL_ID, torch_dtype=DTYPE, variant="fp16", use_safetensors=True
    )
    pipe.to(DEVICE)
    return pipe

@app.on_event("startup")
def warm_pipeline():
    """Warm up the pipeline on application startup."""
    app.state.pipeline = load_pipeline()

def image_bytes_to_pil(image_bytes: bytes) -> Image.Image:
    """Converts image bytes to a PIL Image."""
    try:
        return Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        raise HTTPException(400, "Invalid image file.") from exc

def pil_to_base64(image: Image.Image) -> str:
    """Converts a PIL Image to a base64 string."""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "device": DEVICE, "available_styles": list_presets()}

@app.post("/stylize")
async def stylize(
    image: UploadFile = File(...),
    style: str = Form(...),
    strength: float = Form(0.5),
    guidance_scale: float = Form(0.0),
    seed: Optional[int] = Form(None),
):
    """Stylizes an image based on a given style."""
    preset = STYLE_PRESETS.get(style)
    if not preset:
        raise HTTPException(400, f'Unknown style "{style}".')

    contents = await image.read()
    if len(contents) > 12 * 1024 * 1024:
        raise HTTPException(400, "File too large. Keep it under 12 MB.")

    init_image = image_bytes_to_pil(contents)
    pipeline = app.state.pipeline

    generator = torch.Generator(device=DEVICE)
    if seed is not None:
        generator = generator.manual_seed(int(seed))

    try:
        result = pipeline(
            prompt=preset.prompt,
            negative_prompt=preset.negative_prompt,
            image=init_image,
            strength=float(strength),
            guidance_scale=float(guidance_scale),
            num_inference_steps=2,
            generator=generator,
        ).images[0]
    except Exception as exc:
        raise HTTPException(500, f"Stylization failed: {exc}") from exc

    base64_image = pil_to_base64(result)
    return {
        "style": style,
        "image_base64": base64_image,
        "metadata": {
            "strength": strength,
            "guidance_scale": guidance_scale,
            "seed": seed,
        },
    }

