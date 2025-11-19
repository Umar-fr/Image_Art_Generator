import { API_BASE_URL } from '../config'

export async function stylizeImage({ file, style, strength = 0.7, guidanceScale = 7 }) {
  const body = new FormData()
  body.append('image', file)
  body.append('style', style)
  body.append('strength', String(strength))
  body.append('guidance_scale', String(guidanceScale))

  const response = await fetch(`${API_BASE_URL}/stylize`, {
    method: 'POST',
    body,
  })

  if (!response.ok) {
    const errorPayload = await response.json().catch(() => ({}))
    throw new Error(errorPayload.detail || 'Backend failed to stylize the image.')
  }

  return response.json()
}

