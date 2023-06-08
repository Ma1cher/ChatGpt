import os
import shutil

current_directory = os.path.dirname(os.path.abspath(__file__))
update_file = os.path.join(current_directory, "Chat_Update.txt")

def update_code():
    # Проверяем наличие файла с обновлениями
    if not os.path.isfile(update_file):
        print("Файл с обновлениями не найден.")
        return

    # Открываем файл с обновлениями и считываем содержимое с указанием кодировки
    with open(update_file, "r", encoding="utf-8") as file:
        update_code = file.read()

    # Заменяем текущий код на обновленный код
    current_code_file = os.path.join(current_directory, "Chat Gpt.py")
    shutil.move(current_code_file, current_code_file + ".bak")  # Создаем резервную копию текущего кода
    with open(current_code_file, "w", encoding="utf-8") as file:
        file.write(update_code)

    print("Код успешно обновлен.")

# Запускаем функцию обновления кода
update_code()

