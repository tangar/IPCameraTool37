import json

class CameraConfig:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        
        # Значения по умолчанию
        self.default_config = {
            "rtsp_url_main": "rtsp://admin:6m8vw@198.0.100.108:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
            "rtsp_url_second": "rtsp://admin:6m8vw@198.0.100.108:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
            "CAMERA_HOST": "198.0.100.108",
            "CAMERA_PORT": 80,
            "CAMERA_USER": "admin",
            "CAMERA_PASS": "6m8vw",
            "savePath": "./Frames"
        }
        
        # Загрузка конфигурации
        self.load_config()

    def load_config(self):
        """Загружает конфигурацию из файла JSON или использует значения по умолчанию."""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                print(f"Конфигурация успешно загружена из {self.config_file}")
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Ошибка: не удалось загрузить файл конфигурации {self.config_file}. Используются значения по умолчанию.")
            config = self.default_config

        # Применение параметров
        self.rtsp_url_main = config.get("rtsp_url_main", self.default_config["rtsp_url_main"])
        self.rtsp_url_second = config.get("rtsp_url_second", self.default_config["rtsp_url_second"])
        self.CAMERA_HOST = config.get("CAMERA_HOST", self.default_config["CAMERA_HOST"])
        self.CAMERA_PORT = config.get("CAMERA_PORT", self.default_config["CAMERA_PORT"])
        self.CAMERA_USER = config.get("CAMERA_USER", self.default_config["CAMERA_USER"])
        self.CAMERA_PASS = config.get("CAMERA_PASS", self.default_config["CAMERA_PASS"])
        self.savePath = config.get("savePath", self.default_config["savePath"])

    def save_config(self):
        """Сохраняет текущие параметры в файл JSON."""
        config = {
            "rtsp_url_main": self.rtsp_url_main,
            "rtsp_url_second": self.rtsp_url_second,
            "CAMERA_HOST": self.CAMERA_HOST,
            "CAMERA_PORT": self.CAMERA_PORT,
            "CAMERA_USER": self.CAMERA_USER,
            "CAMERA_PASS": self.CAMERA_PASS,
            "savePath": self.savePath
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            print(f"Конфигурация успешно сохранена в {self.config_file}")
        except IOError as e:
            print(f"Ошибка при сохранении конфигурации в {self.config_file}: {e}")