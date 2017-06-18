# coding=utf-8
import subprocess
import csv
import os
import time
import configparser

#El objetivo es generar un csv para cargar y manipular con pandas.
#Este csv contendrá cada matiz de tiempos generada con el generador en una row y su respectivo valor de
#tupla solución, generada con la heurística.


#levanta los parámetros del archivo .ini
config = configparser.ConfigParser()
config.read('config.ini')
data_size = config['basic']['data_size']
project_location = config['basic']['project_location']

#creamos el csv vacío
csvfile = open('datos_entrenamiento.csv', 'wb')
resultwriter = csv.writer(csvfile, delimiter=',')

for i in range(0,int(data_size)):
    #llamamos un script de bash que se encarga de ejecutar el generador
    #no se ejecutó directamente el generador porque me dio problemas
    subprocess.call(project_location + "call_generador",shell=True)
    #abrimos el archivo generado por el generador
    attrs_example = open('B.u_c_hihi', 'r')

    line = attrs_example.readline() #descartamos la primera la porque se genera
                                    #indicando la cantidad de máquinas
                                    #y de tareas con las que se generó el archivo

    line = attrs_example.readline()
    #lines será una tira con todos los valores del archivo generado más adelante le agregaremos la tupla esperada
    lines = []
    while line:
        lines.append(float(line))
        line = attrs_example.readline()
    #idem a como hice con el generador, llamo la herística y consigo la solución
    subprocess.call(project_location + "call_heuristica",shell=True)
    #abro la solución que guardé en un archivo que se llama target (ver script de bash)
    attr_target = open('target', 'r')
    #ahora descartaremos las lineas del archivo quenerado por la heurística y nos quedamos con la cuarta linea
    attr_target.readline()
    attr_target.readline()
    attr_target.readline()
    line = attr_target.readline()
    line = line.replace("]", "")
    line = line.replace("[", "")
    array_numbers = line.split(" ")
    print array_numbers
    array_numbers.remove('\n')
    array_numbers.remove('')
    #agrego la solución a la linea
    lines.append(map(int,array_numbers))
    #agrego la linea a el csv
    resultwriter.writerow(lines)
    #remuevo todos los archivos, hago flush de las cosas y espero un poco, se ve que la
    #i/o precisa algo de tiempo
    os.remove("B.u_c_hihi")
    os.remove("B.u_c_hihi.log")
    os.remove("target")
    attrs_example.flush()
    attrs_example = None
    print i
    attr_target.flush()
    attr_target = None
    time.sleep(1)
