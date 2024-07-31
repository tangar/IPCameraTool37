from onvif import ONVIFCamera

# Параметры камеры
CAMERA_HOST = '198.0.100.108'  # IP адрес камеры
CAMERA_PORT = 80               # Порт камеры
CAMERA_USER = 'admin'          # Имя пользователя
CAMERA_PASS = '6m8vw'       # Пароль

# Подключение к камере
camera = ONVIFCamera(CAMERA_HOST, CAMERA_PORT, CAMERA_USER, CAMERA_PASS)

# Получение медиасервиса камеры
media_service = camera.create_media_service()

# Получение профилей камеры
profiles = media_service.GetProfiles()
profile_token = profiles[0].token

# Получение PTZ сервиса камеры
ptz_service = camera.create_ptz_service()

# Функция для управления зумом
def set_zoom(ptz_service, profile_token, zoom_level):
    # Создание команды для управления зумом
    ptz_request = ptz_service.create_type('ContinuousMove')
    ptz_request.ProfileToken = profile_token
    ptz_request.Velocity = ptz_service.GetStatus({'ProfileToken': profile_token}).Position
    ptz_request.Velocity.Zoom = {'x': zoom_level}
    
    # Выполнение команды
    ptz_service.ContinuousMove(ptz_request)

# Пример установки уровня зума
zoom_level = 0.5  # Уровень зума от -1.0 до 1.0
set_zoom(ptz_service, profile_token, zoom_level)

# Остановка движения камеры
ptz_service.Stop({'ProfileToken': profile_token})
