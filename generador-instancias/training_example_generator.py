# coding = utf-8
'''
Script para generar ejemplos de entrenamiento de la forma i.input e i.output (archivos)
La idea es setear los parametros en este archivo para determinar el tipo de instancia
de HCSP, y se generan tantas instancias de entrenamiento (par de archivos) como
se quiera
'''
import os
import re
import commands
import sys
import time

import generar_jobs

# Comando para llamar al generador de instancias
GENERATOR_COMMAND = './generator'
# Comando para llamar al resolvedor de instancias del problema
SOLVER_COMMAND = './heuristica-resolucion-hcsp'
SEPARATOR = ' '
# Tipos de archivo de las salidas
INPUT_SUFFIX = '.in'
OUTPUT_SUFFIX = '.out'
MOVE_COMMAND = 'mv'

def main():
    # Se obtienen caracteristicas del problema de consola
    try:
        task_amount = int(sys.argv[1])
        machine_amount = int(sys.argv[2])
        task_heterogeneity_type = int(sys.argv[3])
        machine_heterogeneity_type = int(sys.argv[4])
        consistency_type = int(sys.argv[5])
        amount_of_instances = int(sys.argv[6])
        output_path = str(sys.argv[7])
    except Exception:
        print 'Uso del script: python training_example_generator.py cantidad-tareas \
			cantidad-maquinas heterogeneidad-tareas heterogeneidad-maquinas \
			tipo-consistencia cantidad-instancias directorio-salida'
        print '### Tipos ###'
        print 'cantidad-tareas : int'
        print 'cantidad-maquinas : int'
        print 'heterogeneidad-tareas : 0 = Low, 1 = High'
        print 'heterogeneidad-maquinas : 0 = Low, 1 = High'
        print 'tipo-consistencia : 0 = Consistent, 1 = Semiconsistent, 2 = Inconsistent'
        print 'cantidad-instancias : int'
        print 'directorio-salida : str'
        print 'Ejemplo: python training_example_generator.py 4 16 0 0 0 100 \
			ejemplos-entrenamiento-separados/4x16-000/test/'
    for i in range(0, amount_of_instances):
        # Se genera instancia del problema
        status, output = commands.getstatusoutput(\
        GENERATOR_COMMAND + SEPARATOR + str(task_amount) + SEPARATOR + str(machine_amount) \
		+ SEPARATOR + str(task_heterogeneity_type) + SEPARATOR \
		+ str(machine_heterogeneity_type) + SEPARATOR + str(consistency_type))
        # Se obtiene una referencia al archivo generado
        filename_regex = '.*\[(.*)\].*'
        match = re.search(filename_regex, output)
        filename = match.group(1)
        cmd = SOLVER_COMMAND + SEPARATOR + filename + ' > ' + str(i) + OUTPUT_SUFFIX
        # Se aplica la resolucion a la instancia generada
        os.system(cmd)
        os.rename(filename, str(i) + INPUT_SUFFIX)
        # Si no existe, se genera el directorio de salida
        generar_jobs.generate_dir(output_path)
        # Se mueven archivos generados a carpeta de destino
        cmd = MOVE_COMMAND + SEPARATOR + str(i) + OUTPUT_SUFFIX + SEPARATOR + output_path
        os.system(cmd)
        cmd = MOVE_COMMAND + SEPARATOR + str(i) + INPUT_SUFFIX + SEPARATOR + output_path
        os.system(cmd)
        # Si pasa poco tiempo entre las llamadas al generator, no se genera una random seed
        # nueva (supongo), entonces meto delay para que las instancias generadas
        # sean realmente distintas.
        time.sleep(1)
    # Ahora en el directorio de salida tengo una pareja de archivos .in y .out que representan
    # a una instancia completa del problema (entrada y salida)
    print 'Parejas de archivos ' + INPUT_SUFFIX + ' y ' + OUTPUT_SUFFIX \
	    + ' generados en ' + output_path

if __name__ == "__main__":
    main()
