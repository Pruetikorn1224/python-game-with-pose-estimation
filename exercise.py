from ursina import *
import cv2
import mediapipe as mp
import math
import numpy as np

# Generate map at the beginning
def MapInitialize():
    # Background
    Entity(
        model = 'quad',
        scale = 15,
        z = .1,
        texture = './components/background.jpeg'
        )
    # Ground - Roof
    x = np.arange(-7, 8, dtype=int)
    y = [-4, 4]
    for j in y:
        for k in x:
            Entity(
                model='cube', 
                texture = './components/wooden.jpeg',
                x = k, 
                y = j
                )

# Restart game after game over
def ResetGame():
    global diff_e, diff_o, level, gameOver, entities

    gameOver = False
    level = 1
    diff_e = 0
    diff_o = 0

    player = Player(playerSpeed)
    entities.append(player)
    # Left Sword entity
    sword1 = Weapon(player=player, side="left", speed=weaponSpeed)
    entities.append(sword1)
    # Right Sword entity
    sword2 = Weapon(player=player, side="right", speed=weaponSpeed)
    entities.append(sword2)

# Calculate angle and position from the shoulders
def BodyCalculation(landmarks, hSize):
    rights = [
        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y
    ]
    lefts = [
        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y
    ]

    left_angle = 0
    right_angle = 0
    shoulder_y = hSize

    if lefts != [] or rights != []:
        radians = math.atan2(lefts[1]-lefts[3], lefts[2]-lefts[0])
        left_angle = math.degrees(radians)
        radians = math.atan2(rights[1]-rights[3], rights[0] - rights[2])
        right_angle = math.degrees(radians)
        shoulder_y = (lefts[1] + rights[1]) * 540

    return right_angle, left_angle, shoulder_y

# Define Player class
class Player(Entity):
    def __init__(self, speed):
        super().__init__()
        self.model = 'cube'
        self.color = color.yellow
        self.scale = 0.8
        self.position = (0, 0, 0)
        self.texture = 'white_cube'
        self.collider = 'box'
        self.y_pos = 0
        self.speed = speed
        self.limits = ["up", "center", "down"]
        self.behavior = self.limits[1]
        self.prebehavior = self.limits[1]
    
    def update(self):
        global gameOver, shoulder_y

        hit_info = self.intersects()
        if hit_info.hit:
            gameOver = True

        self.behavior = self.limits[int(shoulder_y/360)]  
        if self.prebehavior == "center" and self.behavior == "up" and self.y < 2:
            self.y_pos += 1
        if self.prebehavior == "center" and self.behavior == "down" and self.y > -2:
            self.y_pos -= 1
        self.prebehavior = self.behavior

        if self.y_pos != 0:
            self.y += self.y_pos
            self.y_pos = 0

# Define Weapon class
class Weapon(Entity):
    def __init__(self, player, side, speed):
        super().__init__()
        self.model = "./components/model/DiamondSword.obj"
        self.texture = "./components/model_texture/Diffuse.png"
        self.scale = .025
        self.rotation_x = 90
        self.collider = 'box'
        self.angle = 0
        self.radius = 1.5
        self.player = player
        self.side = side
        self.speed = speed

        if self.side == "left":
            self.position = (-self.radius, 0, 0)
        elif self.side == "right":
            self.position = (self.radius, 0, 0)
            self.rotation_z = 180
    
    def update(self):
        global enemies, left_a, right_a

        hit_info = self.intersects()
        if hit_info.hit and hit_info.entity in enemies:
            destroy(hit_info.entity)

        if self.side == "left":
            self.x = -math.cos(math.radians(left_a)) * self.radius 
            self.y = (math.sin(math.radians(left_a)) * self.radius) + self.player.y
        elif self.side == "right":
            self.angle += held_keys['e'] * time.dt * self.speed
            self.angle -= held_keys['d'] * time.dt * self.speed
            self.x = math.cos(math.radians(right_a)) * self.radius
            self.y = (math.sin(math.radians(right_a)) * self.radius) + self.player.y

# Define Enemy class
class Enemy(Entity):
    def __init__(self, speed, pos_x, pos_y):
        super().__init__()
        self.model = 'sphere'
        self.color = color.red
        self.collider = 'box'
        self.position = (pos_x, pos_y, 0)
        self.scale = .75
        self.speed = speed
        self.dir_x = 0 - pos_x
        self.dir_y = random.randint(-2, 2) - pos_y
    
    def update(self):
        self.x += self.dir_x * time.dt * self.speed
        self.y += self.dir_y * time.dt * self.speed
        if self.x > 8 or self.x < -8 or self.y > 4 or self.y < -4:
            destroy(self)

