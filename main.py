from telethon import TelegramClient, events
import asyncio

# Значения по умолчанию
DEFAULT_API_ID = '28392313'
DEFAULT_API_HASH = '75d7a2c77d80c4780fa5679769bb2ae7'

# Запрос ввода данных от пользователя
user_api_id = input(f"Enter ID (по умолчанию: {DEFAULT_API_ID}): ").strip()
user_api_hash = input(f"Enter hash (по умолчанию: {DEFAULT_API_HASH}): ").strip()

# Применение введенных данных или значений по умолчанию
api_id = user_api_id if user_api_id else DEFAULT_API_ID
api_hash = user_api_hash if user_api_hash else DEFAULT_API_HASH

# Создаем клиент
client = TelegramClient('session_name', api_id, api_hash)

# Функция для обработки новых сообщений
@client.on(events.NewMessage)
async def handler(event):
    print(f"New message in chat {event.chat.title}: {event.text}")

# Функция для отправки сообщений
async def send_message(chat_name, message):
    try:
        chat = await client.get_input_entity(chat_name)
        await client.send_message(chat, message)
        print(f"The message has sent in chat {chat_name}.")
    except Exception as e:
        print(f"Error message sending: {e}")

# Функция для получения списка чатов
async def list_chats():
    try:
        async for dialog in client.iter_dialogs():
            print(f"{dialog.name} (ID: {dialog.id})")
    except Exception as e:
        print(f"Error chat list taken: {e}")

# Командный интерфейс
async def command_interface():
    while True:
        command = input("Enter command (send, list, exit): ").strip().lower()
        if command == "send":
            chat_name = input("Enter the namechat or ID: ")
            message = input("Enter the message: ")
            await send_message(chat_name, message)
        elif command == "list":
            await list_chats()
        elif command == "exit":
            print("Exit the programm.")
            break
        else:
            print("Unknown command. Available commands: send, list, exit")

# Основная функция
async def main():
    await client.start()
    print("The client is run. Messages awaiting...")
    await command_interface()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())