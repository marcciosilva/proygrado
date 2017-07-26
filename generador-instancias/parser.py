# coding=utf-8
'''
La idea de este módulo es recibir parejas de archivos (entrada y salida esperada) de instancias
del problema y generar en un directorio archivos .csv, para que cada uno sea usado como una
instancia de entrenamiento para el clasificador.
'''
import csv
import os
import re
import subprocess
import sys
import time
import errno

import training_example_generator
import generar_jobs

def main():
	# Se obtienen directorios (donde estan los datos a usar) desde consola
	try:
		instanceAmount = int(sys.argv[1])
		inputPath = str(sys.argv[2])
		outputPath = str(sys.argv[3])
	except:
		print 'Uso del script: python parser.py cantidad-instancias directorio-entrada directorio-salida'
		print '### Tipos ###'
		print 'cantidad-instancias : int'
		print 'directorio-entrada : str'
		print 'directorio-salida : str'
		print 'Ejemplo: python parser.py 100 ejemplos-entrenamiento-separados/4x16-000/test/ ejemplos-entrenamiento-unificados/4x16-000/test/'
	for i in range(0, instanceAmount):
		# Se accede a la entrada del problema
		f = open(inputPath + str(i) +
				training_example_generator.inputSuffix, 'r')
		firstLine = f.readline()
		# Se obtiene la dimension del problema, que deberia estar declarada al principio
		# del archivo
		m = re.search('(\d*)\s(\d*)\n', firstLine)
		taskNumber = int(m.group(1))
		machineNumber = int(m.group(2))
		linesToRead = taskNumber * machineNumber
		etcMatrix = []
		# Leo todas las lineas del documento y genero matriz ETC
		for j in range(0, linesToRead):
			m = re.search('(\d*\.\d*)\n', f.readline())
			value = float(m.group(1))
			etcMatrix.append(value)
		# Abro el archivo de la solucion
		f = open(inputPath + str(i) +
				training_example_generator.outputSuffix, 'r')
		# Se ignoran las tres primeras lineas
		for k in range(0, 3):
			f.readline()
		line = f.readline()
		# Se obtiene vector solucion
		solutionVector = [int(s) for s in line.split() if s.isdigit()]
		# Si no existe, se genera el directorio de salida
		generar_jobs.generateDir(outputPath)
		# Se genera un .csv para cada indice del vector solucion
		for index, value in enumerate(solutionVector):
			fileName = outputPath + str(index) + '.csv'
			if (is_csv_empty(fileName)):
				# Se crea el .csv vacio
				csvfile = open(fileName, 'wb')
			else:
				# Se agrega contenido al .csv existente (se abre con la flag de append)
				csvfile = open(fileName, 'a')
			resultwriter = csv.writer(csvfile, delimiter=',')
			# lines será una tira con todos los valores del archivo generado; más adelante le agregaremos la tupla esperada
			lines = []
			# Se agrega una columna por cada valor de la matriz etc
			for timeValue in etcMatrix:
				lines.append(timeValue)
			# Agrego la asignacion tarea-maquina que corresponda
			lines.append(value)
			# Agrego la linea a el csv
			resultwriter.writerow(lines)
			csvfile.close()
	print 'Archivos .csv creados en ' + outputPath

def is_csv_empty(fileName):
	try:
		with open(fileName, 'r') as csvfile:
			return False
	except IOError:
		return True

if __name__ == "__main__":
	main()
