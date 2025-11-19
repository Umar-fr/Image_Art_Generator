import PropTypes from 'prop-types'

export function UploadZone({ previewUrl, onFileChange, isDisabled }) {
  return (
    <label className={`upload-zone ${isDisabled ? 'upload-zone--disabled' : ''}`}>
      <input
        type="file"
        accept="image/png,image/jpeg"
        onChange={onFileChange}
        disabled={isDisabled}
      />
      {previewUrl ? (
        <img src={previewUrl} alt="Preview" className="upload-zone__preview" />
      ) : (
        <div className="upload-zone__placeholder">
          <p>Drop an image (PNG/JPG) or click to browse</p>
          <span>Max 10 MB • Face-forward portraits work best</span>
        </div>
      )}
    </label>
  )
}

UploadZone.propTypes = {
  previewUrl: PropTypes.string,
  onFileChange: PropTypes.func.isRequired,
  isDisabled: PropTypes.bool,
}

UploadZone.defaultProps = {
  previewUrl: '',
  isDisabled: false,
}

