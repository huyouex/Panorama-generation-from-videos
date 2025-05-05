```markdown
# Panorama Stitching Application

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15-purple)

A Python-based desktop application for creating panoramic images from videos, featuring automatic frame extraction, orientation detection, and intelligent stitching.

## Features

- 📹 Video frame extraction (50 keyframes by default)
- 📐 Automatic video orientation detection (landscape/portrait)
- 🖼️ Image stitching using OpenCV Stitcher
- ✂️ Automatic black border cropping
- 🖥️ PyQt5 graphical interface

## Installation

### Prerequisites
- Python 3.8+
- OpenCV with contrib modules

### Setup
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```
1. Click "Open Video" to select a video file (.mp4/.avi)
2. Adjust settings if needed
3. Click "Generate Panorama"
4. Result will be saved in `outputs/` directory

## Project Structure
```
Panorama_Project/
├── main.py                  # Main application entry
├── src/
│   └── utils.py             # Image processing utilities
├── outputs/                 # Generated panoramas
├── data/                    # Input videos
└── requirements.txt         # Dependency list
```
