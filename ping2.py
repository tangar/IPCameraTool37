from MyPinger import MyPinger
import time

ip_list = ["127.0.0.1", "192.168.37.2", "192.168.37.3"]

def main():
    p = MyPinger()

    while True:
        all_online = True
        for ip in ip_list:
            if p.ping(ip) != 0:
                print(f"{ip} не отвечает.")
                all_online = False
        
        if all_online:
            print("Все IP в сети.")
            # Здесь можно добавить вашу логику работы
        else:
            print("Некоторые IP не доступны.")
        
        time.sleep(1)  # Пауза между проверками

if __name__ == "__main__":
    main()