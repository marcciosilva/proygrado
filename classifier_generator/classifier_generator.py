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
machine_amount = 16  # TODO receive as parameter.
task_amount = 512  # TODO receive as parameter.
problem_instance_amount = 100


def create_train_and_persist_classifier_with_CV(type,activation_type,hidden_layers_size):
    initialize_instance_variables()
    pipeline_classifier = create_pipeline_classifier(type,activation_type,hidden_layers_size)
    training_and_testing_sets_dataframe = get_training_and_testing_sets_dataframe()
    target_column = remove_target_column_from_dataframe(training_and_testing_sets_dataframe)
    
    # Run cross validation with pipeline and target data. This can be uncommented for 
    # analizing the scores of the model.
    #scores = cross_val_score(pipeline_classifier, training_and_testing_sets_dataframe, target_column, cv=5)
    
    # Train the classifier and persist it.
    pipeline_classifier = train_classifier(pipeline_classifier, training_and_testing_sets_dataframe, target_column)
    persist_classifier(pipeline_classifier,type,activation_type,hidden_layers_size)

def load_csv(number_of_csv):
    return pandas.read_csv(training_examples_base_dir + str(number_of_csv) + ".csv", header=None, delimiter=',')

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

def create_pipeline_classifier(type,activation_type,hidden_layers_size):
    if type == 'ANN':
        classifier = create_neural_network_classifier(activation_type,hidden_layers_size)
    elif type == 'SVM':
        classifier = svm.SVC()
    # Apply scaler to classifier to get new classifier.
    pipeline_classifier = Pipeline([('StandardScaler', StandardScaler()), ('classify', classifier)])
    return pipeline_classifier


def create_neural_network_classifier(activation_type,hidden_layers_size):
    # Same heuristic as before to calculate neuron amount in inner layers.
    hidden_layer_amount = hidden_layers_size
    training_instance_amount = problem_instance_amount * task_amount
    input_neuron_amount = machine_amount
    output_neuron_amount = 1
    alpha = 2
    hidden_layer_neuron_amount = training_instance_amount / (alpha * (input_neuron_amount + output_neuron_amount))
    hidden_layers = tuple([int(math.ceil(hidden_layer_neuron_amount))] * hidden_layer_amount)
    classifier = MLPClassifier(activation=activation_type,solver='lbfgs', alpha=1e-2,
                               hidden_layer_sizes=hidden_layers, random_state=1)
    return classifier

def persist_classifier(pipeline_classifier,type,activation_type,hidden_layers_size):
    name = str(type) + "_" + str(activation_type) + "_" + str(hidden_layers_size) + ".pkl"
    joblib.dump(pipeline_classifier, name)


def train_classifier(pipeline_classifier, training_data, target_to_learn):
    pipeline_classifier.fit(training_data, target_to_learn)
    return pipeline_classifier

if __name__ == "__main__":
    print("Training SVM... ")
    create_train_and_persist_classifier_with_CV('SVM',"","")   
    gc.collect()
    print("Training ANNs... ")
    for activation_type in ('identity','tanh','relu'):
        for hidden_layers_size in [2,3,4]:
            print("Activation type: " + str(activation_type) + " Hidden layers size: " + str(hidden_layers_size))
            create_train_and_persist_classifier_with_CV('ANN',activation_type,hidden_layers_size)
            gc.collect()