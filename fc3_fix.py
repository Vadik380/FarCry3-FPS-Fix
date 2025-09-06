import psutil
import time
import subprocess
import os
import sys

# Определяем папку игры
if getattr(sys, 'frozen', False):
    # Если запущено из exe (PyInstaller)
    game_dir = os.path.dirname(sys.executable)
else:
    # Если запускается как скрипт
    game_dir = os.path.dirname(os.path.abspath(__file__))

launcher_exe = os.path.join(game_dir, 'FC3Updater.exe')

# Возможные игровые процессы
game_processes = ['farcry3.exe', 'farcry3_d3d11.exe']

def apply_affinity_to_game():
    """Следит за запуском игры и ставит 4 физических ядра"""
    for _ in range(30):  # проверяем до 30 секунд
        for p in psutil.process_iter(['name']):
            if p.info['name'] and p.info['name'].lower() in game_processes:
                try:
                    p.cpu_affinity([0, 2, 4, 6])
                    print(f"Affinity установлено для {p.info['name']}")
                    return
                except Exception as e:
                    print(f"Ошибка при установке affinity: {e}")
        time.sleep(1)
    print("Игровой процесс не найден в течение 30 секунд.")

def main():
    if not os.path.exists(launcher_exe):
        print(f"Ошибка: {launcher_exe} не найден!")
        input("Нажмите Enter для выхода...")
        return
    subprocess.Popen([launcher_exe])
    print("FC3Updater.exe запущен")
    apply_affinity_to_game()

if __name__ == "__main__":
    main()
