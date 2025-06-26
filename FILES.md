## 🧪 Testing and Examples

### Comprehensive Import/Export Testing
```python
import svgg
import tempfile
import os
from pathlib import Path

def test_complete_workflow():
    """Test complete import/export workflow with multiple formats"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test project structure
        project_dir = Path(temp_dir) / "test_project"
        project_dir.mkdir()
        
        # Create test files
        (project_dir / "README.md").write_text("# Test Project\nThis is a test.")
        (project_dir / "data.json").write_text('{"version": "1.0", "name": "test"}')
        (project_dir / "src").mkdir()
        (project_dir / "src" / "main.py").write_text('print("Hello, World!")')
        
        # Create base SVG
        template_svg = Path(temp_dir) / "template.svg"
        template_svg.write_text('<svg><rect width="100" height="100"/></svg>')
        
        # Test directory import with structure preservation
        importer = svgg.ProjectImporter()
        bundle_svg = Path(temp_dir) / "bundle.svg"
        
        result = importer.import_project(
            svg_file=str(template_svg),
            project_path=str(project_dir),
            output=str(bundle_svg),
            config={
                "preserve_structure": True,
                "generate_tree": True,
                "include_patterns": ["*.md", "*.json", "*.py"]
            }
        )
        
        # Verify import
        lister = svgg.SVGLister()
        files_info = lister.list_files(str(bundle_svg))
        assert len(files_info) == 3  # README.md, data.json, main.py
        
        # Test listing functionality
        detailed_info = lister.list_detailed(str(bundle_svg))
        assert detailed_info.has_structure_metadata
        
        # Test HTML extraction
        web_extractor = svgg.WebExtractor()
        website_dir = Path(temp_dir) / "website"
        
        web_extractor.extract_to_html(
            svg_file=str(bundle_svg),
            output_dir=str(website_dir),
            include_viewer=True,
            preserve_structure=True
        )
        
        # Verify HTML extraction
        assert (website_dir / "index.html").exists()
        assert (website_dir / "files" / "README.md").exists()
        assert (website_dir / "files" / "src" / "main.py").exists()
        
        # Test DOCX export
        doc_exporter = svgg.DocExporter()
        docx_file = Path(temp_dir) / "document.docx"
        
        doc_exporter.export_to_docx(
            svg_file=str(bundle_svg),
            output_file=str(docx_file),
            embed_svg=True,
            extract_files=True,
            metadata_table=True
        )
        
        assert docx_file.exists()
        
        # Test specific file extraction
        file_extractor = svgg.FileExtractor()
        extracted_file = Path(temp_dir) / "extracted_main.py"
        
        file_extractor.extract_specific(
            svg_file=str(bundle_svg),
            filename="src/main.py",
            output_path=str(extracted_file)
        )
        
        assert extracted_file.exists()
        assert extracted_file.read_text() == 'print("Hello, World!")'
        
        print("✅ All tests passed!")

def test_zip_import_export():
    """Test ZIP archive import and export functionality"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test ZIP structure
        import zipfile
        
        zip_path = Path(temp_dir) / "test.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("docs/README.md", "# Documentation")
            zf.writestr("docs/API.md", "# API Reference")
            zf.writestr("src/app.py", "def main(): pass")
            zf.writestr("config.json", '{"debug": true}')
        
        # Create template SVG
        template_svg = Path(temp_dir) / "template.svg"
        template_svg.write_text('<svg><rect width="100" height="100"/></svg>')
        
        # Import ZIP with structure
        zip_importer = svgg.ZipImporter()
        bundle_svg = Path(temp_dir) / "zip_bundle.svg"
        
        result = zip_importer.import_zip_archive(
            svg_file=str(template_svg),
            zip_path=str(zip_path),
            output=str(bundle_svg),
            preserve_structure=True,
            metadata_detail_level="full"
        )
        
        # Verify structure metadata
        lister = svgg.SVGLister()
        info = lister.list_detailed(str(bundle_svg))
        
        assert info.metadata["archive_structure"]["total_files"] == 4
        assert "docs/" in info.metadata["archive_structure"]["tree"]
        assert "src/" in info.metadata["archive_structure"]["tree"]
        
        # Export back to ZIP
        exporter = svgg.SVGExporter()
        output_zip = Path(temp_dir) / "exported.zip"
        
        exporter.export_to_zip(
            svg_file=str(bundle_svg),
            output_file=str(output_zip),
            preserve_structure=True
        )
        
        # Verify exported ZIP
        with zipfile.ZipFile(output_zip, 'r') as zf:
            names = zf.namelist()
            assert "docs/README.md" in names
            assert "docs/API.md" in names
            assert "src/app.py" in names
            assert "config.json" in names
        
        print("✅ ZIP import/export test passed!")

def test_url_import():
    """Test URL import functionality"""
    
    # Mock URL responses for testing
    import unittest.mock
    
    with tempfile.TemporaryDirectory() as temp_dir:
        template_svg = Path(temp_dir) / "template.svg"
        template_svg.write_text('<svg><rect width="100" height="100"/></svg>')
        
        # Mock successful HTTP response
        mock_response = unittest.mock.Mock()
        mock_response.content = b"Mock PDF content"
        mock_response.headers = {"content-type": "application/pdf"}
        mock_response.status_code = 200
        
        with unittest.mock.patch('requests.get', return_value=mock_response):
            multi_importer = svgg.MultiImporter()
            bundle_svg = Path(temp_dir) / "url_bundle.svg"
            
            # Import from mock URL
            multi_importer.import_from_urls(
                svg_file=str(template_svg),
                urls=["https://example.com/document.pdf"],
                output=str(bundle_svg),
                headers={"Authorization": "Bearer test-token"}
            )
            
            # Verify import
            lister = svgg.SVGLister()
            files_info = lister.list_files(str(bundle_svg))
            assert len(files_info) == 1
            assert files_info[0].name == "document.pdf"
            assert files_info[0].mime_type == "application/pdf"
        
        print("✅ URL import test passed!")

if __name__ == "__main__":
    test_complete_workflow()
    test_zip_import_export()
    test_url_import()
    print("🎉 All tests completed successfully!")
```

### Real-world Usage Examples

