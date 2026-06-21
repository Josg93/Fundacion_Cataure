from django.shortcuts import render
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity

def galeria(request):
    # Usamos el nuevo nombre del modelo
  #  archivos = ArchivoDigital.objects.all()
    
    # 1. Obtener parámetros de la URL
    query = request.GET.get('q', '')
    tipo_filtro = request.GET.get('tipo', '') # 'IMG', 'AUD', 'VID', 'DOC'
    lugar = request.GET.get('lugar', '')
    fecha = request.GET.get('fecha', '')
    coleccion_id = request.GET.get('coleccion', '')

    # 2. Lógica de Búsqueda General (Omnibuscador)
    if query:
        archivos = archivos.annotate(
            sim_titulo=TrigramSimilarity('titulo', query),
            sim_autor=TrigramSimilarity('autor', query),
            sim_colaborador=TrigramSimilarity('colaborador', query),
            sim_personas=TrigramSimilarity('personas', query),
            sim_lugar=TrigramSimilarity('lugar_orig', query),
            sim_coleccion=TrigramSimilarity('coleccion', query),
            sim_tema=TrigramSimilarity('tema', query),
            sim_fecha=TrigramSimilarity('fecha_descripcion', query),

        ).filter(
            Q(sim_titulo__gt=0.1) | 
            Q(sim_autor__gt=0.1) | 
            Q(sim_colaborador__gt=0.1) |
            Q(sim_personas__gt=0.1) |
            Q(sim_lugar__gt=0.1) |
            Q(sim_coleccion__gt=0.1) |
            Q(sim_tema__gt=0.1) |
            Q(sim_fecha__gt=0.1) |
            Q(codigo__icontains=query) |
            Q(codigo__icontains=query) # El código suele ser exacto, mejor icontains
        ).order_by('-sim_titulo')
    elif not request.GET:
        # Solo aleatorio si entra a la raíz de la galería sin filtros
        archivos = archivos.order_by('?')

    # 3. Aplicación de Filtros Específicos (No excluyen la búsqueda)
    if tipo_filtro:
        archivos = archivos.filter(tipo=tipo_filtro)
    if lugar:
        archivos = archivos.filter(lugar_orig__icontains=lugar)
    if fecha:
        archivos = archivos.filter(fecha_descripcion__icontains=fecha)
    if coleccion_id:
        archivos = archivos.filter(coleccion_id=coleccion_id)

    return render(request, 'app_fotos/galeria.html', {
        'archivos': archivos,
        'query': query,
        'tipo_actual': tipo_filtro,
     #   'colecciones': Coleccion.objects.all(),
      #  'tipos_disponibles': ArchivoDigital.TIPO_CHOICES # Para armar el menú de filtros
    })