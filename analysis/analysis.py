import sys
import os
import re
import pdb

sys.path.append(os.path.join(os.path.dirname(__file__), '../problem_classification'))
import problem_instance_classifier
import time, sys
from datetime import timedelta

MAX_TASK_AMOUNT = 1024

PROCESSED_DATA_DIRECTORY = '../problem_instance_generator/data-processed/'
CLASSIFIER_DIRECTORY = '../problem_classification/'
PROBLEM_TYPE = '000'  # TODO get from filename?
PROBLEM_INSTANCE_AMOUNT_PER_TYPE = 10
# The classifiers that don't specify their activation function in their file names (except the random
# classifier which doesn't actually exist as such), use relu.
# total_iterations = 0
CLASSIFIER_FILENAMES = [
    # TODO old inconsistent classifiers
    # "512x16-100Instancias-ANN-4CapasOcultas-EscaladoInter.pkl",
    # "512x16-100Instancias-ANN-3CapasOcultas-EscaladoInter.pkl",
    # "128x4-100Instancias-ANN-EscaladoIndependiente.pkl",
    # "128x4-100Instancias-ANN-EscaladoInter.pkl",
    # "128x4-100Instancias-SVM-EscaladoIndependiente.pkl",
    # "128x4-100Instancias-SVM-EscaladoInter.pkl",
    # "512x16-100Instancias-ANN-EscaladoIndependiente.pkl",
    # "512x16-100Instancias-ANN-EscaladoInter.pkl",
    # "512x16-100Instancias-SVM-EscaladoIndependiente.pkl",
    # "512x16-100Instancias-SVM-EscaladoInter.pkl",
    # "random",
    # "activation-functions-test/512x16-100Instancias-ANN-2CapasOcultas-EscaladoInter-Logistic.pkl",
    # "activation-functions-test/512x16-100Instancias-ANN-2CapasOcultas-EscaladoInter-Identity.pkl",#"./activation-functions-test/ANN_identity_2.pkl",
    # "activation-functions-test/512x16-100Instancias-ANN-3CapasOcultas-EscaladoInter-Identity.pkl",#"./activation-functions-test/ANN_identity_3.pkl",
    # "activation-functions-test/512x16-100Instancias-ANN-4CapasOcultas-EscaladoInter-Identity.pkl",#"./activation-functions-test/ANN_identity_4.pkl",
    # "activation-functions-test/512x16-100Instancias-ANN-2CapasOcultas-EscaladoInter-Tanh.pkl",#"./activation-functions-test/ANN_tanh_2.pkl",
    # "activation-functions-test/512x16-100Instancias-ANN-3CapasOcultas-EscaladoInter-Tanh.pkl",#"./activation-functions-test/ANN_tanh_3.pkl",
    # "activation-functions-test/512x16-100Instancias-ANN-4CapasOcultas-EscaladoInter-Tanh.pkl"#"./activation-functions-test/ANN_tanh_4.pkl",
    # TODO consistent classifiers
    # "512x16-000-100Instancias-ANN-2CapasOcultas-EscaladoInter-Identity.pkl",
    # "512x16-000-100Instancias-ANN-3CapasOcultas-EscaladoInter-Identity.pkl",
    # "512x16-000-100Instancias-ANN-4CapasOcultas-EscaladoInter-Identity.pkl",
    # "512x16-000-100Instancias-ANN-2CapasOcultas-EscaladoInter-Tanh.pkl",
    # TODO what's left
    "512x16-000-100Instancias-SVM-EscaladoInter.pkl",
    # "512x16-000-100Instancias-ANN-4CapasOcultas-EscaladoInter-Tanh.pkl",
    # "512x16-000-100Instancias-ANN-3CapasOcultas-EscaladoInter-Tanh.pkl",
    # "512x16-000-100Instancias-ANN-4CapasOcultas-EscaladoInter-Relu.pkl",
    # "512x16-000-100Instancias-ANN-3CapasOcultas-EscaladoInter-Relu.pkl",
    # "512x16-000-100Instancias-ANN-2CapasOcultas-EscaladoInter-Relu.pkl",

]


