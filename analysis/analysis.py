import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../problem_classification'))
import problem_instance_classifier

MACHINE_AMOUNT = 4
MIN_TASK_AMOUNT = MACHINE_AMOUNT + 1
MAX_TASK_AMOUNT = 1024

PROCESSED_DATA_DIRECTORY = '../problem_instance_generator/data-processed/'
CLASSIFIER_DIRECTORY = '../problem_classification/'
PROBLEM_TYPE = '000'  # TODO improve this
PROBLEM_INSTANCE_AMOUNT_PER_TYPE = 10
CLASSIFIER_FILENAMES = [
    "random",
    # "512x16-100Instancias-ANN-EscaladoIndependiente.pkl",
]


# "512x16-100Instancias-ANN-EscaladoInter.pkl",
# "512x16-100Instancias-SVM-EscaladoIndependiente.pkl",
# "512x16-100Instancias-SVM-EscaladoInter.pkl"

def main():
    # iterar sobre cantidad de tareas, con machine amount fija
    # for classifier_prefix in CLASSIFIER_PREFIXES:
    for classifier_filename in CLASSIFIER_FILENAMES:
        print('##########' + classifier_filename + '##########')
        for task_amount in range(MIN_TASK_AMOUNT, MAX_TASK_AMOUNT + 1):
            expected_makespan_sum = 0.0
            calculated_makespan_sum = 0.0
            for problem_instance_index in range(0, PROBLEM_INSTANCE_AMOUNT_PER_TYPE):
                problem_instance_path = PROCESSED_DATA_DIRECTORY + str(task_amount) + 'x' + str(
                    MACHINE_AMOUNT) + '-' + PROBLEM_TYPE + '/training/' + str(problem_instance_index) + '.csv'
                classification_results = problem_instance_classifier.classify_problem_instance(
                    problem_instance_path, CLASSIFIER_DIRECTORY + classifier_filename)
                expected_makespan_sum += classification_results['expected_makespan']
                calculated_makespan_sum += classification_results['calculated_makespan']
            print(str(expected_makespan_sum) + ' ' + str(calculated_makespan_sum) + ' ' + str(task_amount) +
                  ' ' + str(MACHINE_AMOUNT))


# Only run main() if being called directly.
if __name__ == '__main__':
    main()
