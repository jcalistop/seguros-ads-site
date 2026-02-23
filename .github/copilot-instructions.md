# Copilot Instructions — ADS Corredores de Seguros (Jekyll)

## Proyecto

Sitio estático Jekyll migrado desde Laravel/Tabler.io. Se publica en GitHub Pages con dominio personalizado `segurosads.cl`. Sin build steps: Tailwind CSS vía CDN. Fuente original: repositorio de plantilla Jekyll.

## Comandos esenciales

```bash
# Servidor local (SIEMPRE usar --source y --destination para evitar build en subdirectorio equivocado)
bundle exec jekyll serve --source C:\laragon\www\seguros-ads-site --destination C:\laragon\www\seguros-ads-site\_site

# Build de producción
bundle exec jekyll build --source C:\laragon\www\seguros-ads-site --destination C:\laragon\www\seguros-ads-site\_site
```

> **CRÍTICO**: Ejecutar desde `C:\laragon\www\seguros-ads-site\`. Si el CWD fuera un subdirectorio, Jekyll construiría dentro de él generando artefactos contaminados.

## Arquitectura de layouts

Hay **dos layouts independientes** (no uno que hereda del otro):

| Layout                  | Usado por                              | Característica diferencial                                          |
| ----------------------- | -------------------------------------- | ------------------------------------------------------------------- |
| `_layouts/default.html` | Todas las páginas excepto seguros      | Completo: navbar + `{{ content }}` + footer                         |
| `_layouts/seguros.html` | Las 5 páginas de categorías de seguros | Auto-contenido (navbar+footer duplicados) + JS de búsqueda embebido |

`seguros.html` **duplica** navbar y footer deliberadamente para que el JS de búsqueda opere sin conflictos de scope con otras páginas.

## Datos dinámicos → `_data/`

Todos los datos de la BD de producción están en YAML:

- `_data/companies.yml` — 21 aseguradoras (campos: `name`, `logo`, `type`, `paid_link`)
- `_data/insurance_categories.yml` — 5 categorías (campos: `id`, `name`, `slug`, `icon`, `route`, `image`)
- `_data/insurances.yml` — Productos placeholder; **reemplazar con datos reales de BD** (campos: `title`, `slug`, `category`, `subtitle`, `body`)
- `_data/team.yml` — Equipo (6 miembros)
- `_data/social.yml` — Canales de contacto (WhatsApp, Instagram, Facebook). Mantener los datos de contacto centralizados aquí y evitar exponer números o datos personales en archivos públicos de documentación.

## Convenciones de rutas

- URLs con `relative_url`: `{{ '/pagar' | relative_url }}`, `{{ '/assets/images/logo.png' | relative_url }}`
- Imágenes en `assets/images/`, logos de aseguradoras en `assets/images/logos/` (todos **en minúsculas** — GitHub Pages corre en Linux)
- Si el logo de una aseguradoras está en mayúsculas en `_data/companies.yml`, fallará en producción

## Páginas de seguros — patrón estándar

```yaml
---
layout: seguros
title: Nombre de la Categoría
description: "..."
permalink: /slug-de-la-categoria
insurance_category: slug-de-la-categoria
---
{% assign items = site.data.insurances | where: "category", page.insurance_category %}
{% for item in items %}
<div class="insurance-card ..." data-title="{{ item.title | downcase }}">
  ...
</div>
{% endfor %}
```

El JS de búsqueda en `seguros.html` filtra por el atributo `data-title` de `.insurance-card`.

## Hero reutilizable

```liquid
{% include hero.html img="/assets/images/mapa-mundi.jpg" title="Conócenos" subtitle="Texto opcional" %}
```

El include vive en `_includes/hero.html` y usa `include.img`, `include.title`, `include.subtitle`.

## Formulario de contacto

`contacto.html` usa [Web3Forms](https://web3forms.com). El `access_key` está como placeholder `TU_ACCESS_KEY_AQUI` — reemplace con la clave asociada al canal administrativo de la empresa (ver `_data/social.yml`).

## Plugins activos

`jekyll-seo-tag` y `jekyll-sitemap` únicamente. `jekyll-feed` fue eliminado (sin blog activo). El `Gemfile.lock` está trackeado en git para builds reproducibles en CI.

## GitHub Actions / Deploy

`.github/workflows/jekyll.yml` hace deploy automático a GitHub Pages en push a `main`. El archivo `CNAME` contiene `segurosads.cl`.

## Tailwind config (ambos layouts)

Color primario: `#1a56db` (`primary`). Font: Inter (Google Fonts). Iconos: Tabler Icons webfont CDN — usar clases `ti ti-nombre-icono`.
