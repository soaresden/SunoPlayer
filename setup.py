#!/usr/bin/env python3
"""
Setup script for Suno Music Player
Allows installation via: pip install suno-music-player
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="suno-music-player",
    version="1.0.0",
    description="A beautiful desktop app to browse, play and download your Suno.ai music",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Denis",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/suno-music-player",
    license="MIT",
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Players",
    ],
    
    python_requires=">=3.8",
    
    py_modules=["main", "auth", "api"],
    
    install_requires=[
        "PyQt5>=5.15.0",
        "pygame>=2.5.0",
        "pystray>=0.19.0",
        "Pillow>=10.0.0",
        "requests>=2.31.0",
        "selenium>=4.15.0",
        "PyJWT>=2.8.0",
    ],
    
    entry_points={
        "console_scripts": [
            "suno-player=main:main",
        ],
    },
    
    keywords=[
        "suno",
        "music",
        "player",
        "ai-music",
        "desktop",
        "pyqt5",
    ],
    
    project_urls={
        "Bug Reports": "https://github.com/yourusername/suno-music-player/issues",
        "Documentation": "https://github.com/yourusername/suno-music-player/wiki",
        "Source Code": "https://github.com/yourusername/suno-music-player",
    },
)
