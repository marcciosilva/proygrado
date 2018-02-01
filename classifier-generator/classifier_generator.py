import math
import pdb
import sys
import pandas
import numpy
import gc
from sklearn.externals import joblib
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

training_examples_base_dir = 'examples/'
module_name = ''
machine_amount = 4  # TODO receive as parameter.
task_amount = 128  # TODO receive as parameter.
problem_instance_amount = 100

# this method is created to manage the memory issues on training with the classifiers.
def create_train_and_persist_classifier(type):
    initialize_instance_variables()
    pipeline_classifier = create_pipeline_classifier(type)
    persist_classifier(pipeline_classifier)
    for number_of_csv in range(0,problem_instance_amount):
        print("Training with csv: " + str(number_of_csv))
        pipeline_classifier = joblib.load('classifier.pkl')
        training_set_dataframe = load_csv(number_of_csv)
        target_column = remove_target_column_from_dataframe(training_set_dataframe)
        pipeline_classifier = train_classifier(pipeline_classifier, training_set_dataframe, target_column)
        persist_classifier(pipeline_classifier)
        pipeline_classifier = None
        target_column = None
        training_set_dataframe = None
        gc.collect()

def load_csv(number_of_csv):
    return pandas.read_csv(training_examples_base_dir + str(number_of_csv) + ".csv", header=None, delimiter=',')

def create_train_and_persist_classifier_with_CV(type):
    initialize_instance_variables()
    pipeline_classifier = create_pipeline_classifier(type)
    training_and_testing_sets_dataframe = get_training_and_testing_sets_dataframe()
    target_column = remove_target_column_from_dataframe(training_and_testing_sets_dataframe)
    # Run cross validation with pipeline and target data.
    #scores = cross_val_score(pipeline_classifier, training_and_testing_sets_dataframe, target_column, cv=5)
    #save_results_to_file(pipeline_classifier, scores)
    # Train the classifier and persist it.
    pipeline_classifier = train_classifier(pipeline_classifier, training_and_testing_sets_dataframe, target_column)
    persist_classifier(pipeline_classifier)


def initialize_instance_variables():
    global module_name
    module_name = __file__.replace('.py', '')


def get_training_and_testing_sets_dataframe():
    # Each csv includes 128 tasks (ie training instances).
    amount_of_problem_instance_csvs_to_use = problem_instance_amount
    split_data_for_manual_tests = False
    training_and_testing_sets_dataframe = load_csv_data_as_dataframe(amount_of_problem_instance_csvs_to_use)
    makespan = get_makespan_for_examples_dataframe(training_and_testing_sets_dataframe)
    # Save to CSV just in case.
    training_and_testing_sets_dataframe.to_csv(module_name + "_dataframe_backup.csv", sep=',', index=False,
                                               header=False)
    return training_and_testing_sets_dataframe


# TODO move utility to wherever it makes sense (in problem_instance_classifier.py).
def get_makespan_for_examples_dataframe(training_and_testing_sets_dataframe):
    makespan = 0.0
    try:
        for current_training_instance in range(0, len(training_and_testing_sets_dataframe)):
            # If machine_amount == 4, access 5th column ie 4th index.
            current_row = training_and_testing_sets_dataframe.loc[current_training_instance]
            assigned_machine_for_task = current_row[machine_amount]
            # TODO ver que onda con los indices de maquina que se van de rango
            makespan += current_row[assigned_machine_for_task]
        return makespan
    except Exception:
        type, value, traceback = sys.exc_info()
        pdb.set_trace()


def load_csv_data_as_dataframe(amount_of_problem_instance_csvs_to_use):
    data = []
    # Each file includes an ETC matrix and the output vector.
    for i in range(0, amount_of_problem_instance_csvs_to_use):
        data.append(pandas.read_csv(training_examples_base_dir + str(i) + ".csv", header=None, delimiter=','))
    return pandas.concat(data, ignore_index=True)


def remove_target_column_from_dataframe(training_testing):
    target = training_testing.iloc[:, -1]
    del training_testing[len(training_testing.columns) - 1]
    return target


def create_pipeline_classifier(type):
    if type == 'ANN':
        classifier = create_neural_network_classifier()
    elif type == 'SVM':
        classifier = svm.SVC()
    # Apply scaler to classifier to get new classifier.
    pipeline_classifier = Pipeline([('StandardScaler', StandardScaler()), ('classify', classifier)])
    return pipeline_classifier


def create_neural_network_classifier():
    # Same heuristic as before to calculate neuron amount in inner layers.
    hidden_layer_amount = 2
    
    training_instance_amount = problem_instance_amount * task_amount
    input_neuron_amount = machine_amount
    output_neuron_amount = 1
    alpha = 2
    hidden_layer_neuron_amount = training_instance_amount / (alpha * (input_neuron_amount + output_neuron_amount))
    hidden_layers = tuple([int(math.ceil(hidden_layer_neuron_amount))] * hidden_layer_amount)
    classifier = MLPClassifier(solver='lbfgs', alpha=1e-2,
                               hidden_layer_sizes=hidden_layers, random_state=1)
    return classifier


def save_results_to_file(pipeline, scores):
    # In case it's running unattended and not in AWS terminal.
    #f = open(module_name + '_results.out', 'a')
    #f.write('\n\n' + "###################################################" + '\n')
    #f.write("###################################################" + '\n\n')
    #f.write(str(pipeline.get_params()) + '\n')
    #f.write("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2) + '\n')
    #print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2) + '\n')
    print(str(scores.mean()) + " " + str(problem_instance_amount * task_amount))
    #print("Training examples: " + str(problem_instance_amount * task_amount) + " This is: " + str(task_amount) + " tasks and " + str(problem_instance_amount) +" problem instances.")
    #f.close()


def persist_classifier(pipeline_classifier):
    joblib.dump(pipeline_classifier, 'classifier.pkl')


def train_classifier(pipeline_classifier, training_data, target_to_learn):
    pipeline_classifier.fit(training_data, target_to_learn)
    return pipeline_classifier


#create_train_and_persist_classifier('SVM')
create_train_and_persist_classifier_with_CV('SVM')