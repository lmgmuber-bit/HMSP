from .models import ConfiguracionSitio

def configuracion_sitio(request):
    """
    Context processor para hacer la configuración del sitio
    disponible en todos los templates
    """
    return {
        'configuracion': ConfiguracionSitio.get_configuracion()
    }
