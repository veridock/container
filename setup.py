#!/usr/bin/env python3
"""
SVGG - SVG Generator
Setup script for package installation
"""

from setuptools import setup, find_packages
import os
import re

# Read version from version.py
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'svgg', 'version.py')
    with open(version_file, 'r', encoding='utf-8') as f:
        content = f.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")

# Read long description from README.md
def get_long_description():
    readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_file):
        with open(readme_file, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

# Read requirements
def get_requirements():
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_file):
        with open(requirements_file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

def get_dev_requirements():
    dev_requirements_file = os.path.join(os.path.dirname(__file__), 'requirements-dev.txt')
    if os.path.exists(dev_requirements_file):
        with open(dev_requirements_file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="svgg",
    version=get_version(),
    author="SVGG Development Team",
    author_email="dev@svgg.org",
    description="SVG Generator - Universal tool for creating enhanced SVG files with embedded content",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/svgg/svgg",
    project_urls={
        "Documentation": "https://svgg.readthedocs.io/",
        "Source": "https://github.com/svgg/svgg",
        "Tracker": "https://github.com/svgg/svgg/issues",
        "Changelog": "https://github.com/svgg/svgg/blob/main/CHANGELOG.md",
    },
    packages=find_packages(exclude=["tests*", "examples*", "docs*"]),
    include_package_data=True,
    package_data={
        "svgg": [
            "templates/*.svg",
            "templates/website/*.html",
            "templates/website/assets/css/*.css",
            "templates/website/assets/js/*.js",
            "templates/website/assets/images/*",
            "config/*.json",
            "config/*.conf",
        ],
    },
    python_requires=">=3.8",
    install_requires=get_requirements(),
    extras_require={
        "dev": get_dev_requirements(),
        "server": ["flask>=2.0.0", "fastapi>=0.68.0", "uvicorn>=0.15.0"],
        "cloud": ["boto3>=1.20.0", "google-cloud-storage>=2.0.0"],
        "docs": ["sphinx>=4.0.0", "sphinx-rtd-theme>=1.0.0"],
        "testing": ["pytest>=6.0.0", "pytest-cov>=3.0.0", "pytest-mock>=3.6.0"],
    },
    entry_points={
        "console_scripts": [
            "svgg=svgg.cli.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Archiving :: Packaging",
        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Utilities",
    ],
    keywords="svg, vector, graphics, embedding, base64, documents, archive, bundle, web, export",
    license="MIT",
    zip_safe=False,
)