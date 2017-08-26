# coding=utf-8
'''
Este script genera un (o varios) .sh que se va a encargar de generar ejemplos de entrenamiento.
'''
import os
import errno
import math

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
# Whether to generate data serially (so one job will basically generate all of the .in and .out pairs for
# all types of problems FIRST, while the rest can be executed in parallel later) or not.
SERIAL_INITIAL_DATA_GENERATION = True

def chunks(lst, chunk_amount):
    """
    Splits list lst in lists of chunk_amount elements and returns them (as a list of lists)
    """
    chunk_amount = max(1, chunk_amount)
    return [lst[i:i + chunk_amount] for i in xrange(0, len(lst), chunk_amount)]

def generate_dir(path):
    """
    If path doesn't exist, it gets created
    """
    try:
        os.makedirs(path)
        print 'Directory ' + path + ' created or already existed.'
    except OSError as error:
        if error.errno != errno.EEXIST:
            raise

def main():
    # En este array se van a guardar los comandos a ejecutar para generar instancias
    # Se van a tener tantos elementos como archivos de generacion existan
    # La idea es generar tantos archivos como jobs se quieran ejecutar en el cluster,
    # para paralelizar
    commands = []    
    # Generate jobs directory
    generate_dir(OUTPUT_PATH)
    if SERIAL_INITIAL_DATA_GENERATION:
        print 'Working with serial raw data generation'
        # Create serial job that generates training examples (doesn't handle parsing)
        for machine_amount in range(0, 2):
            for task_heterogeneity_type in range(0, 2):
                for machine_heterogeneity_type in range(0, 3):
                    # For each problem type or dimension
                    for tasks in PROBLEM_TYPES.keys():
                        for instance_amount in TEST_TRAINING_AMOUNT:
                            machines = PROBLEM_TYPES[tasks]
                            # If I'm generating training examples, the path suffix is changed
                            if instance_amount == TEST_TRAINING_AMOUNT[0]:
                                dir_suffix = '/test/'
                            else:
                                dir_suffix = '/training/'
                            # sub_dir is the identifier for each problem instance
                            sub_dir = str(tasks) + 'x' + str(machines) + '-' + \
                                str(machine_amount) + str(task_heterogeneity_type) + \
                                str(machine_heterogeneity_type) + dir_suffix
                            directory = GENERATOR_DIR + sub_dir
                            # Add commands to commands object
                            commands.append(GENERATOR + str(tasks) + ' ' + str(machines) + ' ' \
                                + str(machine_amount) + ' ' + str(task_heterogeneity_type) + ' ' \
                                + str(machine_heterogeneity_type) + ' ' + str(instance_amount) \
                                + ' ' + directory)
                            # Output directory is generated for later use
                            generate_dir(directory)
        # Data generation job is created
        # This job should always be executed first
        tmp_file = open(OUTPUT_PATH + 'job-generate-raw-data' + '.sh', 'w')
        for command in commands:
            tmp_file.write(command + '\n')
        tmp_file.close()
        print 'Raw data generation script generated in ' + OUTPUT_PATH
        # Clean up
        commands = []
    ###########################################################################################
    ###########################################################################################

    for machine_amount in range(0, 2):
        for task_heterogeneity_type in range(0, 2):
            for machine_heterogeneity_type in range(0, 3):
                # For each problem type or dimension
                for tasks in PROBLEM_TYPES.keys():
                    for instance_amount in TEST_TRAINING_AMOUNT:
                        machines = PROBLEM_TYPES[tasks]
                        # If I'm generating training examples, the path suffix is changed
                        if instance_amount == TEST_TRAINING_AMOUNT[0]:
                            dir_suffix = '/test/'
                        else:
                            dir_suffix = '/training/'
                        # sub_dir is the identifier for each problem instance
                        sub_dir = str(tasks) + 'x' + str(machines) + '-' + \
                            str(machine_amount) + str(task_heterogeneity_type) + \
                            str(machine_heterogeneity_type) + dir_suffix
                        # If not generating raw data in a serial way, then the generation has to
                        # be split up in jobs, so each job will generate raw data, instead of it
                        # being generated in a serial single job
                        # TODO polish this
                        if not SERIAL_INITIAL_DATA_GENERATION:
                            directory = GENERATOR_DIR + sub_dir
                            # Add commands to commands object
                            commands.append(GENERATOR + str(tasks) + ' ' + str(machines) + ' ' \
                                + str(machine_amount) + ' ' + str(task_heterogeneity_type) + ' ' \
                                + str(machine_heterogeneity_type) + ' ' + str(instance_amount) \
                                + ' ' + directory)
                            # Output directory is generated for later use
                            generate_dir(directory)                            
                        directory = PARSER_DIR + sub_dir
                        commands.append(PARSER + str(instance_amount) + ' ' + PARENT_DIR \
                            + GENERATOR_DIR + sub_dir + ' ' + PARENT_DIR + PARSER_DIR + sub_dir)
                        # Output directory is generated for later use
                        generate_dir(directory)
    # For each job, every one of its commands is added in a single .sh file
    # Everything will be stored at ./jobs/
    generate_dir(OUTPUT_PATH)
    # Adjust command amount per job to actually generate JOB_AMOUNT jobs
    commands_per_job = int(math.ceil(len(commands) / float(JOB_AMOUNT)))
    for index, job in enumerate(chunks(commands, commands_per_job)):
        tmp_file = open(OUTPUT_PATH + 'job-' + str(index) + '.sh', 'w')
        for command in job:
            tmp_file.write(command + '\n')
        tmp_file.close()
    print 'Job scripts created at ' + OUTPUT_PATH        

if __name__ == '__main__':
    main()
