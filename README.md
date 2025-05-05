```markdown
# Panorama Stitching Application

## Description

This is a desktop application developed in Python that generates a panoramic image from a video file. It extracts multiple frames from the video, stitches them together using OpenCV's stitching algorithm, removes unnecessary black borders, and presents a simple graphical user interface built with PyQt5.

## Features

- Extracts frames from video (default: 50 frames)
- Automatically detects video orientation (landscape or portrait)
- Stitches images using OpenCV
- Automatically crops black borders
- Simple and intuitive PyQt5 GUI

## Project Structure

```

Panorama\_Project/
├── main.py                  # Main application file
├── src/
│   └── utils.py             # Utility functions for frame extraction, stitching, and cropping
├── outputs/                 # Output folder for stitched panorama images
├── data/                    # Input video folder
└── requirements.txt         # Python dependencies

````

## Installation

1. Clone the repository:

```bash
git clone git@github.com:yourusername/Panorama_Project.git
cd Panorama_Project
````

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the main Python script to launch the GUI:

```bash
python main.py
```

Follow the on-screen instructions to load a video file and generate a stitched panorama.

## Dependencies

* Python 3.8 or higher
* OpenCV (`opencv-python`)
* NumPy
* PyQt5

You can manually install them with:

```bash
pip install opencv-python numpy pyqt5
```

## Output

The final stitched panorama image will be saved in the `outputs/` directory.

## Future Improvements

* Allow manual selection of keyframes
* Support multiple stitching backends or tuning parameters
* Add export options for different image formats
* Improve cropping accuracy
* Add drag-and-drop support in the GUI