#### Example 1: Documentation Bundle Creation
```python
import svgg
from pathlib import Path

def create_documentation_bundle():
    """Create a complete documentation bundle from a project"""
    
    # Initialize importers
    project_importer = svgg.ProjectImporter()
    repo_importer = svgg.RepositoryImporter()
    
    # Import local documentation
    local_docs = project_importer.import_project(
        svg_file="docs_template.svg",
        project_path="./docs/",
        output="temp_docs.svg",
        config={
            "include_patterns": ["*.md", "*.rst", "*.txt", "*.png", "*.jpg"],
            "preserve_structure": True,
            "generate_tree": True
        }
    )
    
    # Import external examples from GitHub
    repo_importer.import_from_git(
        svg_file="temp_docs.svg",
        repo_url="https://github.com/project/examples.git",
        output="docs_bundle.svg",
        config={
            "branch": "main",
            "paths": ["examples/", "README.md"],
            "file_patterns": ["*.py", "*.js", "*.md"],
            "max_files": 50
        }
    )
    
    # Generate multiple output formats
    web_extractor = svgg.WebExtractor()
    doc_exporter = svgg.DocExporter()
    
    # Create interactive website
    web_extractor.extract_to_html(
        svg_file="docs_bundle.svg",
        output_dir="./docs_website/",
        template="documentation",
        css_framework="bootstrap",
        include_viewer=True,
        create_index=True
    )
    
    # Create Word document
    doc_exporter.export_to_docx(
        svg_file="docs_bundle.svg",
        output_file="documentation.docx",
        template="technical_doc_template.docx",
        embed_svg=True,
        extract_files=True
    )
    
    # Create MHTML archive
    web_extractor.export_to_mhtml(
        svg_file="docs_bundle.svg",
        output_file="documentation_archive.mhtml",
        include_attachments=True
    )
    
    print("✅ Documentation bundle created successfully!")
    print("📁 Website: ./docs_website/")
    print("📄 Word Doc: documentation.docx")
    print("📦 Archive: documentation_archive.mhtml")

#### Example 2: Project Backup and Migration
```python
def backup_and_migrate_project():
    """Backup entire project and prepare for migration"""
    
    # Create comprehensive backup
    project_importer = svgg.ProjectImporter()
    
    # Backup source code
    source_backup = project_importer.import_project(
        svg_file="backup_template.svg",
        project_path="./src/",
        output="source_backup.svg",
        config={
            "include_patterns": ["*.py", "*.js", "*.ts", "*.jsx", "*.vue"],
            "exclude_patterns": ["*.pyc", "__pycache__/*", "node_modules/*"],
            "preserve_structure": True,
            "max_file_size": "10MB"
        }
    )
    
    # Backup configuration and documentation
    config_backup = project_importer.import_project(
        svg_file="source_backup.svg",
        project_path="./",
        output="full_backup.svg",
        config={
            "include_patterns": [
                "*.json", "*.yaml", "*.yml", "*.toml", "*.ini",
                "*.md", "*.rst", "*.txt", "Dockerfile", "requirements.txt"
            ],
            "preserve_structure": True
        }
    )
    
    # Add external dependencies info
    multi_importer = svgg.MultiImporter()
    
    # Import package.json, requirements.txt, etc. from URLs if needed
    urls = [
        "https://raw.githubusercontent.com/project/config/main/package.json",
        "https://raw.githubusercontent.com/project/config/main/requirements.txt"
    ]
    
    multi_importer.import_from_urls(
        svg_file="full_backup.svg",
        urls=urls,
        output="complete_backup.svg"
    )
    
    # Create migration package
    exporter = svgg.SVGExporter()
    
    # Export as organized ZIP
    exporter.export_to_zip(
        svg_file="complete_backup.svg",
        output_file="migration_package.zip",
        preserve_structure=True
    )
    
    # Create migration documentation
    doc_exporter = svgg.DocExporter()
    doc_exporter.export_to_docx(
        svg_file="complete_backup.svg",
        output_file="migration_guide.docx",
        template="migration_template.docx",
        metadata_table=True
    )
    
    # Generate file listing
    lister = svgg.SVGLister()
    detailed_info = lister.list_detailed("complete_backup.svg")
    
    with open("backup_manifest.json", "w") as f:
        import json
        json.dump({
            "backup_date": detailed_info.metadata.get("created_date"),
            "total_files": len(detailed_info.files),
            "total_size": detailed_info.total_size_human,
            "structure": detailed_info.metadata.get("directory_tree"),
            "files": [
                {
                    "name": f.name,
                    "size": f.size_human,
                    "type": f.mime_type,
                    "path": f.path
                }
                for f in detailed_info.files
            ]
        }, f, indent=2)
    
    print("✅ Project backup and migration package created!")
    print("📦 Migration package: migration_package.zip")
    print("📋 Migration guide: migration_guide.docx") 
    print("📄 Backup manifest: backup_manifest.json")

#### Example 3: Multi-format Document Processing
```python
def process_document_collection():
    """Process a collection of documents in various formats"""
    
    # Import documents from different sources
    multi_importer = svgg.MultiImporter()
    
    # Local document directory
    local_docs = multi_importer.import_directory(
        svg_file="document_template.svg",
        directory="./documents/",
        output="temp_collection.svg",
        include_patterns=["*.pdf", "*.docx", "*.xlsx", "*.pptx"],
        preserve_structure=True
    )
    
    # Import from cloud storage URLs
    cloud_urls = [
        "https://storage.googleapis.com/bucket/report_q1.pdf",
        "https://s3.amazonaws.com/bucket/presentation.pptx",
        "https://onedrive.com/shared/spreadsheet.xlsx"
    ]
    
    multi_importer.import_from_urls(
        svg_file="temp_collection.svg",
        urls=cloud_urls,
        output="document_collection.svg",
        headers={"Authorization": "Bearer cloud-token"}
    )
    
    # Process and export in multiple formats
    web_extractor = svgg.WebExtractor()
    doc_exporter = svgg.DocExporter()
    file_extractor = svgg.FileExtractor()
    
    # Create web gallery
    web_extractor.extract_to_html(
        svg_file="document_collection.svg",
        output_dir="./document_gallery/",
        template="gallery",
        include_viewer=True,
        responsive=True
    )
    
    # Extract PDFs separately
    pdf_files = file_extractor.extract_by_pattern(
        svg_file="document_collection.svg",
        pattern="*.pdf",
        output_dir="./pdfs/",
        preserve_structure=True
    )
    
    # Create consolidated report
    doc_exporter.export_to_docx(
        svg_file="document_collection.svg",
        output_file="document_index.docx",
        template="index_template.docx",
        extract_files=False,  # Keep as references
        metadata_table=True
    )
    
    # Create email archive
    web_extractor.export_to_eml(
        svg_file="document_collection.svg",
        output_file="document_archive.eml",
        subject="Document Collection Archive",
        sender="archive@company.com",
        recipient="team@company.com"
    )
    
    # Generate processing report
    lister = svgg.SVGLister()
    files_info = lister.list_files("document_collection.svg")
    
    report = {
        "processing_summary": {
            "total_documents": len(files_info),
            "pdf_count": len([f for f in files_info if f.name.endswith('.pdf')]),
            "office_count": len([f for f in files_info if any(f.name.endswith(ext) for ext in ['.docx', '.xlsx', '.pptx'])]),
            "total_size": sum(f.size for f in files_info),
            "sources": ["local", "cloud_storage"]
        },
        "outputs_created": [
            "document_gallery/ (web interface)",
            "pdfs/ (extracted PDFs)",
            "document_index.docx (consolidated report)",
            "document_archive.eml (email archive)"
        ]
    }
    
    with open("processing_report.json", "w") as f:
        import json
        json.dump(report, f, indent=2)
    
    print("✅ Document collection processed successfully!")
    print(f"📊 Processed {len(files_info)} documents")
    print("🌐 Web gallery: ./document_gallery/")
    print("📄 PDFs extracted to: ./pdfs/")
    print("📋 Index document: document_index.docx")
    print("📧 Email archive: document_archive.eml")

# Run examples
if __name__ == "__main__":
    create_documentation_bundle()
    backup_and_migrate_project() 
    process_document_collection()
```# SVGG - SVG Generator

