import subprocess
import sys
import os
import shutil
from pathlib import Path


def install_and_build():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller успешно установлен")
    except subprocess.CalledProcessError:
        print("Ошибка при установке pyinstaller!")
        return False
    try:
        subprocess.check_call(
            [sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", "converter.py"])
        print("Сборка EXE выполнена успешно")
        return True
    except subprocess.CalledProcessError:
        print("Ошибка при сборке EXE!")
        return False


def move_exe_and_cleanup():
    exe_file = Path("dist/converter.exe")
    if not exe_file.exists():
        print("EXE-файл не найден!")
        return False
    destination = Path("./converter.exe")
    if destination.exists():
        destination.unlink()
    shutil.move(str(exe_file), str(destination))
    # print(f"EXE-файл перемещен в {destination}")
    folders_to_remove = ["build", "dist"]
    for folder in folders_to_remove:
        folder_path = Path(folder)
        if folder_path.exists():
            shutil.rmtree(folder_path)
            # print(f"Папка {folder} удалена")
    files_to_remove = ["converter.spec"]
    for file in files_to_remove:
        file_path = Path(file)
        if file_path.exists():
            os.remove(file_path)
            # print(f"Файл {file} удален")
    return True


if __name__ == "__main__":
    if install_and_build():
        if move_exe_and_cleanup():
            print("Процесс завершен успешно!")
            print("EXE-файл находится в папке с исходным кодом программы.")
            print("При запуске EXE-файла консоль не будет отображаться.")
        else:
            print("Ошибка при перемещении файла или очистке!")
    else:
        print("Процесс завершен с ошибками!")