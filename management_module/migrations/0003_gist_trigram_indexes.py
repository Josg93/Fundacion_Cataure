from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('management_module', '0002_setup_extensions'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS fotografias_titulo_trgm_idx
                ON fotografias USING GIST (titulo gist_trgm_ops);
            CREATE INDEX IF NOT EXISTS fotografias_signatura_trgm_idx
                ON fotografias USING GIST (signatura gist_trgm_ops);
            CREATE INDEX IF NOT EXISTS fotografias_descripcion_trgm_idx
                ON fotografias USING GIST (descripcion gist_trgm_ops);
            CREATE INDEX IF NOT EXISTS autores_nombre_trgm_idx
                ON autores USING GIST (nombre gist_trgm_ops);
            CREATE INDEX IF NOT EXISTS colecciones_nombre_trgm_idx
                ON colecciones USING GIST (nombre gist_trgm_ops);
            CREATE INDEX IF NOT EXISTS lugares_nombre_trgm_idx
                ON lugares USING GIST (nombre gist_trgm_ops);
            """,
            reverse_sql="""
            DROP INDEX IF EXISTS fotografias_titulo_trgm_idx;
            DROP INDEX IF EXISTS fotografias_signatura_trgm_idx;
            DROP INDEX IF EXISTS fotografias_descripcion_trgm_idx;
            DROP INDEX IF EXISTS autores_nombre_trgm_idx;
            DROP INDEX IF EXISTS colecciones_nombre_trgm_idx;
            DROP INDEX IF EXISTS lugares_nombre_trgm_idx;
            """,
        ),
    ]
