# API Reference

## SVGGenerator

Main class for embedding files into SVGs.

### Initialization
```python
generator = SVGGenerator(
    compression=False,  # Enable compression
    overwrite=False,    # Overwrite existing files
    verbose=False       # Show progress information
)
```

### Methods

#### `embed(svg_file, files, output, **kwargs)`
Embed files into an SVG.

**Parameters:**
- `svg_file` (str): Path to SVG template
- `files` (str/list): File(s) to embed (path or list of paths)
- `output` (str): Output file path
- `**kwargs`: Additional options
  - `metadata` (dict): Document metadata
  - `compression` (bool): Enable compression
  - `template_vars` (dict): Template variables

**Returns:**
`Result` object with success status and details

#### `embed_directory(svg_file, directory, output, **kwargs)`
Embed all matching files from a directory.

**Parameters:**
- `directory` (str): Directory path
- `pattern` (str): File pattern (default: "*.*")
- `recursive` (bool): Include subdirectories
- Other parameters same as `embed()`

#### `from_string(svg_content, files, **kwargs)`
Create SVG from string content.

**Parameters:**
- `svg_content` (str): SVG content as string
- Other parameters same as `embed()`

## SVGExtractor

Utility for extracting embedded files from SVGs.

### Methods

#### `extract(svg_file, output_dir, pattern='*')`
Extract embedded files.

**Parameters:**
- `svg_file` (str): Path to SVG file
- `output_dir` (str): Output directory
- `pattern` (str): File pattern to match

**Returns:**
`Result` object with list of extracted files

#### `list_files(svg_file)`
List embedded files without extracting.

**Returns:**
List of embedded file information

#### `get_metadata(svg_file)`
Get metadata from SVG.

**Returns:**
Dictionary of metadata
