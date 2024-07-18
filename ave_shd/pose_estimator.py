import cv2 as cv
import numpy as np
import time
from ave_shd.util import calculate_mean_coords

#摄像头选择
k=1

BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

def calculate_mean_coords(coords):
    if not coords:
        return None
    return np.mean(coords, axis=0)

def collect_and_average_shoulder_positions(duration=10, width=368, height=368, thr=0.2):
    """
    收集指定时间内的左右肩位置数据并计算均值。
    :param duration: 数据收集的持续时间（秒）
    :param width: 输入图像的宽度
    :param height: 输入图像的高度
    :param thr: 阈值值用于姿态部分的热图
    :return: (lsd, rsd, eyes_dis) 左右肩的平均位置和双眼的平均距离
    """
    # 初始化变量
    ls_coords = []  # 存储左肩坐标
    rs_coords = []  # 存储右肩坐标
    eyes_distances = []  # 存储双眼距离
    start_time = time.time()  # 开始时间

    # 设置摄像头
    cap = cv.VideoCapture(k)  # 0 使用默认摄像头

    net = cv.dnn.readNetFromTensorflow("graph_opt.pb")

    while True:
        hasFrame, frame = cap.read()
        if not hasFrame:
            break

        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        net.setInput(cv.dnn.blobFromImage(frame, 1.0, (width, height), (127.5, 127.5, 127.5), swapRB=True, crop=False))
        out = net.forward()
        out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

        points = []
        for i in range(len(BODY_PARTS)):
            heatMap = out[0, i, :, :]
            _, conf, _, point = cv.minMaxLoc(heatMap)
            x = (frameWidth * point[0]) / out.shape[3]
            y = (frameHeight * point[1]) / out.shape[2]
            points.append((int(x), int(y)) if conf > thr else None)

        lshoulder_coord = points[BODY_PARTS["LShoulder"]] if points[BODY_PARTS["LShoulder"]] else None
        rshoulder_coord = points[BODY_PARTS["RShoulder"]] if points[BODY_PARTS["RShoulder"]] else None
        reye_coord = points[BODY_PARTS["REye"]] if points[BODY_PARTS["REye"]] else None
        leye_coord = points[BODY_PARTS["LEye"]] if points[BODY_PARTS["LEye"]] else None

        current_time = time.time()
        elapsed_time = current_time - start_time

        # 如果当前时间在指定时间内，收集数据
        if elapsed_time < duration:
            if lshoulder_coord:
                ls_coords.append(lshoulder_coord)
            if rshoulder_coord:
                rs_coords.append(rshoulder_coord)
            if reye_coord and leye_coord:
                # 计算双眼距离并存储
                eyes_distance = np.linalg.norm(np.array(reye_coord) - np.array(leye_coord))
                eyes_distances.append(eyes_distance)
        else:
            break

    # 计算均值
    lsd = np.round(np.round(calculate_mean_coords(ls_coords))) if ls_coords else None
    rsd = np.round(np.round(calculate_mean_coords(rs_coords))) if rs_coords else None
    eyes_dis_mean = np.round(np.mean(eyes_distances)) if eyes_distances else None

    # 关闭摄像头
    cap.release()

    return lsd, rsd, eyes_dis_mean
