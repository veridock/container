# Getting Started

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Installation

### Install from PyPI
```bash
pip install svgg
```

### Install from source
```bash
git clone https://github.com/veridock/svgg.git
cd svgg
pip install -e .
```

### Verify Installation
```bash
svgg --version
```

## Basic Usage

### Command Line Interface

#### Embed a PDF into an SVG
```bash
svgg embed document.pdf --into template.svg --output enhanced.svg
```

#### Create an SVG bundle from multiple files
```bash
svgg create --files "*.pdf,*.png,*.json" --output bundle.svg
```

#### Extract embedded files from an SVG
```bash
svgg extract document.svg --output-dir ./extracted/
```

#### Show information about embedded files
```bash
svgg info document.svg
```

## Next Steps
- [View API Documentation](./api/)
- [Explore Examples](./examples/)
- [Read the Advanced Guide](./guides/advanced.md)
