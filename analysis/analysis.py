import sys

import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../problem_classification'))
import problem_instance_classifier

MIN_TASK_AMOUNT = 5
MAX_TASK_AMOUNT = 1024
MACHINE_AMOUNT = 4
PROCESSED_DATA_DIRECTORY = '../problem_instance_generator/data-processed/'
CLASSIFIER_DIRECTORY = '../problem_classification/'
PROBLEM_TYPE = '000'  # TODO improve this
PROBLEM_INSTANCE_AMOUNT_PER_TYPE = 10
CLASSIFIER_PREFIXES = ['svm']  # ['ann', 'svm']
CLASSIFIER_SUFFIXES = ['100Inst.pkl', '100Inst-EscaladoInter.pkl']


def main():
    # iterar sobre cantidad de tareas, con machine amount fija
    for classifier_prefix in CLASSIFIER_PREFIXES:
        for classifier_suffix in CLASSIFIER_SUFFIXES:
            classifier_filename = classifier_prefix + classifier_suffix
            print('##########' + classifier_filename + '##########')
            for task_amount in range(MIN_TASK_AMOUNT, MAX_TASK_AMOUNT + 1):
                for problem_instance_index in range(0, PROBLEM_INSTANCE_AMOUNT_PER_TYPE):
                    problem_instance_path = PROCESSED_DATA_DIRECTORY + str(task_amount) + 'x' + str(
                        MACHINE_AMOUNT) + '-' + PROBLEM_TYPE + '/training/' + str(problem_instance_index) + '.csv'
                    analysis_string = problem_instance_classifier.classify_problem_instance(
                        problem_instance_path, CLASSIFIER_DIRECTORY + classifier_filename)
                    print(analysis_string + ' ' + str(task_amount) + ' ' + str(MACHINE_AMOUNT))


# Only run main() if being called directly.
if __name__ == '__main__':
    main()
