// Min-min scheduler.
// Paraetros: <archivo_instancia>
// Primera linea del archivo de instancias tiene el numero de tareas y de maquinas.
//
 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
 
#define INFT 9999999999.0
#define NO_ASIG -1
#define SIZE_NOM_ARCH 80
 
#define DEBUG 0
 
int main(int argc, char *argv[]){
 
if (argc < 2){
        printf("Sintaxis: %s <archivo_instancias> \n", argv[0]);
        exit(1);
}
 
int NT, NM;
 
FILE *fi;
 
char *arch_inst;
arch_inst = (char *)malloc(sizeof(char)*120);
 
strcpy(arch_inst,argv[1]);
 
printf("Archivo: %s\n",arch_inst);
 
if((fi=fopen(arch_inst, "r"))==NULL){
    printf("No se puede leer archivo de instancia %s\n",arch_inst);
    exit(1);
}
 
// Primera linea: NT y NM
fscanf(fi,"%d %d",&NT,&NM);
printf("NT: %d, NM: %d\n",NT,NM);
 
// Leer archivo, almacenando matriz ETC
 
int i,j;
 
float **ETC = (float **) malloc(sizeof(float *)*NT);
 
if (ETC == NULL){
        printf("Error al reservar memoria para ETC, dimensiones %dx%d\n",NT,NM);
        exit(2);
}
 
for (i=0;i<NT;i++){
        ETC[i] = (float *) malloc(sizeof(float)*NM);
        if (ETC[i] == NULL){
                printf("Error al reservar memoria para fila %d de ETC\n",i);
                exit(2);
        }
}
 
int max_etc=0;
 
for (i=0;i<NT;i++){
        for (j=0;j<NM;j++){
        fscanf(fi,"%f",&ETC[i][j]);
        }
}
 
close(fi);
 
// Array de máquinas, almacena el MAT
float *mach = (float *) malloc(sizeof(float)*NM);
if (mach == NULL){
        printf("Error al reservar memoria para mach, dimension %d\n",NT);
        exit(2);
}
 
for (j=0;j<NM;j++){
        mach[j]=0.0;
}
 
// Array de asignaciones
int *asig= (int*) malloc(sizeof(float)*NT);
if (asig == NULL){
        printf("Error al reservar memoria para asig, dimension %d\n",NT);
        exit(2);
}
 
int nro_asig=0;
for (i=0;i<NT;i++){
        asig[i]=NO_ASIG;
}
 
float min_ct;
float min_ct_task;
 
int best_machine, best_mach_task;
int best_task;
 
while (nro_asig < NT){
        // Seleccionar tarea no asignada con ct m▒nimo.
        best_task = -1;
        best_machine = -1;
        min_ct = INFT;
 
        // Recorrer tareas.
        for (i=0;i<NT;i++){
                min_ct_task = INFT;
                best_mach_task = -1;
                if (asig[i] == NO_ASIG){
                        // No est▒ asignada, evaluar el minimo ct de la tarea.
                        float ct=0.0;
                        // Recorrer m▒quinas.
                        for (j=0;j<NM;j++){
                                ct = mach[j]+ETC[i][j];
//printf("Tarea: %d, ct en maq %d: %f\n",i,j,ct);
                                if (ct < min_ct_task){
                                        min_ct_task = ct;
                                        best_mach_task = j;
//printf("Actualizo min_ct_task %f best_mach_task %d\n",min_ct_task,best_mach_task);
                                }
                        }
//printf("Tarea %d, min_ct_task: %f, best_mach_task: %d\n",i,min_ct_task,best_mach_task);
                }
 
                if (min_ct_task < min_ct){
                        min_ct = min_ct_task;
                        best_task = i;
                        best_machine = best_mach_task;
                }
        }
        mach[best_machine]+=ETC[best_task][best_machine];
        asig[best_task]=best_machine;
        nro_asig++;
 
# if DEBUG
        printf("Asigno tarea %d en maquina %d\n",best_task,best_machine);
        for (j=0;j<NM;j++){
                printf("Mach: %f\t",mach[j]);
        }
        printf("\n");
#endif
 
}
 
float makespan=0.0;
for (j=0;j<NM;j++){
        if (mach[j]>makespan){
                makespan = mach[j];
        }
}
 
printf("Makespan: %f\n",makespan);
 
printf("[");
for (i=0;i<NT;i++){
    printf("%d ",asig[i]);
}
printf("]\n");
 
#if DEBUG
printf("Asignacion:\n");
for (i=0;i<NT;i++){
        printf("Tarea %d en maquina %d\n",i,asig[i]);
}
 
for (i=0;i<NT;i++){
    for (j=0;j<NM;j++){
        printf("ETC(%d,%d):%f\n",i,j,ETC[i][j]);
    }
}
#endif
 
}