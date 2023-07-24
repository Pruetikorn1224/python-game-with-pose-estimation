import cv2 
import mediapipe as mp
import math

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
        shoulder_y = (lefts[1] + rights[1])/2

    return right_angle, left_angle, shoulder_y

showBody = True
left_a = 0
right_a = 0
shoulder_y = 0

cap = cv2.VideoCapture(1)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened:
        ret, frame = cap.read()

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

        if showBody:
            mp_drawing.draw_landmarks(
                        frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=3, circle_radius=2))

        cv2.putText(frame, f"Left Angle: {int(left_a)}", (20, 850), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,255), 3)
        cv2.putText(frame, f"Right Angle: {int(right_a)}", (20, 950), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,255), 3)

        cv2.imshow('Body Pose Estimation', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

