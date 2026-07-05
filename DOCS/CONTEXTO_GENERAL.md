# Fundación Cataure — Contexto General del Proyecto

## Stack Tecnológico
- **Backend**: Django 5.2.3 + PostgreSQL
- **Frontend**: HTML templates Django + CSS propio (sin frameworks) + JavaScript vanilla
- **Dependencias**: `Django>=5.2`, `django-environ`, `psycopg2-binary`, `Pillow`

## Estructura del Proyecto
```
Fototeca/
├── Fototeca/                    # Config principal Django
│   ├── settings.py             # DB, apps, middleware, static, context processors
│   ├── urls.py                 # Rutas raíz (admin, auth, management_module)
│   ├── wsgi.py / asgi.py
├── management_module/           # App principal (galería, modelos)
│   ├── models.py               # Autores, Colecciones, Fotografias, Materias, Personas, etc.
│   ├── views.py                # inicio(), galeria() con trigram search + paginación
│   ├── admin.py                # Admin personalizado con inlines
│   ├── urls.py                 # / (inicio), /galeria/
│   ├── management/commands/    # vincular_imagenes (batch image linker por signatura)
│   ├── static/
│   │   ├── css/
│   │   │   └── estilos.css     # Único CSS: design tokens, layout, componentes, responsive
│   │   ├── js/
│   │   │   └── galeria.js      # Hero slider, lightbox, hamburger, toggle filtros
│   │   └── img/                # Imágenes estáticas (slider1, slider2, slider3, muestra)
│   └── templates/app_fotos/
│       ├── base.html           # Layout base (header con logo, nav, footer)
│       ├── inicio.html         # Homepage con hero slider, cards, valores, CTA
│       └── galeria.html        # Galería con buscador, filtros, grid, lightbox
├── authentication_module/       # App de autenticación
│   ├── views.py                # register()
│   ├── urls.py                 # /auth/login/, /auth/logout/, /auth/register/
│   └── templates/auth/
│       ├── login.html
│       └── register.html
├── media/                      # Archivos subidos (imágenes) — ignorado por git
│   ├── fotos_patrimonio/       # Fotografías patrimoniales
│   └── images/                 # Logo de la fundación (Cataure, logotipo, ocre.png)
├── DOCS/                       # Documentación y contexto
├── requirements.txt
├── opencode.json               # Config permisos opencode
└── AGENTS.md                   # Reglas para la IA
```

## Modelo de Datos (PostgreSQL)
```
autores(id, nombre)
colecciones(id, nombre)
materias(id, nombre)
personas(id, nombre)
municipios(id, nombre)
localidades(id, nombre, municipio_id → municipios)
lugares(id, nombre, localidad_id → localidades)
fotografias(signatura PK, titulo, descripcion, anio, foto, 
            autor_fondo_id → autores, autor_id → autores, 
            coleccion_id → colecciones, lugar_id → lugares)
fotografias_materias(fotografia_signatura → fotografias, materia_id → materias)
fotografias_personas(fotografia_signatura → fotografias, persona_id → personas)
```

## Diseño Visual — Sistema "Cataure"

### Paleta de colores
- **Navy oscuro** `#1A1F2B` — Header, footer, fondos oscuros
- **Navy medio** `#252C3E` — Variante de fondo oscuro
- **Crema** `#F5F0E8` — Fondo de página
- **Crema claro** `#FAF7F1` — Fondos de inputs
- **Ocre** `#C4934A` — Acento principal (botones, hover states, bordes decorativos)
- **Ocre claro** `#D4A85C` — Hover de enlaces
- **Ocre oscuro** `#9E763B` — Hover de botones
- **Blanco** `#FFFFFF` — Tarjetas, contenido
- **Texto principal** `#2D2D2D`
- **Texto secundario** `#6B6B6B`

### Tipografía
- **Títulos**: Playfair Display (serif, 600/700 weight) — Google Fonts
- **Cuerpo**: Inter (sans-serif, 300/400/500 weight) — Google Fonts

### Layout
- **Header**: Sticky, 72px de alto, fondo navy oscuro con borde inferior ocre de 2px. Logo + nav centrado + acciones (login/register).
- **Homepage**: Hero slider full-width con overlay degradado y dots. Sección "Explorar" (grid 4 cards con zoom hover). Sección "Valores" (3 columnas con íconos circulares). CTA final con fondo navy oscuro.
- **Galería**: Sidebar de filtros a la izquierda (sticky, 280px), grid de fotos a la derecha (3 columnas). Breadcrumb arriba. Search bar integrada.
- **Lightbox**: Fondo negro 95% con blur. Relación 65/35 imagen/metadata. Navegación entre fotos (anterior/siguiente + teclado).

### Componentes clave
- **Botones**: Primary (ocre sólido), Outline (ocre borde), Outline-dark (ocre borde sobre claro)
- **Cards galería**: Sombra sutil, overlay degradado en hover, zoom de imagen, metadatos con tags
- **Header nav**: Subrayado animado (ancho 0 → 100% en hover), active state ocre
- **Formularios auth**: Tarjeta blanca centrada, inputs con borde sutil y focus glow ocre
- **Paginación**: Números con borde, current page en ocre sólido

### Responsive
- **Desktop (>1024px)**: Sidebar fijo, grid 3 columnas
- **Tablet (640-1024px)**: Sidebar colapsable con botón toggle, grid 2 columnas
- **Móvil (<640px)**: Header 64px, hamburger menu, grid 1 columna, hero 60vh

### Accesibilidad
- Contraste suficiente entre fondos y textos
- `focus-visible` con outline ocre
- `prefers-reduced-motion` desactiva animaciones
- `aria-label` en controles (hamburger, dots, lightbox nav)
- Navegación por teclado en lightbox (Escape, flechas)

## Archivos del Diseño Actual

| Archivo | Rol |
|---|---|
| `static/css/estilos.css` | Sistema de diseño completo (~600 líneas, un solo archivo) |
| `static/js/galeria.js` | Interactividad: slider, lightbox, hamburger, toggle filtros |
| `templates/app_fotos/base.html` | Layout base con header/footer |
| `templates/app_fotos/inicio.html` | Homepage con hero slider |
| `templates/app_fotos/galeria.html` | Galería con lightbox integrado |
| `templates/auth/login.html` | Login (sin inline styles, usa clases CSS) |
| `templates/auth/register.html` | Registro (sin inline styles, usa clases CSS) |

## Comandos Útiles
- `python3 manage.py runserver` — Iniciar servidor
- `python3 manage.py check` — Verificar errores
- `python3 manage.py makemigrations` — Crear migraciones
- `python3 manage.py migrate` — Aplicar migraciones

## Reglas Importantes
- NO modificar la base de datos sin permiso explícito
- NO subir archivos `.env*` al repositorio
- Una tarea a la vez; al terminar, reportar cambios
- Las imágenes están en `media/fotos_patrimonio/` y `media/images/`
- El logo de la fundación está en `media/images/Cataure, logotipo, ocre.png`