# Define Obstacle class
class Obstacle(Entity):
    def __init__(self, speed, pos_x, pos_y):
        super().__init__()
        self.model = 'cube'
        self.texture = './components/lava.jpeg'
        self.collider = 'box'
        self.position = (pos_x, pos_y, 0)
        self.side = pos_x
        self.speed = speed

    def update(self):
        if self.side < 0:
            self.x += self.speed * time.dt
        else:
            self.x -= self.speed * time.dt
        
        if self.x > 8 or self.x < -8:
            destroy(self)

# Define Text class
class LevelText(Button):
    def __init__(self, level):
        super().__init__(
            position = (.45, .35),
            origin = (0, 0),
            scale = (Text.size * 2, Text.size),
            color = color.red,
            text = "text"
        )
        self.text_entity.scale *= 2
        self.value = level
        self.text_entity.text = f'Level: {self.value}'

# Turn on webcamera and start an app
cap = cv2.VideoCapture(1)
app = Ursina()

# Define mediapipe pose solution
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

MapInitialize()

# Draw body skeleton on screen
showBody = True
# The angle of left arm
left_a = 0
# The angle of right arm
right_a = 0
# The position y of shoulders
shoulder_y = 0

# Every Entity in scene
entities = []
# Every Enemy in scene
enemies = []

# Game state
gameOver = False
# Define level difficulty
level = 1
# Define time generating enemy
diff_e = 0
# Define time generating obstacle
diff_o = 0

# Player speed
playerSpeed = 10
# Weapon speed
weaponSpeed = 60

# Player entity
player = Player(playerSpeed)
entities.append(player)
# Left Sword entity
sword1 = Weapon(player=player, side="left", speed=weaponSpeed)
entities.append(sword1)
# Right Sword entity
sword2 = Weapon(player=player, side="right", speed=weaponSpeed)
entities.append(sword2)

# Text showing level
txt = LevelText(level)
# Game Over UI
game_text = Text(text="Game Over", color=color.red, scale=4, x=-.25, y=.2)
b_reset = Button(text="Restart", color=color.azure, scale=.2, y=-.1, on_click=ResetGame)

# Update function
def update():
    global diff_e, diff_o, level, gameOver, entities, enemies, right_a, left_a, shoulder_y
    rate = level * 20

    ret, frame = cap.read()

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        # Make detection
        results = pose.process(image)
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            right_a, left_a, shoulder_y = BodyCalculation(landmarks, frame.shape[0]/2)
        except:
            pass

    cv2.line(frame, (0, 360), (1980, 360), (0,0,255), 2)
    cv2.line(frame, (0, 720), (1980, 720), (0,0,255), 2)

    cv2.imshow("Exercise Game", frame)

    if not gameOver:
        game_text.enabled = False
        b_reset.enabled = False

        diff_e += time.dt
        diff_o += time.dt
        if random.randint(1, 100) <= rate and diff_e > 2:
            xPos = random.choice([-8, 8])
            yPos = random.randint(-3, 3)

            xDir = random.random()
            if xPos > 0: xDir *= -1
            yDir = random.random()
            if yPos > 0: yDir *= -1

            enemy = Enemy(speed=level * .6, pos_x=xPos, pos_y=yPos)
            enemies.append(enemy)
            entities.append(enemy)
            diff_e = 0
        
        if random.randint(1, 100) <= rate and diff_o > 6:
            init_x = random.choice([-8, 8])
            blank = random.choice([-2, -1, 0, 1, 2])

            for i in range(7):
                if i - 3 != blank:
                    obstacle = Obstacle(speed=level, pos_x=init_x, pos_y=i-3)
                    entities.append(obstacle)
            diff_o = 0
    
    else:
        for ent in entities:
            destroy(ent)
        game_text.enabled = True
        b_reset.enabled = True

def input(key):
    global level

    if key == '1':
        level = 1
    if key == '2':
        level = 2
    if key == '3':
        level = 3
    if key == '4':
        level = 4
    if key == '5':
        level = 5
    txt.text_entity.text = f'Level: {level}'

window.center_on_screen = True
window.fps_counter.enabled = True

app.run()