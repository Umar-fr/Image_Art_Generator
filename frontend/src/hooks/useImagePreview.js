import { useEffect, useMemo } from 'react'

export function useImagePreview(file) {
  const previewUrl = useMemo(() => {
    if (!file) {
      return ''
    }

    return URL.createObjectURL(file)
  }, [file])

  useEffect(() => {
    if (!previewUrl) {
      return () => {}
    }

    return () => {
      URL.revokeObjectURL(previewUrl)
    }
  }, [previewUrl])

  return previewUrl
}

