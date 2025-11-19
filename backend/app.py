"""FastAPI backend for style transfer running on Google Colab or local GPU."""

from __future__ import annotations

import base64
import io
import os
from typing import Optional

import torch
from diffusers import (
  AutoencoderKL,
  StableDiffusionXLImg2ImgPipeline,
  UNet2DConditionModel,
)
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from style_config import STYLE_PRESETS, StylePreset, list_presets

MODEL_ID = os.getenv('SDXL_MODEL_ID', 'stabilityai/stable-diffusion-xl-base-1.0')
VAE_ID = os.getenv('SDXL_VAE_ID', 'madebyollin/sdxl-vae-fp16-fix')
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

app = FastAPI(title='DreamForge Studio API', version='0.1.0')

app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)


def _load_pipeline() -> StableDiffusionXLImg2ImgPipeline:
  dtype = torch.float16 if DEVICE == 'cuda' else torch.float32
  vae = AutoencoderKL.from_pretrained(VAE_ID, torch_dtype=dtype)
  unet = UNet2DConditionModel.from_pretrained(MODEL_ID, subfolder='unet', torch_dtype=dtype)
  pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    MODEL_ID,
    vae=vae,
    unet=unet,
    torch_dtype=dtype,
    use_safetensors=True,
  )
  pipe.to(DEVICE)
  pipe.enable_attention_slicing()
  pipe.enable_vae_slicing()
  pipe.enable_model_cpu_offload() if DEVICE != 'cuda' else None
  return pipe


@app.on_event('startup')
def warm_pipeline():
  app.state.pipeline = _load_pipeline()
  app.state.loaded_loras = set()


def _disable_all_loras(pipeline: StableDiffusionXLImg2ImgPipeline):
  if hasattr(pipeline, 'disable_lora_adapters'):
    pipeline.disable_lora_adapters()
    return

  try:
    pipeline.set_adapters([], adapter_weights=[])
  except TypeError:
    pipeline.set_adapters([])


def _apply_lora_if_needed(pipeline: StableDiffusionXLImg2ImgPipeline, preset: StylePreset):
  if not preset.lora_repo:
    _disable_all_loras(pipeline)
    return

  if preset.name not in getattr(app.state, 'loaded_loras', set()):
    pipeline.load_lora_weights(
      preset.lora_repo,
      adapter_name=preset.name,
      weight_name=preset.lora_weight_name,
    )
    app.state.loaded_loras.add(preset.name)

  pipeline.set_adapters([preset.name], adapter_weights=[preset.lora_weight])


def _image_bytes_to_pil(image_bytes: bytes) -> Image.Image:
  try:
    return Image.open(io.BytesIO(image_bytes)).convert('RGB')
  except Exception as exc:  # pylint: disable=broad-except
    raise HTTPException(400, detail='Invalid image file.') from exc


def _pil_to_base64(image: Image.Image) -> str:
  buffer = io.BytesIO()
  image.save(buffer, format='PNG')
  return base64.b64encode(buffer.getvalue()).decode('utf-8')


@app.get('/health')
def health():
  return {'status': 'ok', 'device': DEVICE, 'available_styles': list_presets()}


@app.post('/stylize')
async def stylize(
  image: UploadFile = File(...),
  style: str = Form(...),
  strength: float = Form(0.65),
  guidance_scale: float = Form(7.0),
  seed: Optional[int] = Form(None),
):
  preset = STYLE_PRESETS.get(style)
  if not preset:
    raise HTTPException(400, detail=f'Unknown style "{style}".')

  contents = await image.read()
  if len(contents) > 12 * 1024 * 1024:
    raise HTTPException(400, detail='File too large. Keep it under 12 MB.')

  init_image = _image_bytes_to_pil(contents)
  pipeline: StableDiffusionXLImg2ImgPipeline = app.state.pipeline

  try:
    _apply_lora_if_needed(pipeline, preset)

    generator = torch.Generator(device=DEVICE)
    if seed is not None:
      generator = generator.manual_seed(int(seed))

    result = pipeline(
      prompt=preset.prompt,
      negative_prompt=preset.negative_prompt,
      image=init_image,
      strength=float(strength),
      guidance_scale=float(guidance_scale),
      generator=generator,
    )
  except Exception as exc:  # pylint: disable=broad-except
    raise HTTPException(500, detail=f'Stylization failed: {exc}') from exc

  base64_image = _pil_to_base64(result.images[0])
  return {
    'style': style,
    'image_base64': base64_image,
    'metadata': {
      'strength': strength,
      'guidance_scale': guidance_scale,
      'seed': seed,
    },
  }

