import subprocess
import cv2
import numpy as np
from playvideo  import videoshow
import time
from wake_flow import wake
import tkinter as tk
import os
from playvoice import playsound

#音频路径
drink = 'voice/喝水.mp3'
close = 'voice/近距离提示.mp3'
move = 'voice/运动.mp3'
sit = 'voice/坐姿.mp3'
start = 'voice/开场.mp3'

subprocess.Popen(['python', 'a.py'])

# 视频文件的路径
logo_animation = 'video/logo animation.mp4'
eye_opening = 'video/eye opening.mp4'
eye_wink = 'video/eye_wink.mp4'
intro_standby = 'video/intro_standby.mp4'
loading = 'video/loading.mp4'
distance_notice = 'video/distance_notice.mp4'
look_down = 'video/look_down.mp4'
Look_left = 'video/Look_left.mp4'
Look_right = 'video/Look_right.mp4'
Look_up = 'video/Look_up.mp4'
shacking_eye = 'video/shacking_eye.mp4'
toched_head = 'video/toched_head.mp4'
water_notice = 'video/water_notice.mp4'
eye_blinking_up= 'video/eye_blinking_up.mp4'
eye_blinking_right = 'video/eye_blinking_right.mp4'
eye_blinking_middle = 'video/eye_blinking_middle.mp4'
eye_blinking_left = 'video/eye_blinking_left.mp4'
eye_blinking_down= 'video/eye_blinking_down.mp4'
Alarm_loop = 'video/Alarm_loop.mp4'
Alarm_intro = 'video/Alarm_intro.mp4'
standby_loop = 'video\standby_loop.mp4'


videoshow(logo_animation,1)
playsound(start,1)
videoshow(loading,1)
videoshow(eye_opening,1)


wake(10)
videoshow(intro_standby,1)




# Global variable to simulate environment variable
v = 0

# Function to simulate button press
def on_button_press(number):
    global v
    v = number
    print(f"Button {number} pressed. Environment variable 'v' changed to {number}.")

# Function to check the value of 'v' and play videos accordingly
def check_and_play_video():
    global v
    if v == 0:
        videoshow(standby_loop, 1)
    elif v == 1:
        wake(10)
        print (v)
        v = 0
    elif v == 2:
        subprocess.Popen(['python', 'health_monitoring.py'])
        subprocess.call(['python', 'health_monitoring.py'])
        v = 0  # Reset the value of 'v' after processing
    elif v == 3:
        videoshow(logo_animation,1)
        v = 0
    elif v == 4:
        videoshow(eye_opening,1)
        v = 0
    elif v == 5:
        videoshow(eye_wink,1)
        v = 0
    elif v == 6:
        videoshow(intro_standby,1)
        v = 0
    elif v == 7:
        videoshow(distance_notice,1)
        v = 0
    elif v == 8:
        videoshow(look_down,1)
        v = 0
    elif v == 9:
        videoshow(Look_left,1)
        v = 0
    elif v == 10:
        videoshow(Look_right,1)
        v = 0
    elif v == 11:
        videoshow(Look_up,1)
        v = 0
    elif v == 12:
        videoshow(shacking_eye,1)
        v = 0
    elif v == 13:
        videoshow(water_notice,1)
        v = 0
    elif v == 14:
        videoshow(eye_blinking_up,1)
        v = 0
    elif v == 15:
        videoshow(eye_blinking_right,1)
        v = 0
    elif v == 16:
        videoshow(eye_blinking_middle,1)
        v = 0
    elif v == 17:
        videoshow(eye_blinking_left,1)
        v = 0
    elif v == 18:
        videoshow(eye_blinking_down,1)
        v = 0
    elif v == 19:
        videoshow(Alarm_loop,1)
        v = 0
    elif v == 20:
        videoshow(Alarm_intro,1)
        v = 0
    elif v == 21:
        videoshow(standby_loop,1)
        v = 0
    elif v == 22:
        videoshow(logo_animation,1)
        v = 0
    # Schedule the next check
    root.after(1000, check_and_play_video)  # Check every 1000 milliseconds (1 second)

# Creating the main window
root = tk.Tk()
root.title("Digital Buttons")

# Creating buttons from 0 to 10
for i in range(22):
    button = tk.Button(root, text=str(i), command=lambda i=i: on_button_press(i))
    button.pack(side=tk.LEFT, padx=5, pady=5)

# Schedule the first video check
root.after(1000, check_and_play_video)

# Starting the GUI loop
root.mainloop()





'''
# 初始化摄像头
cap = cv2.VideoCapture(1)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Camera frame width: {frame_width}")
print(f"Camera frame height: {frame_height}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    face_coordinates = detect_largest_face(frame)
    if face_coordinates:
        x, y = face_coordinates
        print(f"Face detected at (x: {x}, y: {y})")
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
    if x<=d:
        videoshow(Look_right,1)
    if x>=1280-d:
        videoshow(Look_left,1)
    else:
        videoshow(eye_opening,1)

    #cv2.imshow('Face Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()

subprocess.Popen(['python', 'under_video.py'])
time.sleep(1)
videoshow(logo_animation,1)

videoshow(Look_left,1)
videoshow(Look_right,1)
videoshow(Look_left,1)
videoshow(Look_right,1)
videoshow(Look_left,1)
videoshow(Look_right,1)
videoshow(look_down,2)

videoshow(Look_left,2)

videoshow(intro_standby,1)

# 使用Popen启动另一个Python脚本
#subprocess.Popen(['python', 'health_monitoring.py'])

# 或者使用call等待脚本执行完毕
#subprocess.call(['python', 'health_monitoring.py'])
#print("已退出健康检测")
'''