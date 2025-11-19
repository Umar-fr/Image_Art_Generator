import PropTypes from 'prop-types'

export function ResultPane({ outputUrl, isLoading, error, onDownload }) {
  return (
    <div className="result-pane">
      <div className="result-pane__header">
        <div>
          <p className="result-pane__title">Stylized output</p>
          <p className="result-pane__subtitle">
            We keep the link in-memory. Download before you refresh.
          </p>
        </div>
        <button
          type="button"
          className="primary-button"
          disabled={!outputUrl || isLoading}
          onClick={onDownload}
        >
          Download
        </button>
      </div>

      <div className="result-pane__body">
        {isLoading && (
          <div className="result-pane__placeholder">
            <div className="spinner" />
            <p>Generating… this usually takes 10-15 seconds in Colab.</p>
          </div>
        )}

        {!isLoading && error && (
          <div className="result-pane__placeholder result-pane__placeholder--error">
            <p>{error}</p>
          </div>
        )}

        {!isLoading && !outputUrl && !error && (
          <div className="result-pane__placeholder">
            <p>Your stylized result will appear here.</p>
          </div>
        )}

        {!isLoading && outputUrl && (
          <img src={outputUrl} alt="Stylized output" className="result-pane__image" />
        )}
      </div>
    </div>
  )
}

ResultPane.propTypes = {
  outputUrl: PropTypes.string,
  isLoading: PropTypes.bool,
  error: PropTypes.string,
  onDownload: PropTypes.func.isRequired,
}

ResultPane.defaultProps = {
  outputUrl: '',
  isLoading: false,
  error: '',
}

