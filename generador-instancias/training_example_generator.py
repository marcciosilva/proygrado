# coding=utf-8
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
import errno

import generar_jobs

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

# Comando para llamar al generador de instancias
generatorCommand = './generator'
# Comando para llamar al resolvedor de instancias del problema
solverCommand = './heuristica-resolucion-hcsp'
separator = ' '
# Tipos de archivo de las salidas
inputSuffix = '.in'
outputSuffix = '.out'
moveCommand = 'mv'

def main():
	# Se obtienen caracteristicas del problema de consola
	try:
		taskAmount = int(sys.argv[1])
		machineAmount = int(sys.argv[2])
		taskHeterogeneityType = int(sys.argv[3])
		machineHeterogeneityType = int(sys.argv[4])
		consistencyType = int(sys.argv[5])
		amountOfInstances = int(sys.argv[6])
		outputPath = str(sys.argv[7])
	except:
		print 'Uso del script: python training_example_generator.py cantidad-tareas cantidad-maquinas heterogeneidad-tareas heterogeneidad-maquinas tipo-consistencia cantidad-instancias directorio-salida'
		print '### Tipos ###'
		print 'cantidad-tareas : int'
		print 'cantidad-maquinas : int'
		print 'heterogeneidad-tareas : 0 = Low, 1 = High'
		print 'heterogeneidad-maquinas : 0 = Low, 1 = High'
		print 'tipo-consistencia : 0 = Consistent, 1 = Semiconsistent, 2 = Inconsistent'
		print 'cantidad-instancias : int'
		print 'directorio-salida : str'
		print 'Ejemplo: python training_example_generator.py 4 16 0 0 0 100 ejemplos-entrenamiento-separados/4x16-000/test/'
	for i in range(0,amountOfInstances):
		# Se genera instancia del problema
		status, output = commands.getstatusoutput(\
		generatorCommand + separator + str(taskAmount) + separator + str(machineAmount) + separator \
		+ str(taskHeterogeneityType) + separator + str(machineHeterogeneityType) \
		+ separator + str(consistencyType) \
		)
		# Se obtiene una referencia al archivo generado
		fileNameRegex = '.*\[(.*)\].*'
		m = re.search(fileNameRegex, output)
		fileName = m.group(1)
		cmd = solverCommand + separator + fileName + ' > ' + str(i) + outputSuffix
		# Se aplica la resolucion a la instancia generada
		os.system(cmd)
		os.rename(fileName, str(i) + inputSuffix)
		# Si no existe, se genera el directorio de salida
		generar_jobs.generateDir(outputPath)
		# Se mueven archivos generados a carpeta de destino
		cmd = moveCommand + separator + str(i) + outputSuffix + separator + outputPath
		os.system(cmd)
		cmd = moveCommand + separator + str(i) + inputSuffix + separator + outputPath
		os.system(cmd)
		# Si pasa poco tiempo entre las llamadas al generator, no se genera una random seed
		# nueva (supongo), entonces meto delay para que las instancias generadas
		# sean realmente distintas.
		time.sleep(1)
	# Ahora en el directorio de salida tengo una pareja de archivos .in y .out que representan
	# a una instancia completa del problema (entrada y salida)
	print 'Parejas de archivos ' + inputSuffix + ' y ' + outputSuffix + ' generados en ' + outputPath

if __name__ == "__main__":
	main()
