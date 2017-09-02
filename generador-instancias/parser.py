# coding=utf-8
'''
This module parses pairs of .in and .out files and returns an .csv file, which will in turn
be used as a training example for some classifier.
It also handles the directory generation for each file.
'''
import csv
import re
import sys

import training_example_generator
import generar_jobs

def main():
    # The .in and .out files' location is obtained from the user input.
    try:
        instance_amount = int(sys.argv[1])
        input_path = str(sys.argv[2])
        output_path = str(sys.argv[3])
    except Exception:
        print 'Usage: python parser.py instance-amount input-directory \
			output-directory'
        print '### Types ###'
        print 'instance-amount : int'
        print 'input-directory : str'
        print 'output-directory : str'
        print 'Example: python parser.py 100 data-raw/4x16-000/test/ data-processed/4x16-000/test/'
    for i in range(0, instance_amount):
        # The problem's input is accessed (.in file).
        tmp_file = open(input_path + str(i) + training_example_generator.INPUT_SUFFIX, 'r')
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
        tmp_file = open(input_path + str(i) + training_example_generator.OUTPUT_SUFFIX, 'r')
        # The three first lines are ignored (they include the makespan value and some other stuff).
        for _ in range(0, 3):
            tmp_file.readline()
        line = tmp_file.readline()
        # The solution vector is obtained.
        solution_vector = [int(s) for s in line.split() if s.isdigit()]
        # The output directory is generated in case if it doesn't exist (view docs).
        generar_jobs.generate_dir(output_path)
        # A unique .csv file is generated for each of the solution vector's entries.
        for index, value in enumerate(solution_vector):
            file_name = output_path + str(index) + '.csv'
            if is_csv_empty(file_name):
                # The empty .csv file is created.
                csvfile = open(file_name, 'wb')
            else:
                # Content is added to the existing .csv file (opened with append flag).
                csvfile = open(file_name, 'a')
            resultwriter = csv.writer(csvfile, delimiter=',')
            # lines will be an array with all of the values of the generated file.
            # The expected tuple will also be added later.
			# Más adelante le agregaremos la tupla esperada.
            lines = []
            # A column is added for each ETC matrix value.
            for time_value in etc_matrix:
                lines.append(time_value)
            # The task-machine assignment is added.
            lines.append(value)
            # The line is added to the .csv file.
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
