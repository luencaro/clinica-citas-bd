import bcrypt

password = "Clinica2025!"
salt = bcrypt.gensalt()
hash_correcto = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

print(f"Contraseña: {password}")
print(f"Hash: {hash_correcto}")

# Verificar
check = bcrypt.checkpw(password.encode('utf-8'), hash_correcto.encode('utf-8'))
print(f"Verificación: {'✅ OK' if check else '❌ FAIL'}")
