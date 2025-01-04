import time, cv2
from MyVideoCapture import MyVideoCapture
  
connStr = "rtsp://admin:6m8vw@192.168.37.3:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
camera = MyVideoCapture(connStr)
camera.Open(connStr)

while True:
  time.sleep(0.05)   # simulate time between events
  frame = camera.read()
  # Определение нового размера
  new_width = int(frame.shape[1] * 0.2)  # Уменьшение ширины до 50%
  new_height = int(frame.shape[0] * 0.2)  # Уменьшение высоты до 50%

  # Изменение размера кадра
  resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

  cv2.imshow("frame", resized_frame)
  
  if chr(cv2.waitKey(1)&255) == 'q':
      break