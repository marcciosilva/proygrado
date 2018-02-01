# coding=utf-8
'''
This module parses pairs of .in and .out files and returns an .csv file, which will in turn
be used as a training example for some classifier.
It also handles the directory generation for each file.
'''
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utilities
import config


def main():
    # The .in and .out files' location is obtained from the user input.
    try:
        instance_amount = int(sys.argv[1])
        input_path = str(sys.argv[2])
        output_path = str(sys.argv[3])
    except Exception:
        print('Usage: python parser_raw_to_csv.py instance-amount input-directory \
			output-directory')
        print('### Types ###')
        print('instance-amount : int')
        print('input-directory : str')
        print('output-directory : str')
        print('Example: python parser_raw_to_csv.py 100 data-raw/4x16-000/test/ data-processed/4x16-000/test/')
    for i in range(0, instance_amount):
        # The problem's input is accessed (.in file).
        tmp_file = open(input_path + str(i) + config.RAW_PROBLEM_INSTANCE_INPUT_FILE_EXTENSION, 'r')
        first_line = tmp_file.readline()
        # The problem's dimension is obtained - which should be declared at the beginning of
        # the .in file.
        match = re.search('(\d*)\s(\d*)\n', first_line)
        task_number = int(match.group(1))
        machine_number = int(match.group(2))
        lines_to_read = task_number * machine_number
        etc_matrix = []
        # Reads all the lines in the document and generates ETC matrix.
        for _ in range(0, lines_to_read):
            match = re.search('(\d*\.\d*)\n', tmp_file.readline())
            value = float(match.group(1))
            etc_matrix.append(value)
        # The solution file is accessed (.out file).
        tmp_file = open(input_path + str(i) + config.RAW_PROBLEM_INSTANCE_OUTPUT_FILE_EXTENSION, 'r')
        # The three first lines are ignored (they include the makespan value and some other stuff).
        for _ in range(0, 3):
            tmp_file.readline()
        line = tmp_file.readline()
        # The solution vector is obtained.
        solution_vector = [int(s) for s in line.split() if s.isdigit()]
        # The output directory is generated in case if it doesn't exist (view docs).
        utilities.generate_dir(output_path)
        # A .csv file is generated
        import pandas as pd
        datasetMatrix = []
        # Generate an array of arrays where each array contains the information for a given task, and its
        # last element is the associated classification.
        for j in range(0, task_number):
            for k in range(0, machine_number):  # Add current task information.
                if (k == 0):
                    datasetMatrix.append([])
                datasetMatrix[j].append(etc_matrix[j * machine_number + k])
            datasetMatrix[j].append(solution_vector[j])  # Add classification.
        # Generate dataframe and print to csv.
        dataset = pd.DataFrame()
        dataset = dataset.append(pd.DataFrame(datasetMatrix), ignore_index=True)
        file_name = output_path + str(i) + '.csv'
        dataset.to_csv(file_name, sep=',', encoding='utf-8', index=False, header=False)
    print('.csv files created at ' + output_path)


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
