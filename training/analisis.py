import pandas
import math
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def createClasiffier():
    task_amount = 128
    no = 1  # Amount of output neurons
    hidden_layer_amount = 2
    # esta funcion se encarga de crear una ann para clasificar.
    # acá usa la heurística esa que saqué de tu código para determinar la cantidad de capas
    # intermedias para la red neuronal.
    hidden_layer_neuron_amount = tuple([int(math.ceil((task_amount - no) / 2))]
                                       * hidden_layer_amount)

    classifier = MLPClassifier(solver='lbfgs', alpha=1e-2,
                               hidden_layer_sizes=hidden_layer_neuron_amount, random_state=1)
    # generlo el pipeline con el escalado y el clasificador:
    pipa = Pipeline([ ('StandardScaler', StandardScaler()), ('classify',classifier) ])
    # pipa se entiende como un nuevo clasificador formado por el preprocesamiento de escalado y un clasificador ANN
    # pipa puede ser tratado como si fuera un clasificador pelado.
    return pipa


def makeCrossValidation():
    # algunos parámetros, algunos están al pedo, no los uso.
    # CSV_QTY es importante, cuántos de los 600 de entrenamiento vamos a usar, recordemos
    # que cada uno de esos 600 tiene 128 tareas. De este parámetro nos van a depender tiempos.
    CSV_QTY = 10
    split_data_for_manual_tests = False
    data = []
    # levanto todos los datos, los datos son los que generamos. 600 archivos que representan una matriz y la máquina
    # a la cual son asignadas las tareas. Los concateno en un DataFrame de pandas. Los datos están en unos csv, los generamos
    # la otra vuelta. Si no los tenés te los paso, trato de que queden acá en el repo, en esta misma carpeta.
    for i in range(0,CSV_QTY):
        data.append(pandas.read_csv(str(i)+".csv", header=None, delimiter=','))
        training_testing = pandas.concat(data, ignore_index=True)

    # Solo lo guardo a csv para tenerlo ahí, qué se yo.
    training_testing.to_csv("variable.csv",sep=',',index=False,header=False)

    # saco del dataframe la columna objetivo.
    target = training_testing.iloc[:,-1]
    del training_testing[len(training_testing.columns) -1]
    # llamo a la funcion nuestra que devuelve el clasificador pipa.
    pipa = createClasiffier()
    # hago un cross cross validation ocn los datos de pipa y targer.
    scores = cross_val_score(pipa, training_testing, target, cv=5)

    ## GUARDO LOS RESULTADOS en un archivo, esto lo hago porque lo ejecutaba desatendido y desvinculado de
    # terminal en el AWS.
    f = open('results.out', 'a')
    f.write('\n\n' + "###################################################" + '\n')
    f.write("###################################################" + '\n\n')
    f.write(str(pipa.get_params()) + '\n')
    f.write("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2) + '\n')
    f.close()

makeCrossValidation()
