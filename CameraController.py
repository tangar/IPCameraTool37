from onvif import ONVIFCamera



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
        
        # get ZOOM absoluteMove request -- requesta
        self.requesta = self.ptz_service.create_type('AbsoluteMove')
        self.requesta.ProfileToken = self.profile_token
        if self.requesta.Position is None:
            self.requesta.Position = self.ptz_service.GetStatus(
                {'ProfileToken': self.profile_token}).Position
        if self.requesta.Speed is None:
            self.requesta.Speed = self.ptz_service.GetStatus(
                {'ProfileToken': self.profile_token}).Position
            
        #init focus etc
        self.vstoken = self.media_service.GetVideoSources()[0].token
        self.imaging_service = self.camera.create_imaging_service()
        self.img_settings = self.imaging_service.GetImagingSettings({'VideoSourceToken': self.vstoken})
        self.move_focus_request = self.imaging_service.create_type('Move')
        self.move_focus_request.VideoSourceToken = self.vstoken

        #set exp to auto
        self.img_settings.Exposure.Mode = 'AUTO'
        self.imaging_service.SetImagingSettings({'VideoSourceToken': self.vstoken, 'ImagingSettings':self.img_settings})

        self.connected = True
        print("Camera connected")
    

    # Функция для управления зумом
    def set_zoom(self, pos):
        self.requesta.Position.Zoom.x = pos
        self.requesta.Speed.Zoom.x = 1
        ret = self.ptz_service.AbsoluteMove(self.requesta)


    def FocusMode(self, autoMode):
        if autoMode == 1:
            print("Focus mode set to AUTO")
            self.img_settings.Focus.AutoFocusMode = 'AUTO'
            self.imaging_service.SetImagingSettings({'VideoSourceToken': self.vstoken, 'ImagingSettings':self.img_settings})
        elif autoMode == 0:
            print("Focus mode set to MANUAL")
            self.img_settings.Focus.AutoFocusMode = 'MANUAL'
            self.imaging_service.SetImagingSettings({'VideoSourceToken': self.vstoken, 'ImagingSettings':self.img_settings})

    def ZoomHandler(self, pos):
        if self.connected:
            self.zoom_level = pos
            print(f"Zoom set to {pos}")
            self.set_zoom(pos)
        else:
            print("Camera not connected")
    
    def FocusHandler(self, pos):
        if self.connected:
            self.focus_level = pos
            speed = 1
            print(f"Focus set to {pos}")
            fc2 = {'Absolute':{'Position':pos, 'Speed':speed}}
            self.imaging_service.Move({'VideoSourceToken': self.move_focus_request.VideoSourceToken, 'Focus': fc2})
            #self.imaging_service.Stop({'VideoSourceToken': self.move_focus_request.VideoSourceToken})
        else:
            print("Camera not connected")
    
    def IrisHandler(self, pos):
        if self.connected:
            self.iris_level = pos
            self.img_settings.Exposure.Iris = pos
            self.imaging_service.SetImagingSettings({'VideoSourceToken': self.vstoken, 'ImagingSettings':self.img_settings})
            self.img_settings = self.imaging_service.GetImagingSettings({'VideoSourceToken': self.vstoken})
            print(f"Iris set to {pos}")
        else:
            print("Camera not connected")
    
    def PhotoHandler(self):
        if self.connected:
            print("Photo taken")
        else:
            print("Camera not connected")