🚀 **Universal tool for creating enhanced SVG files with embedded content**

SVGG (SVG Generator) allows you to embed any files (PDF, images, data) into SVG files, creating self-contained vector documents that work as Progressive Web Applications.

## 🔧 Installation

```bash
pip install svgg
```

## 🚀 Quick Start

### Command Line Interface

```bash
# Embed PDF into SVG
svgg embed document.pdf --into template.svg --output enhanced.svg

# Create SVG bundle from multiple files
svgg create --files "*.pdf,*.png,*.json" --output bundle.svg

# Extract embedded files from SVG
svgg extract document.svg --output-dir ./extracted/

# Show embedded files info
svgg info document.svg
```

### Python API

```python
import svgg

# Create SVG with embedded PDF
generator = svgg.SVGGenerator()
result = generator.embed(
    svg_file="template.svg",
    files=["document.pdf", "image.png"],
    output="enhanced.svg"
)

# Extract embedded content
extractor = svgg.SVGExtractor()
files = extractor.extract("enhanced.svg", output_dir="./extracted/")
print(f"Extracted {len(files)} files")
```

## 📖 Detailed Usage

### 1. Import/Export with Base64 DATA URIs

#### Importing Files as Base64 DATA URIs
```python
import svgg

# Import files as base64 DATA URIs
importer = svgg.SVGImporter()

# Single file import
importer.import_file(
    svg_file="template.svg",
    file_path="document.pdf",
    output="result.svg",
    data_uri=True,  # Convert to base64 DATA URI
    update_metadata=True
)

# Multiple files import
importer.import_files(
    svg_file="template.svg",
    files=["invoice.pdf", "logo.png", "data.json"],
    output="bundle.svg",
    data_uri=True,
    metadata_update={
        "imported_files": 3,
        "import_date": "2025-06-26T10:30:00Z",
        "format": "base64_data_uri"
    }
)

# Import from URL
importer.import_from_url(
    svg_file="template.svg",
    url="https://example.com/document.pdf",
    output="result.svg",
    filename="remote_document.pdf"  # Optional custom name
)
```

#### Extracting to Web Formats
```python
# Extract SVG to HTML website
web_extractor = svgg.WebExtractor()

# Basic HTML export
web_extractor.extract_to_html(
    svg_file="bundle.svg",
    output_dir="./website/",
    template="default",  # or custom template path
    include_viewer=True  # Include interactive SVG viewer
)

# Advanced HTML export with custom styling
web_extractor.extract_to_html(
    svg_file="bundle.svg",
    output_dir="./website/",
    template="custom_template.html",
    css_framework="bootstrap",  # or "tailwind", "bulma"
    include_files=True,  # Extract embedded files to /files/
    create_index=True,   # Create index.html with file listing
    responsive=True      # Mobile-friendly layout
)

# Export to single-file formats
web_extractor.export_to_mhtml(
    svg_file="bundle.svg",
    output_file="document.mhtml",
    include_attachments=True
)

web_extractor.export_to_eml(
    svg_file="bundle.svg", 
    output_file="document.eml",
    subject="Document Bundle",
    sender="noreply@example.com",
    recipient="user@example.com"
)

# Export to DOC format
doc_exporter = svgg.DocExporter()
doc_exporter.export_to_docx(
    svg_file="bundle.svg",
    output_file="document.docx",
    template="default",  # or custom .docx template
    embed_svg=True,      # Include SVG as image
    extract_files=True,  # Add files as attachments
    metadata_table=True  # Include metadata table
)
```

#### Excluding/Extracting Specific Files
```python
# Extract specific file to separate location
file_extractor = svgg.FileExtractor()

# Extract single file
extracted_file = file_extractor.extract_specific(
    svg_file="bundle.svg",
    filename="document.pdf",
    output_path="./extracted/document.pdf",
    remove_from_svg=False  # Keep in SVG or remove
)

# Extract multiple files by pattern
extracted_files = file_extractor.extract_by_pattern(
    svg_file="bundle.svg",
    pattern="*.pdf",  # or regex pattern
    output_dir="./pdfs/",
    remove_from_svg=True,
    update_metadata=True
)

# Exclude files (opposite of extract - remove without saving)
file_extractor.exclude_files(
    svg_file="bundle.svg",
    filenames=["temp.log", "debug.txt"],
    output="cleaned_bundle.svg"
)
```

### 3. Listing Embedded Files

#### Complete File Listing
```python
# List all embedded files with details
lister = svgg.SVGLister()

# Basic listing
files_info = lister.list_files("bundle.svg")
for file_info in files_info:
    print(f"📄 {file_info.name}")
    print(f"   Size: {file_info.size_human}")  # e.g., "1.2 MB"
    print(f"   Type: {file_info.mime_type}")
    print(f"   Encoding: {file_info.encoding}")  # base64, binary, etc.
    print(f"   Added: {file_info.date_added}")

# Detailed listing with metadata
detailed_info = lister.list_detailed("bundle.svg")
print(f"SVG Size: {detailed_info.svg_size_human}")
print(f"Total embedded: {detailed_info.total_size_human}")
print(f"Compression ratio: {detailed_info.compression_ratio}%")
print(f"Files count: {len(detailed_info.files)}")

# Filter by type
pdf_files = lister.list_by_type("bundle.svg", ".pdf")
image_files = lister.list_by_type("bundle.svg", [".png", ".jpg", ".svg"])
```

### 4. Advanced Import Operations

