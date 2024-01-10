import time
import subprocess
from datetime import datetime
import sys

database = {
    'admin': 'admin',
    'pengguna2': 'katasandi2',
}

current_dateTime = datetime.now()
command_history = []  # Menyimpan riwayat perintah


def boot_loader():
    print("Bootloader: Memuat sistem operasi...")
    time.sleep(2)
    print("Bootloader: Menjalankan kernel sistem operasi...")
    time.sleep(2)


def kernel():
    print("Kernel: Inisialisasi sistem...")
    time.sleep(2)
    print("Kernel: Memuat driver perangkat keras...")
    time.sleep(2)
    print("Kernel: Menjalankan sistem operasi...")
    time.sleep(3)
    print("Spesifikasi : Intel I5 13400F")
    print("            : Intel RTX 3050")
    print("            : Asrock B760M PRO RS/D4")


def main():
    print("Proses Boot Dimulai.")
    boot_loader()
    kernel()
    print("Proses Boot Selesai.")


def login():
    print("\n")
    nama_pengguna = input("Masukkan nama pengguna: ")
    kata_sandi = input("Masukkan kata sandi: ")

    if nama_pengguna in database and database[nama_pengguna] == kata_sandi:
        print("Login berhasil")
        command_prompt()
    else:
        print("Nama pengguna atau kata sandi salah.")
        login()


def command_prompt():
    global command_history  # Menyimpan riwayat perintah
    while True:
        user_input = input("Users > ")

        if user_input.lower() == 'exit':
            sys.exit()
        elif user_input.lower() == 'cls':
            print("\033[2J\033[H", end="")
        elif user_input.lower() == 'ipconfig':
            print("192.168.1.9")
        elif user_input.lower() == 'dir':
            print("Menampilkan File/Folder.")
        elif user_input.lower() == 'date':
            print(current_dateTime)
        elif user_input.lower() == 'copy':
            print("Menyalin File.")
        elif user_input.lower() == 'del':
            print("Menghapus File.")
        elif user_input.lower() == 'help':
            print("1. cls.")
            print("2. dir [filename].")
            print("3. copy [filename].")
            print("4. del [filename].")
            print("5. ipconfig.")
            print("6. exit.")
        else:
            try:
                result = subprocess.run(user_input, shell=True, capture_output=True, text=True)
                print(result.stdout)
                if result.stderr:
                    print(f"Error: {result.stderr}")
            except Exception as e:
                print(f"Error: {e}")

        command_history.append(user_input)  # Menambahkan perintah ke dalam riwayat


if __name__ == "__main__":
    main()
    login()
    command_prompt()

    # Setelah keluar dari command_prompt, menghapus riwayat perintah
    command_history = []
