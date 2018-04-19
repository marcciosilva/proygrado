// Generator program for HC and grid scheduling.
// Implements the range-based method by Ali et al. (2000)
//
// Output file format: similar to the one used by Braun et al. (2001), column vector used
// to represent the expected time to compute matrix ETC(t_i,m_j):
// floating point numbers, dimension (TXM)x1, ordered by task identifier
// (t1,m1)\\(t1,m2)\\...\\(t1,mM)\\(t2,m1)\\(t2,m2)...\\(tT,m1)\\...\\(tT,mM).
// The first line in the input file specifies the number of tasks and machines in the
// generated scenario.
// Input parameters:
// Number of tasks, number of machines, task heterogeneity level (0-Low, 1-High),
// machine heterogeneity level (0-Low, 1-High), consistency type (0-consistent,
// 1-semiconsistent, 2-inconsistent).
// Optional parameters:
// [heterogeneity model: 0-Ali et al., 1-Braun et al.] [variable type: 0-real, 1-integer].
// Heterogeneity ranks (tasks, machines): Ali et al. (10-100000,10-100), Braun et al.
// (100-3000,10-1000).
// Heterogeneity model by Braun et al. (100-3000,10-1000) assumed by default.
//
// Bibliographic references
// Ali, S., Siegel, H. J., Maheswaran, M., Ali, S., and Hensgen, D. (2000). Task Execution
// Time Modeling for Heterogeneous Computing Systems. In Proceedings of the 9th
// Heterogeneous Computing Workshop. IEEE Computer Society, Washington, DC, pp. 185.
// Braun, T. D., Siegel, H. J., Beck, N., Blni, L. L., Maheswaran, M., Reuther, A. I.,
// Robertson, J. P., Theys, M. D., Yao, B., Hensgen, D., and Freund, R. F. (2001). A
// comparison of eleven static heuristics for mapping a class of independent tasks onto
// heterogeneous distributed computing systems. Journal of Parallel and Distributed
// Computing 61, 6, pp. 810-837.
#include <math.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>

int partition(float a[], int l, int r)
{
    float pivot;
    float t;
    int i, j;
    pivot = a[l];
    i = l;
    j = r + 1;

    while (1)
    {
        do
            ++i;
        while (a[i] <= pivot && i <= r);
        do
            --j;
        while (a[j] > pivot);
        if (i >= j)
            break;
        t = a[i];
        a[i] = a[j];
        a[j] = t;
    }
    t = a[l];
    a[l] = a[j];
    a[j] = t;
    return j;
}

void quickSort(float a[], int l, int r)
{
    int j;

    if (l < r)
    {
        // divide and conquer
        j = partition(a, l, r);
        quickSort(a, l, j - 1);
        quickSort(a, j + 1, r);
    }
}

