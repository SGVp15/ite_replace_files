import re
import shutil
from pathlib import Path
import time

from config import root_path, dist_path


def organize_files(source_dir, dist_dir):
    root_path = Path(source_dir)
    all_files = [f for f in root_path.rglob('*') if f.is_file() and f.suffix.lower() in ('.txt', '.mp4')]

    for file_path in all_files:
        filename = str(file_path.name)
        if not re.search(r'(\d{8})', filename):
            continue
        is_zoom: bool = True if re.search(r'^gmt', filename.lower()) else False

        date = str(re.findall(r'^(?:gmt)?(\d{8})[.\-]', filename.lower())[0]).strip()
        year = date[:4]
        month = date[4:6]
        day = date[6:]

        all_dirs = [f for f in dist_dir.rglob('*')
                    if f.is_dir()
                    and not any(sub.is_dir() for sub in f.iterdir())]
        if is_zoom:
            all_dirs = [f for f in all_dirs if re.search(r'zoom', str(f.parent.name).lower())]
        else:
            all_dirs = [f for f in all_dirs if not re.search(r'zoom', str(f.parent.name).lower())]

        matches = []
        for dir in all_dirs:
            pattern = fr'{year}\-*{month}\-*{day}'
            if re.search(pattern, dir.name):
                matches.append(dir)

        if not matches:
            print(f'[ Не нашел папку для ] {str(filename)} ')
            continue

        # СЦЕНАРИЙ А: Найдена ровно 1 подходящая папка
        if len(matches) == 1:
            shutil.move(str(file_path), str(Path(matches[0], filename)))
            print(f'[ Успешно ] {str(filename)} '
                  f'\n\t\t ---> '
                  f'\n{str(Path(matches[0])).replace(str(dist_path), "")}  \n\n')

        # СЦЕНАРИЙ Б: Найдено НЕСКОЛЬКО подходящих папок
        elif len(matches) > 1:
            print(f"Файл: '{file_path.relative_to(root_path)}' переместить:")
            for i, folder_name in enumerate(matches, 1):
                print(f"  {i} - Папка [ {folder_name} ]")

            skip_option_num = 0
            print(f"  {skip_option_num} - Пропустить этот файл")
            choice_input = input(f"  Ваш выбор (1-{skip_option_num}): ").strip()

            if choice_input.isdigit():
                choice_num = int(choice_input)
                if 1 <= choice_num <= len(matches):
                    chosen_folder = matches[choice_num - 1]
                    target_dir = root_path / chosen_folder
                    shutil.move(str(file_path), str(Path(target_dir, filename)))
                else:
                    print(f"  Файл '{filename}' пропущен.\n")
                    continue
            else:
                print(f"  Некорректный ввод, файл '{filename}' пропущен.\n")
                continue


if __name__ == "__main__":
    src_path = root_path
    organize_files(root_path, dist_path)
    print("Обработка всех файлов завершена!")
    time.sleep(3)
