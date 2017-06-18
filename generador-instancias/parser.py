# obtener cantidad de tareas
# obtener cantidad de maquinas
# leer cantTareas * cantMaquinas lineas y generar la lista y bla
# con cantidad de maquinas se sabe la cantidad de clasificadores y el tamanho de la salida
import re

availableTrainingExamples = 10

for i in range(0, availableTrainingExamples):
	f = open(str(i) + '.input', 'r')
	firstLine = f.readline()
	m = re.search('(\d*)\s(\d*)\n', firstLine)
	taskNumber = int(m.group(1))
	machineNumber = int(m.group(2))
	print '{} tasks and {} machines'.format(taskNumber,machineNumber)
	linesToRead = taskNumber * machineNumber
	etcMatrix = []
	for j in range(0,linesToRead):
		m = re.search('(\d*\.\d*)\n', f.readline())
		value = float(m.group(1))
		etcMatrix.append(value)
	print etcMatrix

	f = open(str(i) + '.output', 'r')
	# Se ignoran las tres primeras lineas.
	for k in range(0,3):
		f.readline()
	line = f.readline()
	solutionVector = [int(s) for s in line.split() if s.isdigit()]
	print solutionVector
	print ('##############################################')