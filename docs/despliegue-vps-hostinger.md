# Guía de Despliegue Django en VPS Hostinger

## PARTE 1: Configuración Inicial del VPS

### 1. Acceder al VPS

```bash
# Desde tu PowerShell local
ssh root@tu-ip-del-vps
# Ingresa la contraseña que te envió Hostinger
```

### 2. Actualizar Sistema

```bash
# Actualizar paquetes
apt update && apt upgrade -y

# Instalar dependencias básicas
apt install -y python3 python3-pip python3-venv git nginx mysql-server supervisor curl
```

### 3. Crear Usuario para la Aplicación

```bash
# Crear usuario (no usar root para la app)
adduser hmsp
usermod -aG sudo hmsp

# Cambiar a ese usuario
su - hmsp
```

---

## PARTE 2: Configurar MySQL

### 4. Configurar Base de Datos

```bash
# Como root, acceder a MySQL
sudo mysql

# Dentro de MySQL:
CREATE DATABASE hmsp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'hmsp_user'@'localhost' IDENTIFIED BY 'TuPasswordSeguro123!';
GRANT ALL PRIVILEGES ON hmsp_db.* TO 'hmsp_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## PARTE 3: Configurar la Aplicación

### 5. Clonar Repositorio

```bash
# Como usuario hmsp
cd /home/hmsp
git clone https://github.com/lmgmuber-bit/HMSP.git
cd HMSP
```

### 6. Crear Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Instalar Gunicorn (servidor WSGI)
pip install gunicorn mysqlclient
```

### 7. Crear Configuración de Producción

```bash
# Crear archivo de configuración
nano hmsp/settings_prod.py
```

Pegar este contenido:

```python
from .settings import *
import os

DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com', 'tu-ip-del-vps']

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hmsp_db',
        'USER': 'hmsp_user',
        'PASSWORD': 'TuPasswordSeguro123!',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}

# Seguridad
SECRET_KEY = os.environ.get('SECRET_KEY', 'genera-una-clave-secreta-aqui')
SECURE_SSL_REDIRECT = False  # Cambiar a True cuando tengas SSL
SESSION_COOKIE_SECURE = False  # Cambiar a True cuando tengas SSL
CSRF_COOKIE_SECURE = False  # Cambiar a True cuando tengas SSL
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Archivos estáticos y media
STATIC_ROOT = '/home/hmsp/HMSP/staticfiles/'
MEDIA_ROOT = '/home/hmsp/HMSP/media/'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Email (configurar con tus datos)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@tudominio.com'
EMAIL_HOST_PASSWORD = 'tu-password-email'
DEFAULT_FROM_EMAIL = 'tu-email@tudominio.com'
```

Guardar: `Ctrl+O`, Enter, `Ctrl+X`

### 8. Migrar Base de Datos

```bash
# Activar entorno (si no está activo)
source venv/bin/activate

# Aplicar migraciones
python manage.py migrate --settings=hmsp.settings_prod

# Recopilar estáticos
python manage.py collectstatic --noinput --settings=hmsp.settings_prod

# Crear superusuario
python manage.py createsuperuser --settings=hmsp.settings_prod
```

### 9. Crear Directorios para Media

```bash
mkdir -p /home/hmsp/HMSP/media/eventos
mkdir -p /home/hmsp/HMSP/media/noticias
mkdir -p /home/hmsp/HMSP/media/testimonios
mkdir -p /home/hmsp/HMSP/media/configuracion
chmod -R 755 /home/hmsp/HMSP/media
```

---

## PARTE 4: Configurar Gunicorn

### 10. Crear Script de Inicio de Gunicorn

```bash
nano /home/hmsp/start_gunicorn.sh
```

Contenido:

```bash
#!/bin/bash
NAME="hmsp"
DIR=/home/hmsp/HMSP
USER=hmsp
GROUP=hmsp
WORKERS=3
BIND=unix:/home/hmsp/HMSP/gunicorn.sock
DJANGO_SETTINGS_MODULE=hmsp.settings_prod
DJANGO_WSGI_MODULE=hmsp.wsgi
LOG_LEVEL=error

cd $DIR
source venv/bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DIR:$PYTHONPATH

exec venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $WORKERS \
  --user=$USER \
  --group=$GROUP \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --log-file=-
```

Dar permisos:

```bash
chmod +x /home/hmsp/start_gunicorn.sh
```

### 11. Configurar Supervisor (para mantener Gunicorn corriendo)

