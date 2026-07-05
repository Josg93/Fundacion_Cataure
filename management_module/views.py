from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q, TextField, Value, Prefetch, Exists, OuterRef
from django.db.models.functions import Cast, Coalesce, Greatest
from django.contrib.postgres.search import TrigramSimilarity
from management_module.models import Fotografias, Materias, Personas, Colecciones, FotografiasMaterias, FotografiasPersonas

def inicio(request):
    return render(request, "app_fotos/inicio.html")

def galeria(request):
    query = request.GET.get('q', '').strip()
    lugar = request.GET.get('lugar', '')
    coleccion_id = request.GET.get('coleccion', '')

    fotos_qs = Fotografias.objects.select_related(
        'autor_fondo', 'autor', 'coleccion', 'lugar'
    ).prefetch_related(
        Prefetch('materias', queryset=Materias.objects.only('nombre')),
        Prefetch('personas', queryset=Personas.objects.only('nombre')),
    )

    if query and len(query) >= 3:
        materias_exist = FotografiasMaterias.objects.filter(
            fotografia_signatura=OuterRef('signatura'),
            materia__nombre__trigram_similar=query,
        )
        personas_exist = FotografiasPersonas.objects.filter(
            fotografia_signatura=OuterRef('signatura'),
            persona__nombre__trigram_similar=query,
        )

        texto_vacio_sql = Cast(Value(''), TextField())
        fotos_qs = fotos_qs.annotate(
            sim_titulo=TrigramSimilarity(Coalesce('titulo', texto_vacio_sql), query),
            sim_signatura=TrigramSimilarity(Coalesce('signatura', texto_vacio_sql), query),
            sim_descripcion=TrigramSimilarity(Coalesce('descripcion', texto_vacio_sql), query),
            sim_anio=TrigramSimilarity(Coalesce(Cast('anio', TextField()), texto_vacio_sql), query),
            sim_autor_fondo=TrigramSimilarity(Coalesce('autor_fondo__nombre', texto_vacio_sql), query),
            sim_autor=TrigramSimilarity(Coalesce('autor__nombre', texto_vacio_sql), query),
            sim_coleccion=TrigramSimilarity(Coalesce('coleccion__nombre', texto_vacio_sql), query),
            sim_lugar=TrigramSimilarity(Coalesce('lugar__nombre', texto_vacio_sql), query),
        ).annotate(
            max_similitud=Greatest(
                'sim_titulo', 'sim_signatura', 'sim_descripcion', 'sim_anio',
                'sim_autor_fondo', 'sim_autor', 'sim_coleccion', 'sim_lugar',
            )
        ).filter(
            Q(sim_titulo__gt=0.1) | Q(sim_signatura__gt=0.1) |
            Q(sim_descripcion__gt=0.1) | Q(sim_anio__gt=0.1) |
            Q(sim_autor_fondo__gt=0.1) | Q(sim_autor__gt=0.1) |
            Q(sim_coleccion__gt=0.1) | Q(sim_lugar__gt=0.1) |
            Q(Exists(materias_exist)) | Q(Exists(personas_exist))
        ).order_by('-max_similitud')
    elif not request.GET:
        fotos_qs = fotos_qs.order_by('?')

    if lugar:
        fotos_qs = fotos_qs.filter(lugar__nombre__icontains=lugar)
    if coleccion_id:
        fotos_qs = fotos_qs.filter(coleccion_id=coleccion_id)

    paginator = Paginator(fotos_qs, 20)
    page_number = request.GET.get('page', 1)
    fotos = paginator.get_page(page_number)

    colecciones = Colecciones.objects.all().order_by('nombre')

    return render(request, 'app_fotos/galeria.html', {
        'fotos': fotos,
        'colecciones': colecciones,
    })