import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
import pandas as pd
import re  # Import library for regular expressions
from datetime import datetime
import numpy as np

riwayat_transaksi = []
connection = None  # Tambahkan variabel connection global


def select(query_select, role):
    global connection  # Tambahkan variabel connection global
    cursor = connection.cursor()
    cursor.execute(query_select)
    result = cursor.fetchall()
    cursor.close()
    tambahkan_ke_riwayat('Select', {'query': query_select}, role)
    return result


def insert(query_insert, values, role):
    global connection  # Tambahkan variabel connection global
    cursor = connection.cursor()
    cursor.execute(query_insert, values)
    connection.commit()
    cursor.close()
    tambahkan_ke_riwayat('Insert', {'query': query_insert, 'values': values}, role)


def update(query_update, new_values, role):
    global connection  # Tambahkan variabel connection global
    cursor = connection.cursor()
    cursor.execute(query_update, new_values)
    connection.commit()
    cursor.close()
    tambahkan_ke_riwayat('Update', {'query': query_update, 'new_values': new_values}, role)


def delete(query_delete, values, role):
    global connection  # Tambahkan variabel connection global
    cursor = connection.cursor()
    cursor.execute(query_delete, values)
    connection.commit()
    cursor.close()
    tambahkan_ke_riwayat('Delete', {'query': query_delete, 'values': values}, role)


def tambahkan_ke_riwayat(action, detail, role):
    riwayat_transaksi.append({'action': action, 'detail': detail, 'role': role})


def tampilkan_riwayat_pembelian_admin(cursor):
    select_query = '''
    SELECT
        booking.id_booking,
        booking.id_kamar,
        booking.id_user,
        booking.check_in,
        booking.check_out,
        booking.nama,
        booking.telp,
        booking.cara_bayar,
        booking.total_pembelian,
        rooms.type
    FROM booking
    LEFT JOIN rooms ON booking.id_kamar = rooms.id_rooms
    '''
    result = select(select_query, 'admin')

    if result:
        df = pd.DataFrame(result, columns=["ID Booking", "ID Kamar", "ID User", "Check-in", "Check-out", "Nama", "Telepon", "Cara Bayar", "Total Pembelian", "Tipe Kamar"])
        df["Check-in"] = pd.to_datetime(df["Check-in"]).dt.strftime('%A, %d %B %Y')
        df["Check-out"] = pd.to_datetime(df["Check-out"]).dt.strftime('%A, %d %B %Y')

        print(df)
    else:
        print("Tidak ada riwayat pembelian untuk ditampilkan.")



def tampilkan_riwayat_pembelian():
    select_query = "SELECT * FROM booking"
    result = select(select_query, 'admin')  # Menampilkan riwayat dari tabel admin
    print(result)

def tampilkan_grafik_penjualan():
    select_query = '''
    SELECT rooms.type, COUNT(*) as jumlah
    FROM booking
    INNER JOIN rooms ON booking.id_rooms = rooms.id_rooms
    GROUP BY rooms.type
    '''
    result = select(select_query, 'admin')

    if result:
        df = pd.DataFrame(result, columns=['type', 'jumlah'])

        # Menggunakan NumPy untuk mengambil data dari DataFrame
        types = df['type'].values
        counts = df['jumlah'].values

        # Menampilkan grafik menggunakan NumPy dan Matplotlib
        x = np.arange(len(types))
        plt.bar(x, counts, align='center')
        plt.xticks(x, types)

        plt.title('Grafik Penjualan Berdasarkan Type Kamar')
        plt.xlabel('Type Kamar')
        plt.ylabel('Jumlah')
        plt.show()
    else:
        print("Tidak ada data untuk ditampilkan.")


def validate_password(password):
    # Minimal 8 karakter
    return len(password) >= 8


def validate_username(username):
    # Username hanya boleh mengandung huruf, angka, dan underscore
    return re.match(r'^\w+$', username) is not None


def registration(cursor, connection):
    while True:
        username = input("Enter new username: ")

        if not validate_username(username):
            print("Invalid username. Username should only contain letters, numbers, and underscores.")
            continue

        while True:
            password = input("Enter new password: ")
            if validate_password(password):
                break
            else:
                print("Invalid password. Password must be at least 8 characters long.")

        register_user(username, password, cursor, connection)
        break


