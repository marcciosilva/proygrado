start=`date +%s`
HEADER_MSG='Results are in the following form: makespan difference#execution time#average accuracy'
FILE_EXT='.txt'
echo $HEADER_MSG >> 'report_full_etc_sv'$FILE_EXT
echo $HEADER_MSG >> 'report_partial_etc_svm'$FILE_EXT
echo $HEADER_MSG >> 'report_full_etc_ann'$FILE_EXT
echo $HEADER_MSG >> 'report_partial_etc_ann'$FILE_EXT
for i in `seq 1 100`;
do
    echo "-------------------------------------------"
    echo "-    Starting up iteration number "$i"       -"
    echo "-------------------------------------------"
    echo "#### Cleaning up... ####"
    # Usando toda la ETC
    # Limpiar todo
    rm -rf data-raw/
    rm -rf data-processed/
    rm -rf models/
    # Generar directorios y scripts de generacion de datos
    echo "#### Generating directories and jobs... ####"
    python generar_jobs.py
    # Generar datos crudos
    echo "#### Generating raw data... ####"
    sh jobs/job-generate-raw-data.sh
    # Procesar datos y convertirlos a .csv
    echo "#### Generating processed data... ####"
    sh jobs/job-0.sh
    # Usando toda la ETC con SVM
    echo "#### Generating report for full etc with SVM... ####"
    current_file='report_full_etc_sv'
    python classifier_generator.py 128 4 0 0 0 True 1 >> $current_file$FILE_EXT
    # Usando una porcion de la ETC con SVM
    echo "#### Generating report for partial etc with SVM... ####"
    current_file='report_partial_etc_svm'
    python classifier_generator.py 128 4 0 0 0 False 1 >> $current_file$FILE_EXT
    # Usando toda la ETC con ANN
    echo "#### Generating report for full etc with ANN... ####"
    current_file='report_full_etc_ann'
    python classifier_generator.py 128 4 0 0 0 True 0 >> $current_file$FILE_EXT
    # Usando una porcion de la ETC con ANN
    echo "#### Generating report for partial etc with ANN... ####"
    current_file='report_partial_etc_ann'
    python classifier_generator.py 128 4 0 0 0 False 0 >> $current_file$FILE_EXT
    now=`date +%s`
    runtime=$((now-start))
    echo "Runtime up until now is "$runtime" seconds"
done
end=`date +%s`
runtime=$((end-start))
echo "###############################################"
echo "###############################################"
echo "Runtime was "$runtime" seconds"