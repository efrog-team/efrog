#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>
#include <string.h> 
#include <math.h>
#include <stdint.h>
#include <unistd.h>
#include <dirent.h>
#include <stdbool.h>
#include <signal.h>
#include <sys/wait.h>
#include <time.h>
#include <sys/resource.h>

int DEBUG = 0;


double get_time() {
    struct timespec time;
    clock_gettime(CLOCK_MONOTONIC, &time);
    return (double)time.tv_sec + (double)time.tv_nsec * 1e-6;
}

int getbytes(int num) {
    return (int)((floor(log10(num)) + 2));
}


int create_files(int submission_id, char *code, char *language) {

    const int path_length = 14 + getbytes(submission_id);
    char path[path_length]; 

    sprintf(path, "checker_files/%d", submission_id);
    int status = mkdir(path, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

    if (status != 0) { //error

        if(DEBUG) printf("failed to create a dir\n");
        return 1;

    } 

    FILE  *file_code;
    
    if (strcmp(language, "Python 3 (3.10)") == 0) {

        char code_path[path_length + getbytes(submission_id) + 4]; // path_length + getbytes(submission_id) + 4 (/.py)
        sprintf(code_path, "%s/%d.py", path, submission_id);

        file_code = fopen(code_path, "w");

        if (file_code == NULL) {

            if(DEBUG) printf("file_code = NULL\n");
            return 1;

        }

        fprintf(file_code, "%s", code);
        fclose(file_code);

    } else if (strcmp(language, "C++ 17 (g++ 11.2)") == 0 || strcmp(language, "C 17 (gcc 11.2)") == 0) { //cpp and c
        bool cpp = strcmp(language, "C++ 17 (g++ 11.2)") == 0; //c++
        int code_path_length = path_length + getbytes(submission_id) + 5;
        char code_path[code_path_length]; 
        sprintf(code_path, cpp ? "%s/%d.cpp" : "%s/%d.c", path, submission_id);
        file_code = fopen(code_path, "w");

        if (file_code == NULL) {

            if(DEBUG) printf("file_code = NULL\n");
            return 1;

        }

        fprintf(file_code, "%s", code);
        fclose(file_code);

        char compile_command[11 +  2 * code_path_length]; //g++-11 main.cpp -o main len : 7 +  2 * code_path_length
        sprintf(compile_command, cpp ? "g++-11 %s -o %s/%d" : "gcc-11 %s -lm -o %s/%d", code_path, path, submission_id); 
        int status = system(compile_command); 
        if (status == 1) { 
            if (DEBUG) printf("failed to compile (cpp)\n");
        }

    } else {

        if (DEBUG) printf("unknown language\n");
        return 1;

    }

}

int delete_files(int submission_id) {
    const int path_length = 14 + getbytes(submission_id);

    char dir_path[path_length];
    sprintf(dir_path, "checker_files/%d", submission_id);

    char command[7 + path_length];
    sprintf(command, "rm -rf %s", dir_path);

    int result = system(command);

    if (result == 0) {

        return 0;

    } else {

        if (DEBUG) printf("failed to remove the dir");
        return 1;

    }
}

struct Result
{
    int status; /* 0 - Correct answer
                   1 - Wrong answer
                   2 - Compilation error
                   3 - Runtime error
                   4 - Time limit
                   5 - Memory limit
                   6 - Internal error */      
    int time; //ms
    int cpu_time;
    int memory;
    char *output;
    char *description;
};

struct Result *check_test_case(int submission_id, int test_case_id, char *language, char *input, char *solution) {
    int time, cpu_time;//ms
    int memory; //KB
    double start, end;
    struct Result *result = malloc(sizeof(struct Result));

    char output[1000000] = "";

    const int path_length = 14 + getbytes(submission_id);
    const int testpath_input_length = path_length + getbytes(test_case_id) + 11;

    char testpath_input[testpath_input_length]; //..._input.txt 
    char testpath_output[testpath_input_length + 1]; //..._output.txt
    char testpath_solution[testpath_input_length + 3]; //..._solution.txt

    sprintf(testpath_input, "checker_files/%d/%d_input.txt", submission_id, test_case_id);
    sprintf(testpath_output, "checker_files/%d/%d_output.txt", submission_id, test_case_id);
    sprintf(testpath_solution, "checker_files/%d/%d_solution.txt", submission_id, test_case_id);

    FILE *file_output;
    FILE *file_input;
    FILE *file_solution;

    file_input = fopen(testpath_input, "w");

    if (file_input == NULL) {

        if(DEBUG) printf("file_input = NULL\n");
        result->status = 6;
        result->time = 0;
        result->cpu_time = 0;
        result->memory = 0;
        result->output = "";
        result->description = "";
        return result;
        
    }

    fprintf(file_input, "%s", input);
    fclose(file_input);

    file_solution = fopen(testpath_solution, "w");

    if (file_solution == NULL) {

        if(DEBUG) printf("file_solution = NULL\n");
        result->status = 6;
        result->time = 0;
        result->cpu_time = 0;
        result->memory = 0;
        result->output = "";
        result->description = "";
        return result;

    }

    fprintf(file_solution, "%s", solution);
    fclose(file_solution);

    file_output = fopen(testpath_output, "w");

    if (file_solution == NULL) {

        if(DEBUG) printf("file_output = NULL\n");
        result->status = 6;
        result->time = 0;
        result->cpu_time = 0;
        result->memory = 0;
        result->output = "";
        result->description = "";
        return result;

    }
    
    if (strcmp(language, "Python 3 (3.10)") == 0) {

        char code_path[path_length + getbytes(submission_id) + 4]; // path_length + getbytes(submission_id) + 4 (/.py)
        sprintf(code_path, "checker_files/%d/%d.py", submission_id, submission_id);

        struct rusage usage;


        pid_t pid = fork();

        if (pid == 0) {
            //child process

            freopen(testpath_input, "r", stdin);
            freopen(testpath_output, "w", stdout);
            
            char *args[] = {"python3", code_path, NULL};
            execvp("python3", args);

        } else if (pid > 0) {
            //parent process

            int status;

            start = get_time();
            wait(&status);
            end = get_time();

            time = (int)ceil(end - start);
            getrusage(RUSAGE_CHILDREN, &usage);
            cpu_time = usage.ru_utime.tv_usec / 1000;
            memory = usage.ru_maxrss;

        } else {
            if (DEBUG) printf("failed to create child process");
            result->status = 6;
            result->time = 0;
            result->cpu_time = 0;
            result->memory = 0;
            result->output = "";
            result->description = "";
            return result;
        }

        
    } else if (strcmp(language, "C++ 17 (g++ 11.2)") == 0 || strcmp(language, "C 17 (gcc 11.2)") == 0) {

        int code_path_length = path_length + getbytes(submission_id) + 1; // path_length + getbytes(submission_id) + 1 :(/) :)))))))))))))))))))))))))))))))))

        char code_path[code_path_length]; 
        sprintf(code_path, "checker_files/%d/%d", submission_id, submission_id);

        char command[code_path_length + testpath_input_length + testpath_input_length + 7]; 

        sprintf(command, "%s < %s > %s", code_path, testpath_input, testpath_output);

        start = get_time();
        system(command);
        end = get_time();
        time = ceil(end - start);

    } else {

        if (DEBUG) printf("unknown language");
        result->status = 6;
        result->time = 0;
        result->cpu_time = 0;
        result->memory = 0;
        result->output = "";
        result->description = "";

        return result;

    }

    file_output = fopen(testpath_output, "r");
    file_solution = fopen(testpath_solution, "r");

    char output_buffer[1000000], solution_buffer[1000000];
    
    char *output_read = fgets(output_buffer, 1000000, file_output);
    
    char *solution_read = fgets(solution_buffer, 1000000, file_solution);
    
    int status = -1;

    while (output_read != NULL && solution_read != NULL) {

        for (int i = strlen(output_buffer) - 1; i >= 0; i--) {

            if (output_buffer[i] != '\n' && output_buffer[i] != ' ') { 

                output_buffer[i + 1] = '\0';
                break;
            }

        }

        for (int i = strlen(solution_buffer) - 1; i >= 0; i--) {

            if (solution_buffer[i] != '\n' && solution_buffer[i] != ' ') { 

                solution_buffer[i + 1] = '\0';
                break;
            }

        }

        strcat(output, output_buffer);
        strcat(output, "\n");

        if (strcmp(output_buffer, solution_buffer) != 0) {

            status = 1;
            break;
        }

        output_read = fgets(output_buffer, 1000000, file_output);
        solution_read = fgets(solution_buffer, 1000000, file_solution);

    }

    
    if (status == -1) {

        if (output_read != NULL || solution_read != NULL) {

            status = 1;

        } else {

            status = 0;

        }    
    }  

    while (fgets(output_buffer, 1000000, file_output) != NULL) {

        strcat(output, output_buffer);
        strcat(output, "\n");

    }

    fclose(file_solution);      
    pclose(file_output);

    
    
    result->status = status;
    result->time = time;
    result->cpu_time = cpu_time;
    result->memory = memory;
    result->output = output;
    result->description = "";

    return result;
    
}
      
int main() {

    DEBUG = 1;

    create_files(12312365, "num = int(input())\nprint(f\"{num // 10} {num % 10}\")\n", "Python 3 (3.10)");
    //create_files(12312365, "#include <iostream>\n\nusing namespace std;\n\nint main() {\n    int a;\n    cin >> a;\n    cout << a * a;\n    return 0;\n}", "C++ 17 (g++ 11.2)");
    struct Result *result = check_test_case(12312365, 123123, "Python 3 (3.10)", "99", "9 9");
    delete_files(12312365);

    printf("status: %d\noutput: %stime: %dms\ncpu_time: %dms\nmemory: %dKB\n", 

    result->status, 
    result->output, 
    result->time, 
    result->cpu_time, 
    result->memory);

    return 0;

}



