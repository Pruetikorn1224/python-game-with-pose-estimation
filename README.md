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
To play this game, run this command
```bash
python exercise.py
```

## How to Play
In game scene, there is a yellow block \[ Player \] at the center of screen with 2 swords \[ weapon \] on both sides. 

In camera view, it accesses through webcamera to detect body. There are 2 horizontal lines placing at one-third and two-third of screen's height.

As the time passes, there will be poles of lava \[ obstacle \] coming from both sides. User have to move player up and down to avoid hitting obstacle. The program will detect vertical position of user's shoulders. If user moves shoulder above upper red line, player will move up 1 block. On the other hands, players will go down 1 block when user moves below lower line.


https://github.com/Pruetikorn1224/python-game-with-pose-estimation/assets/60211633/503a5b02-480f-49ee-9f9d-fd34be9e4c54


Moreover, there will be red spheres \[ enemy \] coming from both sides and player has to avoid them too. They will be destroyed by weapons. User can control weapons by using arm. The program detects angles from the shoulders to the wrists.

User can change the speed of enemys and obstacles by pressing number *1 - 5* to determine level. The speed will be faster as the level is higher.

## Reference
1.  IlvisFaulbaums, 3d Body Visualisation From Video, \( July 16, 2021 \), GitHub repository, https://github.com/IlvisFaulbaums/3dVisualisationFromVideo
2.  Texture from - [Minecraft](https://www.minecraft.net/en-us)
3.  Model from - [Blender3D](https://sketchfab.com/3d-models/minecraft-diamond-sword-2fd7a88f5bd44d728c2bbdd8dfc27f99)
