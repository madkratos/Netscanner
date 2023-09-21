import sqlite3                             # agregado para la base de datos
from cryptography.fernet import Fernet     # agrefado para la enciptacion de la base de datos, necesario instalar con "pip install cryptography  "
import configparser                        # agregado para manejar el archivo config, puede que se necesario instalar con "pip install configparser"
class DatabaseManager:
# funcion principal para denotar la base de datos y sus parametros
    def __init__(self, db_name='user.db',  config_file='config.ini'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.key = self.config.get('encryption', 'key')

# fuencion para conectar a la base de datos
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

# funcion para desconectar de la base de datos
    def disconnect(self):
        if self.conn:
            self.conn.close()

# funcion para crear la tabla de usuarios
    def create_tables(self):
        self.connect()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        self.disconnect()

# funcion para crear usuarios y pass
    def insert_user(self, username, password):
        self.connect()
        encrypted_password = self.encrypt_password(password)
        self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, encrypted_password))
        self.conn.commit()
        self.disconnect()

# funcion para borrar usuarios
    def delete_user(self, username):
        self.connect()
        self.cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        self.conn.commit()
        self.disconnect()

# funcion para autenticar usuarios de la base de datos
    def authenticate_user(self, username, password):
        self.connect()
        cipher_suite = Fernet(self.key)
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_data = self.cursor.fetchone()
        if user_data:
            encrypted_password = user_data[2]
            try:
                decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
                if decrypted_password == password:
                    return user_data
            except Exception as e:
                print("Error:", e)
        self.disconnect()
        return None
    
# funcion para obtener usuarios de la base de datos
    def get_usernames(self):
        self.connect()
        self.cursor.execute('SELECT username FROM users')
        usernames = [row[0] for row in self.cursor.fetchall()]
        self.disconnect()
        return usernames

# funcion para obtener pass de la base de datos
    def get_passwords(self):
        self.connect()
        self.cursor.execute('SELECT password FROM users')
        passwords = [row[0] for row in self.cursor.fetchall()]
        self.disconnect()
        return passwords
    
# funcion para encriptar el pass con Fernet encryption key
    def encrypt_password(self, password):
        cipher_suite = Fernet(self.key)
        encrypted_password = cipher_suite.encrypt(password.encode()).decode()
        return encrypted_password

# funcion para obtener la existencia del usuario
    def user_exists(self, username):
        self.connect()
        self.cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
        count = self.cursor.fetchone()[0]
        self.disconnect()
        return count > 0
    
if __name__ == "__main__":
    db_manager = DatabaseManager()
