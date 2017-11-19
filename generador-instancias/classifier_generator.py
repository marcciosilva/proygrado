# coding = utf-8
'''
This script generates classifiers trained using data in a directory passed by parameter, and persists them
in another one (also passed by parameter).
'''
# Imports.
from __future__ import absolute_import, division, print_function
import sys
import math
import os
import parser
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
import generar_jobs
import time
from sklearn.preprocessing import StandardScaler

def main():
    # The problem specification is obtained from the user input.
    try:
        task_amount = int(sys.argv[1])
        machine_amount = int(sys.argv[2])
        task_heterogeneity = int(sys.argv[3])
        machine_heterogeneity = int(sys.argv[4])
        consistency_type = int(sys.argv[5])
        USING_ENTIRE_ETC = sys.argv[6] == 'True'
        current_classifier_index = int(sys.argv[7])
    except Exception:
        print('arguments were: ' + str(sys.argv))
        print('Usage: python classifier_generator.py task-amount\n\
        machine-amount task-heterogeneity machine-heterogeneity\n\
        consistency-type USING_ENTIRE_ETC current-classifier-index')
        print('### Types ###')
        print('task-amount : int')
        print('machine-amount : int')
        print('task-heterogeneity : 0 = Low, 1 = High')
        print('machine-heterogeneity : 0 = Low, 1 = High')
        print('consistency-type : 0 = Consistent, 1 = Semiconsistent, 2 = Inconsistent')
        print('USING_ENTIRE_ETC : Boolean')
        print('current-classifier-index : 0 = \'ann\', 1 = \'svm\'')
        print('Example: python classifier_generator.py 128 4 0 0 0 True 1')
        return
    accuracy_scores = []
    classifiers = []
    # Classifier configuration.
    CLASSIFIER_STRING_ANN = 'ann'
    CLASSIFIER_STRING_SVM = 'svm'
    classifier_types = [CLASSIFIER_STRING_ANN, CLASSIFIER_STRING_SVM]
    current_classifier_str = classifier_types[current_classifier_index]
    # Base path for classifier persistence.
    # TODO maybe make ./models/ dir configurable.
    model_base_path = './models/' + current_classifier_str + '/' + str(task_amount) + 'x' + str(machine_amount) \
        + '-' + str(task_heterogeneity) + str(machine_heterogeneity) \
        + str(consistency_type) + '/'
    # TODO make data-processed dir configurable since it's configurable from job generation script.
    baseDir = './data-processed/' + str(task_amount) + 'x' \
        + str(machine_amount) + '-' + str(task_heterogeneity) \
        + str(machine_heterogeneity) + str(consistency_type) + '/'
    model_file_prefix = 'clf-' + current_classifier_str
    model_file_extension = '.pkl'
    if current_classifier_str == CLASSIFIER_STRING_ANN:
        if USING_ENTIRE_ETC:
            dimension = task_amount * machine_amount
            # Reference: https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw
            ns = 600  # Amount of training examples.
            ni = dimension
            no = 1  # Amount of output neurons.
            alpha = 2
            hidden_layer_amount = 2 #int(math.ceil(ns / (alpha * (ni + no)))) # Con 2 hardcodeado parece aprender mejor
            # Each hidden layer has an intermediate amount of neurons (between the neuron amount
            # present in the output layer and the input layer).
            # A tuple is generated to set up the MLPClassifier.
            hidden_layer_neuron_amount = tuple([int(math.ceil((task_amount - no) / 2))]
                                            * hidden_layer_amount)  
        else:
            dimension = machine_amount
            # Reference: https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw
            ns = 600  # Amount of training examples.
            ni = dimension
            no = 1  # Amount of output neurons.
            alpha = 2
            hidden_layer_amount = 2 #int(math.ceil(ns / (alpha * (ni + no)))) # Con 2 hardcodeado parece aprender mejor
            # Each hidden layer has an intermediate amount of neurons (between the neuron amount
            # present in the output layer and the input layer).
            # A tuple is generated to set up the MLPClassifier.
            hidden_layer_neuron_amount = tuple([int(math.ceil((ni - no) / 2))]
                                            * hidden_layer_amount) 
    elif current_classifier_str == CLASSIFIER_STRING_SVM:
        # No mandatory config for SVC method.
        pass
    ################################################################################################################################################################################        
    ################################################################################################################################################################################
    ################################################################################################################################################################################
    # TODO maybe specify classifier configuration along with this (so as to not specify something that might already exist)
    for i in range(0, task_amount):
        try:
            classifier = joblib.load(model_base_path + model_file_prefix + str(i) \
                                    + model_file_extension)
        except Exception:
            print('The classifier for output ' + str(i) + ' didn\'t exist.')
            if current_classifier_str == CLASSIFIER_STRING_ANN:
                classifier = MLPClassifier(solver='lbfgs', alpha=1e-2, 
                    hidden_layer_sizes=hidden_layer_neuron_amount, random_state=1)
            elif current_classifier_str == CLASSIFIER_STRING_SVM:
                classifier = svm.SVC()
        finally:
            # Append classifier to classifier list (in memory).
            classifiers.append(classifier)  
    ################################################################################################################################################################################
    ################################################################################################################################################################################
    ################################################################################################################################################################################
    ################################################################################################################################################################################
    # No threading version.
    start = time.time()
    # Each index corresponds to an instance.
    makespan_instance_machines_heuristic = []
    makespan_instance_machines_prediction = []
    SCALE_DATA = True
    USE_PARAMETER_SELECTION = False
    # Within each index, there'll be an array of machine_amount elements, in which each element
    # is the time during which each machine is running
    # Something along the lines of [[10,20,9,40], [99,88,22,11], ..., [10,9,21,35]]
    for i in range(0, task_amount): # For each task/classifier
        print("Training classifier " + str(i) + "...")
        # Data is loaded.
        TRAINING_FILE = baseDir + 'training/' + str(i) + '.csv' # Training file for current classifier
        TEST_FILE = baseDir + 'test/' + str(i) + '.csv' # Test file for current classifier
        training_set = pd.read_csv(TRAINING_FILE, header=None, delimiter=',')
        test_set = pd.read_csv(TEST_FILE, header=None, delimiter=',')
        
        # Create dataframe for data and separate target.
        df_training = pd.DataFrame(training_set)
        df_training_input = df_training.iloc[:, :-1] # Leave rows alone, slice everything except last column.
        # If not using entire ETC,use only the column relevant to the task/classifier.
        if not USING_ENTIRE_ETC:
            df_training_input = df_training_input.iloc[:, i * machine_amount : i * machine_amount + machine_amount]
        df_training_output = df_training.iloc[:, -1]
        
        # Validation/testing data is loaded.
        df_test = pd.DataFrame(test_set)
        df_test_input = df_test.iloc[:, :-1]
        # If not using entire ETC,use only the column relevant to the task/classifier.
        if not USING_ENTIRE_ETC:
            df_test_input = df_test_input.iloc[:, i * machine_amount : i * machine_amount + machine_amount]    
        df_test_output = df_test.iloc[:, -1]
        if SCALE_DATA:
            # Scale data because http://scikit-learn.org/stable/modules/neural_networks_supervised.html#tips-on-practical-use
            scaler = StandardScaler()  
            # Fit only on training data.
            scaler.fit(df_training_input)
            # Reconvert input training data to dataframe after scaling (which converts it to an array of arrays).
            df_training_input = pd.DataFrame(scaler.transform(df_training_input))
            # Re-init scaler just in case.
            scaler = StandardScaler()  
            scaler.fit(df_test_input)
            # Scale test data.
            df_test_input = pd.DataFrame(scaler.transform(df_test_input))        
        if current_classifier_str == CLASSIFIER_STRING_SVM:
            if USE_PARAMETER_SELECTION:
                # Grid of parameters, including all posible parameters for each configuration of
                # an SVM classifier.
                param_grid = [
                {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']}
                ]
                # Run grid search with all the possible classifier configurations.
                classifiers[i] = GridSearchCV(classifiers[i], param_grid=param_grid)
                # This generates multiple estimators.
                # Now the prediction will use the best estimator of all.
                # Should use grid_search as new classifier, persist it, and use it for prediction
                # as a normal classifier (according to documentation it uses the best estimator)
                # However, it fits every possible estimator with the data, so that's something of note.            
        # Classifier is trained using the data.
        classifiers[i].fit(df_training_input, df_training_output)
        # Classifier directory is generated if it doesn't exist.
        generar_jobs.generate_dir(model_base_path)
        # Classifier is persisted.
        joblib.dump(classifiers[i], model_base_path + model_file_prefix + str(i) \
                    + model_file_extension)
        # Classifier accuracy is determined using test data.
        results = []
        # Go through every test instance manually to calculate makespan for each
        # problem-classifier/task pair
        current_task_index = i * machine_amount # Column index within etc matrix
        print("    Doing makespan stuff...")
        test_instance_amount = len(df_test)
        for j in range(0, test_instance_amount): # For every validation instance
            if USING_ENTIRE_ETC:
                # df_test.iloc[j] is an ETC matrix + the corresponding classification for one task
                etc_matrix_scaled = df_test_input.iloc[j] # Scaled data for classification (since classifiers were
                # trained using scaled data)
                # Non-scaled data is used to calculate real makespan, using the original units of the problem.
                etc_matrix = df_test.iloc[j][:-1] # Get j problem instance, ignoring last column (the output/classification).
                classification_heuristic = float(df_test_output[j])
                # Every test example is classified, and its classification is appended
                # to a results array.
                # Make prediction for current problem instance or etc matrix (using scaled data).
                prediction_pandas = float(classifiers[i].predict(etc_matrix_scaled.values.reshape(1, -1)))
                results.append(prediction_pandas)
                prediction = float(prediction_pandas) # To work in floats.

                # Get subrow from original input data, to get the task/machine times right.
                sub_row_for_current_task = etc_matrix[current_task_index:current_task_index + machine_amount]
                # Makespan value for prediction
                current_makespan_prediction = sub_row_for_current_task[current_task_index + prediction]
                # Makespan value for heuristic
                current_makespan_heuristic = sub_row_for_current_task[current_task_index + classification_heuristic]
                if len(makespan_instance_machines_prediction) <= j: # If there's no entry for this problem instance.
                    # Init entry for problem instance, with each machine's makespan starting at 0.0.
                    makespan_instance_machines_prediction.append([0.0] * machine_amount)
                    makespan_instance_machines_heuristic.append([0.0] * machine_amount)
                makespan_instance_machines_prediction[j][int(prediction)] += current_makespan_prediction
                makespan_instance_machines_heuristic[j][int(classification_heuristic)] += current_makespan_heuristic
            else:
                # df_test.iloc[j] is an ETC matrix + the corresponding classification for one task
                sub_row_for_current_task_scaled = df_test_input.iloc[j] # Scaled data for classification (since classifiers were
                # trained using scaled data)
                # Non-scaled data is used to calculate real makespan, using the original units of the problem.
    #             etc_matrix = df_test.iloc[j][:-1] # Get j problem instance, ignoring last column (the output/classification).
    #             print("A: ")
    #             print(etc_matrix_scaled)
    #             print("B: ")
                sub_row_for_current_task = df_test.iloc[:, :-1].iloc[j, i * machine_amount : i * machine_amount + machine_amount]                
    #             print(etc_matrix)
                classification_heuristic = float(df_test_output[j])
                # Every test example is classified, and its classification is appended
                # to a results array.
                # Make prediction for current problem instance or etc matrix (using scaled data).
                prediction_pandas = float(classifiers[i].predict(sub_row_for_current_task_scaled.values.reshape(1, -1)))
                results.append(prediction_pandas)
                prediction = float(prediction_pandas) # To work in floats.

                # Makespan value for prediction
                current_makespan_prediction = sub_row_for_current_task[current_task_index + prediction]
                # Makespan value for heuristic
                current_makespan_heuristic = sub_row_for_current_task[current_task_index + classification_heuristic]
                if len(makespan_instance_machines_prediction) <= j: # If there's no entry for this problem instance.
                    # Init entry for problem instance, with each machine's makespan starting at 0.0.
                    makespan_instance_machines_prediction.append([0.0] * machine_amount)
                    makespan_instance_machines_heuristic.append([0.0] * machine_amount)
                makespan_instance_machines_prediction[j][int(prediction)] += current_makespan_prediction
                makespan_instance_machines_heuristic[j][int(classification_heuristic)] += current_makespan_heuristic            
        print("    Done with makespan stuff...")
        # Actual classification results are compared to expected values.
        accuracy = accuracy_score(df_test_output, results)
        print("    Classifier accuracy: " + str(accuracy))
        # Calculated accuracy is added to accuracies list.
        accuracy_scores.append(accuracy)
    end = time.time()
    print('Training took ' + str(end - start) + ' seconds')
    ################################################################################################################################################################################
    ################################################################################################################################################################################
    ################################################################################################################################################################################
    ################################################################################################################################################################################
    # Array that holds makespan values for the prediction.
    makespan_prediction = []
    for i in range(0, len(makespan_instance_machines_prediction)):
        makespan_prediction.append(np.max(makespan_instance_machines_prediction[i]))
    # Array that holds makespan values for the heuristic
    makespan_heuristic = []
    for i in range(0, len(makespan_instance_machines_heuristic)):
        makespan_heuristic.append(np.max(makespan_instance_machines_heuristic[i]))
    # Array that holds the difference between heuristic and prediction makespan.
    makespan_diff = []
    for i in range(0, len(makespan_prediction)):
        makespan_diff.append(makespan_prediction[i] - makespan_heuristic[i])
    # Calculate average difference between methods.
    avg_difference_between_methods = np.mean(makespan_diff)
    print('Average difference between techniques: ' + str(avg_difference_between_methods))
    if avg_difference_between_methods > 0:
        print('The heuristic works better on average')
    elif avg_difference_between_methods < 0:
        print('Savant works better on average')
    else:
        print('Both techniques work equivalently on average')
    ################################################################################################################################################################################
    ################################################################################################################################################################################
    ################################################################################################################################################################################
    ################################################################################################################################################################################
    # Average accuracy (for all classifiers) is calculated (nothing to do with threading).
    promedio = 0.
    score_amount = len(accuracy_scores)
    for i in range(0, score_amount):
        promedio += accuracy_scores[i]
    promedio /= score_amount
    print ('The average accuracy is {}'.format(promedio))        

if __name__ == "__main__":
    main()