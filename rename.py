import datetime
import re
import time
from config import root_path

all_files = [f for f in root_path.rglob('*') if f.is_file() and f.suffix.lower() in ('.txt', '.mp4')]

for file_path in all_files:
    filename = str(file_path.name)

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    if re.search(r'^\d{8}', filename):
        continue

    new_file_name = f'{year}{month:02}{day:02}-{filename}'
    new_file_path = file_path.with_name(new_file_name)

    try:
        file_path.rename(new_file_path)
        print(f"Файл '{file_path}' успешно переименован в '{new_file_path}'")
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
    except FileExistsError:
        print(f"Ошибка: Файл с именем '{new_file_path}' уже существует.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

time.sleep(3)
