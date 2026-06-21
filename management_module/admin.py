from django.contrib import admin
from .models import (
    Autores, Colecciones, Fotografias, FotografiasMaterias, 
    FotografiasPersonas, Localidades, Lugares, Materias, 
    Municipios, Personas
)

# =====================================================================
# 1. CONFIGURACIÓN DE TABLAS INTERMEDIAS (INLINES)
# =====================================================================
# Permiten gestionar relaciones Muchos a Muchos en la misma ficha de la fotografía.

class FotografiasMateriasInline(admin.TabularInline):
    model = FotografiasMaterias
    extra = 1  # Número de filas vacías para agregar nuevas materias rápidamente
    verbose_name = "Materia asociada"
    verbose_name_plural = "Materias de la fotografía"


class FotografiasPersonasInline(admin.TabularInline):
    model = FotografiasPersonas
    extra = 1  # Número de filas vacías para agregar nuevas personas rápidamente
    verbose_name = "Persona asociada"
    verbose_name_plural = "Personas en la fotografía"


# =====================================================================
# 2. CONFIGURACIÓN DEL MODELO PRINCIPAL (FOTOGRAFÍAS)
# =====================================================================

@admin.register(Fotografias)
class FotografiasAdmin(admin.ModelAdmin):
    # Columnas que aparecerán en la lista principal de fotos
    list_display = ('signatura', 'titulo', 'autor', 'anio', 'coleccion', 'lugar')
    
    # Filtros laterales rápidos para la segmentación del catálogo
    list_filter = ('anio', 'coleccion', 'autor', 'lugar__localidad__municipio')
    
    # Buscador de texto completo (busca en la firma, título, descripción y nombres relacionados)
    search_fields = ('signatura', 'titulo', 'descripcion', 'autor__nombre')
    
    # Orden predeterminado (por año descendente, las fotos más recientes primero)
    ordering = ('-anio',)
    
    # Inyección de los formularios intermedios (Materias y Personas)
    inlines = [FotografiasMateriasInline, FotografiasPersonasInline]


# =====================================================================
# 3. CONFIGURACIÓN DE TABLAS MAESTRAS (METADATOS)
# =====================================================================

@admin.register(Autores)
class AutoresAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Colecciones)
class ColeccionesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Materias)
class MateriasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Personas)
class PersonasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('nombre',)


# =====================================================================
# 4. CONFIGURACIÓN DE UBICACIONES GEOGRÁFICAS
# =====================================================================

@admin.register(Municipios)
class MunicipiosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Localidades)
class LocalidadesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'municipio')
    list_filter = ('municipio',)
    search_fields = ('nombre', 'municipio__nombre')
    ordering = ('nombre',)


@admin.register(Lugares)
class LugaresAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'get_localidad', 'get_municipio')
    search_fields = ('nombre', 'localidad__nombre')
    list_filter = ('localidad__municipio',)
    ordering = ('nombre',)

    # Métodos personalizados para aplanar la información geográfica en la tabla principal de Lugares
    def get_localidad(self, obj):
        return obj.localidad.nombre
    get_localidad.short_description = 'Localidad'

    def get_municipio(self, obj):
        return obj.localidad.municipio.nombre
    get_municipio.short_description = 'Municipio'
    
    
    
