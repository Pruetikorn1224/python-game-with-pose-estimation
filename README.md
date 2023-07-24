# Python Game with Pose Estimation
A python game developed with Ursina Engine Library and implemented with Mediapipe's pose estimation framework

## Introduction
The project's purpose is to develop an exercise game by using computer and camera, or without additional equipment. It is inconvinient to have another hardware components to exercise since it costs more and is hard to apply. The main programming language is Python with [Mediapipe](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/python) to detect body movement, and [Ursina](https://www.ursinaengine.org/documentation.html) to create game environment.

## Installation
This program is developed by Python

It is not necessary to install virtual environment; however, it is better to run this program in separated environment
```bash
# Install virtual environment
pip install virtualenv
```
Download this repository and build virtual environment
```bash
# Download git repository
git clone https://github.com/Pruetikorn1224/python-game-with-pose-estimation.git <file_name>
cd <file_name>

# Build virtual environment
python -m venv <environment_name>
source <environment_name>/bin/activate

# Install libraries
pip install requirements.txt
```
