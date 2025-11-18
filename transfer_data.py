import os
import sys
import django
from django.core.management import call_command
from django.core.serializers.json import DjangoJSONEncoder
from io import StringIO

# Configurar el módulo de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hmsp.settings')

# Configurar Django
django.setup()

def export_app_data(app_label):
    filename = f'{app_label.replace(".", "_")}.json'  # Cambiado el nombre del archivo
    try:
        # Exportar datos a un StringIO primero para verificar
        output = StringIO()
        call_command('dumpdata', app_label, indent=2, stdout=output)
        
        # Obtener los datos y verificar que no estén vacíos
        data = output.getvalue()
        if data.strip() == '[]':
            print(f'No data found for {app_label}')
            return None
            
        # Guardar los datos en el archivo
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data)
            
        print(f'Successfully exported {app_label} to {filename}')
        print(f'Data preview: {data[:100]}...')  # Mostrar los primeros 100 caracteres
        return filename
    except Exception as e:
        print(f'Error exporting {app_label}: {str(e)}')
        # Si hubo error, intentar limpiar el archivo
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except:
            pass
        return None

def import_app_data(filename):
    if not filename or not os.path.exists(filename):
        print(f'File {filename} does not exist')
        return False
        
    try:
        # Leer y verificar el contenido del archivo
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            print(f'\nVerificando contenido de {filename}:')
            print(f'Primeros 200 caracteres: {content[:200]}')
            
        if not content or content == '[]':
            print(f'File {filename} is empty or contains no data')
            return False
            
        # Intentar cargar el archivo
        call_command('loaddata', filename, verbosity=2)  # Aumentado verbosity para más detalles
        print(f'Successfully loaded {filename}')
        return True
    except Exception as e:
        print(f'Error loading {filename}: {str(e)}')
        return False

if __name__ == '__main__':
    # Orden específico para la importación
    apps = [
        'auth.user',     # Primero usuarios
        'core',          # Luego core
        'backoffice'     # Finalmente backoffice
    ]
    
    success = True
    files_to_import = []
    
    # Primero exportamos todos los datos
    print("=== Exporting data ===")
    for app in apps:
        print(f"Exporting {app}...")
        filename = export_app_data(app)
        if filename and os.path.exists(filename):
            print(f"Verificando archivo {filename}...")
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content and content != '[]':
                    files_to_import.append(filename)
                    print(f"Archivo {filename} válido y contiene datos")
                else:
                    print(f"Archivo {filename} está vacío o solo contiene []")
        else:
            print(f"Error: No se pudo crear el archivo para {app}")
            success = False
            break
    
    # Si la exportación fue exitosa, procedemos con la importación
    if success and files_to_import:
        print("\n=== Importing data ===")
        for filename in files_to_import:
            if not import_app_data(filename):
                success = False
                break
        
        if success:
            print("\n=== Data transfer completed successfully ===")
        else:
            print("\n=== Data transfer failed ===")
    else:
        print("\n=== Export failed, skipping import ===")
    
    # Limpieza de archivos temporales
    print("\n=== Cleaning up temporary files ===")
    for filename in files_to_import:
        try:
            os.remove(filename)
            print(f"Removed {filename}")
        except Exception as e:
            print(f"Could not remove {filename}: {str(e)}")