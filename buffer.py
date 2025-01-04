import os, cv2, queue, threading, time

# bufferless VideoCapture
class MyVideoCapture:
  def __init__(self, name):
    self.isReady = False
    self.cap = None
    self.connStr = name
    self.q = queue.Queue()
    self.t = None
    self.t = threading.Thread(target=self._reader)
    self.t.daemon = True
    self.t.start()
    
  def Open(self, name):
    self.connStr = name
    self.cap = cv2.VideoCapture(
        self.connStr,
        apiPreference=cv2.CAP_ANY,
        params=[cv2.CAP_PROP_READ_TIMEOUT_MSEC, 1000, cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 1000],  # 1 second
    )
        # Проверяем, открыта ли камера
    if not self.cap.isOpened():
      print("Не удалось открыть видеокамеру")
      self.isReady = False
    else:
      print("Видеокамера открыта успешно")
      self.isReady = True 

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      if (self.isReady):
        ret, frame = self.cap.read()
        if not ret:
          break
        if not self.q.empty():
          try:
            self.q.get_nowait()   # discard previous (unprocessed) frame
          except queue.Empty:
            pass
        self.q.put(frame)

  def read(self):
    return self.q.get()
  
connStr = "rtsp://admin:6m8vw@192.168.37.3:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
camera = MyVideoCapture(connStr)
camera.Open(connStr)

while True:
  time.sleep(0.01)   # simulate time between events
  frame = camera.read()
  # Определение нового размера
  new_width = int(frame.shape[1] * 0.5)  # Уменьшение ширины до 50%
  new_height = int(frame.shape[0] * 0.5)  # Уменьшение высоты до 50%

  # Изменение размера кадра
  resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

  # 1. Средний фильтр
  blurred = cv2.blur(resized_frame, (5, 5))

  # 2. Гауссовское размытие
  gaussian_blurred = cv2.GaussianBlur(resized_frame, (5, 5), 0)

  # 3. Медианный фильтр
  median_blurred = cv2.medianBlur(resized_frame, 5)

  # 4. Билатеральное размытие
  bilateral_blurred = cv2.bilateralFilter(resized_frame, 9, 75, 75)

  cv2.imshow("frame", resized_frame)
  # cv2.imshow("frame2", gaussian_blurred)
  
  if chr(cv2.waitKey(1)&255) == 'q':
      break