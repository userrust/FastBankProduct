import sqlite3
import os

# 1. Проверяем путь к базе данных
db_path = "FastBank.db"
print(f"База данных находится по пути: {os.path.abspath(db_path)}")
#D:\Пользователи\Андрюша\Програмирование\FastBank\FastBankProduct
#D:\Пользователи\Андрюша\Програмирование\FastBank\FastBankProduct\FastBank.db
# Подключение к базе данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Правильный запрос на вставку данных
#cursor.execute("""
#INSERT INTO users (
#    name, sur_name, middle_name, number_phone,
#    chet_one, chet_two, chet_three,
#    val_chet_one, val_chet_two, val_chet_three,
#    data_chet, chat_id
#) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#""", ("1", "1", "1", "1", "Главный щет", "not", "not", 100, 0, 0, "1", "1"))

# Выборка всех данных
cursor.execute("SELECT * FROM users")
a = cursor.fetchall()

# Вывод результатов
for i in a:
    print(i)

# Фиксация изменений и закрытие соединения
conn.commit()
conn.close()