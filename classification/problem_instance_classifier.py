# receive problem instance somehow
# levantar tantos clasificadores como sea
# generar solucion
# devolver solucion
from sklearn.externals import joblib
import pandas


def load_csv_problem_instance():
    return pandas.read_csv('problem_instance.csv', header=None, delimiter=',')

def remove_target_column_from_dataframe(training_testing):
    target = training_testing.iloc[:, -1]
    del training_testing[len(training_testing.columns) - 1]
    return target



def main():
    problem_instance_dataframe = load_csv_problem_instance()  # se pueden cargar instancias del problema con cualquier cantidad
    # de tareas, pero el numero de maquinas es fijo
    # o sea que si en la matriz tengo fila = tarea, columna = maquina, puedo tener tantas filas como quiera, pero cada fila
    # sigue teniendo la misma cantidad de columnas (numero de maquinas)
    target_column = remove_target_column_from_dataframe(problem_instance_dataframe)
    classifier = joblib.load('classifier.pkl')
    results = classifier.predict(problem_instance_dataframe)
    print(results)

main()
