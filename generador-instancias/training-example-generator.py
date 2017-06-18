'''
Script para generar ejemplos de entrenamiento de la forma i.input e i.output (archivos)
La idea es setear los parametros en este archivo para determinar el tipo de instancia
de HCSP, y se generan tantas instancias de entrenamiento (par de archivos) como
se quiera
'''

import os
import re
import commands
import sys
import time

class TaskHeterogeneityType:
    Low=0
    High=1

class MachineHeterogeneityType:
    Low=0
    High=1	

class ConsistencyType:
    Consistent=0
    Semiconsistent=1
    Inconsistent=2	

def main():
	generatorCommand = './generator'
	solverCommand = './heuristica-resolucion-hcsp'
	separator = ' '
	taskAmount = 32
	machineAmount = 2
	taskHeterogeneityType = TaskHeterogeneityType.Low
	machineHeterogeneityType = MachineHeterogeneityType.Low
	consistencyType = ConsistencyType.Consistent
	amountOfInstances = 10
	for i in range(0,amountOfInstances):
		status, output = commands.getstatusoutput(\
		generatorCommand + separator + str(taskAmount) + separator + str(machineAmount) + separator \
		+ str(taskHeterogeneityType) + separator + str(machineHeterogeneityType) \
		+ separator + str(consistencyType) \
		)
		fileNameRegex = '.*\[(.*)\].*'
		m = re.search(fileNameRegex, output)
		fileName = m.group(1)
		cmd = solverCommand + separator + fileName + ' > ' + str(i) + '.output'
		os.system(cmd)
		os.rename(fileName, str(i) + '.input')
		# Si pasa poco tiempo entre las llamadas al generator, no se genera una random seed
		# nueva (supongo), entonces meto delay para que las instancias generadas
		# sean realmente distintas.
		time.sleep(1)

main()