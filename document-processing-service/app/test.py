import re
from datetime import datetime

def parse_string(input_str):
    # Шаблоны для поиска частей строки
    name_pattern = r'\b[А-ЯЁ][а-яё]*\s[А-ЯЁ]\.[А-ЯЁ]\.'
    role_pattern = r'\b[А-ЯЁ][а-яё]+\b'
    date_pattern = r'\b\d{2}\.\d{2}\.\d{4}\b'

    # Поиск частей строки
    names = re.findall(name_pattern, input_str)
    roles = re.findall(role_pattern, input_str)
    date = re.search(date_pattern, input_str).group()

    # Удаляем найденные имена и дату из строки, чтобы выделить сообщение
    remaining_str = re.sub(name_pattern, '', input_str)
    remaining_str = re.sub(date_pattern, '', remaining_str).strip()

    # Предполагаем, что роли следуют сразу за именами
    roles_cleaned = []
    for role in roles:
        if not any(name.endswith(role) for name in names):
            roles_cleaned.append(role)

    owner_name, initiator_name = names[:2]
    owner_role, initiator_role = roles_cleaned[:2]
    task_message = remaining_str.replace(owner_role, '').replace(initiator_role, '').strip()

    # Проверяем и формируем словарь с результатами
    result = {
        'owner_name': owner_name,
        'owner_role': owner_role,
        'initiator_name': initiator_name,
        'initiator_role': initiator_role,
        'task_message': task_message,
        'end_date': date
    }
    return result

# Пример строки
input_str = 'Директор Иванов И.И. 26.05.2024 Петров П.П. Работник отчёт 26.05.2024'

# Парсинг строки
parsed_result = parse_string(input_str)

# Вывод результата
for key, value in parsed_result.items():
    print(f"{key}: {value}")