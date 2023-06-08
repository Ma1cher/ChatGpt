import os
import json
import openai
import platform
import time
import ctypes


openai.api_key = ""

accounts_folder = "Accounts"
chat_folder = "Chat"

gpt_profile_file = os.path.join(accounts_folder, "Gpt_Profile.json")
user_profile_file = os.path.join(accounts_folder, "User_Profile.json")
chat_history_file = os.path.join(chat_folder, "Chat_History.txt")
update_log_file = os.path.join(chat_folder, "Update_Log.txt")

def generate_chat(prompt, max_tokens):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.7,
        n=1,
        stop=None,
    )
    message = response.choices[0].text.strip()
    return message

def load_chat_history(file_path):
    if not os.path.isfile(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        chat_history = [line.strip() for line in file.readlines() if line.strip()]

    return chat_history

def save_chat_history(file_path, chat_history):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(chat_history))

def load_profile(file_path):
    if not os.path.isfile(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        profile = json.load(file)

    return profile

def save_profile(file_path, profile):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(profile, file, indent=4)

def load_update_log(file_path):
    if not os.path.isfile(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        update_log = [line.strip() for line in file.readlines() if line.strip()]

    return update_log

def save_update_log(file_path, update_log):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(update_log))

def request_username():
    username = input("Введите ваш никнейм: ")
    return username

def request_openai_key():
    openai_key = input("Введите ваш OpenAI API Key: ")
    return openai_key

def initialize_profiles():
    if not os.path.isfile(gpt_profile_file):
        gpt_profile = {
            "username": "Chat_GPT",
            "api_key": openai.api_key
        }
        save_profile(gpt_profile_file, gpt_profile)

    if not os.path.isfile(user_profile_file):
        username = request_username()
        openai_key = request_openai_key()
        user_profile = {
            "username": username,
            "api_key": openai_key
        }
        save_profile(user_profile_file, user_profile)

def format_chat_message(username, message):
    return f"{username} - {message}"

def print_chat_message(username, message):
    print(f"{username}: {message}")

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def delete_account():
    print("Вы уверены, что хотите удалить ваш аккаунт из чата?")
    confirmation = input("Введите 'Да' для подтверждения: ")
    if confirmation.lower() == "да":
        if os.path.isfile(user_profile_file):
            os.remove(user_profile_file)
            print("Ваш аккаунт был успешно удален.")
            print("Чат будет закрыт через 2 секунды.")
            time.sleep(2)
            if platform.system() == "Windows":
                ctypes.windll.user32.MessageBoxW(0, "Ваш аккаунт был успешно удален.", "Удаление аккаунта", 0x40 | 0x1)
            exit()
        else:
            print("Ваш аккаунт не найден.")
    else:
        print("Удаление аккаунта отменено.")

# Создание папок, если они не существуют
if not os.path.exists(accounts_folder):
    os.makedirs(accounts_folder)

if not os.path.exists(chat_folder):
    os.makedirs(chat_folder)

# Инициализация профилей и истории чата
initialize_profiles()
gpt_profile = load_profile(gpt_profile_file)
user_profile = load_profile(user_profile_file)
chat_history = load_chat_history(chat_history_file)
update_log = load_update_log(update_log_file)

# Установка текущего никнейма и API Key OpenAI
gpt_username = gpt_profile["username"]
gpt_api_key = gpt_profile["api_key"]
user_username = user_profile["username"]
user_api_key = user_profile["api_key"]

if user_api_key != "":
    openai.api_key = user_api_key

# Вывод информации о версии чата и GPT
clear_screen()
print("Чат с GPT-3.5 v0.1.6.0 Стабильная")
print("Введите '/помощь' для получения списка команд чата.")
print("-------------------------")

while True:
    user_input = input(f"{user_username}: ")
    if user_input.lower() == 'выход':
        break

    if user_input.lower() == '/помощь':
        print("Доступные команды:")
        print("/помощь - отображение списка команд")
        print("/сброс - сброс чата")
        print("/обновления - отображение лога обновлений")
        print("/сохранить - сохранить историю чата в файл")
        print("/удалить аккаунт - удаление вашего аккаунта из чата")
        print("-------------------------")
        continue

    if user_input.lower() == '/сброс':
        clear_screen()
        print("Чат с GPT-3.5 v0.1.6.0 Стабильная")
        print("Введите '/помощь' для получения списка команд чата.")
        print("-------------------------")
        chat_history = []
        save_chat_history(chat_history_file, chat_history)
        continue

    if user_input.lower() == '/обновления' or user_input.lower() == 'покажи обновления':
        clear_screen()
        print("GPT: Вот обновления чата:")
        for update in update_log:
            print(update)
        print(f"Текущая версия чата: v0.1.6.0S")
        chat_history.append(format_chat_message(user_username, user_input))
        chat_history.append(format_chat_message(gpt_username, "Выведены обновления чата"))
        continue

    if user_input.lower() == '/сохранить':
        save_chat_history(chat_history_file, chat_history)
        print("История чата сохранена в файл Chat_History.txt")
        print("-------------------------")
        continue

    if user_input.lower() == '/удалить аккаунт':
        delete_account()
        continue

    prompt = format_chat_message(user_username, user_input)

    chat_response = generate_chat(prompt, max_tokens=4000)
    chat_history.append(format_chat_message(user_username, user_input))
    chat_history.append(format_chat_message(gpt_username, chat_response))

    print_chat_message(gpt_username, chat_response)

# Сохранение профилей пользователя и GPT
gpt_profile["api_key"] = gpt_api_key
save_profile(gpt_profile_file, gpt_profile)
save_profile(user_profile_file, user_profile)
save_chat_history(chat_history_file, chat_history)
save_update_log(update_log_file, update_log)
