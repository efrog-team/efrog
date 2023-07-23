#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <signal.h>
#include <sys/wait.h>
#include <time.h>
#include <math.h>
#include <sys/resource.h>

double get_time() {
    struct timespec time;
    clock_gettime(CLOCK_MONOTONIC, &time);
    return (double)time.tv_sec + (double)time.tv_nsec * 1e-6;
}

int main() {
    
    float t1, t2, t3, t4;
    double res;
    char command[] = "./test < input.txt > output.txt";
    t3 = get_time();
    system(command);
    t4 = get_time();
    double res2 = t4 - t3;
    printf("system time %dms\n", (int) ceil(res2));
    pid_t pid = fork();
    if (pid == 0) {
        //child process
        freopen("input.txt", "r", stdin);

        freopen("output.txt", "w", stdout);

        freopen("stderr.txt", "w", stderr);

        printf("child process\n");
        char* args[] = {"./test", NULL};
        execvp("./test", args);

    } else if (pid > 0) {
        //parent process
        int status;
        t1 = get_time();
        wait(&status);
        t2 = get_time();
        res = t2 - t1;
        struct rusage usage;
        getrusage(RUSAGE_CHILDREN, &usage);
        printf("cpu user time: %ld ms\ncpu system time: %ldms\n", usage.ru_stime.tv_usec / 1000, usage.ru_utime.tv_usec / 1000);
        printf("fork time(user time): %dms\n", (int) ceil(res));
        if (WIFEXITED(status)) {
            if (WEXITSTATUS(status) != 0) {
                printf("error");
            }
        }

    }
    

    printf("sub : %f ms\n", (res2 - res));

}
