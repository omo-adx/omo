import pygame

def playsound(audio_path, play_times):
    # 初始化pygame的音频模块
    pygame.mixer.init()

    # 加载音频文件
    pygame.mixer.music.load(audio_path)

    # 循环播放音频指定次数
    for _ in range(play_times):
        # 播放音频
        pygame.mixer.music.play()

        # 等待音频播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    # 关闭pygame的音频模块
    pygame.mixer.quit()
