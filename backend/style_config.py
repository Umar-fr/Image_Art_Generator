from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StylePreset:
  name: str
  prompt: str
  negative_prompt: str
  lora_repo: str | None = None
  lora_weight: float = 0.6


STYLE_PRESETS: dict[str, StylePreset] = {
  'ghibli': StylePreset(
    name='Studio Ghibli',
    prompt='Studio Ghibli concept art, whimsical, painterly, soft lighting, high detail',
    negative_prompt='grainy, noisy, distorted, low resolution, dull colors, ugly, deformed, watermark, text',
    lora_repo='KBlueLeaf/kohaku-XL-ZavyChromaGhibli',
    lora_weight=0.65,
  ),
  'naruto': StylePreset(
    name='Naruto Manga',
    prompt='Naruto manga panel, bold ink, high energy, shonen jump, cel shading, speed lines',
    negative_prompt='photorealistic, blurry, washed out colors, realistic lighting, low detail, text',
    lora_repo='pcuenq/naruto-anime-xl-lora',
  ),
  'dragonball': StylePreset(
    name='Dragon Ball Z',
    prompt='Dragon Ball Z anime still, bold outlines, saturated colors, kinetic motion, akira toriyama style',
    negative_prompt='painterly, watercolor, muted tones, noise, low detail, soft focus, text',
    lora_repo='ckpt/DBZ-XL-LoRA',
  ),
  'picasso': StylePreset(
    name='Picasso Cubism',
    prompt='Picasso cubist portrait, angular geometry, abstract forms, bold color blocking, overlapping perspective',
    negative_prompt='photorealistic, soft lighting, smooth shading, realistic proportions, text',
    lora_repo=None,
  ),
  'davinci': StylePreset(
    name='Da Vinci Sketch',
    prompt='Leonardo da Vinci charcoal sketch, sfumato shading, renaissance study, parchment background, precise anatomy',
    negative_prompt='bright colors, comic style, digital artifacts, sharp modern lines, text',
    lora_repo='mikekage/DaVinciSketchXL',
    lora_weight=0.5,
  ),
}


def list_presets() -> list[str]:
  return list(STYLE_PRESETS.keys())

