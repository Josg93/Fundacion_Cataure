import os
from django.core.management.base import BaseCommand
from django.core.files import File
from management_module.models import Fotografias  # Asegúrate de usar el nombre correcto de tu app

class Command(BaseCommand):
    help = 'Vincula las imágenes de la carpeta temporal con los registros de la base de datos usando la signatura'

    def handle(self, *args, **options):
        # Ruta donde tienes guardadas tus imágenes actualmente
        ruta_imagenes = '/home/laptop/Escritorio/Desarrollo de software y portafolio/Proyecto Fundación Cataure/Fototeca/media/images'
        
        if not os.path.exists(ruta_imagenes):
            self.stdout.write(self.style.ERROR(f"La ruta especificada no existe: {ruta_imagenes}"))
            return

        # Listar todos los archivos en esa carpeta
        archivos_en_carpeta = os.listdir(ruta_imagenes)
        
        # Mapear los archivos eliminando la extensión para comparar con la signatura
        # Ejemplo: {"abc123xyz": "abc123xyz.jpg"}
        mapa_imagenes = {}
        for archivo in archivos_en_carpeta:
            nombre_sin_extension, _ = os.path.splitext(archivo)
            mapa_imagenes[nombre_sin_extension] = archivo

        # Obtener los registros que aún no tienen foto asignada
        registros_pendientes = Fotografias.objects.filter(foto__isnull=True) | Fotografias.objects.filter(foto='')
        
        total_registros = registros_pendientes.count()
        self.stdout.write(self.style.SUCCESS(f"Se encontraron {total_registros} registros sin imagen asociada."))

        vinculados = 0
        no_encontrados = 0

        for registro in registros_pendientes:
            # Limpiamos espacios en blanco por si acaso en la signatura de la BD
            signatura = str(registro.signatura).strip() if registro.signatura else None

            if signatura in mapa_imagenes:
                nombre_archivo_real = mapa_imagenes[signatura]
                ruta_completa_archivo = os.path.join(ruta_imagenes, name=nombre_archivo_real)

                # Abrimos el archivo físico en modo lectura binaria
                with open(ruta_completa_archivo, 'rb') as f:
                    django_file = File(f)
                    # El método .save() guarda físicamente el archivo en MEDIA_ROOT/fundacion_fotos/
                    # y actualiza automáticamente la ruta en la base de datos PostgreSQL
                    registro.foto.save(nombre_archivo_real, django_file, save=True)
                
                vinculados += 1
                self.stdout.write(self.style.SUCCESS(f"✔ Vinculado: Registro {registro.id} con {nombre_archivo_real}"))
            else:
                no_encontrados += 1
                self.stdout.write(self.style.WARNING(f"⚠ No se encontró archivo para la signatura: '{signatura}'"))

        self.stdout.write(self.style.SUCCESS(
            f"\n--- Proceso Finalizado ---\n"
            f"Imágenes vinculadas exitosamente: {vinculados}\n"
            f"Registros cuyas imágenes no se encontraron en la carpeta: {no_encontrados}"
        ))