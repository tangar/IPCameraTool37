import json

# "second_rtsp_url": "rtsp://192.168.37.4:554/11",

class CameraConfig:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        
        self.controller_ip = None
        self.controller_port_tx = None
        self.controller_port_rx = None
        self.main_ip = None
        self.main_rtsp_url = None
        self.second_ip = None
        self.second_rtsp_url = None
        self.CAMERA_HOST = None
        self.CAMERA_PORT = None
        self.CAMERA_USER = None
        self.CAMERA_PASS = None
        self.SAVE_PATH = None

        # rtsp://admin:admin@198.0.100.109:554/stream0

        self.default_config = {
            "controller_ip": "192.168.37.2",
            "controller_port_tx": 9999,
            "controller_port_rx": 9998,
            "main_ip": "192.168.37.3",
            "second_ip": "192.168.37.4",
            "main_rtsp_url": "rtsp://192.168.37.3:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
            "second_rtsp_url": 0,
            "CAMERA_HOST": "192.168.37.3",
            "CAMERA_PORT": 80,
            "CAMERA_USER": "admin",
            "CAMERA_PASS": "6m8vw",
            "SAVE_PATH": "./Frames"
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
        self.controller_ip = config.get("controller_ip", self.default_config["controller_ip"])
        self.controller_port_tx = config.get("controller_port_tx", self.default_config["controller_port_tx"])
        self.controller_port_rx = config.get("controller_port_rx", self.default_config["controller_port_rx"])
        self.main_ip = config.get("main_ip", self.default_config["main_ip"])
        self.second_ip = config.get("second_ip", self.default_config["second_ip"])
        self.main_rtsp_url = config.get("main_rtsp_url", self.default_config["main_rtsp_url"])
        self.second_rtsp_url = config.get("second_rtsp_url", self.default_config["second_rtsp_url"])
        self.CAMERA_HOST = config.get("CAMERA_HOST", self.default_config["CAMERA_HOST"])
        self.CAMERA_PORT = config.get("CAMERA_PORT", self.default_config["CAMERA_PORT"])
        self.CAMERA_USER = config.get("CAMERA_USER", self.default_config["CAMERA_USER"])
        self.CAMERA_PASS = config.get("CAMERA_PASS", self.default_config["CAMERA_PASS"])
        self.SAVE_PATH = config.get("SAVE_PATH", self.default_config["SAVE_PATH"])

    def save_config(self):
        config = {
            "controller_ip": self.controller_ip,
            "controller_port_tx": self.controller_port_tx,
            "controller_port_rx": self.controller_port_rx,
            "main_ip": self.main_ip,
            "second_ip": self.second_ip,
            "main_rtsp_url": self.main_rtsp_url,
            "second_rtsp_url": self.second_rtsp_url,
            "CAMERA_HOST": self.CAMERA_HOST,
            "CAMERA_PORT": self.CAMERA_PORT,
            "CAMERA_USER": self.CAMERA_USER,
            "CAMERA_PASS": self.CAMERA_PASS,
            "SAVE_PATH": self.SAVE_PATH
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            print(f"Конфигурация успешно сохранена в {self.config_file}")
            print(config)
        except IOError as e:
            print(f"Ошибка при сохранении конфигурации в {self.config_file}: {e}")