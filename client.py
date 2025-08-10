from socket import *             # Імпортуємо бібліотеку socket для спілкування по мережі
import threading                 # Імпортуємо threading для багатозадачності

client_socket = socket(AF_INET, SOCK_STREAM)  # Створюємо сокет для підключення до сервера
name = input("Введіть ім'я: ")                # Запитуємо ім’я у користувача
client_socket.connect(('0.tcp.eu.ngrok.io', 16775))  # Підключаємося до сервера по IP/домену та порту
client_socket.send(name.encode())             # Відправляємо ім’я серверу

def send_message():                           # Функція для відправки повідомлень
    while True:
        client_message = input()               # Чекаємо, що користувач введе
        if client_message.lower() == 'exit':   # Якщо він написав "exit"
            client_socket.close()              # Закриваємо з’єднання
            break                              # Виходимо з циклу
        client_socket.send(client_message.encode())  # Відправляємо повідомлення на сервер

threading.Thread(target=send_message).start()  # Запускаємо потік для відправки повідомлень

while True:                                    # Основний цикл для отримання повідомлень
    try:
        message = client_socket.recv(1024).decode().strip()  # Отримуємо повідомлення від сервера
        if message:                             # Якщо повідомлення не порожнє
            print(message)                      # Виводимо його на екран
    except:
        break                                   # Якщо помилка — виходимо з циклу
