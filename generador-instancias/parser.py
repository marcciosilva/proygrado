# coding=utf-8
'''
La idea de este módulo es recibir parejas de archivos (entrada y salida esperada) de instancias
del problema y generar en un directorio archivos .csv, para que cada uno sea usado como una
instancia de entrenamiento para el clasificador.
'''
import csv
import re
import sys

import training_example_generator
import generar_jobs

def main():
    # Se obtienen directorios (donde estan los datos a usar) desde consola.
    try:
        instance_amount = int(sys.argv[1])
        input_path = str(sys.argv[2])
        output_path = str(sys.argv[3])
    except Exception:
        print 'Uso del script: python parser.py cantidad-instancias directorio-entrada \
			directorio-salida'
        print '### Tipos ###'
        print 'cantidad-instancias : int'
        print 'directorio-entrada : str'
        print 'directorio-salida : str'
        print 'Ejemplo: python parser.py 100 ejemplos-entrenamiento-separados/4x16-000/test/ \
			ejemplos-entrenamiento-unificados/4x16-000/test/'
    for i in range(0, instance_amount):
        # Se accede a la entrada del problema.
        tmp_file = open(input_path + str(i) + training_example_generator.INPUT_SUFFIX, 'r')
        first_line = tmp_file.readline()
        # Se obtiene la dimension del problema, que deberia estar declarada al principio.
        # del archivo
        match = re.search('(\d*)\s(\d*)\n', first_line)
        task_number = int(match.group(1))
        machine_number = int(match.group(2))
        lines_to_read = task_number * machine_number
        etc_matrix = []
        # Leo todas las lineas del documento y genero matriz ETC.
        for _ in range(0, lines_to_read):
            match = re.search('(\d*\.\d*)\n', tmp_file.readline())
            value = float(match.group(1))
            etc_matrix.append(value)
        # Abro el archivo de la solucion.
        tmp_file = open(input_path + str(i) + training_example_generator.OUTPUT_SUFFIX, 'r')
        # Se ignoran las tres primeras lineas.
        for _ in range(0, 3):
            tmp_file.readline()
        line = tmp_file.readline()
        # Se obtiene vector solucion.
        solution_vector = [int(s) for s in line.split() if s.isdigit()]
        # Si no existe, se genera el directorio de salida.
        generar_jobs.generate_dir(output_path)
        # Se genera un .csv para cada indice del vector solucion.
        for index, value in enumerate(solution_vector):
            file_name = output_path + str(index) + '.csv'
            if is_csv_empty(file_name):
                # Se crea el .csv vacio.
                csvfile = open(file_name, 'wb')
            else:
                # Se agrega contenido al .csv existente (se abre con la flag de append).
                csvfile = open(file_name, 'a')
            resultwriter = csv.writer(csvfile, delimiter=',')
            # lines será una tira con todos los valores del archivo generado.
			# Más adelante le agregaremos la tupla esperada.
            lines = []
            # Se agrega una columna por cada valor de la matriz etc.
            for time_value in etc_matrix:
                lines.append(time_value)
            # Agrego la asignacion tarea-maquina que corresponda.
            lines.append(value)
            # Agrego la linea a el csv.
            resultwriter.writerow(lines)
            csvfile.close()
    print 'Archivos .csv creados en ' + output_path

def is_csv_empty(file_name):
    '''
    Returns true if csv is empty.
    '''
    try:
        with open(file_name, 'r') as _:
            return False
    except IOError:
        return True

if __name__ == "__main__":
    main()
