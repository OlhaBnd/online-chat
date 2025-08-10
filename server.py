from socket import *        # Імпортуємо бібліотеку socket — вона допомагає програмам спілкуватися через інтернет
import threading            # Імпортуємо threading — щоб одночасно обслуговувати багатьох користувачів

server_socket = socket(AF_INET, SOCK_STREAM)   # Створюємо "розетку" для спілкування (AF_INET - IPv4, SOCK_STREAM - протокол TCP)
server_socket.bind(('0.0.0.0', 8080))          # Прив’язуємо сервер до всіх IP-адрес комп’ютера (0.0.0.0) і порту 8080
server_socket.listen(5)                        # Кажемо серверу "слухати" підключення (максимум 5 в черзі)
print("Server running...")                     # Повідомлення, що сервер запущений

clients = []                                   # Список усіх підключених клієнтів

def broadcast(message):                        # Функція, щоб відправити повідомлення всім
    for client in clients:                     # Перебираємо всіх клієнтів
        try:
            client.send(f"{message}\n".encode())  # Відправляємо текст у вигляді байтів
        except:
            pass                               # Якщо помилка — нічого не робимо (ігноруємо)

def handle_client(client_socket):              # Функція для спілкування з одним клієнтом
    name = client_socket.recv(1024).decode().strip()  # Отримуємо ім’я користувача від клієнта
    broadcast(f"{name} joined!")               # Сповіщаємо всіх, що він приєднався

    while True:                                # Безкінечний цикл, поки клієнт з нами
        try:
            message = client_socket.recv(1024).decode().strip()  # Читаємо повідомлення
            broadcast(f"{name}: {message}")    # Відправляємо його всім
        except:
            clients.remove(client_socket)      # Якщо помилка — видаляємо з списку клієнтів
            broadcast(f"{name} left!")         # Повідомляємо, що він вийшов
            client_socket.close()              # Закриваємо його з’єднання
            break                              # Виходимо з циклу

while True:                                    # Головний цикл сервера
    client_socket, addr = server_socket.accept()   # Чекаємо нового користувача
    clients.append(client_socket)              # Додаємо його до списку клієнтів
    threading.Thread(                          # Створюємо новий потік (щоб не блокувати інших)
        target=handle_client,                  # Вказуємо, що виконувати
        args=(client_socket,),                 # Передаємо сокет клієнта
        daemon=True                            # Потік закриється разом із програмою
    ).start()                                  # Запускаємо потік
