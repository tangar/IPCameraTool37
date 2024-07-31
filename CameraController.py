from onvif import ONVIFCamera

# Функция для управления зумом
def set_zoom(ptz_service, profile_token, zoom_level):
    # get absoluteMove request -- requesta
    requesta = ptz_service.create_type('AbsoluteMove')
    requesta.ProfileToken = profile_token
    if requesta.Position is None:
        requesta.Position = ptz_service.GetStatus(
            {'ProfileToken': profile_token}).Position
    if requesta.Speed is None:
        requesta.Speed = ptz_service.GetStatus(
            {'ProfileToken': profile_token}).Position
        
    requesta.Position.Zoom.x = zoom_level
    requesta.Speed.Zoom.x = 1
    ret = ptz_service.AbsoluteMove(requesta)

class CameraController:
    def __init__(self):
        # Параметры камеры
        self.CAMERA_HOST = '198.0.100.108'  # IP адрес камеры
        self.CAMERA_PORT = 80               # Порт камеры
        self.CAMERA_USER = 'admin'          # Имя пользователя
        self.CAMERA_PASS = '6m8vw'       # Пароль



        self.connected = False
        self.zoom_level = 0
        self.focus_level = 0
        self.iris_level = 0
    
    def Connect(self):
        # Подключение к камере
        self.camera = ONVIFCamera(self.CAMERA_HOST, self.CAMERA_PORT, self.CAMERA_USER, self.CAMERA_PASS)

        # Получение медиасервиса камеры
        self.media_service = self.camera.create_media_service()

        # Получение профилей камеры
        self.profiles = self.media_service.GetProfiles()
        self.profile_token = self.profiles[0].token
        
        # Получение PTZ сервиса камеры
        self.ptz_service = self.camera.create_ptz_service()
        
        self.connected = True
        print("Camera connected")
    
    def ZoomHandler(self, pos):
        if self.connected:
            self.zoom_level = pos
            print(f"Zoom set to {pos}")
            set_zoom(self.ptz_service, self.profile_token, self.zoom_level)
        else:
            print("Camera not connected")
    
    def FocusHandler(self, pos):
        if self.connected:
            self.focus_level = pos
            print(f"Focus set to {pos}")
        else:
            print("Camera not connected")
    
    def IrisHandler(self, pos):
        if self.connected:
            self.iris_level = pos
            print(f"Iris set to {pos}")
        else:
            print("Camera not connected")
    
    def PhotoHandler(self):
        if self.connected:
            print("Photo taken")
        else:
            print("Camera not connected")

