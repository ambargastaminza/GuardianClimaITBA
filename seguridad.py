import bcrypt

# --------- Hashear la contraseña al registrarse ---------
def hashear_contrasena(password_plano):
    password_bytes = password_plano.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password_bytes, salt)
    return hash.decode('utf-8')

# --------- Verificar al iniciar sesión ---------
def verificar_contrasena(password_ingresada, hash_guardado):
    password_bytes = password_ingresada.encode('utf-8')
    hash_bytes = hash_guardado.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hash_bytes)