from django import template
import re

register = template.Library()

@register.filter(name='youtube_embed_url')
def youtube_embed_url(url):
    """Convierte una URL de YouTube en una URL de embebido."""
    if not url:
        return ''
    
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    
    if match:
        video_id = match.group(1)
        return f'https://www.youtube.com/embed/{video_id}?autoplay=0&controls=1&rel=0'
    return url