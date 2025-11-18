from PIL import Image, ImageDraw, ImageFont
import os

def create_misa_image():
    # Crear imagen para misa
    img = Image.new('RGB', (800, 400), '#e6f3ff')
    draw = ImageDraw.Draw(img)
    
    # Dibujar cruz
    draw.rectangle([385, 100, 415, 220], fill='#1e3799')  # Vertical
    draw.rectangle([340, 140, 460, 170], fill='#1e3799')  # Horizontal
    
    # Texto
    draw.text((400, 300), "Celebración Eucarística", fill='#1e3799', anchor="mm", font=None)
    
    return img

def create_retiro_image():
    # Crear imagen para retiro
    img = Image.new('RGB', (800, 400), '#fff4e6')
    draw = ImageDraw.Draw(img)
    
    # Dibujar biblia
    draw.rectangle([290, 100, 510, 250], fill='#8b4513')
    draw.rectangle([295, 105, 505, 245], fill='#d2691e')
    
    # Cruz en la biblia
    draw.rectangle([380, 140, 420, 210], fill='#8b4513')
    draw.rectangle([365, 155, 435, 195], fill='#8b4513')
    
    # Texto
    draw.text((400, 300), "Retiro Espiritual", fill='#8b4513', anchor="mm", font=None)
    
    return img

def create_oracion_image():
    # Crear imagen para oración
    img = Image.new('RGB', (800, 400), '#e8f5e9')
    draw = ImageDraw.Draw(img)
    
    # Círculo principal
    draw.ellipse([350, 150, 450, 250], outline='#558b2f', width=3)
    
    # Manos en oración (simplificado)
    draw.arc([370, 120, 430, 180], 0, 180, fill='#558b2f', width=3)
    
    # Texto
    draw.text((400, 300), "Jornada de Oración", fill='#558b2f', anchor="mm", font=None)
    
    return img

def create_juvenil_image():
    # Crear imagen para juventud
    img = Image.new('RGB', (800, 400), '#fce4ec')
    draw = ImageDraw.Draw(img)
    
    # Corazón simplificado
    draw.ellipse([350, 100, 450, 200], fill='#c2185b')
    
    # Cruz en el corazón
    draw.rectangle([390, 130, 410, 170], fill='white')
    draw.rectangle([370, 145, 430, 155], fill='white')
    
    # Texto
    draw.text((400, 300), "Encuentro Juvenil", fill='#c2185b', anchor="mm", font=None)
    
    return img

# Crear directorio si no existe
output_dir = 'static/img/ejemplos/'
os.makedirs(output_dir, exist_ok=True)

# Crear y guardar las imágenes
images = {
    'noticia-misa.jpg': create_misa_image(),
    'noticia-retiro.jpg': create_retiro_image(),
    'noticia-oracion.jpg': create_oracion_image(),
    'noticia-juvenil.jpg': create_juvenil_image()
}

for filename, img in images.items():
    img.save(os.path.join(output_dir, filename), 'JPEG', quality=95)