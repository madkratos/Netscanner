from cryptography.fernet import Fernet   # agregado para la criptografia

# generador de clave
key = Fernet.generate_key()

# impresion de la clave
print(key)
