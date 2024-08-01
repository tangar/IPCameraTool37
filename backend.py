from CameraController import CameraController

def main():

    camera = CameraController()

    z = 0
    f = 0
    i = 0

    camera.Connect()

    while True:
        command = input("Введите команду (q для выхода): ")

        if command == 'q':
            print("Выход из программы.")
            break

        if command == 'p':
            print("сделать снимок")
            camera.PhotoHandler()

        parts = command.split()
        if len(parts) == 2 :
            try:
                value = CheckValue(parts[1])
                
                if parts[0] == 'z' or parts[0] == 'Z': 
                     z = value
                     print(f"Переменной 'z' присвоено значение {value}")
                     camera.ZoomHandler(z)

                elif parts[0] == 'f' or parts[0] == 'F': 
                     f = value
                     print(f"Переменной 'f' присвоено значение {value}")
                     camera.FocusHandler(f)

                elif parts[0] == 'i' or parts[0] == 'I': 
                     i = value
                     print(f"Переменной 'i' присвоено значение {value}")
                     camera.IrisHandler(i)

                elif parts[0] == 'a' or parts[0] == 'A': 
                     i = value
                     print(f"Управление режимом фокуса")
                     camera.FocusMode(value)
                else:
                     print(f"Неизвестная команда или неверный формат: {command}")


            except ValueError:
                print("Пожалуйста, введите допустимое число.")
        
        else:
            print(f"Неизвестная команда или неверный формат: {command}")

def CheckValue(input):
    value = float(input)
    if value < 0:
        value = 0
    elif value > 1:
        value = 1
    return value

if __name__ == "__main__":
    main()