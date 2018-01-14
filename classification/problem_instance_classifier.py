import pandas
from sklearn.externals import joblib


def main():
    results = classify_problem_instance('problem_instance.csv',
                                        'classifier.pkl')  # TODO receive paths from calling module
    print(results)


def classify_problem_instance(problem_instance_path, classifier_path):
    problem_instance_dataframe = load_csv_problem_instance(problem_instance_path)
    remove_target_column_from_dataframe(problem_instance_dataframe)
    classifier = joblib.load(classifier_path)
    results = classifier.predict(problem_instance_dataframe)  # TODO parallelize?
    return results


def load_csv_problem_instance(path):
    return pandas.read_csv(path, header=None, delimiter=',')


def remove_target_column_from_dataframe(dataframe):
    target = dataframe.iloc[:, -1]
    del dataframe[len(dataframe.columns) - 1]
    return target


# Only run main() if being called directly.
if __name__ == '__main__':
    main()
