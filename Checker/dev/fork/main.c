#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <signal.h>
#include <sys/wait.h>
#include <time.h>
#include <math.h>


double get_time() {
    struct timespec time;
    clock_gettime(CLOCK_MONOTONIC, &time);
    return (double)time.tv_sec + (double)time.tv_nsec * 1e-6;
}

int main() {
    pid_t pid = fork();
    float t1, t2;
    
    if (pid == 0) {
        //child process
        printf("child process\n");
        char* args[] = {"python3", "test.py", NULL};
        
        execvp("python3", args);
        

    } else if (pid > 0) {
        //parent process
        printf("parent process waiting...\n");
        t1 = get_time();
        wait(NULL);
        t2 = get_time();
        
        double res = t2 - t1;
        printf("%dms\n%f", (int) ceil(res), res);

    }
    

}
