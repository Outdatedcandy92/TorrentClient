import os
import shutil
import winreg


def setup():
    print("Welcome to the setup wizard for PyTorrent!")
    print("Please select an option:")
    print("1. Install PyTorrent")
    print("2. Uninstall PyTorrent")
    print("4. Exit")
    choice = int(input(""))

    if choice == 1:
        install()
    elif choice == 2:
        uninstall()
    elif choice == 3:
        print("Exiting setup wizard...")
    else:
        print("Invalid choice. Exiting setup wizard...")        

def install():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    source_file = os.path.join(current_dir, 'main.py')
    destination_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'pytorrent')
    destination_file = os.path.join(destination_dir, 'main.py')

    os.makedirs(destination_dir, exist_ok=True)

    print(f"Copying file from {source_file} to {destination_file}")

    shutil.copy2(source_file, destination_file)

    print("File copied successfully!")

    print("Creating batch file...")

    batch_file_content = f'@echo off\npython "{destination_file}" %*\n'
    batch_file_path = os.path.join(destination_dir, 'pytorrent.bat')

    with open(batch_file_path, 'w') as batch_file:
        batch_file.write(batch_file_content)

    print(f"Batch file created at {batch_file_path}")

    print("Adding directory to PATH...")

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_ALL_ACCESS) as key:
        current_path = winreg.QueryValueEx(key, 'PATH')[0]
        print(f"Current PATH: {current_path}")
        if destination_dir not in current_path:
            new_path = f"{current_path};{destination_dir}"
            winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path)
            print(f"New PATH: {new_path}")
        else:
            print(f"{destination_dir} is already in PATH")

    print("Installation complete! Please restart your command prompt or log out and log back in for the changes to take effect.")

def uninstall():
    destination_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'pytorrent')

    print(f"Removing directory {destination_dir}...")

    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
        print("Directory removed successfully!")
    else:
        print("Directory does not exist.")

    print("Removing directory from PATH...")

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_ALL_ACCESS) as key:
        current_path = winreg.QueryValueEx(key, 'PATH')[0]
        print(f"Current PATH: {current_path}")
        new_path = ';'.join([p for p in current_path.split(';') if p != destination_dir])
        winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path)
        print(f"New PATH: {new_path}")

    print("Uninstallation complete! Please restart your command prompt or log out and log back in for the changes to take effect.")

if __name__ == "__main__":
    setup()