# coding=utf-8
'''
This script generates one (or multiple) .sh file that'll handle the generation of training examples (processed .csv files ultimately).
'''
import math
import os.path
import sys
from enum import Enum, auto

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utilities

PARENT_DIR = ''
OUTPUT_PATH_FOR_GENERATOR_SCRIPTS = 'data-generation-scripts/'
RAW_INSTANCE_GENERATOR_COMMAND = 'python raw_problem_instance_generator.py '
RAW_DATA_DIRECTORY = 'data-raw/'
PARSER_SCRIPT_COMMAND = 'python parser_raw_to_csv.py '
PROCESSED_DATA_DIRECTORY = 'data-processed/'
# Amount of jobs in which the whole task will be divided.
# If the data generation is not serial, this should be an even number, so each generation + parsing task is
# contained in a single job.
JOB_AMOUNT = 1  # TODO make this not matter when serial data generation is used.
AMOUNT_OF_TEST_PROBLEM_INSTANCES_TO_GENERATE = 0
AMOUNT_OF_TRAINING_PROBLEM_INSTANCES_TO_GENERATE = 10
SUPPORTED_PROBLEM_SIZES = {}  # Loaded at runtime.
# Whether to generate data serially (so one job will basically generate all of the .in and .out pairs for
# all types of problems FIRST, while the rest of the jobs can be executed in parallel later) or not.
SERIAL_RAW_DATA_GENERATION = True
# List of lists where:
#   Element at index 0 is the task heterogeneity (possible values: 0, 1)
#   Element at index 1 is the machine heterogeneity (possible values: 0, 1)
#   Element at index 2 is the consistency type (possible values: 0, 1, 2)
SUPPORTED_PROBLEM_TYPES = [
    [0, 0, 0]
]


class InstanceTypes(Enum):
    Training = auto()
    Test = auto()


def main():
    populate_supported_problem_sizes()
    generate_raw_data_generation_script()
    generate_processed_data_generation_script()
    print('Job scripts created at ' + OUTPUT_PATH_FOR_GENERATOR_SCRIPTS)


def generate_processed_data_generation_script():
    commands_to_append_to_generator_script = []
    utilities.generate_dir(OUTPUT_PATH_FOR_GENERATOR_SCRIPTS)
    for problem_type in SUPPORTED_PROBLEM_TYPES:
        task_heterogeneity = problem_type[0]
        machine_heterogeneity = problem_type[1]
        consistency_type = problem_type[2]
        # For each problem type or dimension
        for task_amount in SUPPORTED_PROBLEM_SIZES.keys():
            machines = SUPPORTED_PROBLEM_SIZES[task_amount]
            for instance_type in InstanceTypes:
                directory_suffix = get_directory_suffix_for_instance_type(instance_type)
                amount_of_instances_to_generate = get_amount_of_instances_to_generate_for_instance_type(instance_type)
                append_commands_to_generate_processed_instances(amount_of_instances_to_generate,
                                                                commands_to_append_to_generator_script,
                                                                consistency_type, directory_suffix,
                                                                machine_heterogeneity, machines, task_amount,
                                                                task_heterogeneity)
    # Adjust command amount per job to actually generate JOB_AMOUNT jobs
    commands_per_job = int(math.ceil(len(commands_to_append_to_generator_script) / float(JOB_AMOUNT)))
    for index, job in enumerate(
            utilities.split_list_in_chunks(commands_to_append_to_generator_script, commands_per_job)):
        tmp_file = open(OUTPUT_PATH_FOR_GENERATOR_SCRIPTS + 'job-' + str(index) + '.sh', 'w')
        for command in job:
            tmp_file.write(command + '\n')
        tmp_file.close()


def get_directory_suffix_for_instance_type(instance_type):
    if instance_type == InstanceTypes.Test:
        return '/test/'
    elif instance_type == InstanceTypes.Training:
        return '/training/'


def get_amount_of_instances_to_generate_for_instance_type(instance_type):
    if instance_type == InstanceTypes.Test:
        return AMOUNT_OF_TEST_PROBLEM_INSTANCES_TO_GENERATE
    elif instance_type == InstanceTypes.Training:
        return AMOUNT_OF_TRAINING_PROBLEM_INSTANCES_TO_GENERATE


def populate_supported_problem_sizes():
    max_task_amount = 1024
    for i in range(1, max_task_amount + 1):
        SUPPORTED_PROBLEM_SIZES[i] = 4


