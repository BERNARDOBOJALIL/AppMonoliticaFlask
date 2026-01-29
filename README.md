App Web Monolítica con Flask

https://github.com/BERNARDOBOJALIL/AppMonoliticaFlask.git

Descripción

Este proyecto consiste en una aplicación web monolítica desarrollada con Flask, utilizando Jinja como motor de templates para el frontend y SQLite como sistema de persistencia de datos.
La aplicación implementa un CRUD completo para la entidad Producto, así como un login ficticio con manejo de sesiones, cumpliendo con los requerimientos establecidos.

Funcionalidades
- Login ficticio con usuario definido.
- Protección de rutas del CRUD mediante sesión.
- CRUD de la entidad Producto.
- Persistencia en SQLite.

Validaciones mínimas
- El nombre del producto no puede estar vacío.
- El precio y el stock deben ser valores numéricos.
- El precio y el stock no pueden ser negativos.

Reflexión
1. ¿Qué quedó más acoplado en el monolito?
El mayor acoplamiento se encuentra entre la lógica de negocio, las rutas del backend, los templates.
2. ¿Qué separarías primero si lo migraras a API/microservicio?
Migraría la lógica del CRUD de productos y el acceso a la base de datos. Esto dejaría el frontend desacoplado y consumiría los datos mediante peticiones HTTP.
3. ¿Qué problemas surgen si dos equipos trabajan en paralelo en el mismo monolito?
Conflictos en archivos, dependencia entre frontend y backend y menor escalabilidad.

Ejecución
1. pip install flask
2. python app.py
