#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <time.h>
#include <barectf-platform-linux-fs.h>
#include <barectf.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>

//#define DEBUG
//#define BE_TIMELY

FILE *data_file;
char *data_filename = "test.txt";

struct barectf_platform_linux_fs_ctx *platform_ctx;

void initialize()
{
  /* initialize platform */
  platform_ctx = barectf_platform_linux_fs_init(1024, "ctf", 1, 2, 20);
  
  data_file = fopen(data_filename, "r");
  if (!data_file) {
    fprintf(stderr, "Unable to open file %s\n", data_filename);
    exit(0);
  }
}

void finalize( )
{
  barectf_platform_linux_fs_fini(platform_ctx);

  fclose(data_file);
}

#define BUFSZ 100
char buf[BUFSZ];
int simulate_rcv(uint32_t *ts, char **network_id, char **node_id, uint8_t *data)
{
  int result = 1;
  int i;
  char *s = fgets(buf, BUFSZ, data_file);
  if (s) {
    s = strtok(s, ",");
    *ts = atoi(s);
    s = strtok(NULL, ",");
    *network_id = s;
    s = strtok(NULL, ",");
    *node_id = s;
    s = strtok(NULL, ",");
    for ( i = 0; i < 8 && s; i++ ) {
      data[i] = strtol(s, NULL, 16);
    }
    result = 0;
  }
  return result;
}

static void usage(char *s)
{
  printf("USAGE\n\
%s <can_data.txt>\n\
where all arguments are positional, and used as follows:\n\
<can_data.txt> [default: test.txt] is a CSV file containing\n\
    timestamp (us), channel, node id, and 8 fields of 2 hextets each for data\n\
", s);
}

int main(int argc, char *argv[])
{
  int result = 0;
  uint32_t last_ts = 0;
  uint32_t ts;
  char *network_id;
  char *node_id;
  uint8_t data[8];

  /* FIXME: better arg processing */
  switch (argc) {
  default:
  case 2: data_filename = argv[1]; break;
  case 1: usage(argv[0]); exit(1);
  }

  initialize();

  printf("Running at approximately the same speed as the log.\n");

  while ( result == 0 ) {
    result = simulate_rcv(&ts, &network_id, &node_id, data);
    if ( ts > last_ts ) {
#if defined(BE_TIMELY)
      usleep(ts-last_ts); /* maintain timeliness */
#endif
    } else {
      printf("WARN: rcv timestamp (%d) <= (%d) last timestamp\n", ts, last_ts);
    }
    last_ts = ts;

    barectf_default_trace_canbus_rcv(
        barectf_platform_linux_fs_get_barectf_ctx(platform_ctx),
        ts, network_id, node_id,
        data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
        result, "read");
  }

  finalize();

  return 0;
}
