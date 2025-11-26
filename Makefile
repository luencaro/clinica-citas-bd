.PHONY: help status logs info test test-validators test-models test-all

help:
	@echo "Sistema de Gestión de Citas Médicas"
	@echo "Comandos disponibles:"
	@echo "  make status   - Ver estado de contenedores"
	@echo "  make logs     - Ver logs en tiempo real"
	@echo "  make info     - Ver información de conexión"
	@echo "  make test     - Ejecutar todos los tests"
	@echo "  make test-validators - Tests de validadores"
	@echo "  make test-models     - Tests de modelos"

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

test:
	@echo "Ejecutando todos los tests..."
	@python3 tests/run_tests.py

test-validators:
	@echo "Ejecutando tests de validadores..."
	@python3 -m pytest tests/test_validators.py -v 2>/dev/null || python3 tests/run_tests.py

test-models:
	@echo "Ejecutando tests de modelos..."
	@python3 -m pytest tests/test_integration.py -v 2>/dev/null || python3 tests/run_tests.py

test-all:
	@echo "Ejecutando suite completa de tests..."
	@python3 -m pytest tests/ -v 2>/dev/null || python3 tests/run_tests.py
