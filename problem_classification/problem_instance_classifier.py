import random

import pandas
import pdb
import sys
import numpy
from sklearn.externals import joblib
import re

# task_amounts = [128, 256, 512, 1024]
machine_amount = 0


def main():
    pass
    # TODO this is for testing only, classify_problem_instance will be called from outside.
    # for task_amount in task_amounts:
    # # print("############# " + str(task_amount) + "x" + str(machine_amount) + "#############")
    # # TODO receive paths from calling module
    # csv_problem_instance_path = str(task_amount) + 'x4.csv'
    # classifier_path = 'svm100Inst-EscaladoInter.pkl'
    # obtained_results_vector = classify_problem_instance(csv_problem_instance_path, classifier_path)


def set_machine_amount(new_machine_amount_value):
    global machine_amount
    machine_amount = new_machine_amount_value


def classify_problem_instance(csv_problem_instance_path, classifier_path, print_shit):
    if print_shit:
        print("##### Expected makespan array #####")
    problem_instance_dataframe = load_csv_problem_instance(csv_problem_instance_path)
    expected_makespan = get_makespan_for_examples_dataframe(problem_instance_dataframe, print_shit)
    expected_solution = remove_target_column_from_dataframe(problem_instance_dataframe)
    generating_random_solutions = classifier_path.find("random") != -1
    if generating_random_solutions:
        obtained_solution = []
        row_amount = problem_instance_dataframe.shape[0]
        for row in range(0, row_amount):
            random_machine_selection = random.randint(0, machine_amount - 1)
            obtained_solution.append(float(random_machine_selection))
        obtained_solution = numpy.array(obtained_solution)
    else:
        classifier = joblib.load(classifier_path)
        obtained_solution = classifier.predict(problem_instance_dataframe)
    obtained_solution_dataframe = pandas.DataFrame({'classification': obtained_solution})
    problem_instance_dataframe = problem_instance_dataframe.join(obtained_solution_dataframe)
    if print_shit:
        print("##### Calculated makespan array #####")
    calculated_makespan = get_makespan_for_examples_dataframe(problem_instance_dataframe, print_shit)
    accuracy = get_accuracy_for_problem_instance(expected_solution, obtained_solution)
    # TODO extra metrics
    is_consistent = is_problem_instance_consistent(problem_instance_dataframe)
    time_lost_in_bad_assignments = get_time_lost_in_bad_assignments(problem_instance_dataframe, expected_solution,
                                                                    obtained_solution)
    return {
        "expected_makespan": expected_makespan,
        "calculated_makespan": calculated_makespan,
        "accuracy": accuracy,
        "is_consistent": is_consistent,
        "time_lost_in_bad_assignments": time_lost_in_bad_assignments
    }


def load_csv_problem_instance(path):
    return pandas.read_csv(path, header=None, delimiter=',')


def remove_target_column_from_dataframe(dataframe):
    target = dataframe.iloc[:, -1]
    del dataframe[len(dataframe.columns) - 1]
    return target


def get_makespan_for_examples_dataframe(training_and_testing_sets_dataframe, print_shit):
    makespan_array = [0.0] * machine_amount
    try:
        for current_training_instance in range(0, len(training_and_testing_sets_dataframe)):
            # If machine_amount == 4, access 5th column ie 4th index.
            current_row = training_and_testing_sets_dataframe.loc[current_training_instance]
            assigned_machine_for_task = int(current_row[machine_amount])
            makespan_array[assigned_machine_for_task] += current_row[assigned_machine_for_task]
        if print_shit:
            print(makespan_array)
        return numpy.amax(makespan_array)
    except Exception:
        type, value, traceback = sys.exc_info()
        pdb.set_trace()


def get_accuracy_for_problem_instance(expected_solution, obtained_solution):
    validate_equal_list_lengths(expected_solution, obtained_solution)
    solution_length = len(expected_solution)
    amount_of_failed_classifications = 0
    for i in range(solution_length):
        if obtained_solution[i] != expected_solution[i]:
            amount_of_failed_classifications += 1
    accuracy = 1 - amount_of_failed_classifications / solution_length
    return accuracy


def validate_equal_list_lengths(first_list, second_list):
    if (len(first_list) != len(second_list)):
        raise Exception('first_list\'s length should be the same as second_list\'s length')


def get_time_lost_in_bad_assignments(problem_instance_dataframe, expected_solution, obtained_solution):
    validate_equal_list_lengths(expected_solution, obtained_solution)
    solution_length = len(expected_solution)
    time_lost_in_bad_assignments = 0.0
    for i in range(solution_length):
        current_row = problem_instance_dataframe.loc[i]
        obtained_machine = obtained_solution[i]
        expected_machine = expected_solution[i]
        if obtained_machine != expected_machine:
            # TODO sumar la diferencia entre el makespan esperado y el obtenido
            # calculado - esperado, asi cuando andemos bien queda negativo
            time_lost_in_bad_assignments += current_row[obtained_machine] - current_row[expected_machine]
    return time_lost_in_bad_assignments


def is_problem_instance_consistent(problem_instance_dataframe):
    is_consistent = True
    row_amount = len(problem_instance_dataframe)
    relations_for_current_row = []
    for i in range(0, row_amount):
        current_row = problem_instance_dataframe.iloc[i]
        last_machine_index = len(current_row) - 2  # to ignore the classification value
        tmp_relations_for_current_row = []
        for j in range(0, last_machine_index):
            tmp_relations_for_current_row.append(current_row[j] > current_row[j + 1])
        # print (tmp_relations_for_current_row)
        if len(relations_for_current_row) == 0:
            relations_for_current_row = tmp_relations_for_current_row
        elif tmp_relations_for_current_row != relations_for_current_row:
            is_consistent = False
            break
    return is_consistent


# Only run main() if being called directly.
if __name__ == '__main__':
    main()
