from django.contrib import admin
from .models import (
    Autores, Colecciones, Fotografias, FotografiasMaterias, 
    FotografiasPersonas, Localidades, Lugares, Materias, 
    Municipios, Personas
)
from django.utils.html import format_html

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
class FotografiaAdmin(admin.ModelAdmin):
    # 1. Agrega 'foto' (o el método 'ver_miniatura') a la lista de columnas visibles
    list_display = ('signatura', 'ver_miniatura', 'titulo', 'autor', 'anio') 
    
    # 2. Agrega campos por los que puedas buscar o filtrar si lo deseas
    search_fields = ('signatura', 'titulo', 'autor')
    list_filter = ('autor',)

    # 3. Método personalizado para renderizar la miniatura de la foto de forma segura en el panel
    def ver_miniatura(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="width: 50px; height: auto; border-radius: 4px;" />', obj.foto.url)
        return "Sin foto"
    
    # Cambia el encabezado de la columna en el admin de Django
    ver_miniatura.short_description = 'Miniatura'


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
    
    
    
