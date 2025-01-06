import datetime
import cv2, queue, threading

# bufferless VideoCapture
class MyVideoCapture:
  def __init__(self, name, timeout_ms):
    self.isReady = False
    self.cap = None
    self.connStr = name
    self.q = queue.Queue()
    self.t = None
    self.t = threading.Thread(target=self._reader)
    self.t.daemon = True
    self.t.start()
    self.timeout = timeout_ms
  
  def SetConnStr(self, conn):
    self.connStr = conn

  def Open(self):
    if (self.connStr != None):
      # доработка для открытия встроенных видеокамер
      if(isinstance(self.connStr, str)) :
        self.cap = cv2.VideoCapture(
          self.connStr,
          apiPreference=cv2.CAP_ANY,
          params=[cv2.CAP_PROP_READ_TIMEOUT_MSEC, self.timeout, cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, self.timeout],  # 1 second
        )
      else:
        self.cap = cv2.VideoCapture(self.connStr)  
      # Проверяем, открыта ли камера
      if not self.cap.isOpened():
        print("Не удалось открыть видеокамеру")
        self.isReady = False
      else:
        print("Видеокамера открыта успешно")
        self.isReady = True 
    
  def Release(self):
    self.isReady = False
    self.cap.release()
    print("End of Release")

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
        current_dateTime = datetime.datetime.now()
        print(current_dateTime + "Failed to connect to camera, exception was thrown")  # wont run


  def read(self):
    try:
      return self.q.get()
    except:
      return None