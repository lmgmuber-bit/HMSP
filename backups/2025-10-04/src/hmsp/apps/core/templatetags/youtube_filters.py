from django import template
import re

register = template.Library()

@register.filter
def youtube_embed_url(url):
    """
    Convierte una URL de YouTube en una URL de embebido.
    Soporta varios formatos de URL de YouTube.
    """
    if not url:
        return ''
        
    # Patrones de URL de YouTube
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            video_id = match.group(1)
            return f'https://www.youtube.com/embed/{video_id}?autoplay=0&controls=1&rel=0'
    
    return url  # Retorna la URL original si no coincide con ningún patrón