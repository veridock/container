# Advanced Usage

## Custom Templates

You can create custom SVG templates with placeholders that will be replaced during the embedding process.

### Template Example (`template.svg`)
```xml
<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#f0f0f0"/>
  <text x="20" y="40" font-family="Arial" font-size="24">
    {{ title }}
  </text>
  <text x="20" y="70" font-family="Arial" font-size="12">
    Generated on {{ date }}
  </text>
  <!-- Content will be inserted here -->
  <g id="embedded-content"></g>
</svg>
```

### Using the Template
```python
from datetime import datetime
import svgg

generator = svgg.SVGGenerator()
result = generator.embed(
    svg_file="template.svg",
    files=["data.json"],
    output="custom_output.svg",
    template_vars={
        "title": "Custom Report",
        "date": datetime.now().strftime("%Y-%m-%d")
    }
)
```

## Batch Processing

Process multiple SVGs in a directory:

```python
import os
from pathlib import Path
import svgg

generator = svgg.SVGGenerator()
input_dir = "input_svgs/"
output_dir = "output_svgs/"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process all SVGs in the input directory
for svg_file in Path(input_dir).glob("*.svg"):
    output_file = Path(output_dir) / f"enhanced_{svg_file.name}"
    
    result = generator.embed(
        svg_file=str(svg_file),
        files=["logo.png", "styles.css"],
        output=str(output_file)
    )
    
    if result.success:
        print(f"Created {output_file}")
    else:
        print(f"Error processing {svg_file}: {result.error}")
```

## Working with Metadata

### Adding Metadata
```python
metadata = {
    "title": "Quarterly Report",
    "author": "Analytics Team",
    "created": "2025-06-28",
    "version": "1.0.0",
    "tags": ["report", "quarterly", "2025"]
}

generator.embed(
    svg_file="template.svg",
    files=["report.pdf"],
    output="report_with_metadata.svg",
    metadata=metadata
)
```

### Reading Metadata
```python
from svgg import SVGExtractor

extractor = SVGExtractor()
metadata = extractor.get_metadata("report_with_metadata.svg")
print("Document metadata:", metadata)
```

## Performance Considerations

### Compression
Enable compression for large files:
```python
generator = svgg.SVGGenerator(compression=True)
```

### Memory Management
For very large files, process them in chunks:
```python
# Process large files in chunks
def process_large_file(input_file, output_file, chunk_size=1024*1024):  # 1MB chunks
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while chunk := f_in.read(chunk_size):
            # Process chunk
            f_out.write(process_chunk(chunk))
```

## Integration with Web Applications

### FastAPI Example
```python
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import svgg
import tempfile
import os

app = FastAPI()

def process_svg(svg_file, files, output_path):
    generator = svgg.SVGGenerator()
    result = generator.embed(
        svg_file=svg_file,
        files=files,
        output=output_path
    )
    return result

@app.post("/embed")
async def embed_files(
    svg_template: UploadFile = File(...),
    files: list[UploadFile] = File(...)
):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded files
        svg_path = os.path.join(temp_dir, "template.svg")
        with open(svg_path, "wb") as f:
            f.write(await svg_template.read())
        
        file_paths = []
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())
            file_paths.append(file_path)
        
        # Process files
        output_path = os.path.join(temp_dir, "output.svg")
        result = process_svg(svg_path, file_paths, output_path)
        
        if result.success:
            return FileResponse(
                output_path,
                media_type="image/svg+xml",
                filename="output.svg"
            )
        else:
            return {"error": str(result.error)}
```
