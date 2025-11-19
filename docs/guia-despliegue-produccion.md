# Guía paso a paso para subir archivos y cambios a producción (HMSP)

## 1. Revisión y preparación de archivos
- Verifica que todos los cambios estén probados en el entorno de desarrollo.
- Asegúrate de que los archivos modificados estén guardados y sin errores.
- Revisa los siguientes archivos principales:
  - Código fuente: `hmsp/apps/core/models.py`, `hmsp/apps/core/views.py`, `hmsp/settings.py`, etc.
  - Templates: `templates/base.html`, `templates/core/*.html`, etc.
  - Archivos estáticos: `static/`, `media/`
  - Archivos de migración: `hmsp/apps/core/migrations/`
  - Archivos de traducción: `locale/`, `django.po`, `django.mo`
  - Requisitos: `requirements.txt`

## 2. Control de versiones (Git)
- Realiza commit de todos los cambios locales:
  ```powershell
  git add .
  git commit -m "Describe los cambios realizados"
  git push origin developerV2
  ```
- Haz merge a la rama principal si corresponde:
  ```powershell
  git checkout main
  git merge developerV2
  git push origin main
  ```

## 3. Backup y sincronización
- Realiza un backup de la base de datos y archivos importantes:
  - `db.sqlite3` o tu base de datos en uso
  - Carpeta `media/` y archivos estáticos
- Sincroniza los archivos con el servidor de producción (por ejemplo, usando `scp`, `rsync` o FTP):
  ```powershell
  scp -r . usuario@servidor:/ruta/proyecto/
  ```

## 4. Instalación de dependencias en producción
- Accede al servidor y activa el entorno virtual:
  ```powershell
  source .venv/bin/activate  # Linux
  .venv\Scripts\activate   # Windows
  ```
- Instala los requisitos:
  ```powershell
  pip install -r requirements.txt
  ```

## 5. Migraciones y compilación de traducciones
- Aplica migraciones:
  ```powershell
  python manage.py migrate
  ```
- Compila archivos de traducción:
  ```powershell
  python manage.py compilemessages
  ```

## 6. Recolección de archivos estáticos
- Ejecuta:
  ```powershell
  python manage.py collectstatic
  ```

## 7. Reinicio de servicios
- Reinicia el servidor web (Gunicorn, Supervisor, Nginx, etc.) según tu configuración:
  ```powershell
  sudo systemctl restart gunicorn
  sudo systemctl restart nginx
  ```

## 8. Verificación final
- Accede al sitio en producción y verifica:
  - Que los cambios estén reflejados
  - Que la búsqueda y traducción funcionen
  - Que no haya errores en los logs

---
**Notas:**
- Mantén siempre un backup antes de subir cambios críticos.
- Documenta los cambios realizados y notifica al equipo si es necesario.
- Si usas Docker, revisa el Dockerfile y reconstruye la imagen.

---
**Última actualización:** 19/11/2025