```bash
# Como root
sudo nano /etc/supervisor/conf.d/hmsp.conf
```

Contenido:

```ini
[program:hmsp]
command=/home/hmsp/start_gunicorn.sh
user=hmsp
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/hmsp/HMSP/logs/gunicorn.log
stderr_logfile=/home/hmsp/HMSP/logs/gunicorn_error.log
```

Crear directorio de logs:

```bash
mkdir -p /home/hmsp/HMSP/logs
```

Activar Supervisor:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start hmsp
sudo supervisorctl status
```

---

## PARTE 5: Configurar Nginx

### 12. Crear Configuración de Nginx

```bash
sudo nano /etc/nginx/sites-available/hmsp
```

Contenido:

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com tu-ip-del-vps;

    client_max_body_size 10M;

    access_log /home/hmsp/HMSP/logs/nginx-access.log;
    error_log /home/hmsp/HMSP/logs/nginx-error.log;

    location /static/ {
        alias /home/hmsp/HMSP/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/hmsp/HMSP/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://unix:/home/hmsp/HMSP/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### 13. Activar Sitio

```bash
# Crear enlace simbólico
sudo ln -s /etc/nginx/sites-available/hmsp /etc/nginx/sites-enabled/

# Eliminar sitio default si existe
sudo rm /etc/nginx/sites-enabled/default

# Verificar configuración
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

---

## PARTE 6: Configurar SSL (HTTPS) con Let's Encrypt

### 14. Instalar Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 15. Obtener Certificado SSL

```bash
# Asegúrate de que tu dominio apunte a la IP del VPS
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

Sigue las instrucciones. Certbot configurará automáticamente Nginx para HTTPS.

### 16. Actualizar Settings para SSL

```bash
nano /home/hmsp/HMSP/hmsp/settings_prod.py
```

Cambiar:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 17. Reiniciar Servicios

```bash
sudo supervisorctl restart hmsp
sudo systemctl restart nginx
```

---

## PARTE 7: Configurar Firewall

### 18. Configurar UFW

```bash
# Habilitar firewall
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

---

## PARTE 8: Verificación

### 19. Probar el Sitio

1. Abre navegador: `http://tu-ip-del-vps` o `https://tu-dominio.com`
2. Verifica que cargue la página principal
3. Accede al admin: `https://tu-dominio.com/admin`
4. Prueba subir una imagen
5. Verifica formulario de contacto

---

## PARTE 9: Mantenimiento y Actualizaciones

### 20. Script para Actualizar

```bash
nano /home/hmsp/update.sh
```

Contenido:

```bash
#!/bin/bash
cd /home/hmsp/HMSP
git pull origin developer
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=hmsp.settings_prod
python manage.py collectstatic --noinput --settings=hmsp.settings_prod
sudo supervisorctl restart hmsp
```

Dar permisos:

```bash
chmod +x /home/hmsp/update.sh
```

Para actualizar en el futuro:

```bash
./update.sh
```

---

## PARTE 10: Backup Automático

### 21. Script de Backup

```bash
sudo nano /home/hmsp/backup.sh
```

Contenido:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/hmsp/backups"
mkdir -p $BACKUP_DIR

# Backup base de datos
mysqldump -u hmsp_user -p'TuPasswordSeguro123!' hmsp_db | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup media
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/hmsp/HMSP/media/

# Limpiar backups antiguos (más de 7 días)
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete
```

Dar permisos:

```bash
chmod +x /home/hmsp/backup.sh
```

### 22. Automatizar con Cron

```bash
crontab -e
```

Agregar (backup diario a las 2 AM):

```
0 2 * * * /home/hmsp/backup.sh
```

---

## PARTE 11: Monitoreo

### 23. Ver Logs

```bash
# Logs de Gunicorn
tail -f /home/hmsp/HMSP/logs/gunicorn.log

# Logs de Nginx
sudo tail -f /var/log/nginx/error.log

# Logs de aplicación
tail -f /home/hmsp/HMSP/logs/nginx-access.log
```

### 24. Estado de Servicios

```bash
# Ver estado Supervisor
sudo supervisorctl status

# Ver estado Nginx
sudo systemctl status nginx

# Ver estado MySQL
sudo systemctl status mysql
```

---

## Comandos Útiles de Referencia Rápida

```bash
# Reiniciar aplicación
sudo supervisorctl restart hmsp

# Reiniciar Nginx
sudo systemctl restart nginx

# Ver logs en tiempo real
tail -f /home/hmsp/HMSP/logs/gunicorn.log

