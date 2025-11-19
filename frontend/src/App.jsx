import { useMemo, useState } from 'react'
import './App.css'
import { STYLE_PRESETS, getStyleById } from './data/stylePresets'
import { UploadZone } from './components/UploadZone'
import { StyleSelector } from './components/StyleSelector'
import { ResultPane } from './components/ResultPane'
import { stylizeImage } from './services/api'
import { useImagePreview } from './hooks/useImagePreview'

function App() {
  const [file, setFile] = useState(null)
  const [style, setStyle] = useState(STYLE_PRESETS[0].id)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [resultUrl, setResultUrl] = useState('')
  const [strength, setStrength] = useState(0.65)
  const [guidance, setGuidance] = useState(7)

  const previewUrl = useImagePreview(file)
  const activeStyle = useMemo(() => getStyleById(style), [style])

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0]
    if (!selectedFile) {
      setFile(null)
      return
    }

    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('Max file size is 10 MB.')
      return
    }

    setError('')
    setResultUrl('')
    setFile(selectedFile)
  }

  const handleProcess = async () => {
    if (!file) {
      setError('Please upload an image first.')
      return
    }

    setIsLoading(true)
    setError('')

    try {
      const response = await stylizeImage({
        file,
        style,
        strength,
        guidanceScale: guidance,
      })
      const dataUrl = `data:image/png;base64,${response.image_base64}`
      setResultUrl(dataUrl)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDownload = () => {
    if (!resultUrl) return
    const link = document.createElement('a')
    link.href = resultUrl
    link.download = `${style}-art.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="page">
      <header className="page__header">
        <div>
          <p className="eyebrow">Zero-cost art stylization pipeline</p>
          <h1>DreamForge Studio</h1>
          <p className="lede">
            Upload a reference photo, pick a preset, and let the Colab backend remaster it using
            open-source diffusion checkpoints.
          </p>
        </div>
        <div className="header__pill">
          <span>Active preset</span>
          <strong style={{ color: activeStyle.accent }}>{activeStyle.label}</strong>
        </div>
      </header>

      <section className="panel">
        <div className="panel__column">
          <UploadZone previewUrl={previewUrl} onFileChange={handleFileChange} isDisabled={isLoading} />

          <div className="panel__controls">
            <label>
              <span>Strength: {strength.toFixed(2)}</span>
              <input
                type="range"
                min="0.2"
                max="0.95"
                step="0.01"
                value={strength}
                onChange={(event) => setStrength(Number(event.target.value))}
              />
            </label>
            <label>
              <span>Guidance: {guidance.toFixed(1)}</span>
              <input
                type="range"
                min="3"
                max="12"
                step="0.1"
                value={guidance}
                onChange={(event) => setGuidance(Number(event.target.value))}
              />
            </label>
          </div>

          <button type="button" className="primary-button primary-button--lg" onClick={handleProcess} disabled={isLoading}>
            {isLoading ? 'Processing…' : 'Process image'}
          </button>

          {error && <p className="error-chip">{error}</p>}
        </div>

        <div className="panel__column panel__column--grow">
          <ResultPane outputUrl={resultUrl} isLoading={isLoading} error={error} onDownload={handleDownload} />
        </div>
      </section>

      <section>
        <div className="section-heading">
          <h2>Pick an art direction</h2>
          <p>Each preset maps to a prompt + negative prompt pair in the Python backend.</p>
        </div>
        <StyleSelector styles={STYLE_PRESETS} selectedStyle={style} onSelect={setStyle} />
      </section>
    </div>
  )
}

export default App
