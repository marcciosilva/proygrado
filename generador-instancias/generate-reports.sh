start=`date +%s`
HEADER_MSG='Results are in the following form: makespan difference#execution time#average accuracy'
FILE_EXT='.txt'
echo $HEADER_MSG >> 'report_full_etc_sv'$FILE_EXT
echo $HEADER_MSG >> 'report_partial_etc_svm'$FILE_EXT
echo $HEADER_MSG >> 'report_full_etc_ann'$FILE_EXT
echo $HEADER_MSG >> 'report_partial_etc_ann'$FILE_EXT
for i in `seq 1 50`;
do
    echo "-------------------------------------------"
    echo "-    Starting up iteration number "$i"       -"
    echo "-------------------------------------------"
    echo "#### Cleaning up... ####"
    # Usando toda la ETC
    # Limpiar todo
    rm -rf data-raw/
    rm -rf data-processed/
    # Generar directorios y scripts de generacion de datos
    echo "#### Generating directories and jobs... ####"
    python generar_jobs.py
    # Generar datos crudos
    echo "#### Generating raw data... ####"
    sh jobs/job-generate-raw-data.sh
    # Procesar datos y convertirlos a .csv
    echo "#### Generating processed data... ####"
    sh jobs/job-0.sh
    # Usando toda la ETC
    rm -rf models/
    echo "#### Generating report for full etc with SVM and ANN... ####"
    current_file='report_full_etc_sv'
    echo "#### Generating reports with full ETC... ####"
    ((python classifier_generator.py 128 4 0 0 0 True 1 >> 'report_full_etc_svm'$FILE_EXT) & (python classifier_generator.py 128 4 0 0 0 True 0 >> 'report_full_etc_ann'$FILE_EXT)) \
        && echo "#### Removing models to test with partial ETC... ####" && rm -rf models/ \
        && ((python classifier_generator.py 128 4 0 0 0 False 1 >> 'report_partial_etc_svm'$FILE_EXT) & (python classifier_generator.py 128 4 0 0 0 False 0 >> 'report_partial_etc_ann'$FILE_EXT))
    now=`date +%s`
    runtime=$((now-start))
    echo "Runtime up until now is "$runtime" seconds"
done
end=`date +%s`
runtime=$((end-start))
echo "###############################################"
echo "###############################################"
echo "Runtime was "$runtime" seconds"