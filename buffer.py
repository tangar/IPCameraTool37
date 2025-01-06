import time, cv2
from MyVideoCapture import MyVideoCapture
  
def CloseConn(cam:MyVideoCapture):
  print("Отключение камеры")
  cam.Release()
  cv2.destroyAllWindows()
  print("End of CloseConn")

# connStr = "rtsp://admin:6m8vw@192.168.37.3:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
connStr = 0
camera = MyVideoCapture(connStr, 2000)
camera.Open()

while True:
  time.sleep(0.05)   # simulate time between events
  if(camera.isReady == False):
    break
  
  frame = camera.read()
  # Определение нового размера
  new_width = int(frame.shape[1] * 0.2)  # Уменьшение ширины дой50%
  new_height = int(frame.shape[0] * 0.2)  # Уменьшение высоты до 50%

  # Изменение размера кадра
  resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

  cv2.imshow("frame", resized_frame)
  
  ch = chr(cv2.waitKey(1)&255)
  if ((ch == 'q') or (ch == 'é')):
    break
  
CloseConn(camera)