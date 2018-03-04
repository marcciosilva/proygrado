import random

import pandas
import pdb
import sys
import numpy
from sklearn.externals import joblib

machine_amount = 16


# task_amounts = [128, 256, 512, 1024]


def main():
    pass
    # TODO this is for testing only, classify_problem_instance will be called from outside.
    # for task_amount in task_amounts:
    # # print("############# " + str(task_amount) + "x" + str(machine_amount) + "#############")
    # # TODO receive paths from calling module
    # csv_problem_instance_path = str(task_amount) + 'x4.csv'
    # classifier_path = 'svm100Inst-EscaladoInter.pkl'
    # obtained_results_vector = classify_problem_instance(csv_problem_instance_path, classifier_path)


def classify_problem_instance(csv_problem_instance_path, classifier_path):
    problem_instance_dataframe = load_csv_problem_instance(csv_problem_instance_path)
    expected_makespan = get_makespan_for_examples_dataframe(problem_instance_dataframe)
    # print('expected makespan: ' + str(expected_makespan))
    remove_target_column_from_dataframe(problem_instance_dataframe)
    generating_random_solutions = classifier_path.find("random") != -1
    if generating_random_solutions:
        results = []
        row_amount = problem_instance_dataframe.shape[0]
        for row in range(0, row_amount):
            random_machine_selection = random.randint(0, machine_amount - 1)
            results.append(float(random_machine_selection))
        results = numpy.array(results)
    else:
        classifier = joblib.load(classifier_path)
        results = classifier.predict(problem_instance_dataframe)
    new_classification_column = pandas.DataFrame({'classification': results})
    problem_instance_dataframe = problem_instance_dataframe.join(new_classification_column)
    calculated_makespan = get_makespan_for_examples_dataframe(problem_instance_dataframe)
    return {
        "expected_makespan": expected_makespan,
        "calculated_makespan": calculated_makespan
    }


def load_csv_problem_instance(path):
    return pandas.read_csv(path, header=None, delimiter=',')


def remove_target_column_from_dataframe(dataframe):
    target = dataframe.iloc[:, -1]
    del dataframe[len(dataframe.columns) - 1]
    return target


# TODO move utility to wherever it makes sense (in problem_instance_classifier.py).
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


# Only run main() if being called directly.
if __name__ == '__main__':
    main()
