class CameraController:
    def __init__(self):
        self.connected = False
        self.zoom_level = 0
        self.focus_level = 0
        self.iris_level = 0
    
    def Connect(self):
        self.connected = True
        print("Camera connected")
    
    def ZoomHandler(self, pos):
        if self.connected:
            self.zoom_level = pos
            print(f"Zoom set to {pos}")
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

