# coding = utf-8
'''
This script generates instances of the HCSP problem in the form of a pair of .in and .out files (raw data).
'''
import os
import re
import subprocess
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utilities
import config

# Command to execute the problem instance generator (legacy software).
GENERATOR_COMMAND = './generator'
# Command to execute the problem solver, given a problem instance (legacy software).
SOLVER_COMMAND = './solver'
SEPARATOR = ' '
MOVE_COMMAND = 'mv'


def main():
    # The problem specification is obtained from the user input.
    try:
        task_amount = int(sys.argv[1])
        machine_amount = int(sys.argv[2])
        task_heterogeneity_type = int(sys.argv[3])
        machine_heterogeneity_type = int(sys.argv[4])
        consistency_type = int(sys.argv[5])
        amount_of_instances = int(sys.argv[6])
        output_path = str(sys.argv[7])
    except Exception:
        print('Usage: python raw_problem_instance_generator.py task-amount \
			machine-amount task-heterogeneity machine-heterogeneity \
			consistency-type instance-amount output-dir')
        print('### Tipos ###')
        print('task-amount : int')
        print('machine-amount : int')
        print('task-heterogeneity : 0 = Low, 1 = High')
        print('machine-heterogeneity : 0 = Low, 1 = High')
        print('consistency-type : 0 = Consistent, 1 = Semiconsistent, 2 = Inconsistent')
        print('instance-amount : int')
        print('output-dir : str')
        print('Example: python raw_problem_instance_generator.py 4 16 0 0 0 100 \
			data-raw/4x16-000/test/')
    for i in range(0, amount_of_instances):
        # The problem instance is generated.
        status, output = subprocess.getstatusoutput( \
            GENERATOR_COMMAND + SEPARATOR + str(task_amount) + SEPARATOR + str(machine_amount) \
            + SEPARATOR + str(task_heterogeneity_type) + SEPARATOR \
            + str(machine_heterogeneity_type) + SEPARATOR + str(consistency_type))
        # A reference to the generated files is obtained.
        # TODO maybe generate a path for this individual instance of the script to deal
        # with the filesystem, so as to allow multi processing in the future.
        # Executions of this script must be serial as of now.
        filename_regex = '.*\[(.*)\].*'
        match = re.search(filename_regex, output)
        filename = match.group(1)
        cmd = SOLVER_COMMAND + SEPARATOR + filename + ' > ' + str(i) + config.RAW_PROBLEM_INSTANCE_OUTPUT_FILE_EXTENSION
        # The solver is applied to the generated problem instance.
        os.system(cmd)
        os.rename(filename, str(i) + config.RAW_PROBLEM_INSTANCE_INPUT_FILE_EXTENSION)
        # The output directory is generated if it doesn't exist (view docs).
        utilities.generate_dir(output_path)
        # Generated files are moved to the destination folder.
        cmd = MOVE_COMMAND + SEPARATOR + str(
            i) + config.RAW_PROBLEM_INSTANCE_OUTPUT_FILE_EXTENSION + SEPARATOR + output_path
        os.system(cmd)
        cmd = MOVE_COMMAND + SEPARATOR + str(
            i) + config.RAW_PROBLEM_INSTANCE_INPUT_FILE_EXTENSION + SEPARATOR + output_path
        os.system(cmd)
        # A sleep is required because if generator calls are too close (in time) to each other, 
        # maybe the C/C++ random seed isn't regenerated and the exact same problem instance is
        # generated.
        time.sleep(1)
    # Now I have a pair of .in and .out files in my output directory, representing a complete
    # problem instance (featuring an input or representation, and output or solution).
    print(
        'Pair of ' + config.RAW_PROBLEM_INSTANCE_INPUT_FILE_EXTENSION + ' and ' + config.RAW_PROBLEM_INSTANCE_OUTPUT_FILE_EXTENSION \
        + ' files generated at ' + output_path)


if __name__ == "__main__":
    main()
