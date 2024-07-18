# face_detection.py

import cv2

def detect_largest_face(image):
    """
    Detects the largest face in the image and returns its center coordinates.
    
    Parameters:
    image (numpy.ndarray): The input image.
    
    Returns:
    tuple: (x, y) coordinates of the center of the largest face, or None if no face is found.
    """
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    max_area = 0
    max_face = None
    for (x, y, w, h) in faces:
        area = w * h
        if area > max_area:
            max_area = area
            max_face = (x, y, w, h)

    if max_face:
        x, y, w, h = max_face
        center_x = x + w // 2
        center_y = y + h // 2
        return center_x, center_y
    else:
        return None
