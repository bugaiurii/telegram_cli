from telethon import TelegramClient, events
import asyncio
import os
from aioconsole import ainput  # Асинхронный аналог input()

# Значения по умолчанию
DEFAULT_API_ID = 'xxxxxxxx'
DEFAULT_API_HASH = 'xxxxxxxxxxxxxxxxxx'

# Запрос ввода данных от пользователя
user_api_id = input(f"Enter ID (default: {DEFAULT_API_ID}): ").strip()
user_api_hash = input(f"Enter hash (default: {DEFAULT_API_HASH}): ").strip()

# Применение введенных данных или значений по умолчанию
api_id = user_api_id if user_api_id else DEFAULT_API_ID
api_hash = user_api_hash if user_api_hash else DEFAULT_API_HASH

# Создаем клиент
client = TelegramClient('session_name', api_id, api_hash)


# ANSI-коды для цветов
COLOR_BLUE = "\033[94m"  # Синий цвет для отправленных сообщений
COLOR_GREEN = "\033[92m"  # Зеленый цвет для полученных сообщений
COLOR_RESET = "\033[0m"  # Сброс цвета

# Функция для обработки новых сообщений
@client.on(events.NewMessage)
async def handler(event):
    # Выводим информацию о сообщении и отправителе
    sender = await event.get_sender()
    print(f"\n{COLOR_GREEN}New message from {sender.first_name} ({sender.id}):\n{event.text}{COLOR_RESET}")

# Функция для отправки сообщений
async def send_message(chat_name, message):
    try:
        chat = await client.get_input_entity(chat_name)
        await client.send_message(chat, message)
        # Выводим отправленное сообщение с отступом и синим цветом
        print(f"{COLOR_BLUE}\n\t\t\t\t\t\t Sent to {chat_name}:\n\t\t\t\t\t\t {message}{COLOR_RESET}")
    except Exception as e:
        print(f"Error sending message: {e}")

# Функция для получения списка чатов
async def list_chats():
    try:
        async for dialog in client.iter_dialogs():
            print(f"{dialog.name} (ID: {dialog.id})")
    except Exception as e:
        print(f"Error fetching chat list: {e}")

# Командный интерфейс
async def command_interface():
    while True:
        command = await ainput("\nEnter command (send, list, exit): ")  # Асинхронный ввод
        command = command.strip().lower()
        if command == "send":
            chat_name = await ainput("Enter the chat name or ID: ")
            message = await ainput("Enter the message: ")
            await send_message(chat_name, message)
        elif command == "list":
            await list_chats()
        elif command == "exit":
            print("Exiting the program.")
            await client.disconnect()
            break
        else:
            print("Unknown command. Available commands: send, list, exit")

# Основная функция
async def main():
    try:
        # Проверяем, существует ли файл сессии
        if os.path.exists('session_name.session'):
            print("Found existing session. Connecting...")
        else:
            print("Creating a new session...")

        # Запускаем клиент
        await client.start()
        print("The client is running. Waiting for messages...")

        # Запускаем командный интерфейс и прослушивание сообщений одновременно
        await asyncio.gather(
            command_interface(),
            client.run_until_disconnected()
        )
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Закрываем клиент при завершении
        if client.is_connected():
            await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