#### Import from Multiple Sources
```python
# Import from multiple URLs
multi_importer = svgg.MultiImporter()

urls = [
    "https://api.example.com/report.pdf",
    "https://storage.example.com/logo.png", 
    "https://data.example.com/stats.json"
]

multi_importer.import_from_urls(
    svg_file="template.svg",
    urls=urls,
    output="bundle.svg",
    headers={"Authorization": "Bearer token123"},
    timeout=30,  # seconds
    retry_count=3
)

# Import entire directory structure
multi_importer.import_directory(
    svg_file="template.svg",
    directory="./project/",
    output="project_bundle.svg",
    include_patterns=["*.md", "*.json", "*.py", "*.txt"],
    exclude_patterns=["*.pyc", ".git/*", "node_modules/*"],
    preserve_structure=True  # Keep folder structure in metadata
)

# Import from Git repository
multi_importer.import_from_repository(
    svg_file="template.svg",
    repo_url="https://github.com/user/repo.git",
    output="repo_bundle.svg",
    branch="main",
    include_patterns=["docs/*", "src/*", "README.md"],
    max_file_size="10MB"
)
```

#### ZIP Archive Import
```python
# Import entire ZIP archive with structure preservation
zip_importer = svgg.ZipImporter()

# Import ZIP with full structure mapping
zip_importer.import_zip_archive(
    svg_file="template.svg",
    zip_path="project.zip",
    output="archive_bundle.svg",
    preserve_structure=True,
    metadata_detail_level="full"  # "basic", "detailed", "full"
)

# Import from ZIP URL
zip_importer.import_zip_from_url(
    svg_file="template.svg",
    zip_url="https://github.com/user/repo/archive/main.zip",
    output="github_bundle.svg",
    extract_patterns=["*.md", "*.py", "*.json"],
    max_files=100
)

# The resulting SVG will contain JSON metadata like:
{
    "archive_structure": {
        "name": "project.zip",
        "total_files": 25,
        "total_size": "2.5MB",
        "tree": {
            "src/": {
                "type": "directory",
                "files": [
                    {"name": "main.py", "size": "1.2KB", "type": "text/python"},
                    {"name": "utils.py", "size": "856B", "type": "text/python"}
                ]
            },
            "docs/": {
                "type": "directory", 
                "files": [
                    {"name": "README.md", "size": "3.4KB", "type": "text/markdown"},
                    {"name": "API.md", "size": "5.1KB", "type": "text/markdown"}
                ]
            },
            "README.md": {"size": "2.1KB", "type": "text/markdown"},
            "package.json": {"size": "445B", "type": "application/json"}
        }
    }
}
```

### 2. Metadata Management

#### Updating Metadata
```python
# Update metadata after import/export operations
metadata_manager = svgg.MetadataManager()

# Add metadata
metadata_manager.update_metadata(
    svg_file="bundle.svg",
    metadata={
        "files_count": 3,
        "last_modified": "2025-06-26T10:30:00Z",
        "creator": "SVGG v1.0.0",
        "description": "Document bundle with embedded files"
    }
)

# Update specific metadata fields
metadata_manager.update_field(
    svg_file="bundle.svg",
    field="last_access",
    value="2025-06-26T11:00:00Z"
)
```

#### Removing Metadata
```python
# Remove specific metadata fields
metadata_manager.remove_metadata(
    svg_file="bundle.svg",
    fields=["temp_data", "debug_info"]
)

# Remove all custom metadata (keep only essential)
metadata_manager.clean_metadata(
    svg_file="bundle.svg",
    keep_essential=True  # Keep: title, description, creator
)

# Complete metadata removal
metadata_manager.remove_all_metadata(
    svg_file="bundle.svg"
)
```

### 3. Changelog Generation

#### Automatic Changelog
```python
# Enable automatic changelog tracking
changelog = svgg.ChangelogManager()

# Start tracking changes
changelog.start_tracking("bundle.svg")

# Perform operations (automatically logged)
importer.import_file("bundle.svg", "new_doc.pdf", data_uri=True)
exporter.export_file("bundle.svg", "old_doc.pdf", remove_from_svg=True)
metadata_manager.update_metadata("bundle.svg", {"version": "1.1"})

# Generate changelog
changelog.generate_changelog(
    svg_file="bundle.svg",
    output_file="CHANGELOG.md",
    format="markdown"  # or "json", "xml"
)
```

### 4. Embedding Files

#### Single File Embedding
```python
import svgg

# Basic embedding
generator = svgg.SVGGenerator()
generator.embed(
    svg_file="base.svg",
    files="document.pdf",
    output="result.svg"
)

# With metadata
generator.embed(
    svg_file="base.svg", 
    files="document.pdf",
    output="result.svg",
    metadata={
        "title": "Invoice Document",
        "author": "Company Inc.",
        "created": "2025-06-26"
    }
)
```

#### Multiple Files Embedding
```python
# Embed multiple files
generator.embed(
    svg_file="template.svg",
    files=[
        "invoice.pdf",
        "logo.png", 
        "data.json",
        "styles.css"
    ],
    output="bundle.svg",
    compression=True  # Enable compression
)

# From directory
generator.embed_directory(
    svg_file="template.svg",
    directory="./assets/",
    patterns=["*.pdf", "*.png", "*.json"],
    output="bundle.svg"
)
```

### 2. Creating SVG from Scratch

```python
# Create new SVG with embedded content
creator = svgg.SVGCreator()

# Basic SVG creation
svg_content = creator.create(
    width=800,
    height=600,
    files=["document.pdf", "chart.png"],
    title="Document Bundle"
)

# Save to file
with open("created.svg", "w") as f:
    f.write(svg_content)

# Advanced creation with custom template
svg_content = creator.create_from_template(
    template="custom_template.svg",
    files=["data.json", "report.pdf"],
    variables={
        "title": "Monthly Report",
        "date": "2025-06-26"
    }
)
```

### 3. Extracting Content

```python
# Extract all files
extractor = svgg.SVGExtractor()
extracted_files = extractor.extract_all(
    svg_file="bundle.svg",
    output_dir="./extracted/"
)

# Extract specific file types
pdf_files = extractor.extract_by_type(
    svg_file="bundle.svg",
    file_types=[".pdf"],
    output_dir="./pdfs/"
)

# Extract single file
data = extractor.extract_file(
    svg_file="bundle.svg",
    filename="document.pdf"
)
# Returns file content as bytes
```

### 4. Information and Analysis

```python
# Get embedded files info
info = svgg.get_info("bundle.svg")
print(f"Files: {len(info.files)}")
print(f"Total size: {info.total_size} bytes")
print(f"Compression: {info.compression_ratio}%")

for file_info in info.files:
    print(f"- {file_info.name} ({file_info.size} bytes, {file_info.type})")

# Check if SVG has embedded content
has_content = svgg.has_embedded_content("document.svg")
print(f"Has embedded files: {has_content}")
```

