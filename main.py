import re
import time

from config import root_path, dist_path

from pathlib import Path
import shutil

from ui import select_num_folder_gui


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
            choice_num = select_num_folder_gui(file_path, root_path, matches, filename)
            # Нажали "Пропустить"
            if choice_num is None:
                print(f"Файл '{filename}' пропущен.\n")
                continue

            chosen_folder = matches[choice_num - 1]

            # Перемещаем файл
            target_dir = root_path / chosen_folder

            shutil.move(
                str(file_path),
                str(target_dir / filename)
            )
            print(f'[ Успешно ] {str(filename)} '
                  f'\n\t\t ---> '
                  f'\n{str(Path(chosen_folder)).replace(str(dist_path), "")}  \n\n')


if __name__ == "__main__":
    src_path = root_path
    organize_files(root_path, dist_path)
    print("Обработка всех файлов завершена!")
    time.sleep(3)
