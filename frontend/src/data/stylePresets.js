export const STYLE_PRESETS = [
  {
    id: 'ghibli',
    label: 'Studio Ghibli',
    tagline: 'Soft palettes, painterly fantasy vibes.',
    accent: '#5fb3b3',
    prompt:
      'Studio Ghibli concept art, whimsical atmosphere, painterly textures, soft natural lighting, high detail',
    negativePrompt:
      'grainy, noisy, distorted, low resolution, dull colors, ugly, deformed, watermark, text',
  },
  {
    id: 'naruto',
    label: 'Naruto Manga',
    tagline: 'High-contrast shonen ink style.',
    accent: '#f78f3f',
    prompt:
      'Naruto manga panel, dynamic cel shading, crisp inked lines, hyper stylized shonen jump aesthetic',
    negativePrompt:
      'photorealistic, blurry, washed out colors, realistic lighting, low detail, text',
  },
  {
    id: 'dragonball',
    label: 'Dragon Ball Z',
    tagline: 'Bold lines, saturated energy.',
    accent: '#f3d03e',
    prompt:
      'Dragon Ball Z anime frame, bold outlines, saturated cel shading, kinetic energy fx, toriyama style',
    negativePrompt:
      'painterly, watercolor, muted tones, noise, low detail, soft focus, text',
  },
  {
    id: 'picasso',
    label: 'Picasso Cubism',
    tagline: 'Abstract cubist reinterpretation.',
    accent: '#d66c6c',
    prompt:
      'Picasso cubist portrait, angular geometry, abstract forms, bold color blocking, overlapping perspective',
    negativePrompt:
      'photorealistic, smooth shading, realistic proportions, soft lighting, text',
  },
  {
    id: 'davinci',
    label: 'Da Vinci Sketch',
    tagline: 'Renaissance graphite study.',
    accent: '#c2a878',
    prompt:
      'Leonardo da Vinci charcoal sketch, sfumato shading, renaissance study, parchment background, precise anatomy',
    negativePrompt:
      'bright colors, comic style, digital artifacts, sharp modern lines, text',
  },
]

export const getStyleById = (id) =>
  STYLE_PRESETS.find((style) => style.id === id)

