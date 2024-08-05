from onvif import ONVIFCamera


class CameraController:
    def __init__(self,
                 CAMERA_HOST='198.0.100.108',
                 CAMERA_PORT=80,
                 CAMERA_USER='admin',
                 CAMERA_PASS='6m8vw'):
        # Подключение к камере
        self.camera = ONVIFCamera(CAMERA_HOST, CAMERA_PORT, CAMERA_USER, CAMERA_PASS)
        # Получение медиасервиса камеры
        self.media_service = self.camera.create_media_service()
        # Получение профилей камеры
        self.profiles = self.media_service.GetProfiles()
        self.profile_token = self.profiles[0].token
        # Получение PTZ сервиса камеры
        self.ptz_service = self.camera.create_ptz_service()

        self.request_abs = self.get_zoom_request()
        self.vs_token = self.media_service.GetVideoSources()[0].token
        self.imaging_service = self.camera.create_imaging_service()
        self.img_settings = self.imaging_service.GetImagingSettings({'VideoSourceToken': self.vs_token})
        self.move_focus_request = self.imaging_service.create_type('Move')

        self.connected = False
        self.zoom_level = 0
        self.focus_level = 0
        self.iris_level = 0

    # get ZOOM absoluteMove request
    def get_zoom_request(self):
        request_abs = self.ptz_service.create_type('AbsoluteMove')
        request_abs.ProfileToken = self.profile_token
        if request_abs.Position is None:
            request_abs.Position = self.ptz_service.GetStatus(
                {'ProfileToken': self.profile_token}).Position
        if request_abs.Speed is None:
            request_abs.Speed = self.ptz_service.GetStatus(
                {'ProfileToken': self.profile_token}).Position
        return request_abs

    # def set_zoom(self, zoom_level):
    #     self.zoom_level = zoom_level
    #     ptz_request = self.ptz_service.create_type('ContinuousMove')
    #     ptz_request.ProfileToken = self.profile_token
    #     ptz_request.Velocity = self.ptz_service.GetStatus({'ProfileToken': self.profile_token}).Position
    #     ptz_request.Velocity.Zoom = {'x': zoom_level}
    #
    #     self.ptz_service.ContinuousMove(ptz_request)

    def connect(self):
        self.move_focus_request.VideoSourceToken = self.vs_token

        # set exp to auto
        self.img_settings.Exposure.Mode = 'AUTO'
        self.imaging_service.SetImagingSettings(
            {'VideoSourceToken': self.vs_token, 'ImagingSettings': self.img_settings})
        self.connected = True
        # print("Camera connected")

    def validate_value(self, value):
        if value < 0:
            value = 0
        if value > 1:
            value = 1
        return value

    # Управление зумом
    def set_zoom(self, pos):
        self.request_abs.Position.Zoom.x = self.validate_value(pos)
        self.request_abs.Speed.Zoom.x = 1
        self.ptz_service.AbsoluteMove(self.request_abs)

    def focus_mode(self, auto_mode=False):
        if auto_mode:
            print("Focus mode set to AUTO")
            self.img_settings.Focus.AutoFocusMode = 'AUTO'
        else:
            print("Focus mode set to MANUAL")
            self.img_settings.Focus.AutoFocusMode = 'MANUAL'

        self.imaging_service.SetImagingSettings(
            {'VideoSourceToken': self.vs_token, 'ImagingSettings': self.img_settings}
        )

    def zoom_handler(self, pos):
        if self.connected:
            pos = self.validate_value(pos)
            self.zoom_level = pos
            print(f"Zoom set to {pos}")
            self.set_zoom(pos)
        else:
            print("Camera not connected")

    def focus_handler(self, pos, speed=1):
        if self.connected:
            pos = self.validate_value(pos)
            self.focus_level = pos
            print(f"Focus set to {pos}")
            fc2 = {'Absolute': {'Position': pos, 'Speed': speed}}
            self.imaging_service.Move({'VideoSourceToken': self.move_focus_request.VideoSourceToken, 'Focus': fc2})
            # self.imaging_service.Stop({'VideoSourceToken': self.move_focus_request.VideoSourceToken})
        else:
            print("Camera not connected")

    def iris_handler(self, pos):
        if self.connected:
            pos = self.validate_value(pos)
            self.iris_level = pos
            self.img_settings.Exposure.Iris = pos
            self.imaging_service.SetImagingSettings(
                {'VideoSourceToken': self.vs_token, 'ImagingSettings': self.img_settings})
            self.img_settings = self.imaging_service.GetImagingSettings({'VideoSourceToken': self.vs_token})
            print(f"Iris set to {pos}")
        else:
            print("Camera not connected")

    def photo_handler(self):
        if self.connected:
            print("Photo taken")
        else:
            print("Camera not connected")
