from django import template

register = template.Library()

@register.filter
def youtube_embed_url(url):
    if not url:
        return ''
    if 'youtube.com/watch?v=' in url:
        video_id = url.split('watch?v=')[1]
        if '&' in video_id:
            video_id = video_id.split('&')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    elif 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[1]
        if '?' in video_id:
            video_id = video_id.split('?')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    return url