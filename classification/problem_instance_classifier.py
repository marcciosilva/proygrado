import pandas
import pdb
import sys
from sklearn.externals import joblib

machine_amount = 4
task_amounts = [128, 256, 512, 1024]

def main():
    for task_amount in task_amounts:
        print("############# " + str(task_amount) + "x" + str(machine_amount) + "#############")
        results = classify_problem_instance(str(task_amount) + 'x4.csv',
                                            'classifier.pkl')  # TODO receive paths from calling module
        print(results)


def classify_problem_instance(problem_instance_path, classifier_path):
    problem_instance_dataframe = load_csv_problem_instance(problem_instance_path)
    expected_makespan = get_makespan_for_examples_dataframe(problem_instance_dataframe)
    print('expected makespan: ' + str(expected_makespan))
    remove_target_column_from_dataframe(problem_instance_dataframe)
    classifier = joblib.load(classifier_path)
    results = classifier.predict(problem_instance_dataframe)  # TODO parallelize?
    # TODO append results to dataframe and recalculate makespan to ver que onda

    new_classification_column = pandas.DataFrame({'classification': results})
    problem_instance_dataframe = problem_instance_dataframe.join(new_classification_column)
    new_makespan = get_makespan_for_examples_dataframe(problem_instance_dataframe)
    print('calculated makespan: ' + str(new_makespan))
    return results


def load_csv_problem_instance(path):
    return pandas.read_csv(path, header=None, delimiter=',')


def remove_target_column_from_dataframe(dataframe):
    target = dataframe.iloc[:, -1]
    del dataframe[len(dataframe.columns) - 1]
    return target


# TODO move utility to wherever it makes sense (in problem_instance_classifier.py).
def get_makespan_for_examples_dataframe(training_and_testing_sets_dataframe):
    makespan = 0.0
    try:
        for current_training_instance in range(0, len(training_and_testing_sets_dataframe)):
            # If machine_amount == 4, access 5th column ie 4th index.
            current_row = training_and_testing_sets_dataframe.loc[current_training_instance]
            assigned_machine_for_task = int(current_row[machine_amount])
            # TODO ver que onda con los indices de maquina que se van de rango
            makespan += current_row[assigned_machine_for_task]
        return makespan
    except Exception:
        type, value, traceback = sys.exc_info()
        pdb.set_trace()


# Only run main() if being called directly.
if __name__ == '__main__':
    main()
