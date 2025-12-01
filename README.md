# bay.md
About the project #bay.md

# Interactive Light Curve Analysis Tool

A comprehensive GUI application for analyzing astronomical light curves using the Lightkurve package. This tool allows you to search for stars, download their data from space telescope missions (TESS, Kepler, K2), and perform detailed light curve analysis.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

### 🔍 Star Search
- Search for any star by name
- Support for multiple missions: TESS, Kepler, K2
- Automatic download with quality filtering

### 📊 Multiple Visualizations
1. **Pixel File View** - Target pixel file with aperture mask
2. **Light Curve** - Raw light curve from the telescope
3. **Flattened LC** - Detrended light curve 
4. **Binned LC** - Interactive binning of folded light curve (adjustable via slider: 10-500 bins)
5. **Periodogram** - Find the best period for periodic signals
6. **Folded LC** - Light curve folded at the detected period

### ✨ Interactive Features
- Real-time bin size adjustment with slider
- Matplotlib navigation tools (zoom, pan, save)
- Multiple tabs for easy navigation between plots
- Load local FITS files or search online

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/exoplanet-analysis.git
cd exoplanet-analysis

# Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required packages
pip install lightkurve matplotlib numpy astropy
```

## Required Dependencies

- Python 3.7+
- lightkurve
- matplotlib
- numpy
- astropy
- tkinter (usually comes with Python)

## Usage

### Running the Application

```bash
python interactive_lightcurve_app.py
```

### Quick Start

1. **Search for a star:**
   - Enter star name (e.g., "WASP-18", "Kepler-10")
   - Select mission (TESS, Kepler, or K2)
   - Click "Search & Download"

2. **Or load a local FITS file:**
   - Click "Load FITS File"
   - Select your .fits file

3. **Explore the data:**
   - Navigate through tabs to see different plots
   - Use the slider in "Binned LC" tab to adjust binning
   - All plots are automatically generated

### Example Stars to Try

- **WASP-18** (TESS) - Hot Jupiter with 0.94 day period
- **Kepler-10** (Kepler) - First rocky exoplanet confirmed by Kepler
- **HAT-P-7** (Kepler) - Hot Jupiter with phase curve variations
- **TRAPPIST-1** (K2) - Seven Earth-sized planets

## How It Works

1. **Data Acquisition**: Downloads target pixel files from MAST archive
2. **Light Curve Extraction**: Extracts flux from all pixels
3. **Detrending**: Applies Savitzky-Golay filter to remove systematic trends
4. **Period Finding**: Uses Lomb-Scargle periodogram
5. **Phase Folding**: Folds light curve at detected period
6. **Binning**: Bins folded data for clearer transit visualization

## Project Structure

```
exoplanet-analysis/
├── interactive_lightcurve_app.py  # Main GUI application
├── lightkurve notebook.ipynb      # Analysis notebook
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## Screenshots

The application provides six different visualization tabs for comprehensive light curve analysis.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with [Lightkurve](https://docs.lightkurve.org/) - A Python package for Kepler and TESS data analysis
- Data from NASA's MAST archive (TESS, Kepler, K2 missions)

## Contact

For questions or suggestions, please open an issue on GitHub.

---

**Note**: This tool requires an internet connection to search and download data from the MAST archive. Downloaded FITS files are automatically excluded from version control (.gitignore).
