import cv2
import numpy as np

def videoshow(video_path, play_times):
    # 使用OpenCV打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 检查视频是否成功打开
    if not cap.isOpened():
        #print("WRONG")
        return

    # 获取视频的宽度和高度
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 获取显示器的分辨率
    screen_width = 1920  # 示例宽度，替换为您的显示宽度
    screen_height = 1080  # 示例高度，替换为您的显示高度

    # 创建一个全屏窗口
    cv2.namedWindow('OMO', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('OMO', screen_width, screen_height)

    # 创建一个黑色背景的图像
    black_screen = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

    # 循环播放视频指定次数
    for _ in range(play_times):
        # 重置视频到开始位置
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # 循环读取视频帧
        while True:
            # 读取一帧
            ret, frame = cap.read()

            # 如果读取成功，显示帧
            if ret:
                # 如果视频分辨率与屏幕分辨率不匹配，可以在此处调整视频大小
                frame = cv2.resize(frame, (screen_width, screen_height))
                cv2.imshow('OMO', frame)

            

            else:
                # 视频播放完毕，显示黑屏
                cv2.imshow('OMO', black_screen)
                break  # 如果用户按下'q'键，则退出循环
            # 如果按下'q'键，则退出循环
            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit()
                
            

    # 释放视频捕获对象
    cap.release()
    # 关闭所有OpenCV窗口（这个调用现在被注释掉，因为窗口将保持打开状态）
    # cv2.destroyAllWindows()

# 调用函数播放视频
videoshow('path_to_your_video.mp4', play_times=1)
