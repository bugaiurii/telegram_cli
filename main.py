from telethon import TelegramClient, events
import asyncio

# Введите свои api_id и api_hash
api_id = '28392313'  # Замените на ваш api_id
api_hash = '75d7a2c77d80c4780fa5679769bb2ae7'  # Замените на ваш api_hash

# Создаем клиент
client = TelegramClient('session_name', api_id, api_hash)

# Функция для обработки новых сообщений
@client.on(events.NewMessage)
async def handler(event):
    print(f"Новое сообщение в чате {event.chat.title}: {event.text}")

# Функция для отправки сообщений
async def send_message(chat_name, message):
    try:
        chat = await client.get_input_entity(chat_name)
        await client.send_message(chat, message)
        print(f"Сообщение отправлено в чат {chat_name}.")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

# Функция для получения списка чатов
async def list_chats():
    try:
        async for dialog in client.iter_dialogs():
            print(f"{dialog.name} (ID: {dialog.id})")
    except Exception as e:
        print(f"Ошибка при получении списка чатов: {e}")

# Командный интерфейс
async def command_interface():
    while True:
        command = input("Введите команду (send, list, exit): ").strip().lower()
        if command == "send":
            chat_name = input("Введите имя чата или ID: ")
            message = input("Введите сообщение: ")
            await send_message(chat_name, message)
        elif command == "list":
            await list_chats()
        elif command == "exit":
            print("Выход из программы.")
            break
        else:
            print("Неизвестная команда. Доступные команды: send, list, exit")

# Основная функция
async def main():
    await client.start()
    print("Клиент запущен. Ожидание сообщений...")
    await command_interface()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())