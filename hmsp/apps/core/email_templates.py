from django.template.loader import render_to_string


def render_evento_email(evento, suscriptor=None, logo_url=None):
    return render_to_string('core/email_evento.html', {
        'evento': evento,
        'suscriptor': suscriptor,
        'logo_url': logo_url,
        'url_cancelar': 'https://hmsp.cl/suscripcion/'
    })

def render_noticia_email(noticia, suscriptor=None, logo_url=None):
    return render_to_string('core/email_noticia.html', {
        'noticia': noticia,
        'suscriptor': suscriptor,
        'logo_url': logo_url
    })
