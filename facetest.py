import cv2
from face_detect import detect_largest_face
import numpy as np

# 初始化摄像头
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    face_coordinates = detect_largest_face(frame)
    if face_coordinates:
        x, y = face_coordinates
        print(f"Face detected at (x: {x}, y: {y})")  # 打印中心坐标
        cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)  # 在图像上标记中心点
        
        eye_radius = 100  # 眼睛半径
        # 确保眼睛坐标在画布范围内，并转换为整数
        left_eye_x = int(max(eye_radius, min(x - 2.5 * eye_radius, frame.shape[1] - eye_radius)))
        left_eye_y = int(max(eye_radius, min(y, frame.shape[0] - eye_radius)))
        right_eye_x = int(max(eye_radius, min(x + 2.5 * eye_radius, frame.shape[1] - eye_radius)))
        right_eye_y = int(max(eye_radius, min(y, frame.shape[0] - eye_radius)))
        
        # 绘制左眼
        cv2.circle(frame, (left_eye_x, left_eye_y), eye_radius, (255, 0, 0), 10)
        # 绘制右眼
        cv2.circle(frame, (right_eye_x, right_eye_y), eye_radius, (255, 0, 0), 10)
    
    # 创建一个纯黑色的背景
    black_background = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    
    # 将眼睛的图像叠加到纯黑色背景上
    black_background[left_eye_y - eye_radius:left_eye_y + eye_radius,
                    left_eye_x - eye_radius:left_eye_x + eye_radius] = frame[left_eye_y - eye_radius:left_eye_y + eye_radius,
                                                                              left_eye_x - eye_radius:left_eye_x + eye_radius]
    black_background[right_eye_y - eye_radius:right_eye_y + eye_radius,
                    right_eye_x - eye_radius:right_eye_x + eye_radius] = frame[right_eye_y - eye_radius:right_eye_y + eye_radius,
                                                                                  right_eye_x - eye_radius:right_eye_x + eye_radius]
    
    # 显示结果
    cv2.imshow('Face Detection', black_background)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
