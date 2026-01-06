from dataclasses import dataclass

@dataclass(frozen=True)
class StylePreset:
    name: str
    prompt: str
    negative_prompt: str

STYLE_PRESETS = {
    "cinematic": StylePreset(
        name="Cinematic",
        prompt="cinematic still, emotional, harmonious, vignette, highly detailed, high budget, bokeh, cinemascope, moody, epic, gorgeous, film grain, grainy",
        negative_prompt="anime, cartoon, graphic, text, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured"
    ),
    "digital-art": StylePreset(
        name="Digital Art",
        prompt="concept art, digital artwork, illustrative, painterly, matte painting, highly detailed",
        negative_prompt="photo, photorealistic, realism, ugly"
    ),
}

def list_presets() -> list[str]:
    return list(STYLE_PRESETS.keys())

