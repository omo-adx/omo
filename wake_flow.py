import subprocess
import cv2
import numpy as np
from playvideo import videoshow
import time
from face_detect import detect_largest_face

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




# 模拟按下 'q' 键
d = 500

# 运行时间的变量
#run_time   # 例如，运行5秒后退出

# 初始化摄像头
#cap = cv2.VideoCapture(1)

#frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#print(f"Camera frame width: {frame_width}")
#print(f"Camera frame height: {frame_height}")

# 定义一个函数来处理摄像头和视频播放
def wake(run_time):
    cap = cv2.VideoCapture(1)
    start_time = time.time()
    while time.time() - start_time < run_time:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        face_coordinates = detect_largest_face(frame)
        if face_coordinates:
            x, y = face_coordinates
            print(f"Face detected at (x: {x}, y: {y})")
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            
            if x < d:
                videoshow(Look_right, 1)
                videoshow(eye_blinking_right,1)
            elif x >= 1280 - d:
                videoshow(Look_left, 1)
                videoshow(eye_blinking_left,1)
            else:
                videoshow(eye_blinking_middle, 1)
        
        # 显示结果
        # cv2.imshow('Face Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# 调用函数并传入运行时间
#process_video(run_time)
