import PropTypes from 'prop-types'

export function StyleSelector({ styles, selectedStyle, onSelect }) {
  return (
    <div className="style-grid">
      {styles.map((style) => {
        const isSelected = style.id === selectedStyle
        return (
          <button
            key={style.id}
            type="button"
            className={`style-card ${isSelected ? 'style-card--active' : ''}`}
            style={{ borderColor: isSelected ? style.accent : 'transparent' }}
            onClick={() => onSelect(style.id)}
          >
            <div className="style-card__dot" style={{ background: style.accent }} />
            <div>
              <p className="style-card__label">{style.label}</p>
              <p className="style-card__tagline">{style.tagline}</p>
            </div>
          </button>
        )
      })}
    </div>
  )
}

StyleSelector.propTypes = {
  styles: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired,
      tagline: PropTypes.string.isRequired,
      accent: PropTypes.string.isRequired,
    }),
  ).isRequired,
  selectedStyle: PropTypes.string.isRequired,
  onSelect: PropTypes.func.isRequired,
}

