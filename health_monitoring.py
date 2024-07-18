import cv2 as cv
import numpy as np
import argparse
#import os
import time
import subprocess
from playvideo  import videoshow
#from face_detect import detect_largest_face
#from wake_flow import wake
import tkinter as tk
from playvoice import playsound

drink = 'voice/喝水.mp3'
close = 'voice/近距离提示.mp3'
move = 'voice/运动.mp3'
sit = 'voice/坐姿.mp3'


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

videoshow(loading,1)


#摄像头选择
k=1
#坐姿容差d1
d1 = 35
#屏幕距离容差
d2 = 35
#久坐时间设置t1
t1 = 30
#靠近屏幕太近时间设置t2
t2 = 5
#停止时间
t3 = 60

longst=0

import sys

sys.path.append('C:/Users/24572/Desktop/OMO_PY')  # 将 ave_shd 包的路径添加到 sys.path

import ave_shd

# 使用 ave_shd 包中的函数
lsd, rsd, eyes_dis_mean = ave_shd.collect_and_average_shoulder_positions(duration=8)
print(f"Left Shoulder Mean: {lsd}")
print(f"Right Shoulder Mean: {rsd}")

if rsd is None:
    print('please try again.')
    exit()
if lsd is None:
    print('please try again.')
    exit()
else:
    dsd = lsd[1] - rsd[1]
    des_sd = np.abs(dsd)
    print('mean different ', des_sd)

print(f" eyes_dis_Mean: {eyes_dis_mean}")


parser = argparse.ArgumentParser()
parser.add_argument('--input', help='Path to image or video. Skip to capture frames from camera')
parser.add_argument('--thr', default=0.2, type=float, help='Threshold value for pose parts heat map')
parser.add_argument('--width', default=368, type=int, help='Resize input to specific width.')
parser.add_argument('--height', default=368, type=int, help='Resize input to specific height.')

args = parser.parse_args()

BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

inWidth = args.width
inHeight = args.height

net = cv.dnn.readNetFromTensorflow("graph_opt.pb")
#控制帧率 
frame_rate_limit = 60
wait_time = int(1000 / frame_rate_limit)


#启动外摄
cap = cv.VideoCapture(k)
# 初始化帧计数器
frame_count = 0


# Initialize a timer to track the last time both hips were detected
last_hips_detected_time = time.time()
eyes_distance_too_large_start_time = None

#time stop
stop_wait_time = t3
stop_start_time = time.time()

while cv.waitKey(1) < 0:
    
    hasFrame, frame = cap.read()
    if not hasFrame:
        cv.waitKey()
        break

    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    
    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    out = net.forward()
    out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

    assert(len(BODY_PARTS) == out.shape[1])

    points = []
    for i in range(len(BODY_PARTS)):
        heatMap = out[0, i, :, :]
        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]
        points.append((int(x), int(y)) if conf > args.thr else None)

    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]
        if points[idFrom] and points[idTo]:
            cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

    nose_id = BODY_PARTS["Nose"]
    nose_coord = points[nose_id]
    lshoulder_id = BODY_PARTS["LShoulder"]
    lshoulder_coord = points[lshoulder_id]
    rshoulder_id = BODY_PARTS["RShoulder"]
    rshoulder_coord = points[rshoulder_id]

    # 在计算肩部差值时，确保 rsd 不是 None
    if lshoulder_coord is not None and rshoulder_coord is not None:
        ndsd = lshoulder_coord[1] - rshoulder_coord[1]
        tnds = np.abs(ndsd)
 
        if tnds:
            cv.putText(frame, f"D-value: {tnds}", (20, 120), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)
        if des_sd + d1 <= tnds:  #偏差阈值暂定
            videoshow(shacking_eye,1)##############pesition###########
            playsound(sit,1)
            cv.putText(frame, f"SITTNG POSITION WORNING !!!", (20, 200), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)
            print("worning!")
    else:
        print("Shoulder coordinates not detected.")
        tnds = None


    if nose_coord:
        cv.putText(frame, f"Nose: {nose_coord}", (20, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)
    if lshoulder_coord:
        cv.putText(frame, f"LShoulder: {lshoulder_coord}", (20, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)
    if rshoulder_coord:
        cv.putText(frame, f"RShoulder: {rshoulder_coord}", (20, 90), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)
    if tnds:
        cv.putText(frame, f"D-value: {tnds}", (20, 120), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)

    print(f"Nose: {nose_coord}")      
    print(f"Lshoulder: {lshoulder_coord}") 
    print(f"Rshoulder: {rshoulder_coord}") 
################################################################longsit###########################################
    hips_detected = False
    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            if partFrom == "RHip" or partTo == "RHip" or partFrom == "LHip" or partTo == "LHip":
                hips_detected = True
            cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

    if hips_detected:
        last_hips_detected_time = time.time()

    current_time = time.time()
    longst = current_time - last_hips_detected_time
    print("long_sit_time",longst)
    if current_time - last_hips_detected_time > t1:
        videoshow(water_notice,1)#########################################longsit##############################
        playsound(move,1)
        playsound(drink,1)

        cv.putText(frame, 'Time to get up and move around!', (20, 300), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)
#######################################################eyes_distance_too_close_to_screem#########################################################
    # 计算两个眼睛之间的距离
    reye_id = BODY_PARTS["REye"]
    reye_coord = points[reye_id]
    leye_id = BODY_PARTS["LEye"]
    leye_coord = points[leye_id]

    if reye_coord and leye_coord:
        eyes_distance = np.sqrt((reye_coord[0] - leye_coord[0]) ** 2 + (reye_coord[1] - leye_coord[1]) ** 2)
        if eyes_dis_mean:
            cv.putText(frame, f"eyes_dis: {eyes_distance}", (20, 150), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)
        # 检查眼睛距离是否超过平均值d2
        if eyes_distance > eyes_dis_mean + d2:
            cv.putText(frame, 'Eyes too close ', (20, 360), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)
            # 如果是第一次超过，则记录开始时间
            if eyes_distance_too_large_start_time is None:
                eyes_distance_too_large_start_time = time.time()
            # 检查是否已经超过t2秒
            elif time.time() - eyes_distance_too_large_start_time > t2:
                videoshow(distance_notice,1)#################################################distance##############
                playsound(close,1)
                cv.putText(frame, 'Eyes too close to screen for too long!', (20, 390), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)
        else:
            # 如果眼睛距离不再超过平均值50，则重置开始时间
            eyes_distance_too_large_start_time = None

############################################################################################################################################
    t, _ = net.getPerfProfile()
    freq = cv.getTickFrequency() / 1000
    cv.putText(frame, '%.2fms' % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    #cv.imshow('OpenPose using OpenCV', frame)
    videoshow(eye_blinking_middle,1)
    if time.time() - stop_start_time >= stop_wait_time:
        exit()
    if cv.waitKey(wait_time) & 0xFF == ord('q'):
        break



'''
     #保存画面到 'test' 文件夹
    frame_filename = os.path.join(directory, f"frame_{frame_count}.jpg")
    cv.imwrite(frame_filename, frame)
    frame_count += 1
'''