## 🎛️ CLI Reference

### Global Options
```bash
svgg [command] [options]

Global Options:
  --verbose, -v     Enable verbose output
  --quiet, -q       Suppress output
  --help, -h        Show help
  --version         Show version
```

### Commands

#### `import` - Import files as base64 DATA URIs
```bash
svgg import <files...> --into <svg_file> [options]

Options:
  --into <file>          Target SVG file (required)
  --output <file>        Output SVG file (default: overwrites input)
  --data-uri             Convert to base64 DATA URI (default: true)
  --update-metadata      Update metadata after import
  --metadata <json>      Add custom metadata
  --from-url <url>       Import from URL instead of file

Examples:
  svgg import document.pdf --into template.svg --update-metadata
  svgg import *.pdf *.png --into base.svg --output bundle.svg
  svgg import --from-url https://example.com/doc.pdf --into template.svg
```

#### `export` - Export embedded files
```bash
svgg export <svg_file> [options]

Options:
  --output-dir <dir>     Output directory (default: ./exported/)
  --file <name>          Export specific file
  --type <ext>           Export files of specific type
  --remove               Remove files from SVG after export
  --update-metadata      Update metadata after removal
  --to-url <endpoint>    Upload to API endpoint
  --headers <json>       HTTP headers for URL upload

Examples:
  svgg export bundle.svg --output-dir ./files/ --remove
  svgg export bundle.svg --file document.pdf --remove --update-metadata
  svgg export bundle.svg --to-url https://api.example.com/upload --headers '{"Authorization":"Bearer token"}'
```

#### `metadata` - Manage SVG metadata
```bash
svgg metadata <svg_file> [options]

Options:
  --update <json>        Update metadata fields
  --remove <fields>      Remove specific fields (comma-separated)
  --clean               Remove all non-essential metadata
  --clear               Remove all metadata
  --show                Show current metadata

Examples:
  svgg metadata bundle.svg --show
  svgg metadata bundle.svg --update '{"version":"1.1","author":"John"}'
  svgg metadata bundle.svg --remove "temp_data,debug_info"
  svgg metadata bundle.svg --clean
```

#### `changelog` - Generate changelog
```bash
svgg changelog <svg_file> [options]

Options:
  --output <file>        Changelog output file (default: CHANGELOG.md)
  --format <type>        Output format: markdown, json, xml (default: markdown)
  --since <date>         Show changes since date (ISO format)
  --track                Start tracking changes for this SVG

Examples:
  svgg changelog bundle.svg --output CHANGES.md
  svgg changelog bundle.svg --format json --output changes.json
  svgg changelog bundle.svg --since 2025-06-01T00:00:00Z
```

#### `embed` - Embed files into existing SVG (Legacy)
```bash
svgg embed <files...> --into <svg_file> [options]

Options:
  --into <file>          Target SVG file (required)
  --output <file>        Output SVG file (default: overwrites input)
  --compress, -c         Enable compression
  --metadata <json>      Add metadata (JSON format)
  --base64-encode        Force base64 encoding

Examples:
  svgg embed document.pdf --into template.svg
  svgg embed *.pdf *.png --into base.svg --output bundle.svg --compress
  svgg embed data.json --into chart.svg --metadata '{"title":"Data Chart"}'
```

#### `create` - Create new SVG with embedded files
```bash
svgg create [options]

Options:
  --files <pattern>      Files to embed (glob pattern)
  --directory <dir>      Directory to embed
  --output <file>        Output SVG file (required)
  --template <file>      Use custom SVG template
  --width <pixels>       SVG width (default: 800)
  --height <pixels>      SVG height (default: 600)
  --title <text>         Document title

Examples:
  svgg create --files "*.pdf" --output bundle.svg
  svgg create --directory ./assets/ --output package.svg --title "Asset Bundle"
  svgg create --files "data/*" --template custom.svg --output result.svg
```

#### `extract` - Extract embedded files
```bash
svgg extract <svg_file> [options]

Options:
  --output-dir <dir>     Output directory (default: ./extracted/)
  --file <name>          Extract specific file
  --type <ext>           Extract files of specific type (.pdf, .png, etc.)
  --list, -l             Only list embedded files

Examples:
  svgg extract bundle.svg
  svgg extract document.svg --output-dir ./files/
  svgg extract bundle.svg --type .pdf --output-dir ./pdfs/
  svgg extract bundle.svg --file document.pdf
  svgg extract bundle.svg --list
```

#### `info` - Show embedded files information
```bash
svgg info <svg_file> [options]

Options:
  --json                 Output as JSON
  --files, -f            Show detailed file list
  --metadata, -m         Show metadata

Examples:
  svgg info bundle.svg
  svgg info document.svg --json
  svgg info package.svg --files --metadata
```

## 🔧 Configuration

### Configuration File
Create `svgg.config.json` in your project directory:

```json
{
  "compression": true,
  "default_template": "./templates/base.svg",
  "output_directory": "./output/",
  "metadata": {
    "generator": "SVGG",
    "version": "1.0.0"
  },
  "encoding": {
    "text_files": "utf-8",
    "binary_files": "base64"
  }
}
```

### Environment Variables
```bash
export SVGG_COMPRESSION=true
export SVGG_OUTPUT_DIR="./output/"
export SVGG_TEMPLATE="./template.svg"
```

## 🌐 URL/API Integration Solutions

### 1. Built-in API Server
```python
# Start SVGG API server
import svgg.server

# Basic server setup
server = svgg.server.SVGGServer(
    host="localhost",
    port=8080,
    auth_token="your-secret-token"
)

# Start server
server.run()

# API Endpoints:
# POST /api/import - Import files to SVG
# POST /api/export - Export files from SVG  
# GET  /api/info   - Get SVG information
# POST /api/metadata - Update metadata
# GET  /api/changelog - Get changelog
```

### 2. Cloud Storage Integration
```python
# AWS S3 Integration
s3_config = {
    "bucket": "my-svg-bucket",
    "region": "us-east-1",
    "access_key": "AKIAIOSFODNN7EXAMPLE",
    "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

# Import from S3
importer.import_from_s3(
    svg_file="template.svg",
    s3_key="documents/invoice.pdf",
    config=s3_config,
    output="result.svg"
)

# Export to S3
exporter.export_to_s3(
    svg_file="bundle.svg",
    filename="document.pdf",
    s3_key="exports/document.pdf",
    config=s3_config,
    remove_from_svg=True
)

# Google Drive Integration
drive_config = {
    "credentials_file": "credentials.json",
    "folder_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
}

# Import from Google Drive
importer.import_from_drive(
    svg_file="template.svg",
    file_id="1mGkl5Z8X9vN_example_id",
    config=drive_config,
    output="result.svg"
)
```

