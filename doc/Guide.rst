=======================
 Proyecto 2: Web Consultancy
=======================

El primer proyecto consiste en la creación de una estructura de datos correspondiente a un árbol auto-balanceable, en este caso el AVL Tree, donde se implemente y pruebe el correcto funcionamiento de la misma. 


Integrantes
===========
* Ricardo Jiménez Anchía
* Laura Rincón Riveros

Documentación
=============

Esta guía de usuario consta de cuatro partes principales:

* Creación y uso del proyecto
* Estructura del proyecto.
* Vistas.


1. Creación y uso del proyecto
------------------------------
Dado que el proyecto utiliza compilación automática para construir el proyecto se puede hacer uso de la siguiente secuencia de comandos:
::

    make build
    make run
    make runserver

2. Estructura del proyecto.
-----------------------------------------
El proyecto Consultancy consisten de una única applicación llamada appointments y se encuentra estructurado de la siguiente manera:

| appointments
| ├── __init__.py 
| ├── admin.py
| ├── apps.py
| ├── forms.py
| ├── models.py
| ├── views.py
| ├── utils.py
| ├── static
| ├── templates

* Models: Estructuras de bases almacenados.
    * Client : usuario con información básica del cliente y datos como *username* o *password* para efectuar la dinámica de autenticación.
    * Project : Información del proyecto de consultoría que requiere de cita, cada proyecto posee un cliente relacionado.

* Views: Funciones que despliegan datos a las peticiones web.
    * New : Encargada de retornar formulario para crear un nuevo proyecto. En el caso del *admin*, despliega una opción adicional para escoger el usuario respectivo.
    * Modify : Retorna un formulario con los campos del proyecto que se desea modificar.
    * Check : Vista que contiene los proyectos de un usuario o de todos los usuarios, sea usuario tradicional o *admin*, respectivamente.
    * Delete : Lógica para eliminar un proyecto específico de la base de datos.
    * Signup : Registro de usuario nuevo. En caso de proveer permisos de *admin* al usuario nuevo, este debe ser registrado por un *admin*.

* Forms : Estructura de datos para los formularios de proyectos y clientes nuevos.
* Utils : Lógica para desplegar el calendario del mes con la citas reservadas.
* Templates : Archivos HTML necesarios para desplegar las vistas de index, login, check, new y signup.
* Static: Archivos de estilos e imágines utilizados en los *templates*.

