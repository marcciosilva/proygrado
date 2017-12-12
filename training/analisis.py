import pandas
import math
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


USE_SVM = True
USE_ANN = True
CSV_QTY = 150
task_amount = 3
no = 1  # Amount of output neurons
hidden_layer_amount = 2
split_data_for_manual_tests = False

def createClasiffier():

    hidden_layer_neuron_amount = tuple([int(math.ceil((task_amount - no) / 2))]
                                       * hidden_layer_amount)
    classifier = MLPClassifier(solver='lbfgs', alpha=1e-2,
                               hidden_layer_sizes=hidden_layer_neuron_amount, random_state=1)
    pipa = Pipeline([ ('StandardScaler', StandardScaler()), ('classify',classifier) ])
    return pipa


data = []
for i in range(0,CSV_QTY):
    data.append(pandas.read_csv(str(i)+".csv", header=None, delimiter=','))
    print("marccio puto")

print("marccio puto2")
training_testing = pandas.concat(data, ignore_index=True)
training_testing.to_csv("variable.csv",sep=',',index=False,header=False)
print("marccio puto2")

if split_data_for_manual_tests:
    train, test = train_test_split(training_testing, train_size = 0.8)
    train_y = train.iloc[:,-1]
    test_y = test.iloc[:,-1]
    del train.iloc[:,-1]
    del test.iloc[:,-1]

else:
    print("marccio puto3")
    target = training_testing.iloc[:,-1]
    del training_testing[len(training_testing.columns) -1]

    pipa = createClasiffier()
    print("marccio puto4")
    scores = cross_val_score(pipa, training_testing, target, cv=5)
    print(pipa.get_params())
    print("marccio puto5")
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
