// Simple Helper for CPUFace
// Wrote by Artur 'h0m3' Paiva and under GPLv3
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Show help in case of user trying to use this function
int show_help() {
    printf("[CPUFace] This is a Helper for CPUFace\n");
    printf("[CPUFace] Try 'cpuface --help' instead\n");
    return 2;
}

// Append information to a file
int edit_file(int cpu, char *path, char *text) {
    char *new_path = (char *)malloc(sizeof(char) * (strlen(path) + 3));
    if (sprintf(new_path, path, cpu) < 0) {
        printf("Unable to format string '%s'\n", path);
        return 3;
    }

    FILE *buf = fopen(new_path, "w");
    if (buf == NULL) {
        printf("Unable to open '%s' for writing!\n", new_path);
        free(new_path);
        return 4;
    }

    if (fprintf(buf, "%s", text) < 0) {
        printf("Unable to write data (%s) into '%s'\n", text ,new_path);
        fclose(buf);
        free(new_path);
        return 5;
    }

    fclose(buf);
    free(new_path);
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        return show_help();
    }

    int cpu = atoi(argv[1]);
    if (!strcmp(argv[2], "online")) {
        char path[] = "/sys/devices/system/cpu/cpu%d/online";
        return edit_file(cpu, path, (char *)"1");
    } else if (!strcmp(argv[2], "offline")) {
        char path[] = "/sys/devices/system/cpu/cpu%d/online";
        return edit_file(cpu, path, (char *)"0");
    } else if (argc < 4) {
        return show_help();
    } else if (!strcmp(argv[2], "governor")) {
        char path[] = "/sys/devices/system/cpu/cpu%d/cpufreq/scaling_governor";
        return edit_file(cpu, path, argv[3]);
    } else if (!strcmp(argv[2], "speed")) {
        char path[] = "/sys/devices/system/cpu/cpu%d/cpufreq/scaling_cur_freq";
        return edit_file(cpu, path, argv[3]);
    } else {
        return show_help();
    }
}
