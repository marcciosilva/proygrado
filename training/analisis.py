import math

import pandas
from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib


def make_cross_validation():
    training_and_testing_sets_dataframe = get_training_and_testing_sets_dataframe()
    target_column = remove_target_column_from_dataframe(training_and_testing_sets_dataframe)
    pipeline_classifier = create_pipeline_classifier()
    # Run cross validation with pipeline and target data.
    scores = cross_val_score(pipeline_classifier, training_and_testing_sets_dataframe, target_column, cv=5)
    save_results_to_file(pipeline_classifier, scores)
    # Train the classifier and persist it.
    pipeline_classifier = train_classifier(pipeline_classifier,training_and_testing_sets_dataframe,target_column)
    persist_classifier(pipeline_classifier)

def get_training_and_testing_sets_dataframe():
    # Each csv includes 128 tasks (ie training instances).
    amount_of_problem_instance_csvs_to_use = 10
    split_data_for_manual_tests = False
    training_and_testing_sets_dataframe = load_csv_data_as_dataframe(amount_of_problem_instance_csvs_to_use)
    # Save to CSV just in case.
    training_and_testing_sets_dataframe.to_csv("variable.csv", sep=',', index=False, header=False)
    return training_and_testing_sets_dataframe


def load_csv_data_as_dataframe(amount_of_problem_instance_csvs_to_use):
    data = []
    # Each file includes an ETC matrix and the output vector.
    for i in range(0, amount_of_problem_instance_csvs_to_use):
        data.append(pandas.read_csv(str(i) + ".csv", header=None, delimiter=','))
    return pandas.concat(data, ignore_index=True)


def remove_target_column_from_dataframe(training_testing):
    target = training_testing.iloc[:, -1]
    del training_testing[len(training_testing.columns) - 1]
    return target


def create_pipeline_classifier():
    classifier = create_neural_network_classifier()
    # Apply scaler to classifier to get new classifier.
    pipeline_classifier = Pipeline([('StandardScaler', StandardScaler()), ('classify', classifier)])
    return pipeline_classifier


def create_neural_network_classifier():
    task_amount = 128
    output_neuron_amount = 1
    hidden_layer_amount = 2
    # Same heuristic as before to calculate neuron amount in inner layers.
    hidden_layer_neuron_amount = tuple([int(math.ceil((task_amount - output_neuron_amount) / 2))]
                                       * hidden_layer_amount)
    classifier = MLPClassifier(solver='lbfgs', alpha=1e-2,
                               hidden_layer_sizes=hidden_layer_neuron_amount, random_state=1)
    return classifier


def save_results_to_file(pipeline, scores):
    # In case it's running unattended and not in AWS terminal.
    f = open('results.out', 'a')
    f.write('\n\n' + "###################################################" + '\n')
    f.write("###################################################" + '\n\n')
    f.write(str(pipeline.get_params()) + '\n')
    f.write("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2) + '\n')
    f.close()


def persist_classifier(pipeline_classifier):
    joblib.dump(pipeline_classifier, 'classifier.pkl')

def train_classifier(pipeline_classifier,training_data,target_to_learn):
    pipeline_classifier.fit(training_data,target_to_learn)
    return pipeline_classifier


make_cross_validation()
