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

## Requisitos previos
- Python 3.7 o superior

## Dependencias
El proyecto utiliza las siguientes dependencias de Python:
```
blinker==1.9.0
click==8.3.1
colorama==0.4.6
Flask==3.1.2
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
Werkzeug==3.1.5
```

## Instrucciones de instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/BERNARDOBOJALIL/AppMonoliticaFlask.git
   cd AppMonoliticaFlask
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## Instrucciones de ejecución

1. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

2. **Acceder a la aplicación**
   - Abrir un navegador web y visitar: `http://localhost:5000`

3. **Credenciales de acceso ficticias de prueba**
   - Usuario: admin
   - Contraseña: 1234

## Estructura del proyecto
```
AppMonolitica/
│
├── app.py                 # Aplicación principal Flask
├── db.py                  # Configuración y gestión de base de datos
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Documentación del proyecto
└── templates/            # Plantillas HTML
    ├── index.html
    ├── login.html
    ├── producto_form.html
    └── productos.html
```

