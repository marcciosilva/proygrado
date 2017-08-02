# coding=utf-8
'''
Este script genera un (o varios) .sh que se va a encargar de generar ejemplos de entrenamiento.
'''
import os
import errno

PARENT_DIR = ''
# Donde van a quedar alojados los scripts finales
OUTPUT_PATH = 'jobs/'
# Comando para llamar al generador de instancias
GENERATOR = 'python training_example_generator.py '
# Directorio donde se van a dejar los ejemplos al final (instancia y solucion en archivos separados)
GENERATOR_DIR = 'ejemplos-entrenamiento-separados/'
# Comando para llamar al parser que unifica instancias con sus salidas
PARSER = 'python parser.py '
# Directorio donde se van a dejar los ejemplos unificados
PARSER_DIR = 'ejemplos-entrenamiento-unificados/'
# En este array se van a guardar los comandos a ejecutar para generar instancias
# Se van a tener tantos elementos como archivos de generacion existan
# La idea es generar tantos archivos como jobs se quieran ejecutar en el cluster,
# para paralelizar
commands = []
# Cantidad de jobs a iniciar para generar ejemplos de entrenamiento
# Deberia ser un numero par (para que en el split de listas no queden separados
# la generacion y el parsing de un ejemplo)
JOB_AMOUNT = 10
# Cantidad de instancias de test a utilizar en primer lugar, cantidad de instancias
# de entrenamiento a utilizar en segundo lugar
TEST_TRAINING_AMOUNT = [100, 600]
# Tipos de problema, donde la clave indica la cantidad de tareas del problema, y el valor
# indica la cantidad de maquinas
PROBLEM_TYPES = {128: 4, 512: 16}

def chunks(lst, chunk_amount):
    """
    Dada una lista lst y un parametro chunk_amount, se devuelven listas de n elementos en la medida
    de lo posible
    """
    chunk_amount = max(1, chunk_amount)
    return [lst[i:i + chunk_amount] for i in xrange(0, len(lst), chunk_amount)]

def generate_dir(path):
    """
    Si el directorio dado por path no existe, lo crea
    """
    try:
        os.makedirs(path)
        print 'Directory ' + path + ' created.'
    except OSError as error:
        if error.errno != errno.EEXIST:
            raise

def main():
    for machine_amount in range(0, 2):
        for task_heterogeneity_type in range(0, 2):
            for machine_heterogeneity_type in range(0, 3):
                # Para cada tipo o dimension del problema
                for tasks in PROBLEM_TYPES.keys():
                    for instance_amount in TEST_TRAINING_AMOUNT:
                        machines = PROBLEM_TYPES[tasks]
                        # Si estoy generando instancias de entrenamiento, cambio el sufijo del path
                        if instance_amount == TEST_TRAINING_AMOUNT[0]:
                            dir_suffix = '/test/'
                        else:
                            dir_suffix = '/training/'
                        # sub_dir es el identificador de cada instancia del problema
                        sub_dir = str(tasks) + 'x' + str(machines) + '-' + \
                            str(machine_amount) + str(task_heterogeneity_type) + \
                            str(machine_heterogeneity_type) + dir_suffix
                        directory = GENERATOR_DIR + sub_dir
                        # Agrego comandos al objeto commands
                        commands.append(GENERATOR + str(tasks) + ' ' + str(machines) + ' ' \
							+ str(machine_amount) + ' ' + str(task_heterogeneity_type) + ' ' \
							+ str(machine_heterogeneity_type) + ' ' + str(instance_amount) \
							+ ' ' + directory)
                        # Genero directorio de salida que va a ser usado posteriormente
                        generate_dir(directory)
                        directory = PARSER_DIR + sub_dir
                        commands.append(PARSER + str(instance_amount) + ' ' + PARENT_DIR \
							+ GENERATOR_DIR + sub_dir + ' ' + PARENT_DIR + PARSER_DIR + sub_dir)
                        # Genero directorio de salida que va a ser usado posteriormente
                        generate_dir(directory)
    # Para cada job, agrego todos los comandos que correspondan generando un .sh
    # Todo queda en el directorio ./jobs/
    generate_dir(OUTPUT_PATH)
    for index, job in enumerate(chunks(commands, JOB_AMOUNT)):
        tmp_file = open(OUTPUT_PATH + 'job-' + str(index) + '.sh', 'w')
        for command in job:
            tmp_file.write(command + '\n')
        tmp_file.close()
    print 'Scripts .sh creados en el directorio ' + OUTPUT_PATH

if __name__ == '__main__':
    main()