def booking_kamar(id_rooms, id_user, cursor):
    global connection  # Tambahkan variabel connection global

    # Cek apakah kamar tersedia berdasarkan ID kamar
    cek_ketersediaan_query = "SELECT * FROM rooms WHERE id_rooms = %s AND status = 'Avaible'"
    cursor.execute(cek_ketersediaan_query, (id_rooms,))

    kamar_tersedia = cursor.fetchone()

    if kamar_tersedia:
        # Meminta informasi tambahan dari pengguna
        nama = input("Masukkan Nama: ")
        telp = input("Masukkan Nomor Telepon: ")
        cara_bayar = input("Masukkan Cara Bayar:")
        check_in_str = input("Masukkan Tanggal Check-in (YYYY-MM-DD): ")
        check_out_str = input("Masukkan Tanggal Check-out (YYYY-MM-DD): ")

        # Parsing tanggal menggunakan datetime
        check_in = datetime.strptime(check_in_str, "%Y-%m-%d")
        check_out = datetime.strptime(check_out_str, "%Y-%m-%d")

        # Mendapatkan harga kamar
        get_harga_query = "SELECT harga FROM rooms WHERE id_rooms = %s"
        cursor.execute(get_harga_query, (id_rooms,))
        harga_kamar = cursor.fetchone()[0]

        # Menghitung selisih hari
        selisih_hari = (check_out - check_in).days

        # Menghitung total biaya
        total_biaya = selisih_hari * harga_kamar * 1  # Contoh: Total harga = harga * 1
        print(f"Total biaya adalah: {total_biaya}")

        # Tambahkan data booking ke dalam tabel booking
        insert_booking_query = "INSERT INTO booking (id_rooms, id_user, check_in, check_out, nama, telp, cara_bayar, total_pembelian) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(
            insert_booking_query,
            (id_rooms, id_user, check_in, check_out, nama, telp, cara_bayar, total_biaya)
        )
        print("Booking successful!")

        # Update status kamar menjadi 'booked'
        update_status_query = "UPDATE rooms SET status = 'booked' WHERE id_rooms = %s"
        cursor.execute(update_status_query, (id_rooms,))
        connection.commit()
    else:
        print("Kamar tidak tersedia atau ID Kamar tidak valid.")


def connect_to_database():
    global connection  # Tambahkan variabel connection global
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'hotel'
    }

    try:
        connection = mysql.connector.connect(**db_config)
        print("Connected to MySQL database")
        return connection
    except Error as err:
        print(f"Error: {err}")
        return None


def close_connection(connection, cursor):
    try:
        if cursor:
            cursor.close()
    except ReferenceError:
        print("ReferenceError: Objek Cursor sudah ditutup atau tidak ada.")

    try:
        if connection:
            if connection.is_connected():
                connection.close()
                print("Koneksi ditutup")
    except ReferenceError:
        print("ReferenceError: Objek Koneksi sudah ditutup atau tidak ada.")


