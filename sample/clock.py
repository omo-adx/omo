import time
import datetime
import threading

# 闹钟功能
def set_alarm(alarm_time):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Current time: {current_time}")
    print(f"Alarm is set for {alarm_time}")

    while True:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if current_time == alarm_time:
            print("Wake up! It's time!")
            break
        time.sleep(1)

# 倒计时功能
def countdown_timer(seconds):
    print(f"Countdown timer set for {seconds} seconds")
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1
    print("Time's up!")

# 日程安排功能
def schedule_event(event_time, event_name):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Current time: {current_time}")
    print(f"Event '{event_name}' is scheduled for {event_time}")

    event_time_obj = datetime.datetime.strptime(event_time, "%Y-%m-%d %H:%M:%S")
    
    while True:
        current_time = datetime.datetime.now()
        if current_time >= event_time_obj:
            print(f"Event '{event_name}' is starting now!")
            break
        time.sleep(1)



