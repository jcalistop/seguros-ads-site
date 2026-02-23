# ADS Corredores de Seguros — Sitio corporativo

Este repositorio contiene el código fuente del sitio web corporativo de ADS Corredores de Seguros. El propósito del proyecto es ofrecer una presencia online clara y comercial que permita a clientes conocer servicios, cotizar y contactarse fácilmente.

## Resumen comercial

- **Objetivo**: Presentar la oferta de seguros (personas, empresas, viajes, comunidades y vida), generar leads y facilitar pagos y contacto.
- **Audiencia**: Clientes particulares y empresas que buscan soluciones de seguros integradas.
- **Valor**: Navegación clara, acceso a cotizaciones y contacto por canales digitales gestionados desde el sitio.

## Qué incluye este repositorio

- Arquitectura de layouts e includes para mantener consistencia visual.
- Contenido dinámico gestionado en YAML bajo `_data/` (aseguradoras, categorías, productos, equipo y canales de contacto).
- Integraciones básicas SEO y sitemap para visibilidad en buscadores.

## Cómo editar contenido (para equipo no técnico)

- Textos y listas de productos se mantienen en archivos bajo `_data/` y páginas estáticas en la raíz del proyecto.
- Para actualizar canales de contacto (teléfono, WhatsApp, redes), editar `_data/social.yml`.
- Las páginas comerciales (por ejemplo, categorías de seguros) se actualizan directamente en los archivos HTML/Markdown del sitio.

## Flujo de publicación

- El sitio está pensado para desplegarse en GitHub Pages mediante acciones CI/CD o mediante cualquier servicio de hosting de sitios estáticos.
- Los cambios en la rama principal pueden publicarse automáticamente si la configuración de Actions está habilitada.

## Buenas prácticas para el contenido

- Evitar exponer datos personales o sensibles dentro de archivos de documentación pública. Mantener contactos oficiales centralizados en `_data/social.yml`.
- Mantener logos y recursos gráficos en `assets/images/` usando nombres en minúsculas.

## Soporte y contacto

Para contacto comercial o soporte operativo, utilice la página `contacto.html` del sitio o los canales configurados en `_data/social.yml`.

## Contribuciones

Si desea contribuir (texto, correcciones o activos gráficos), abra un Pull Request con una descripción del cambio y su justificativo comercial.

---

Esta versión del `README` está enfocada a un público comercial y de producto. Para detalles técnicos de instalación y desarrollo, consulte las guías internas o pida acceso a la documentación de desarrolladores.