# Actualizar aplicación
cd /home/hmsp/HMSP && git pull && ./update.sh

# Acceder a shell de Django
cd /home/hmsp/HMSP
source venv/bin/activate
python manage.py shell --settings=hmsp.settings_prod

# Ver procesos de Python
ps aux | grep python

# Ver uso de recursos
htop

# Reiniciar todo
sudo supervisorctl restart hmsp
sudo systemctl restart nginx
sudo systemctl restart mysql
```

---

## Solución de Problemas Comunes

### Error 502 Bad Gateway
```bash
# Verificar que Gunicorn esté corriendo
sudo supervisorctl status
# Si no está corriendo:
sudo supervisorctl start hmsp
```

### Error 500 Internal Server Error
```bash
# Ver logs de Gunicorn
tail -100 /home/hmsp/HMSP/logs/gunicorn_error.log
# Ver logs de Django
cd /home/hmsp/HMSP
source venv/bin/activate
python manage.py check --settings=hmsp.settings_prod
```

### Archivos estáticos no cargan
```bash
# Recopilar estáticos nuevamente
cd /home/hmsp/HMSP
source venv/bin/activate
python manage.py collectstatic --noinput --settings=hmsp.settings_prod
# Verificar permisos
sudo chown -R hmsp:hmsp /home/hmsp/HMSP/staticfiles
sudo chmod -R 755 /home/hmsp/HMSP/staticfiles
```

### No se pueden subir imágenes
```bash
# Verificar permisos de media
sudo chown -R hmsp:www-data /home/hmsp/HMSP/media
sudo chmod -R 775 /home/hmsp/HMSP/media
```

### Error de conexión a MySQL
```bash
# Verificar que MySQL esté corriendo
sudo systemctl status mysql
# Probar conexión
mysql -u hmsp_user -p
# Verificar credenciales en settings_prod.py
```

---

## Checklist de Despliegue

- [ ] VPS actualizado y configurado
- [ ] MySQL instalado y base de datos creada
- [ ] Usuario 'hmsp' creado
- [ ] Código clonado desde GitHub
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas (requirements.txt + gunicorn + mysqlclient)
- [ ] settings_prod.py configurado correctamente
- [ ] Migraciones aplicadas
- [ ] Superusuario creado
- [ ] Archivos estáticos recopilados
- [ ] Directorios de media creados con permisos
- [ ] Script start_gunicorn.sh creado y ejecutable
- [ ] Supervisor configurado y gunicorn corriendo
- [ ] Nginx configurado
- [ ] Sitio enlace simbólico creado
- [ ] Nginx probado y reiniciado
- [ ] SSL instalado con Certbot (opcional)
- [ ] Settings actualizados para SSL
- [ ] Firewall UFW configurado
- [ ] Sitio accesible desde navegador
- [ ] Admin funcional
- [ ] Subida de imágenes funcional
- [ ] Formulario de contacto funcional
- [ ] Script de actualización creado
- [ ] Script de backup creado
- [ ] Cron de backup configurado
- [ ] Logs funcionando correctamente

---

## Información de Contacto y Soporte

**Repositorio:** https://github.com/lmgmuber-bit/HMSP  
**Branch:** developer

**Servicios Corriendo:**
- Django: Puerto interno (socket Unix)
- Nginx: Puerto 80 (HTTP) y 443 (HTTPS)
- MySQL: Puerto 3306 (localhost)
- Gunicorn: Socket Unix en /home/hmsp/HMSP/gunicorn.sock

**Rutas Importantes:**
- Aplicación: `/home/hmsp/HMSP/`
- Entorno virtual: `/home/hmsp/HMSP/venv/`
- Logs: `/home/hmsp/HMSP/logs/`
- Estáticos: `/home/hmsp/HMSP/staticfiles/`
- Media: `/home/hmsp/HMSP/media/`
- Backups: `/home/hmsp/backups/`

**Usuarios:**
- Sistema: `hmsp`
- Base de datos: `hmsp_user`
- Django admin: (creado en paso 8)

---

## Notas Finales

1. **Seguridad**: Cambia todas las contraseñas por defecto
2. **Backups**: Los backups automáticos se ejecutan diariamente a las 2 AM
3. **SSL**: Renovación automática de certificados Let's Encrypt cada 90 días
4. **Actualizaciones**: Usa el script `./update.sh` para actualizar la aplicación
5. **Monitoreo**: Revisa los logs regularmente para detectar problemas

**¡Despliegue completo!** 🚀
