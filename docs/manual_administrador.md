# Manual de Administración - Panel de Control HMSP

## Contenido
1. [Acceso al Panel](#acceso-al-panel)
2. [Gestión de Eventos](#gestión-de-eventos)
3. [Gestión de Noticias](#gestión-de-noticias)
4. [Gestión de Testimonios](#gestión-de-testimonios)
5. [Gestión de Oraciones](#gestión-de-oraciones)
6. [Gestión de Usuarios](#gestión-de-usuarios)
7. [Configuraciones](#configuraciones)
8. [Respaldo y Seguridad](#respaldo-y-seguridad)

## Acceso al Panel

### Ingreso al Sistema
- URL de acceso: `/admin/`
- Credenciales necesarias:
  - Usuario
  - Contraseña
- Recomendaciones de seguridad:
  - Usar contraseñas fuertes
  - No compartir credenciales
  - Cerrar sesión al terminar

## Gestión de Eventos

### Crear Nuevo Evento
1. Ir a "Eventos" > "Agregar Evento"
2. Campos obligatorios:
   - Título
   - Descripción
   - Fecha
   - Ubicación
   - Imagen Principal (recomendada)

### Requisitos de Imágenes
- **Formato**: JPG o PNG
- **Tamaño máximo**: 30MB
- **Dimensiones recomendadas**: 1200x800 píxeles
- **Proporción**: 3:2 (horizontal)
- **Resolución mínima**: 72 DPI
- **Consejos**:
  - Usar imágenes nítidas y bien iluminadas
  - Evitar imágenes con texto superpuesto
  - Preferir fotos horizontales para mejor visualización
  - Optimizar las imágenes antes de subirlas

### Configuración Multimedia
- **Tipos de contenido multimedia**:
  1. Ninguno
  2. Video de YouTube
  3. Video Local

#### Para Videos de YouTube
1. Seleccionar "Video de YouTube" en tipo multimedia
2. Pegar la URL del video de YouTube
3. El sistema convertirá automáticamente la URL al formato correcto

#### Para Videos Locales
1. Seleccionar "Video Local" en tipo multimedia
2. Subir archivo MP4
3. Recomendaciones:
   - Tamaño máximo: 100MB
   - Resolución recomendada: 1920x1080 o 1280x720
   - Formato: MP4 con codificación H.264
   - Duración recomendada: 30-60 segundos

### Preferencia de Visualización en Carrusel
Cuando un evento tiene tanto imagen como video, puede elegir qué contenido mostrar en el carrusel principal:

1. **Mostrar Imagen**: Se mostrará la imagen del evento en el carrusel, independientemente de si tiene video.
2. **Mostrar Video**: Se mostrará el video (YouTube o local) en el carrusel si está disponible.

Para configurar:
1. En el formulario del evento, buscar el campo "Preferencia de visualización"
2. Seleccionar la opción deseada:
   - "Mostrar Imagen" (opción por defecto)
   - "Mostrar Video"
3. Guardar los cambios

Esta configuración solo afecta la visualización en el carrusel principal. En la página de detalle del evento se mostrarán tanto la imagen como el video si están disponibles.

### Configuración del Formulario
- Campo opcional para URL de formulario de Google
- Se mostrará automáticamente en la página del evento

### Estado del Evento
- Activo: visible en el sitio
- Inactivo: oculto temporalmente

## Gestión de Noticias

### Crear Nueva Noticia
1. Acceder a "Noticias" > "Agregar Noticia"
2. Campos requeridos:
   - Título
   - Contenido
   - Imagen Principal

### Requisitos de Imágenes para Noticias
- **Formato**: JPG o PNG
- **Tamaño máximo**: 30MB
- **Dimensiones recomendadas**: 1600x900 píxeles
- **Proporción**: 16:9 (horizontal)
- **Resolución mínima**: 72 DPI
- **Consideraciones**:
  - Usar imágenes de alta calidad y relevantes al contenido
  - Evitar imágenes con marcas de agua o logos externos
  - Las imágenes deben ser horizontales para mantener consistencia
  - Optimizar el peso de la imagen antes de subirla
  - Respetar derechos de autor y usar imágenes propias o con licencia

### Opciones de Noticias
- Marcar como destacada
- Programar publicación
- Gestionar imágenes
- Estado de publicación

## Gestión de Testimonios

### Moderación de Testimonios
1. Revisar nuevos testimonios
2. Verificar contenido apropiado
3. Aprobar o rechazar
4. Editar si es necesario

### Criterios de Aprobación
- Contenido apropiado
- Información verificable
- Imágenes adecuadas

## Gestión de Oraciones

### Categorías
- Personal
- Familia
- Sanación
- Intercesión

### Administración
1. Agregar nuevas oraciones
2. Editar existentes
3. Organizar por categorías
4. Activar/Desactivar

## Gestión de Usuarios

### Roles de Usuario
1. **Superadministrador**:
   - Acceso total
   - Gestión de usuarios
   - Configuraciones del sistema

2. **Administrador**:
   - Gestión de contenido
   - Sin acceso a configuraciones críticas

3. **Editor**:
   - Crear/editar contenido
   - Sin acceso a configuraciones

### Crear Nuevos Usuarios
1. Ir a "Usuarios" > "Agregar Usuario"
2. Definir:
   - Nombre de usuario
   - Correo electrónico
   - Contraseña temporal
   - Rol/permisos

## Configuraciones

### Configuraciones del Sitio
- Información de contacto
- Redes sociales
- Correos de contacto
- Mensajes del sistema

### Configuraciones de Medios
- Tamaños máximos de archivo
- Tipos de archivo permitidos
- Optimización de imágenes

## Respaldo y Seguridad

### Respaldos
- Ubicación: `/backups/`
- Frecuencia: Diaria
- Contenido respaldado:
  - Base de datos
  - Archivos multimedia
  - Configuraciones

### Restauración
1. Acceder a la carpeta de respaldos
2. Seleccionar fecha
3. Seguir procedimiento de restauración

### Recomendaciones de Seguridad
1. **Contraseñas**:
   - Cambiar cada 90 días
   - Usar caracteres especiales
   - Mínimo 12 caracteres

2. **Acceso**:
   - Usar conexiones seguras
   - No compartir credenciales
   - Cerrar sesión al terminar

3. **Contenido**:
   - Verificar archivos antes de subir
   - Respetar derechos de autor
   - Mantener copias locales

## Solución de Problemas Comunes

### Problemas con Videos
1. **Video no se reproduce**:
   - Verificar formato (debe ser MP4)
   - Comprobar tamaño máximo
   - Revisar codificación

2. **Error al subir archivos**:
   - Verificar tamaño máximo permitido
   - Comprobar conexión
   - Revisar permisos

### Problemas de Acceso
1. Verificar credenciales
2. Limpiar caché del navegador
3. Contactar al administrador del sistema

## Mantenimiento

### Tareas Regulares
1. **Diarias**:
   - Revisar nuevos testimonios
   - Moderar comentarios
   - Verificar respaldos

2. **Semanales**:
   - Actualizar eventos
   - Publicar noticias
   - Revisar estadísticas

3. **Mensuales**:
   - Limpieza de archivos temporales
   - Verificar usuarios inactivos
   - Actualizar contenido estático

## Contacto de Soporte Técnico

Para problemas técnicos:
1. Correo: [correo del soporte técnico]
2. Teléfono: [número de soporte]
3. Horario de atención: [horario]

---

**Última actualización**: Octubre 2025

Este manual se actualizará según se implementen nuevas funcionalidades o cambios en el sistema.