### 3. Webhook Integration
```python
# Setup webhooks for automatic processing
webhook_config = {
    "on_import": "https://api.example.com/webhooks/import",
    "on_export": "https://api.example.com/webhooks/export", 
    "on_metadata_change": "https://api.example.com/webhooks/metadata",
    "headers": {"Authorization": "Bearer token123"}
}

# Enable webhooks
svgg.configure_webhooks(webhook_config)

# Webhooks will be called automatically during operations
importer.import_file("template.svg", "doc.pdf")  # Triggers webhook
```

### 4. REST API Client
```python
# SVGG REST API Client
client = svgg.SVGGClient(
    base_url="https://api.svgg.cloud",
    api_key="your-api-key"
)

# Upload SVG and get ID
svg_id = client.upload_svg("local_file.svg")

# Import file from URL
client.import_from_url(
    svg_id=svg_id,
    url="https://example.com/document.pdf",
    filename="document.pdf"
)

# Export file to URL
client.export_to_url(
    svg_id=svg_id,
    filename="document.pdf",
    target_url="https://storage.example.com/upload"
)

# Download processed SVG
client.download_svg(svg_id, "processed_file.svg")
```

### 5. Docker Integration
```yaml
# docker-compose.yml
version: '3.8'
services:
  svgg-api:
    image: svgg/svgg-server:latest
    ports:
      - "8080:8080"
    environment:
      - SVGG_AUTH_TOKEN=your-secret-token
      - SVGG_STORAGE_TYPE=s3
      - AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
      - AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
```

```bash
# Start SVGG API server
docker-compose up -d

# Use API
curl -X POST http://localhost:8080/api/import \
  -H "Authorization: Bearer your-secret-token" \
  -F "svg=@template.svg" \
  -F "files=@document.pdf"
```

### 6. CDN Integration
```python
# CloudFlare/CDN integration
cdn_config = {
    "provider": "cloudflare",
    "zone_id": "your-zone-id",
    "api_token": "your-api-token",
    "domain": "cdn.example.com"
}

# Upload to CDN
cdn_url = exporter.export_to_cdn(
    svg_file="bundle.svg",
    filename="document.pdf",
    config=cdn_config,
    public=True,  # Make publicly accessible
    expiry_days=30
)

print(f"File available at: {cdn_url}")
```

## 📊 Advanced Examples

### Complete Workflow with URL Integration
```python
import svgg
from datetime import datetime, timedelta

# Initialize components
importer = svgg.SVGImporter()
exporter = svgg.SVGExporter()
metadata_manager = svgg.MetadataManager()
changelog = svgg.ChangelogManager()

# Start tracking
changelog.start_tracking("document_bundle.svg")

# Import from various sources
# 1. Local file
importer.import_file(
    svg_file="template.svg",
    file_path="local_document.pdf",
    output="bundle.svg",
    data_uri=True,
    update_metadata=True
)

# 2. From URL
importer.import_from_url(
    svg_file="bundle.svg",
    url="https://api.example.com/reports/monthly.pdf",
    output="bundle.svg",
    filename="monthly_report.pdf",
    headers={"Authorization": "Bearer token123"}
)

# 3. From cloud storage
importer.import_from_s3(
    svg_file="bundle.svg",
    s3_key="assets/logo.png",
    config=s3_config,
    output="bundle.svg"
)

# Update metadata
metadata_manager.update_metadata(
    svg_file="bundle.svg",
    metadata={
        "bundle_created": datetime.now().isoformat(),
        "files_count": 3,
        "sources": ["local", "api", "s3"],
        "version": "1.0.0"
    }
)

# Process and export
# Export specific file to API
exporter.export_to_url(
    svg_file="bundle.svg",
    filename="monthly_report.pdf",
    upload_url="https://processing.example.com/analyze",
    headers={"Content-Type": "application/pdf"},
    remove_after_upload=False  # Keep in SVG
)

# Export to multiple destinations
destinations = [
    {
        "type": "s3",
        "config": s3_config,
        "key": "processed/monthly_report.pdf"
    },
    {
        "type": "url",
        "url": "https://backup.example.com/upload",
        "headers": {"Authorization": "Bearer backup-token"}
    }
]

for dest in destinations:
    if dest["type"] == "s3":
        exporter.export_to_s3(
            svg_file="bundle.svg",
            filename="monthly_report.pdf",
            s3_key=dest["key"],
            config=dest["config"]
        )
    elif dest["type"] == "url":
        exporter.export_to_url(
            svg_file="bundle.svg", 
            filename="monthly_report.pdf",
            upload_url=dest["url"],
            headers=dest["headers"]
        )

# Clean up old files
files_to_remove = ["temp_data.json", "debug.log"]
for filename in files_to_remove:
    exporter.export_file(
        svg_file="bundle.svg",
        filename=filename,
        output_path=f"./temp/{filename}",
        remove_from_svg=True
    )

# Update metadata after cleanup
metadata_manager.update_metadata(
    svg_file="bundle.svg",
    metadata={
        "last_cleanup": datetime.now().isoformat(),
        "files_count": 1,  # Only monthly_report.pdf remains
        "version": "1.1.0"
    }
)

# Generate changelog
changelog.generate_changelog(
    svg_file="bundle.svg",
    output_file="CHANGELOG.md",
    format="markdown"
)

print("✅ Complete workflow finished!")
print(f"📄 Changelog saved to CHANGELOG.md")
print(f"📦 Final bundle: bundle.svg")
```

