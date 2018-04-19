import sys
import os
import re
import pdb

sys.path.append(os.path.join(os.path.dirname(__file__), '../problem_classification'))
import problem_instance_classifier

MAX_TASK_AMOUNT = 1024

PROCESSED_DATA_DIRECTORY = '../problem_instance_generator/data-processed/'
CLASSIFIER_DIRECTORY = '../problem_classification/'
PROBLEM_TYPE = '000'  # TODO improve this
PROBLEM_INSTANCE_AMOUNT_PER_TYPE = 10
# The classifiers that don't specify their activation function in their file names (except the random
# classifier which doesn't actually exist as such), use relu.
CLASSIFIER_FILENAMES = [
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
    "activation-functions-test/512x16-100Instancias-ANN-2CapasOcultas-EscaladoInter-Identity.pkl",#"./activation-functions-test/ANN_identity_2.pkl",
    # "activation-functions-test/512x16-100Instancias-ANN-3CapasOcultas-EscaladoInter-Identity.pkl",#"./activation-functions-test/ANN_identity_3.pkl",
    # "activation-functions-test/512x16-100Instancias-ANN-4CapasOcultas-EscaladoInter-Identity.pkl",#"./activation-functions-test/ANN_identity_4.pkl",
    # "activation-functions-test/512x16-100Instancias-ANN-2CapasOcultas-EscaladoInter-Tanh.pkl",#"./activation-functions-test/ANN_tanh_2.pkl",
    # "activation-functions-test/512x16-100Instancias-ANN-3CapasOcultas-EscaladoInter-Tanh.pkl",#"./activation-functions-test/ANN_tanh_3.pkl"
    # "activation-functions-test/512x16-100Instancias-ANN-4CapasOcultas-EscaladoInter-Tanh.pkl"#"./activation-functions-test/ANN_tanh_4.pkl"
]

def main():
    # iterar sobre cantidad de tareas, con machine amount fija
    # for classifier_prefix in CLASSIFIER_PREFIXES:
    for classifier_filename in CLASSIFIER_FILENAMES:
        print('##########' + classifier_filename + '##########')
        print('(Output format is: expected_makespan_average calculated_makespan_average '
              'accuracy_average task_amount machine_amount)')
        regex_match = re.search('x(\d+)-', classifier_filename)
        machine_amount = int(regex_match[1])
        min_task_amount = machine_amount + 1
        problem_instance_classifier.set_machine_amount(machine_amount)

        for task_amount in range(min_task_amount, MAX_TASK_AMOUNT + 1):
            expected_makespan_average = 0.0
            calculated_makespan_average = 0.0
            accuracy_average = 0.0
            time_lost_in_bad_assignments = 0.0
            is_consistent_problem_dimension = True
            amount_inconsistent_problem_instances = 0.0
            for problem_instance_index in range(0, PROBLEM_INSTANCE_AMOUNT_PER_TYPE):
                problem_instance_path = PROCESSED_DATA_DIRECTORY + str(task_amount) + 'x' + str(
                    machine_amount) + '-' + PROBLEM_TYPE + '/training/' + str(problem_instance_index) + '.csv'
                classification_results = problem_instance_classifier.classify_problem_instance(
                    problem_instance_path, CLASSIFIER_DIRECTORY + classifier_filename, False)#problem_instance_index == 0)
                # TODO only prints makespan array if first problem instance for dimension
                expected_makespan_average += classification_results['expected_makespan']
                calculated_makespan_average += classification_results['calculated_makespan']
                accuracy_average += classification_results['accuracy']
                time_lost_in_bad_assignments += classification_results['time_lost_in_bad_assignments']
                is_consistent_problem_instance = classification_results['is_consistent']
                if not is_consistent_problem_instance:
                    pdb.set_trace()
                    amount_inconsistent_problem_instances += 1
                is_consistent_problem_dimension = is_consistent_problem_dimension and is_consistent_problem_instance
            expected_makespan_average /= PROBLEM_INSTANCE_AMOUNT_PER_TYPE
            calculated_makespan_average /= PROBLEM_INSTANCE_AMOUNT_PER_TYPE
            accuracy_average /= PROBLEM_INSTANCE_AMOUNT_PER_TYPE
            time_lost_in_bad_assignments /= PROBLEM_INSTANCE_AMOUNT_PER_TYPE

            percentage_of_inconsistent_problem_instances_for_dimension = float(amount_inconsistent_problem_instances / PROBLEM_INSTANCE_AMOUNT_PER_TYPE)
            print('{0:.2f} {1:.2f} {2:.2f} {3} {4} {5:.2f} {6}'.format(
                expected_makespan_average,
                calculated_makespan_average,
                accuracy_average,
                task_amount,
                machine_amount,
                time_lost_in_bad_assignments,
                percentage_of_inconsistent_problem_instances_for_dimension))

# Only run main() if being called directly.
if __name__ == '__main__':
    main()
