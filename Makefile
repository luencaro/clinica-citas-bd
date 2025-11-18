.PHONY: help status logs info

help:
	@echo "Sistema de Gestión de Citas Médicas"
	@echo "Comandos: make status, make logs, make info"

status:
	@sudo docker compose ps

logs:
	@sudo docker compose logs -f

info:
	@echo "========================================"
	@echo "Sistema de Gestión de Citas Médicas"
	@echo "========================================"
	@echo "Base de Datos: localhost:5433"
	@echo "Usuario: clinica_admin"
	@echo "Database: clinica_citas"
	@echo "Admin: admin@clinica.com / Clinica2025!"