def generate_raw_data_generation_script():
    commands_to_append_to_generator_script = []
    # Generate jobs directory
    utilities.generate_dir(OUTPUT_PATH_FOR_GENERATOR_SCRIPTS)
    if SERIAL_RAW_DATA_GENERATION:
        print('Working with serial raw data generation')
        # Create serial job that generates training examples (doesn't handle parsing)
        # TODO Make ranges configurable (maybe I just want to generate 000 and not 001 and so on).
        for problem_type in SUPPORTED_PROBLEM_TYPES:
            task_heterogeneity = problem_type[0]
            machine_heterogeneity = problem_type[1]
            consistency_type = problem_type[2]
            # For each problem type or dimension
            for task_amount in SUPPORTED_PROBLEM_SIZES.keys():
                machines = SUPPORTED_PROBLEM_SIZES[task_amount]
                for instance_type in InstanceTypes:
                    dir_suffix = ''
                    amount_of_instances_to_generate = 0
                    if instance_type == InstanceTypes.Test:
                        dir_suffix = '/test/'
                        amount_of_instances_to_generate = AMOUNT_OF_TEST_PROBLEM_INSTANCES_TO_GENERATE
                    elif instance_type == InstanceTypes.Training:
                        dir_suffix = '/training/'
                        amount_of_instances_to_generate = AMOUNT_OF_TRAINING_PROBLEM_INSTANCES_TO_GENERATE
                    append_commands_to_generate_raw_instances(amount_of_instances_to_generate,
                                                              commands_to_append_to_generator_script, consistency_type,
                                                              dir_suffix, machine_heterogeneity, task_amount, machines,
                                                              task_heterogeneity)
        output_data_generation_script(commands_to_append_to_generator_script)


def append_commands_to_generate_raw_instances(amount_of_instances_to_generate, commands_to_append_to_generator_script,
                                              consistency_type, directory_suffix, machine_heterogeneity, task_amount,
                                              machines, task_heterogeneity):
    if amount_of_instances_to_generate > 0:
        # sub_dir is the identifier for each problem instance
        sub_dir = str(task_amount) + 'x' + str(machines) + '-' + \
                  str(task_heterogeneity) + str(machine_heterogeneity) + \
                  str(consistency_type) + directory_suffix
        directory = RAW_DATA_DIRECTORY + sub_dir
        commands_to_append_to_generator_script.append(
            RAW_INSTANCE_GENERATOR_COMMAND + str(task_amount) + ' ' + str(machines) + ' ' \
            + str(task_heterogeneity) + ' ' + str(machine_heterogeneity) + ' ' \
            + str(consistency_type) + ' ' + str(amount_of_instances_to_generate) \
            + ' ' + directory)
        # Output directory is generated for later use
        utilities.generate_dir(directory)


def output_data_generation_script(commands_to_append_to_generator_script):
    tmp_file = open(OUTPUT_PATH_FOR_GENERATOR_SCRIPTS + 'job-generate-raw-data' + '.sh', 'w')
    for command in commands_to_append_to_generator_script:
        tmp_file.write(command + '\n')
    tmp_file.close()
    print('Raw data generation script generated in ' + OUTPUT_PATH_FOR_GENERATOR_SCRIPTS)


def append_commands_to_generate_processed_instances(amount_of_instances_to_generate,
                                                    commands_to_append_to_generator_script, consistency_type,
                                                    directory_suffix, machine_heterogeneity, machines, task_amount,
                                                    task_heterogeneity):
    if amount_of_instances_to_generate > 0:
        # sub_dir is the identifier for each problem instance
        sub_dir = str(task_amount) + 'x' + str(machines) + '-' + \
                  str(task_heterogeneity) + str(machine_heterogeneity) + \
                  str(consistency_type) + directory_suffix
        # TODO split commands in N arrays (maybe using chunks utility) if not using serial generation.
        directory = PROCESSED_DATA_DIRECTORY + sub_dir
        commands_to_append_to_generator_script.append(
            PARSER_SCRIPT_COMMAND + str(amount_of_instances_to_generate) + ' ' + PARENT_DIR \
            + RAW_DATA_DIRECTORY + sub_dir + ' ' + PARENT_DIR + PROCESSED_DATA_DIRECTORY + sub_dir)
        # Output directory is generated for later use
        utilities.generate_dir(directory)


if __name__ == '__main__':
    main()