### Batch Processing with API Integration  
```python
import svgg
import asyncio
from pathlib import Path

async def process_svg_batch(svg_files, api_endpoints):
    """Process multiple SVG files with API integration"""
    
    client = svgg.SVGGClient(
        base_url="https://api.svgg.cloud",
        api_key="your-api-key"
    )
    
    results = []
    
    for svg_file in svg_files:
        try:
            # Upload SVG to cloud
            svg_id = await client.upload_svg_async(svg_file)
            
            # Import from multiple URLs
            for endpoint in api_endpoints:
                await client.import_from_url_async(
                    svg_id=svg_id,
                    url=endpoint["url"],
                    filename=endpoint["filename"],
                    headers=endpoint.get("headers", {})
                )
            
            # Process and export
            processed_svg = await client.process_svg_async(svg_id)
            
            # Export to different destinations
            export_tasks = [
                client.export_to_url_async(
                    svg_id=svg_id,
                    filename=file["name"],
                    target_url=file["destination"]
                )
                for file in processed_svg["embedded_files"]
            ]
            
            await asyncio.gather(*export_tasks)
            
            # Download final SVG
            final_svg = f"processed_{Path(svg_file).name}"
            await client.download_svg_async(svg_id, final_svg)
            
            results.append({
                "original": svg_file,
                "processed": final_svg,
                "svg_id": svg_id,
                "status": "success"
            })
            
        except Exception as e:
            results.append({
                "original": svg_file,
                "error": str(e),
                "status": "failed"
            })
    
    return results

# Usage
svg_files = ["doc1.svg", "doc2.svg", "doc3.svg"]
api_endpoints = [
    {
        "url": "https://api1.example.com/data.json",
        "filename": "api_data.json",
        "headers": {"Authorization": "Bearer token1"}
    },
    {
        "url": "https://api2.example.com/report.pdf", 
        "filename": "external_report.pdf",
        "headers": {"Authorization": "Bearer token2"}
    }
]

# Run batch processing
results = asyncio.run(process_svg_batch(svg_files, api_endpoints))

for result in results:
    if result["status"] == "success":
        print(f"✅ {result['original']} -> {result['processed']}")
    else:
        print(f"❌ {result['original']}: {result['error']}")
```

### Complete Project Import with Structure Preservation
```python
import svgg
from pathlib import Path

# Import entire project with full structure mapping
project_importer = svgg.ProjectImporter()

# Import local project directory
project_importer.import_project(
    svg_file="template.svg",
    project_path="./my-project/",
    output="project_bundle.svg",
    config={
        "include_patterns": ["*.py", "*.md", "*.json", "*.yaml", "*.txt"],
        "exclude_patterns": [
            "*.pyc", "__pycache__/*", ".git/*", 
            "node_modules/*", "venv/*", "*.log"
        ],
        "max_file_size": "5MB",
        "max_total_size": "50MB",
        "preserve_structure": True,
        "include_hidden": False,
        "generate_tree": True
    }
)

# Import from ZIP with detailed structure
zip_result = project_importer.import_zip_with_structure(
    svg_file="template.svg",
    zip_path="backup.zip",
    output="backup_bundle.svg",
    structure_detail="full"  # "basic", "detailed", "full"
)

# The resulting metadata will include complete directory tree:
print("Imported structure:")
print(f"📁 Total directories: {zip_result.stats.directories}")
print(f"📄 Total files: {zip_result.stats.files}")
print(f"💾 Total size: {zip_result.stats.total_size_human}")
print(f"🗂️ Structure: {zip_result.tree}")
```

### Batch Processing with Multiple Formats
```python
# Process multiple SVGs with different export formats
batch_processor = svgg.BatchProcessor()

svg_files = ["doc1.svg", "doc2.svg", "doc3.svg"]

# Export each SVG to multiple formats
for svg_file in svg_files:
    base_name = Path(svg_file).stem
    
    # Extract to HTML website
    batch_processor.extract_to_html(
        svg_file=svg_file,
        output_dir=f"./websites/{base_name}/",
        template="professional",
        include_viewer=True,
        responsive=True
    )
    
    # Export to DOCX
    batch_processor.extract_to_docx(
        svg_file=svg_file,
        output_file=f"./documents/{base_name}.docx",
        include_svg=True,
        extract_files=True
    )
    
    # Export to MHTML for archival
    batch_processor.extract_to_mhtml(
        svg_file=svg_file,
        output_file=f"./archives/{base_name}.mhtml",
        include_attachments=True
    )
    
    # Create ZIP of all embedded files
    batch_processor.export_to_zip(
        svg_file=svg_file,
        output_file=f"./zips/{base_name}_files.zip",
        preserve_structure=True
    )

print("✅ Batch processing completed!")
```

### Repository Import with Branch Selection
```python
# Import specific parts of a Git repository
repo_importer = svgg.RepositoryImporter()

# Import documentation from repository
repo_importer.import_from_git(
    svg_file="template.svg",
    repo_url="https://github.com/facebook/react.git",
    output="react_docs.svg",
    config={
        "branch": "main",
        "paths": ["docs/", "README.md", "CHANGELOG.md"],
        "file_patterns": ["*.md", "*.mdx"],
        "max_files": 100,
        "clone_depth": 1,  # Shallow clone
        "include_history": False
    }
)

# Import from multiple repositories
repos = [
    {
        "url": "https://github.com/user/frontend.git",
        "branch": "main",
        "paths": ["src/", "README.md"]
    },
    {
        "url": "https://github.com/user/backend.git", 
        "branch": "develop",
        "paths": ["api/", "docs/"]
    }
]

multi_repo_bundle = repo_importer.import_multiple_repos(
    svg_file="template.svg",
    repositories=repos,
    output="multi_repo_bundle.svg",
    merge_strategy="separate_directories"  # or "flat", "by_repo"
)
```

### Advanced File Filtering and Processing
```python
# Smart file filtering and processing during import
smart_importer = svgg.SmartImporter()

# Import with intelligent filtering
smart_importer.import_with_filters(
    svg_file="template.svg",
    source="./large-project/",
    output="filtered_bundle.svg",
    filters={
        "size_filters": {
            "max_file_size": "10MB",
            "max_total_size": "100MB"
        },
        "content_filters": {
            "text_files": {
                "encoding": "utf-8",
                "max_lines": 1000,
                "exclude_patterns": ["password", "secret", "api_key"]
            },
            "image_files": {
                "max_dimensions": "2048x2048",
                "compress": True,
                "formats": [".png", ".jpg", ".svg"]
            },
            "binary_files": {
                "allowed_types": [".pdf", ".zip", ".xlsx"],
                "scan_for_malware": True
            }
        },
        "metadata_filters": {
            "preserve_timestamps": True,
            "include_checksums": True,
            "track_origin": True
        }
    }
)

# Process files during import
smart_importer.import_with_processing(
    svg_file="template.svg",
    source="./documents/",
    output="processed_bundle.svg",
    processors={
        "*.md": "markdown_to_html",
        "*.py": "syntax_highlight",
        "*.pdf": "extract_text_preview",
        "*.xlsx": "extract_summary",
        "*.png": "generate_thumbnail"
    }
)
```
```python
import svgg
from datetime import datetime

# Create invoice bundle with PDF, logo, and data
generator = svgg.SVGGenerator()

invoice_data = {
    "invoice_number": "INV-2025-001",
    "date": datetime.now().isoformat(),
    "amount": "$1,234.56"
}

# Save invoice data as JSON
import json
with open("invoice_data.json", "w") as f:
    json.dump(invoice_data, f)

# Create bundle
generator.embed(
    svg_file="invoice_template.svg",
    files=[
        "invoice.pdf",
        "company_logo.png", 
        "invoice_data.json"
    ],
    output="invoice_bundle.svg",
    metadata={
        "title": f"Invoice {invoice_data['invoice_number']}",
        "type": "invoice",
        "date": invoice_data["date"]
    }
)
```

