import json

def fix_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        # Asegurarse de que no hay BOM
        if content.startswith('\ufeff'):
            content = content[1:]
        # Verificar que el JSON es válido
        json.loads(content)  # Esto lanzará una excepción si el JSON no es válido
        # Guardar el archivo sin BOM
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed and validated {filename}")
        # Mostrar los primeros caracteres para verificación
        print(f"First few characters: {content[:50]}")
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filename}: {str(e)}")
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")

print("Starting JSON file fixing process...")
# Procesar todos los archivos
files = ['auth_user_clean.json', 'eventos_clean.json', 'noticias_clean.json', 'testimonios_clean.json']
for file in files:
    print(f"\nProcessing {file}...")
    fix_json_file(file)
print("\nJSON fixing process completed.")