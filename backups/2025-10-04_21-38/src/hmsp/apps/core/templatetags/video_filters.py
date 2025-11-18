from django import template
import re

register = template.Library()

@register.filter
def youtube_embed_url(url):
    """
    Convierte una URL de YouTube en una URL de embebido.
    Soporta varios formatos de URL de YouTube.
    """
    youtube_regex = (
        r'(?:https?:\/\/)?'
        r'(?:www\.)?'
        r'(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)'
        r'([a-zA-Z0-9_-]{11})'
    )
    
    match = re.search(youtube_regex, url)
    if match:
        video_id = match.group(1)
        return f'https://www.youtube.com/embed/{video_id}?autoplay=0&controls=1&rel=0'
    return url