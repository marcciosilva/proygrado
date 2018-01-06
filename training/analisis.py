import math
import pandas
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def make_cross_validation():
    # Each csv includes 128 tasks (ie training instances).
    amount_of_problem_instance_csvs_to_use = 10
    split_data_for_manual_tests = False
    training_testing = load_csv_data(amount_of_problem_instance_csvs_to_use)
    # Save to CSV just in case.
    training_testing.to_csv("variable.csv",sep=',',index=False,header=False)
    target = remove_target_column_from_dataframe(training_testing)
    pipeline = create_pipeline_classifier()
    # Run cross validation with pipeline and target data.
    scores = cross_val_score(pipeline, training_testing, target, cv=5)
    save_results_to_file(pipeline, scores)

def load_csv_data(amount_of_problem_instance_csvs_to_use):
    data = []
    # Each file includes an ETC matrix and the output vector.
    for i in range(0,amount_of_problem_instance_csvs_to_use):
        data.append(pandas.read_csv(str(i) + ".csv", header=None, delimiter=','))
        training_testing = pandas.concat(data, ignore_index=True)
    return training_testing

def remove_target_column_from_dataframe(training_testing):
    target = training_testing.iloc[:,-1]
    del training_testing[len(training_testing.columns) -1]
    return target

def create_pipeline_classifier():
    classifier = create_neural_network_classifier()
    # generlo el pipeline con el escalado y el clasificador:
    pipeline = Pipeline([ ('StandardScaler', StandardScaler()), ('classify',classifier) ])
    # pipa se entiende como un nuevo clasificador formado por el preprocesamiento de escalado y un clasificador ANN
    # pipa puede ser tratado como si fuera un clasificador pelado.
    return pipeline

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

make_cross_validation()
