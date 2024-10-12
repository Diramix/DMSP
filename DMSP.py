import os
import subprocess
import shutil
import psutil
import msvcrt

def close_discord():
    discord_executables = ['Discord.exe', 'DiscordCanary.exe', 'DiscordPTB.exe']
    
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in discord_executables:
            print(f"Закрытие {proc.info['name']} (PID: {proc.info['pid']})...")
            proc.kill()

def get_asar_command():
    return [r'C:\Program Files\nodejs\npx.cmd', 'asar']

def unpack_asar(asar_file, output_dir):
    asar_command = get_asar_command()
    subprocess.run(asar_command + ['extract', asar_file, output_dir], check=True)

def pack_asar(input_dir, asar_file):
    asar_command = get_asar_command()
    subprocess.run(asar_command + ['pack', input_dir, asar_file], check=True)

def replace_files(asar_unpack_dir, patch_dir):
    bootstrap_dir = os.path.join(asar_unpack_dir, 'app_bootstrap')

    for item_name in os.listdir(patch_dir):
        source_item = os.path.join(patch_dir, item_name)
        target_item = os.path.join(bootstrap_dir, item_name)

        if os.path.isfile(source_item):
            shutil.copy2(source_item, target_item)
            print(f"Заменён файл: {item_name}")
        elif os.path.isdir(source_item):
            if os.path.exists(target_item):
                shutil.rmtree(target_item)
            shutil.copytree(source_item, target_item)
            print(f"Заменена папка: {item_name}")

def main():
    while True:
        asar_file = input("Введите путь к файлу app.asar: ")
        
        if not os.path.exists(asar_file):
            print("Файл app.asar не найден. Пожалуйста, попробуйте снова.")
            continue

        break

    asar_dir = os.path.dirname(asar_file)
    output_dir = os.path.join(asar_dir, 'asar_unpack')
    patch_dir = os.path.join(os.getcwd(), 'patch')

    print("Проверка и закрытие запущенных процессов Discord...")
    close_discord()

    print("Распаковка app.asar...")
    unpack_asar(asar_file, output_dir)

    print("Замена файлов в app_bootstrap...")
    replace_files(output_dir, patch_dir)

    print("Запаковка обратно в app.asar...")
    pack_asar(output_dir, asar_file)

    print("Удаление папки asar_unpack...")
    shutil.rmtree(output_dir)

    print("Патч успешно применён! Нажмите любую клавишу для закрытия...")
    msvcrt.getch()

if __name__ == "__main__":
    main()
