from django.db import models

# =====================================================================
# 1. TABLAS MAESTRAS (SOPORTE Y METADATOS)
# =====================================================================

class Autores(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'autores'

    def __str__(self):
        return self.nombre or f"Autor #{self.id}"


class Colecciones(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'colecciones'

    def __str__(self):
        return self.nombre or f"Colección #{self.id}"


class Materias(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'materias'

    def __str__(self):
        return self.nombre


class Personas(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField(unique=True)

    class Meta:
        managed = True
        db_table = 'personas'

    def __str__(self):
        return self.nombre


# =====================================================================
# 2. TABLAS GEOGRÁFICAS
# =====================================================================

class Municipios(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField()

    class Meta:
        managed = True
        db_table = 'municipios'

    def __str__(self):
        return self.nombre


class Localidades(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField(blank=True, null=True)
    municipio = models.ForeignKey(Municipios, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'localidades'

    def __str__(self):
        return f"{self.nombre} ({self.municipio.nombre})"


class Lugares(models.Model):
    id = models.BigAutoField(primary_key=True)
    localidad = models.ForeignKey(Localidades, on_delete=models.CASCADE)
    nombre = models.TextField()

    class Meta:
        managed = True
        db_table = 'lugares'

    def __str__(self):
        return f"{self.nombre} - {self.localidad.nombre}"


# =====================================================================
# 3. MODELO PRINCIPAL (FOTOGRAFÍAS)
# =====================================================================

class Fotografias(models.Model):
    signatura = models.TextField(primary_key=True)
    titulo = models.TextField()
    descripcion = models.TextField(blank=True, null=True)
    anio = models.SmallIntegerField(blank=True, null=True)
    
    # Claves foráneas corregidas y con comportamiento controlado
    autor_fondo = models.ForeignKey(Autores, on_delete=models.SET_NULL, related_name='fotos_fondo_set', blank=True, null=True)
    autor = models.ForeignKey(Autores, on_delete=models.SET_NULL, related_name='fotografias_autor_set', blank=True, null=True)
    coleccion = models.ForeignKey(Colecciones, on_delete=models.SET_NULL, blank=True, null=True)
    lugar = models.ForeignKey(Lugares, on_delete=models.SET_NULL, related_name='fotografias_lugar_set', blank=True, null=True)

    # Relaciones Muchos a Muchos que utilizan las tablas intermedias existentes físicamente
    materias = models.ManyToManyField(Materias, through='FotografiasMaterias', related_name='fotografias')
    personas = models.ManyToManyField(Personas, through='FotografiasPersonas', related_name='fotografias')

    class Meta:
        managed = True
        db_table = 'fotografias'

    def __str__(self):
        return f"{self.signatura} - {self.titulo}"


# =====================================================================
# 4. TABLAS INTERMEDIAS REQUERIDAS POR POSTGRESQL (RELACIONES M2M)
# =====================================================================

class FotografiasMaterias(models.Model):
    id = models.BigAutoField(primary_key=True)  # Django requiere una PK única interna si actúan como intermediarias explícitas
    fotografia_signatura = models.ForeignKey(Fotografias, on_delete=models.CASCADE, db_column='fotografia_signatura')
    materia = models.ForeignKey(Materias, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'fotografias_materias'
        unique_together = (('fotografia_signatura', 'materia'),)


class FotografiasPersonas(models.Model):
    id = models.BigAutoField(primary_key=True)  # Django requiere una PK única interna si actúan como intermediarias explícitas
    fotografia_signatura = models.ForeignKey(Fotografias, on_delete=models.CASCADE, db_column='fotografia_signatura')
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'fotografias_personas'
        unique_together = (('fotografia_signatura', 'persona'),)
       
        
