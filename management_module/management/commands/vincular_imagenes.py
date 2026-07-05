import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files import File
from django.db.models import Q
from management_module.models import Fotografias

class Command(BaseCommand):
    help = 'Vincula las imágenes del disco con los registros de la base de datos usando la signatura'

    def handle(self, *args, **options):
        ruta_origen = os.path.join(settings.MEDIA_ROOT, 'images')
        
        # Extensiones de imagen soportadas
        extensiones = ['.jpg', '.jpeg', '.png', '.JPG', '.PNG']
        
        # 1. Buscamos registros donde el campo 'foto' esté vacío o nulo
        registros_pendientes = Fotografias.objects.filter(Q(foto__isnull=True) | Q(foto__exact=''))
        
        self.stdout.write(self.style.SUCCESS(f"Se encontraron {registros_pendientes.count()} registros pendientes por vincular."))
        
        exitos = 0
        errores = 0

        for registro in registros_pendientes:
            # Usamos el campo 'signatura' como nombre del archivo (asumiendo que se llama 'signatura')
            nombre_base_archivo = str(registro.signatura).strip()
            archivo_encontrado = None
            ext_encontrada = ""

            # Probamos con las diferentes extensiones en la carpeta
            for ext in extensiones:
                nombre_completo = f"{nombre_base_archivo}{ext}"
                ruta_completa_imagen = os.path.join(ruta_origen, nombre_completo)
                
                if os.path.exists(ruta_completa_imagen):
                    archivo_encontrado = ruta_completa_imagen
                    ext_encontrada = ext
                    break
            
            if archivo_encontrado:
                try:
                    # 2. Abrimos el archivo físicamente
                    with open(archivo_encontrado, 'rb') as f:
                        archivo_django = File(f)
                        # 3. La magia de Django: guarda el archivo en el destino final 
                        # configurado en tu modelo y actualiza la base de datos de Postgres.
                        nombre_guardado = f"{nombre_base_archivo}{ext_encontrada}"
                        registro.foto.save(nombre_guardado, archivo_django, save=True)
                        
                    self.stdout.write(self.style.SUCCESS(f"✔ Vinculado: {nombre_base_archivo}"))
                    exitos += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ Error al guardar {nombre_base_archivo}: {str(e)}"))
                    errores += 1
            else:
                self.stdout.write(self.style.WARNING(f"⚠ Archivo no encontrado para la signatura: {nombre_base_archivo}"))
                errores += 1

        self.stdout.write(self.style.SUCCESS(f"\nProceso terminado. Éxitos: {exitos} | No vinculados: {errores}"))