### Batch Processing
```python
import svgg
import os
from pathlib import Path

# Process multiple directories
generator = svgg.SVGGenerator()
base_template = "base_template.svg"

for project_dir in Path("./projects/").iterdir():
    if project_dir.is_dir():
        output_file = f"bundles/{project_dir.name}_bundle.svg"
        
        generator.embed_directory(
            svg_file=base_template,
            directory=str(project_dir),
            patterns=["*.pdf", "*.png", "*.json", "*.md"],
            output=output_file,
            metadata={
                "project": project_dir.name,
                "created": datetime.now().isoformat()
            }
        )
        print(f"Created bundle: {output_file}")
```

### Web Integration
```python
from flask import Flask, request, send_file
import svgg
import tempfile

app = Flask(__name__)

@app.route("/create-bundle", methods=["POST"])
def create_bundle():
    # Get uploaded files
    files = request.files.getlist("files")
    template = request.files.get("template")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded files
        file_paths = []
        for file in files:
            path = os.path.join(temp_dir, file.filename)
            file.save(path)
            file_paths.append(path)
        
        # Save template
        template_path = os.path.join(temp_dir, "template.svg")
        template.save(template_path)
        
        # Create bundle
        output_path = os.path.join(temp_dir, "bundle.svg")
        generator = svgg.SVGGenerator()
        generator.embed(
            svg_file=template_path,
            files=file_paths,
            output=output_path
        )
        
        return send_file(output_path, as_attachment=True)
```

## 🧪 Testing

```python
import svgg
import tempfile
import os

def test_embed_and_extract():
    # Create test data
    test_content = b"Test PDF content"
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        test_pdf = os.path.join(temp_dir, "test.pdf")
        with open(test_pdf, "wb") as f:
            f.write(test_content)
        
        template_svg = os.path.join(temp_dir, "template.svg")
        with open(template_svg, "w") as f:
            f.write('<svg><rect width="100" height="100"/></svg>')
        
        # Embed
        output_svg = os.path.join(temp_dir, "output.svg")
        generator = svgg.SVGGenerator()
        generator.embed(
            svg_file=template_svg,
            files=[test_pdf],
            output=output_svg
        )
        
        # Extract
        extract_dir = os.path.join(temp_dir, "extracted")
        extractor = svgg.SVGExtractor()
        extracted = extractor.extract_all(output_svg, extract_dir)
        
        # Verify
        assert len(extracted) == 1
        assert extracted[0].name == "test.pdf"
        
        with open(os.path.join(extract_dir, "test.pdf"), "rb") as f:
            assert f.read() == test_content

if __name__ == "__main__":
    test_embed_and_extract()
    print("✅ All tests passed!")
```

## 🔍 Error Handling and Validation

```python
import svgg
from svgg.exceptions import (
    SVGGError, FileNotFoundError, InvalidSVGError, 
    ImportError, ExportError, MetadataError,
    StructureError, CompressionError
)

def robust_svgg_operations():
    """Example of robust error handling in SVGG operations"""
    
    try:
        # Import with validation
        importer = svgg.SmartImporter()
        result = importer.import_with_validation(
            svg_file="template.svg",
            source="./documents/",
            output="bundle.svg",
            validation_config={
                "check_file_integrity": True,
                "scan_for_malware": True,
                "validate_encoding": True,
                "check_size_limits": True
            }
        )
        
        if result.warnings:
            print("⚠️ Import warnings:")
            for warning in result.warnings:
                print(f"  - {warning}")
        
        # Export with error recovery
        exporter = svgg.SVGExporter()
        exporter.export_with_recovery(
            svg_file="bundle.svg",
            output_dir="./exported/",
            recovery_config={
                "skip_corrupted": True,
                "create_error_log": True,
                "fallback_encoding": "utf-8"
            }
        )
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e.filename}")
        print(f"   Expected location: {e.expected_path}")
        
    except InvalidSVGError as e:
        print(f"❌ Invalid SVG file: {e.svg_file}")
        print(f"   Validation errors: {e.validation_errors}")
        
    except ImportError as e:
        print(f"❌ Import failed: {e.source}")
        print(f"   Reason: {e.reason}")
        print(f"   Failed files: {e.failed_files}")
        
    except ExportError as e:
        print(f"❌ Export failed: {e.target}")
        print(f"   Partial results: {e.partial_results}")
        
    except MetadataError as e:
        print(f"❌ Metadata error: {e.operation}")
        print(f"   Invalid fields: {e.invalid_fields}")
        
    except StructureError as e:
        print(f"❌ Structure error: {e.structure_type}")
        print(f"   Conflicts: {e.conflicts}")
        
    except CompressionError as e:
        print(f"❌ Compression error: {e.algorithm}")
        print(f"   Original size: {e.original_size}")
        
    except SVGGError as e:
        print(f"❌ General SVGG error: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        # Create error report
        svgg.create_error_report(
            error=e,
            context="robust_operations",
            output_file="error_report.json"
        )

def validate_before_processing():
    """Validate files and structure before processing"""
    
    validator = svgg.SVGValidator()
    
    # Validate SVG file
    validation_result = validator.validate_svg("input.svg")
    
    if not validation_result.is_valid:
        print("❌ SVG validation failed:")
        for error in validation_result.errors:
            print(f"  - {error.code}: {error.message}")
        return False
    
    # Validate embedded files
    file_validation = validator.validate_embedded_files("input.svg")
    
    if file_validation.corrupted_files:
        print("⚠️ Corrupted embedded files found:")
        for file_info in file_validation.corrupted_files:
            print(f"  - {file_info.name}: {file_info.error}")
    
    # Validate structure metadata
    structure_validation = validator.validate_structure("input.svg")
    
    if not structure_validation.is_consistent:
        print("⚠️ Structure inconsistencies found:")
        for inconsistency in structure_validation.inconsistencies:
            print(f"  - {inconsistency}")
    
    return True

# Example usage
if __name__ == "__main__":
    if validate_before_processing():
        robust_svgg_operations()
    else:
        print("❌ Validation failed, skipping processing")
```

## 📊 Performance Tips

- Use compression for large files: `compression=True`
- Process files in batches for better memory usage
- Use specific file patterns to avoid unnecessary files
- Enable verbose mode for debugging: `--verbose`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Create the future of document bundling! 🚀**


