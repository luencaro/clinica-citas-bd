import bcrypt

# Hash almacenado en la BD
hash_bd = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIVr8WCvSO"

# Contraseñas a probar
passwords = [
    "Clinica2025!",
    "clinica2025!",
    "CLINICA2025!",
]

print("=" * 70)
print("TEST BCRYPT DIRECTO")
print("=" * 70)
print(f"Hash en BD: {hash_bd}")
print(f"Longitud: {len(hash_bd)}")
print()

for pwd in passwords:
    try:
        resultado = bcrypt.checkpw(pwd.encode('utf-8'), hash_bd.encode('utf-8'))
        print(f"Password '{pwd}': {'✅ CORRECTO' if resultado else '❌ INCORRECTO'}")
    except Exception as e:
        print(f"Password '{pwd}': ❌ ERROR - {e}")

# Generar nuevo hash para comparar
print("\n" + "=" * 70)
print("GENERANDO NUEVO HASH")
print("=" * 70)
nueva_contraseña = "Clinica2025!"
salt = bcrypt.gensalt()
nuevo_hash = bcrypt.hashpw(nueva_contraseña.encode('utf-8'), salt).decode('utf-8')
print(f"Nueva contraseña: {nueva_contraseña}")
print(f"Nuevo hash: {nuevo_hash}")
print(f"Verificación: {'✅ OK' if bcrypt.checkpw(nueva_contraseña.encode('utf-8'), nuevo_hash.encode('utf-8')) else '❌ FAIL'}")