def create_users_table(cursor):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL
    )
    '''
    cursor.execute(create_table_query)


def register_user(username, password, cursor, connection):
    insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(insert_query, (username, password))
    connection.commit()
    print("Registration successful!")


def login_user(username, password, cursor):
    query_user = "SELECT * FROM users WHERE username = %s AND password = %s"
    query_admin = "SELECT * FROM logad WHERE username = %s AND password = %s"

    try:
        cursor.execute(query_user, (username, password))
        user = cursor.fetchone()

        if user:
            print("Login successful!")
            return 'user', user[0]  # Mengembalikan role dan id_user
    except Exception as e:
        print(f"Error during user login: {e}")

    try:
        cursor.execute(query_admin, (username, password))
        admin = cursor.fetchone()
        if admin:
            print("Selamat datang, Admin")
            return 'admin', None  # Mengembalikan role 'admin', id_user tidak diperlukan
    except Exception as e:
        print(f"Error during admin login: {e}")

    print("Login failed. Invalid username or password.")
    return None, None  # Mengembalikan None untuk role dan id_user



def select_rooms(cursor):
    select_query = "SELECT * FROM rooms"
    cursor.execute(select_query)
    result = cursor.fetchall()
    print(result)


def delete_room(cursor):
    id_rooms = input("Masukkan ID Kamar yang akan dihapus: ")
    delete_query = "DELETE FROM rooms WHERE id_rooms = %s"
    cursor.execute(delete_query, (id_rooms,))
    connection.commit()
    print("Data kamar berhasil dihapus.")


def update_room(cursor):
    id_rooms = input("Masukkan ID Kamar yang akan diupdate: ")
    new_price = input("Masukkan harga baru untuk kamar: ")
    update_query = "UPDATE rooms SET harga = %s WHERE id_rooms = %s"
    cursor.execute(update_query, (new_price, id_rooms))
    connection.commit()
    print("Data kamar berhasil diupdate.")


def tambah_data_kamar(cursor):
    tipe_kamar = input("Masukkan Tipe Kamar: ")
    harga_kamar = input("Masukkan Harga Kamar: ")
    status_kamar = input("Masukkan Status Kamar (Avaible/booked): ")

    insert_query = "INSERT INTO rooms (type, harga, status) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (tipe_kamar, harga_kamar, status_kamar))
    connection.commit()
    print("Data kamar berhasil ditambahkan.")


def main():
    global connection
    connection = connect_to_database()

    if connection:
        try:
            cursor = connection.cursor()

            create_users_table(cursor)

            while True:
                print("=== Menu ===")
                print("1. Login")
                print("2. Register")
                print("3. Exit")

                choice = input("Masukkan pilihan Anda (1/2/3): ")

                if choice == '1':
                    print("==========================================="
                          "|        WELCOME TO HOTELA LOGIN          |"
                          "===========================================")

                    username = input("Masukkan username: ")
                    password = input("Masukkan password: ")
                    role, id_user = login_user(username, password, cursor)

                    if role:
                        while True:
                            print("==========================================="
                                  "|        WELCOME TO HOTELA MENU          |"
                                  "===========================================")
                            if role == 'admin':
                                print("1. Lihat Pilihan Kamar")
                                print("2. Booking Kamar")
                                print("3. Riwayat Transaksi")
                                print("4. Lihat Grafik Penjualan")
                                print("5. Tambah Data Kamar")
                                print("6. Update Data Kamar")
                                print("7. Hapus Data Kamar")
                                print("8. Logout")
                            else:
                                print("1. Lihat Pilihan Kamar")
                                print("2. Booking Kamar")
                                print("3. Riwayat Transaksi")
                                print("4. Logout")

                            submenu_choice = input("Masukkan pilihan Anda: ")

                            if role == 'admin':
                                if submenu_choice == '1':
                                    select_rooms(cursor)
                                elif submenu_choice == '2':
                                    id_rooms = input("Masukkan ID Kamar yang akan dibooking: ")
                                    booking_kamar(id_rooms, id_user, cursor)
                                elif submenu_choice == '3':
                                    tampilkan_riwayat_pembelian()
                                elif submenu_choice == '4':
                                    tampilkan_grafik_penjualan()
                                elif submenu_choice == '5':
                                    tambah_data_kamar(cursor)
                                elif submenu_choice == '6':
                                    update_room(cursor)
                                elif submenu_choice == '7':
                                    delete_room(cursor)
                                elif submenu_choice == '8':
                                    connection = None
                                    break
                                else:
                                    print("Pilihan tidak valid. Silakan pilih antara kembali")
                            else:
                                if submenu_choice == '1':
                                    select_query = "SELECT id_rooms, type `tipe_kamar`, lantai, harga, status FROM rooms"
                                    rooms = select(select_query, role)

                                    for (id_rooms, tipe_kamar, lantai, harga, status) in rooms:
                                        available_status_text = 'Ya' if status == 'Avaible' else 'Tidak'

                                        print(f'''
ID Kamar: {id_rooms}
Tipe kamar: {tipe_kamar}
Lantai: {lantai}
Harga per malam: {harga}
Tersedia: {available_status_text}
---''')

                                elif submenu_choice == '2':
                                    id_rooms = input("Masukkan ID Kamar yang akan dibooking: ")
                                    booking_kamar(id_rooms, id_user, cursor)
                                elif submenu_choice == '3':
                                    tampilkan_riwayat_pembelian_user(id_user, cursor)
                                elif submenu_choice == '4':
                                    # Kembali ke fungsi login
                                    break
                                else:
                                    print("Pilihan tidak valid. Silakan pilih kembali")
                            # Tidak ada break di sini

                elif choice == '2':
                    print("==========================================="
                          "|        WELCOME TO HOTELA LOGIN          |"
                          "===========================================")

                    print("1. Register User")
                    print("2. Exit Registration")

                    register_choice = input("Masukkan pilihan Anda (1/2): ")

                    if register_choice == '1':
                        registration(cursor, connection)
                    elif register_choice == '2':
                        pass
                    else:
                        print("Pilihan tidak valid. Silakan pilih antara 1 atau 2.")

                elif choice == '3':
                    break

        finally:
            close_connection(connection, cursor)

if __name__ == "__main__":
    main()
