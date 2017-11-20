# Proyecto de Grado 2017

## Informe

Links al informe en Overleaf:
* Ver: https://www.overleaf.com/read/bywzptctqyzp

Para generar datos:
* Editar el archivo `generar_jobs.py` modificando las variables de configuración para definir cosas como los tipos de problemas a generar, directorios a utilizar y demás.
* Ese archivo va a generar scripts de bash en el directorio definido en la variable de configuración `OUTPUT_PATH` (`./jobs/` por defecto), que a su vez se pueden ejecutar para generar los datos. Estos datos se van a generar de acuerdo a las variables `GENERATOR_DIR` y `PARSER_DIR` definidas también en el primer script de Python.
* Una vez que se ejecuta uno o todos los scripts generados por `generar_jobs.py`, se van a tener los datos prontos para utilizar a la hora de generar clasificadores, en el directorio definido por `PARSE_DIR`.

Próximamente:
* El código contenido en el Python notebook va a pasarse a formato script, para que recibiendo parámetros del problema a estudiar (y el tipo de clasificador que se desea utilizar), genere y persista clasificadores, y además evalúe su performance devolviendo valores de makespan, accuracy y tiempo de ejecución a la hora de generarse.