def main():
    # iterar sobre cantidad de tareas, con machine amount fija
    # for classifier_prefix in CLASSIFIER_PREFIXES:
    for classifier_filename in CLASSIFIER_FILENAMES:
        print('##########' + classifier_filename + '##########')
        print('(Output format is: expected_makespan_average calculated_makespan_average '
              'accuracy_average task_amount machine_amount time_lost_in_bad_assignments_absolute '
              'time_lost_in_bad_assignments_relative percentage_of_faster_machines_chosen_for_incorrect_assignment)')
        regex_match = re.search('x(\d+)-', classifier_filename)
        machine_amount = int(regex_match[1])
        min_task_amount = machine_amount + 1
        problem_instance_classifier.set_machine_amount(machine_amount)

        for task_amount in range(min_task_amount, MAX_TASK_AMOUNT + 1):
            expected_makespan_average = 0.0
            calculated_makespan_average = 0.0
            accuracy_average = 0.0
            time_lost_in_bad_assignments_relative = 0.0
            time_lost_in_bad_assignments_absolute = 0.0
            percentage_of_faster_machines_chosen_for_incorrect_assignment = 0
            for problem_instance_index in range(0, PROBLEM_INSTANCE_AMOUNT_PER_TYPE):
                problem_instance_path = PROCESSED_DATA_DIRECTORY + str(task_amount) + 'x' + str(
                    machine_amount) + '-' + PROBLEM_TYPE + '/training/' + str(problem_instance_index) + '.csv'
                classification_results = problem_instance_classifier.classify_problem_instance(
                    problem_instance_path, CLASSIFIER_DIRECTORY + classifier_filename)
                # TODO only prints makespan array if first problem instance for dimension
                expected_makespan_average += classification_results['expected_makespan']
                calculated_makespan_average += classification_results['calculated_makespan']
                accuracy_average += classification_results['accuracy']
                percentage_of_faster_machines_chosen_for_incorrect_assignment += classification_results[
                    'percentage_of_faster_machines_chosen_for_incorrect_assignment']
                time_lost_in_bad_assignments_relative += classification_results['time_lost_in_bad_assignments_relative']
                time_lost_in_bad_assignments_absolute += classification_results['time_lost_in_bad_assignments_absolute']
            expected_makespan_average /= PROBLEM_INSTANCE_AMOUNT_PER_TYPE
            calculated_makespan_average /= PROBLEM_INSTANCE_AMOUNT_PER_TYPE
            accuracy_average /= PROBLEM_INSTANCE_AMOUNT_PER_TYPE
            percentage_of_faster_machines_chosen_for_incorrect_assignment /= PROBLEM_INSTANCE_AMOUNT_PER_TYPE
            time_lost_in_bad_assignments_relative /= PROBLEM_INSTANCE_AMOUNT_PER_TYPE
            time_lost_in_bad_assignments_absolute /= PROBLEM_INSTANCE_AMOUNT_PER_TYPE
            print('{0:.2f} {1:.2f} {2:.2f} {3} {4} {5:.2f} {6:.2f} {7:.2f}'.format(
                expected_makespan_average,
                calculated_makespan_average,
                accuracy_average,
                task_amount,
                machine_amount,
                time_lost_in_bad_assignments_absolute,
                time_lost_in_bad_assignments_relative,
                percentage_of_faster_machines_chosen_for_incorrect_assignment))


# Only run main() if being called directly.
if __name__ == '__main__':
    start_time = time.time()
    main()
    execution_time_in_seconds = time.time() - start_time
    print("Execution took " + str(timedelta(seconds=execution_time_in_seconds)) + " (HH:MM:SS.ss)")
