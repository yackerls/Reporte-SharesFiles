Contenido para tu README.md
Markdown
# 🛡️ Reporte-SharesFiles

Este proyecto permite auditar y visualizar de forma gráfica los permisos NTFS de carpetas compartidas en servidores Windows (probado en Windows Server 2008 R2). Utiliza un script de PowerShell para la extracción y una aplicación web en Python (Streamlit) corriendo en Docker para el análisis.

## 🚀 Estructura del Proyecto
* **Windows Server:** Script de PowerShell para generar el reporte CSV.
* **Docker/Portainer:** Contenedor Python que procesa y muestra los datos.
* **Interfaz Web:** Filtros dinámicos por Share y búsqueda de usuarios reales (excluye cuentas de sistema).

---

## 🛠️ Paso 1: Extracción en Windows Server
Ejecuta el siguiente script en PowerShell como Administrador en el servidor donde se encuentran los Shares. Este script creará la carpeta `C:\scripts` y generará el archivo `permisos_shares.csv`.

### **Script de PowerShell**
```powershell
# Crear directorio de trabajo
New-Item -ItemType Directory -Force -Path "C:\scripts"

# Definir ruta de salida
$outputPath = "C:\scripts\permisos_shares.csv"

# Obtener los recursos compartidos (Type 0 = Carpetas de usuario)
$shares = Get-WmiObject Win32_Share | Where-Object { $_.Type -eq 0 }
$results = New-Object System.Collections.Generic.List[PSCustomObject]

foreach ($share in $shares) {
    $path = $share.Path
    if (Test-Path $path) {
        try {
            $acl = Get-Acl $path
            foreach ($access in $acl.Access) {
                $obj = New-Object PSObject -Property @{
                    ShareName   = $share.Name
                    LocalPath   = $path
                    Identity    = $access.IdentityReference.ToString()
                    Rights      = $access.FileSystemRights.ToString()
                    AccessType  = $access.AccessControlType.ToString()
                    IsInherited = $access.IsInherited
                }
                $results.Add($obj)
            }
        } catch {
            Write-Warning "No se pudo acceder a: $path"
        }
    }
}

# Exportar a CSV para la web
$results | Export-Csv -Path $outputPath -NoTypeInformation -Encoding UTF8
Write-Host "Reporte generado en: $outputPath" -ForegroundColor Green
🐋 Paso 2: Despliegue en Docker (Linux)
Clonar el repositorio:

Bash
cd /opt
git clone [https://github.com/yackerls/Reporte-SharesFiles.git](https://github.com/yackerls/Reporte-SharesFiles.git)
cd Reporte-SharesFiles
Levantar el contenedor:

Bash
docker compose up -d --build
Acceso: Abre tu navegador en http://tu-ip-servidor:8050

📊 Características de la App
Carga Manual: Sube el CSV directamente desde el navegador.

Limpieza Automática: Se omiten grupos de sistema como SYSTEM, Administrators, Everyone, etc., para mostrar solo usuarios reales.

Buscador: Filtrado instantáneo por nombre de Share o usuario.

Gráficas: Visualización del Top 10 de usuarios con más acceso.

Autor: yackerls

Entorno: Infraestructura IT


---

### **¿Cómo subirlo a GitHub?**
Desde la consola de tu servidor o tu PC:
1. Crea el archivo: `nano README.md`
2. Pega el contenido de arriba.
3. Guarda y sube:
   ```bash
   git add README.md
   git commit -m "Add professional README with PowerShell script"
   git push origin main