/*
 * catcho - outputing text to the standard output
 *
 * Usage
 * -----
 *  catcho [options]
 *
 * Options
 * -------
 *  -m --mode MODE      Set the initial text mode (Default: passthrough)
 *  -v --version        Display program information and exit
 *  -V --verbose        Duplicate stdout on stderr
 *
 * Modes
 * -----
 *  passthru / passthrough / normal / n - Input is copied to output verbatim.
 *  null / z - Input is dropped.
 *  hb - Input (interpreted as hex) is compressed to bytes on the output.
 *  bh - The opposite of hb.
 *  ib - Input (interpreted as bit-bytes) is compressed to bytes on the output.
 *  bi - The opposite of ib.
 *
 *  Append 'f' to any mode (eg:  bhf):  Input is interpreted as '\n'-delimited
 *  filenames.  File contents are filtered based on mode and sent to output.
 *
 * Switching modes
 * ---------------
 *  When catcho receives signal SIGINT (ctrl-C from the terminal, for example),
 *  any pending input/output is flushed and catcho then interprets the input
 *  as a mode name terminated by a '\n'.  Once the input provides a string\n,
 *  it switches the desired mode and input processing resumes.
 *
 * Exiting catcho
 * --------------
 *  Since SIGINT is used for mode switching, the 'normal' way to terminate
 *  catcho is by sending it an End-Of-File byte on its input. (ctrl-D on your
 *  terminal)
 */

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <getopt.h>
#include <signal.h>

#define LAST_STR_CHAR(s) (s[strlen(s)-1])

/* modes */
enum mode
{
    N,
    Z,
    HB,
    BH,
    IB,
    BI
};

/* global state */
static enum mode current_mode = N;
static int  current_mode_f = 0;
static int  current_verbose = 0;

static size_t ccfwrite(const void *ptr, size_t size, size_t nmemb)
{
    size_t ret;
    ret = fwrite(ptr, size, nmemb, stdout);

    if (current_verbose)
        fwrite(ptr, size, nmemb, stderr);

    return ret;
}

static void sigint(int sig)
{
    (void)sig;
    ccfwrite("in signal handler\n", 18, 1);
}

static int set_mode(const char *mode)
{
    if (!mode)
        return 0;

    if (!strcmp(mode, "passthru") || // these don't support 'f' suffix
        !strcmp(mode, "passthrough") ||
        !strcmp(mode, "normal"))
    {
        current_mode = N;
        current_mode_f = 0;
    }
    else if (!strcmp(mode, "null")) // this doesn't support 'f' suffix
    {
        current_mode = Z;
        current_mode_f = 0;
    }
    else if (!strncmp(mode, "n", 1))
    {
        current_mode = N;
        current_mode_f = (LAST_STR_CHAR(mode) == 'f');
    }
    else if (!strncmp(mode, "z", 1))
    {
        current_mode = Z;
        current_mode_f = (LAST_STR_CHAR(mode) == 'f');
    }
    else if (!strncmp(mode, "hb", 2))
    {
        current_mode = HB;
        current_mode_f = (LAST_STR_CHAR(mode) == 'f');
    }
    else if (!strncmp(mode, "bh", 2))
    {
        current_mode = BH;
        current_mode_f = (LAST_STR_CHAR(mode) == 'f');
    }
    else if (!strncmp(mode, "ib", 2))
    {
        current_mode = IB;
        current_mode_f = (LAST_STR_CHAR(mode) == 'f');
    }
    else if (!strncmp(mode, "bi", 2))
    {
        current_mode = BI;
        current_mode_f = (LAST_STR_CHAR(mode) == 'f');
    }
    else
    {
        fprintf(stderr, "Mode string '%s' not recognized\n", mode);
        return 0;
    }

    return 1;
}

void show_version(const char *name)
{
    printf("%s version 1.0\n", name);
}

int main(int argc, char **argv)
{
    /*
     * handling command-line arguments:
     * i'm going to leave opterr alone (defaults to non-zero)
     * \this causes getopt to print its own error messages to
     *  stderr if things go wrong, which is fine.
     */

    const char *shortopts = "m:vV";

    const struct option longopts[] = {
        { "mode",    required_argument, NULL, 'm' },
        { "version", no_argument,       NULL, 'v' },
        { "verbose", no_argument,       NULL, 'V' },
        { NULL,      0,                 NULL,  0  }
    };

    int opt;

    while ((opt = getopt_long(argc, argv, shortopts, longopts, NULL)) != -1)
    {
        switch (opt)
        {
            case '?':
                return 1;

            case 'm':
                if (!set_mode(optarg))
                    return 1;
                break;

            case 'v':
                show_version(argv[0]);
                return 0;

            case 'V':
                current_verbose = 1;
                break;
        }
    }

    /* setup signals (mode switch) */
    signal(SIGINT, &sigint);


    char memes[4];
    fread(memes, 4, 1, stdin);
    switch (current_mode)
    {
        case N:  printf("NORMAL\n"); break;
        case Z:  printf("NULL\n"); break;
        case HB: printf("hex to bytes\n"); break;
        case BH: printf("bytes to hex\n"); break;
        case IB: printf("bits to bytes\n"); break;
        case BI: printf("bytes to bits\n"); break;
    }

    printf("file mode: %i\n", current_mode_f);
    printf("verbose mode: %i\n", current_verbose);

    return 0;
}