int main(int argc, char *argv[])
{
    if (argc < 6)
    {
        printf("Sintaxis: %s <num_tasks> <num_machines> <task_heterogeneity> <machine_heterogeneity> <consistency> [model] [type] [seed]\n", argv[0]);
        printf("Task heterogeneity levels: (0-Low, 1-High), machine heterogeneity levels: (0-Low, 1-High).\n");
        printf("Consistency type: (0-Consistent, 1-Semiconsistent, 2-Inconsistent).\n");
        printf("Optional: heterogeneity model: (0-Ali et al., 1-Braun et al.).\n");
        printf("\tRanks (tasks, machines) 0(Ali):(10-100000,10-100), 1(Braun):(100-3000,10-1000).\n");
        printf("\t(ranks by Braun et al. (100-3000,10-1000) assumed by default).\n");
        printf("Optional: type of task execution times: (0-real, 1-integer).\n");
        printf("Optional: seed for the pseudorandom number generator.\n");
        exit(1);
    }
    char *ht_st;  // "hi" or "lo"
    char *hm_st;  // "hi" or "lo"
    char consist; // "c": consistent, "u": inconsistent, "s" semiconsistent.
    char mod;     // "A": Ali et al. (2000), "B": Braun et al. (2001).
    char dist;    // "u": uniform.
    int RT, RM, model;
    char type;
    ht_st = (char *)malloc(sizeof(char) * 2);
    hm_st = (char *)malloc(sizeof(char) * 2);
    if (argc > 6)
    {
        model = atoi(argv[6]);
        if (model == 0)
        {
            mod = 'A';
        }
        else
        {
            if (model > 1)
            {
                printf("Heterogeneity model by Braun et al. (2001) assumed by default\n");
            }
            mod = 'B';
        }
    }
    else
    {
        model = 1;
        mod = 'B';
        printf("Heterogeneity model by Braun et al. (2001) assumed by default\n");
    }
    if (argc > 7)
    {
        type = atoi(argv[7]);
        if (type == 1)
        {
            printf("Type of task execution times: integer.\n");
        }
        else
        {
            type = 0;
            printf("Type of task execution times: real.\n");
        }
    }
    else
    {
        type = 0;
        printf("Type of task execution times: real (assumed by default).\n");
    }
    int seed;
    if (argc > 8)
    {
        printf("argv_8: %s\n", argv[8]);
        seed = atoi(argv[8]);
        printf("seed: %d\n", seed);
    }
    else
    {
        seed = time(NULL);
    }
    // Initialization of the pseudorandom number generator.
    srand48(seed);
    int NT = atoi(argv[1]);
    int NM = atoi(argv[2]);
    dist = 'u'; // Uniform distribution.
    int HT = atoi(argv[3]);
    if (HT == 0)
    {
        strcpy(ht_st, "lo");
        if (model == 0)
        {
            RT = 10;
        }
        else
        {
            RT = 100;
        }
    }
    else
    {
        strcpy(ht_st, "hi");
        if (HT > 1)
        {
            printf("Task heterogeneity level: 1-High (by default).\n");
            HT = 1;
        }
        if (model == 0)
        {
            RT = 100000;
        }
        else
        {
            RT = 3000;
        }
    }
    int HM = atoi(argv[4]);
    if (HM == 0)
    {
        strcpy(hm_st, "lo");
        RM = 10;
    }
    else
    {
        strcpy(hm_st, "hi");
        if (HM > 1)
        {
            printf("Machine heterogeneity level: 1-High (by default).\n");
            HM = 1;
        }
        if (model == 0)
        {
            RM = 100;
        }
        else
        {
            RM = 1000;
        }
    }
    int cons = atoi(argv[5]);
    if (cons == 0)
    {
        consist = 'c';
    }
    else if (cons == 1)
    {
        consist = 's';
    }
    else
    {
        if (cons > 2)
        {
            printf("Consistency type: 2-Inconsistent (by default).\n");
        }
        cons = 2;
        consist = 'i';
    }
    int i, j;
    float **ETC = (float **)malloc(sizeof(float *) * NT);
    if (ETC == NULL)
    {
        printf("Error in memory allocation for ETC, dimension %dx%d\n", NT, NM);
        exit(2);
    }
    for (i = 0; i < NT; i++)
    {
        ETC[i] = (float *)malloc(sizeof(float) * NM);
        if (ETC[i] == NULL)
        {
            printf("Error in memory allocation for row %d of ETC.\n", i);
            exit(2);
        }
    }
    char file_out[15];
    char file_log[15];
    sprintf(file_out, "%c.%c_%c_%s%s", mod, dist, consist, ht_st, hm_st);
    printf("file out: [%s]\n", file_out);
    sprintf(file_log, "%s.log", file_out);
    FILE *fp;
    FILE *fl;
    if ((fl = fopen(file_log, "w")) == NULL)
    {
        printf("Cannot write in file %s\n", file_log);
        exit(1);
    }
    fprintf(fl, "File: [%s]\n", file_out);
    fprintf(fl, "Test scenario with %d tasks and %d machines\n", NT, NM);
    fprintf(fl, "Model %c, distribution %c, consistency %c\n", mod, dist, consist);
    fprintf(fl, "RT:%d, RM:%d\n", RT, RM);
    fprintf(fl, "Task heterogeneity: %s, Machine heterogeneity: %s\n", ht_st, hm_st);
    if ((fp = fopen(file_out, "w")) == NULL)
    {
        printf("Cannot write in file %s\n", file_out);
        exit(1);
    }
    if (type == 1)
    {
        // ETC: integer values.
        fprintf(fl, "Type of task execution times: integer.\n");
    }
    else
    {
        fprintf(fl, "Type of task execution times: real.\n");
    }
    fprintf(fl, "seed: [%d]\n", seed);
    float p;
    float *fila = (float *)malloc(sizeof(float) * NM);
    for (i = 0; i < NT; i++)
    {
        p = RT * drand48();
        for (j = 0; j < NM; j++)
        {
            fila[j] = p * RM * drand48();
        }
        // Consistent instance: reordering of rows is required.
        if (cons == 0)
        {
            // Sort row
            quickSort(fila, 0, NM - 1);
        }
        else
        {
            if (cons == 1)
            {
                // Semiconsistent instance: reordering of odd rows is required.
                if ((i % 2) == 0)
                {
                    quickSort(fila, 0, NM - 1);
                }
            }
        }
        for (j = 0; j < NM; j++)
        {
            ETC[i][j] = fila[j];
        }
    }
    // The first row in the file specifies the number of tasks and machines in the scenario.
    fprintf(fp, "%d %d\n", NT, NM);
    for (i = 0; i < NT; i++)
    {
        for (j = 0; j < NM; j++)
        {
            if (type == 1)
            {
                // ETC: real values
                fprintf(fp, "%.0f\n", floor(ETC[i][j]));
            }
            else
            {
                // ETC: integer values
                fprintf(fp, "%.2f\n", ETC[i][j]);
            }
        }
    }
    close(fp);
    close(fl);
}
