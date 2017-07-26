# coding=utf-8
'''
Este script genera un (o varios) .sh que se va a encargar de generar ejemplos de entrenamiento.
'''
import os
import errno

parentDir = ''
# Donde van a quedar alojados los scripts finales
outputPath = 'jobs/'
# Comando para llamar al generador de instancias
generator = 'python training_example_generator.py '
# Directorio donde se van a dejar los ejemplos al final (instancia y solucion en archivos separados)
generatorDir = 'ejemplos-entrenamiento-separados/'
# Comando para llamar al parser que unifica instancias con sus salidas
parser = 'python parser.py '
# Directorio donde se van a dejar los ejemplos unificados
parserDir = 'ejemplos-entrenamiento-unificados/'
# En este array se van a guardar los comandos a ejecutar para generar instancias
# Se van a tener tantos elementos como archivos de generacion existan
# La idea es generar tantos archivos como jobs se quieran ejecutar en el cluster,
# para paralelizar
commands = []
# Cantidad de jobs a iniciar para generar ejemplos de entrenamiento
# Deberia ser un numero par (para que en el split de listas no queden separados
# la generacion y el parsing de un ejemplo)
jobAmount = 10
# Cantidad de instancias de test a utilizar en primer lugar, cantidad de instancias
# de entrenamiento a utilizar en segundo lugar
testTrainingAmount = [100, 600]
# Tipos de problema, donde la clave indica la cantidad de tareas del problema, y el valor
# indica la cantidad de maquinas
problemTypes = {128: 4, 512: 16}

def chunks(l, n):
	"""
	Dada una lista l y un parametro n, se devuelven listas de n elementos en la medida
	de lo posible
	"""
	n = max(1, n)
	return [l[i:i + n] for i in xrange(0, len(l), n)]

def generateDir(path):
	"""
	Si el directorio dado por path no existe, lo crea
	"""
	try:
		os.makedirs(path)
		print('Directory ' + path + ' created.')
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise

def main():
	for machineAmount in range(0, 2):
		for taskHeterogeneityType in range(0, 2):
			for machineHeterogeneityType in range(0, 3):
				# Para cada tipo o dimension del problema
				for tasks in problemTypes.keys():
					for instanceAmount in testTrainingAmount:
						machines = problemTypes[tasks]
						# Si estoy generando instancias de entrenamiento, cambio el sufijo del path
						if (instanceAmount == testTrainingAmount[0]):
							dirSuffix = '/test/'
						else:
							dirSuffix = '/training/'
						# subDir es el identificador de cada instancia del problema
						subDir = str(tasks) + 'x' + str(machines) + '-' + \
							str(machineAmount) + str(taskHeterogeneityType) + \
							str(machineHeterogeneityType) + dirSuffix
						directory = generatorDir + subDir
						# Agrego comandos al objeto commands
						commands.append(generator + str(tasks) + ' ' + str(machines)
										+ ' ' + str(machineAmount) + ' ' + str(
							taskHeterogeneityType) + ' ' + str(machineHeterogeneityType)
							+ ' ' + str(instanceAmount) +
							' ' + directory)
						# Genero directorio de salida que va a ser usado posteriormente
						generateDir(directory)
						directory = parserDir + subDir
						commands.append(
							parser + str(instanceAmount) + ' ' + parentDir + generatorDir + subDir
							+ ' ' + parentDir + parserDir + subDir)
						# Genero directorio de salida que va a ser usado posteriormente
						generateDir(directory)
	# Para cada job, agrego todos los comandos que correspondan generando un .sh
	# Todo queda en el directorio ./jobs/
	generateDir(outputPath)
	for index, job in enumerate(chunks(commands, jobAmount)):
		file = open(outputPath + 'job-' + str(index) + '.sh', 'w')
		for command in job:
			file.write(command + '\n')
		file.close()
	print 'Scripts .sh creados en el directorio ' + outputPath

if __name__ == '__main__':
	main()
