# ============================================================================
# Startup Script - Medical Appointments Web Application
# ============================================================================

Write-Host ""
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  Sistema de Gestión de Citas Médicas - Iniciando Aplicación Web" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Verificando Docker..." -ForegroundColor Yellow
$dockerRunning = docker info 2>$null
if (-not $dockerRunning) {
    Write-Host "Error: Docker no está en ejecución" -ForegroundColor Red
    Write-Host "Por favor inicia Docker Desktop e intenta de nuevo" -ForegroundColor Red
    exit 1
}
Write-Host "Docker está corriendo" -ForegroundColor Green

# Start containers
Write-Host ""
Write-Host "Iniciando contenedores..." -ForegroundColor Yellow
docker compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error al iniciar contenedores" -ForegroundColor Red
    exit 1
}

# Wait for database
Write-Host ""
Write-Host "Esperando a que la base de datos esté lista..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Show logs
Write-Host ""
Write-Host "=================================================================" -ForegroundColor Green
Write-Host "  Aplicación Iniciada Exitosamente" -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "URL: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Database: localhost:5432" -ForegroundColor Cyan
Write-Host ""
Write-Host "Credenciales de prueba:" -ForegroundColor Yellow
Write-Host "  Admin: admin@clinica.com / Clinica2025!" -ForegroundColor White
Write-Host ""
Write-Host "Comandos útiles:" -ForegroundColor Yellow
Write-Host "  Ver logs:       docker compose logs -f app" -ForegroundColor White
Write-Host "  Detener:        docker compose down" -ForegroundColor White
Write-Host "  Reiniciar:      docker compose restart app" -ForegroundColor White
Write-Host ""
Write-Host "Abriendo navegador..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
Start-Process "http://localhost:5000"

Write-Host ""
Write-Host "Presiona Ctrl+C para ver los logs en tiempo real o Enter para salir" -ForegroundColor Yellow
$response = Read-Host

if ($response -eq "") {
    exit 0
}
else {
    docker compose logs -f app
}
