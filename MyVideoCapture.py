import datetime
import cv2, queue, threading

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
        params=[cv2.CAP_PROP_READ_TIMEOUT_MSEC, 2000, cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 2000],  # 1 second
    )
        # Проверяем, открыта ли камера
    if not self.cap.isOpened():
      print("Не удалось открыть видеокамеру")
      self.isReady = False
    else:
      print("Видеокамера открыта успешно")
      self.isReady = True 
    
  def Close(self):
    self.isReady = False
    self.cap = cv2.VideoCapture.release()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      try:
        if (self.isReady):
          success, frame = self.cap.read()
          if not success:
            break
          if not self.q.empty():
            try:
              self.q.get_nowait()   # discard previous (unprocessed) frame
            except queue.Empty:
              pass
          self.q.put(frame)
      except:
        print(f"{datetime.now().strftime('%H:%M:%S')} || Failed to connect to camera, exception was thrown")  # wont run


  def read(self):
    return self.q.get()