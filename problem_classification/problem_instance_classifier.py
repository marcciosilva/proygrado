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


def classify_problem_instance(csv_problem_instance_path, classifier_path):
    problem_instance_dataframe = load_csv_problem_instance(csv_problem_instance_path)
    expected_makespan = get_makespan_for_examples_dataframe(problem_instance_dataframe)
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
    calculated_makespan = get_makespan_for_examples_dataframe(problem_instance_dataframe)
    accuracy = get_accuracy_for_problem_instance(expected_solution, obtained_solution)
    # TODO extra metrics
    time_lost_in_bad_assignments = get_time_lost_in_bad_assignments(problem_instance_dataframe, expected_solution,
                                                                    obtained_solution)
    percentage_of_faster_machines_chosen_for_incorrect_assignment = get_percentage_of_faster_machines_chosen_for_incorrect_assignment(
        problem_instance_dataframe, expected_solution,
        obtained_solution)
    return {
        "expected_makespan": expected_makespan,
        "calculated_makespan": calculated_makespan,
        "accuracy": accuracy,
        "percentage_of_faster_machines_chosen_for_incorrect_assignment": percentage_of_faster_machines_chosen_for_incorrect_assignment,
        "time_lost_in_bad_assignments_relative": time_lost_in_bad_assignments['time_lost_in_bad_assignments_relative'],
        "time_lost_in_bad_assignments_absolute": time_lost_in_bad_assignments['time_lost_in_bad_assignments_absolute']
    }


def load_csv_problem_instance(path):
    return pandas.read_csv(path, header=None, delimiter=',')


def remove_target_column_from_dataframe(dataframe):
    target = dataframe.iloc[:, -1]
    del dataframe[len(dataframe.columns) - 1]
    return target


def get_makespan_for_examples_dataframe(training_and_testing_sets_dataframe):
    makespan_array = [0.0] * machine_amount
    try:
        for current_training_instance in range(0, len(training_and_testing_sets_dataframe)):
            # If machine_amount == 4, access 5th column ie 4th index.
            current_row = training_and_testing_sets_dataframe.loc[current_training_instance]
            assigned_machine_for_task = int(current_row[machine_amount])
            makespan_array[assigned_machine_for_task] += current_row[assigned_machine_for_task]
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
    time_lost_in_bad_assignments_relative = 0.0
    time_lost_in_bad_assignments_absolute = 0.0
    for i in range(solution_length):
        current_row = problem_instance_dataframe.loc[i]
        obtained_machine = obtained_solution[i]
        expected_machine = expected_solution[i]
        if obtained_machine != expected_machine:
            expected_machine_time = current_row[expected_machine]
            time_difference = current_row[obtained_machine] - expected_machine_time
            if expected_machine_time == 0:
                expected_machine_time = 0.001  # TODO because reasons (we trunc with two decimals so we lose data)
            time_lost_in_bad_assignments_relative += time_difference / expected_machine_time
            time_lost_in_bad_assignments_absolute += time_difference
    return {
        "time_lost_in_bad_assignments_relative": time_lost_in_bad_assignments_relative,
        "time_lost_in_bad_assignments_absolute": time_lost_in_bad_assignments_absolute
    }


def get_percentage_of_faster_machines_chosen_for_incorrect_assignment(problem_instance_dataframe, expected_solution,
                                                                      obtained_solution):
    validate_equal_list_lengths(expected_solution, obtained_solution)
    solution_length = len(expected_solution)
    times_faster_machines_were_chosen = 0
    for i in range(solution_length):
        current_row = problem_instance_dataframe.loc[i]
        obtained_machine = obtained_solution[i]
        expected_machine = expected_solution[i]
        if current_row[obtained_machine] < current_row[expected_machine]:
            times_faster_machines_were_chosen += 1
    return times_faster_machines_were_chosen / solution_length


# Only run main() if being called directly.
if __name__ == '__main__':
    main()
