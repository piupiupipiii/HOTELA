import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
from mysql.connector import Error

db_config = {'host': 'localhost', 'user': 'root', 'password': '', 'database': 'hotel'}

riwayat_transaksi = []

# Menambahkan variabel role
role_admin = 'admin'
role_user = 'user'

try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print('Terhubung ke database MySQL')
except mysql.connector.Error as e:
    print(f"Error koneksi ke MySQL: {e}")

def select(query_select, role):
    kursor = connection.cursor()
    kursor.execute(query_select)
    hasil = kursor.fetchall()
    kursor.close()
    tambahkan_ke_riwayat('Select', {'query': query_select}, role)
    return hasil

def insert(query_insert, nilai, role):
    kursor = connection.cursor()
    kursor.execute(query_insert, nilai)
    connection.commit()
    kursor.close()
    tambahkan_ke_riwayat('Insert', {'query': query_insert, 'nilai': nilai}, role)

def update(query_update, nilai_baru, role):
    kursor = connection.cursor()
    kursor.execute(query_update, nilai_baru)
    connection.commit()
    kursor.close()
    tambahkan_ke_riwayat('Update', {'query': query_update, 'nilai_baru': nilai_baru}, role)

def delete(query_delete, nilai, role):
    kursor = connection.cursor()
    kursor.execute(query_delete, nilai)
    connection.commit()
    kursor.close()
    tambahkan_ke_riwayat('Delete', {'query': query_delete, 'nilai': nilai}, role)

def tambahkan_ke_riwayat(aksi, detail, role):
    riwayat_transaksi.append({'aksi': aksi, 'detail': detail, 'role': role})

def tampilkan_riwayat_pembelian():
    select_query = "SELECT * FROM riwayat_pembelian"
    result = select(select_query, role_admin)
    print(result)

def tampilkan_grafik_penjualan():
    select_query = "SELECT type, COUNT(*) as jumlah FROM riwayat_pembelian GROUP BY type"
    result = select(select_query, role_admin)

    if result:
        df = pd.DataFrame(result, columns=['type', 'jumlah'])
        df.plot(kind='bar', x='type', y='jumlah', legend=False)
        plt.title('Grafik Penjualan Berdasarkan Type Kamar')
        plt.xlabel('Type Kamar')
        plt.ylabel('Jumlah')
        plt.show()
    else:
        print("Tidak ada data untuk ditampilkan.")

def connect_to_database():
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

def close_connection(connection, cursor=None):
    if cursor:
        cursor.close()
    if connection.is_connected():
        connection.close()
        print("Connection closed")

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

def login_user(username, password, cursor, role):
    query = f"SELECT * FROM {role} WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        print(f"{role.capitalize()} login successful!")
    else:
        print(f"Login failed. Invalid username or password for {role}.")

def main():
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

                choice = input("Enter your choice (1/2/3): ")

                if choice == '1':
                    print("=== Login ===")
                    role = input("Enter role (admin/user): ")
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    login_user(username, password, cursor, role)
                elif choice == '2':
                    print("=== Register ===")
                    username = input("Enter new username: ")
                    password = input("Enter new password: ")
                    register_user(username, password, cursor, connection)
                elif choice == '3':
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")

        finally:
            close_connection(connection, cursor)

if __name__ == "__main__":
    main()
