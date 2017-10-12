#include "pi_2_dht_read.h"
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include "pi_2_mmio.h"
#include <stdint.h>
#include <time.h>
#include <barectf-platform-linux-fs.h>
#include <barectf.h>
#include <sys/stat.h>

#define USE_SIMULATED_SENSOR
#if defined(USE_SIMULATED_SENSOR)
FILE *sensor_data_file;
char *sensor_data_filename = "temperature.csv";
#endif

struct TH {
  float temperature;
  float humidity;
};

enum state {
  IDLE = 0,
  HEATING = 1,
  COOLING = 2
};
const char *state_names[3] = {"IDLE", "HEATING", "COOLING"};

enum state current_state;
float setpoint;
struct barectf_platform_linux_fs_ctx *platform_ctx;

void initialize( )
{
  /* initialize platform */
  platform_ctx = barectf_platform_linux_fs_init(1024, "ctf", 1, 2, 20);
  setpoint = 72.5f;
  current_state = IDLE;

#if defined(USE_SIMULATED_SENSOR)
  sensor_data_file = fopen(sensor_data_filename, "r");
  if (!sensor_data_file) {
    fprintf(stderr, "Unable to open file %s\n", sensor_data_filename);
    exit(0);
  }
#endif
}

void finalize( )
{
  barectf_platform_linux_fs_fini(platform_ctx);

#if defined(USE_SIMULATED_SENSOR)
  fclose(sensor_data_file);
#endif
}

#if defined(USE_SIMULATED_SENSOR)
#define BUFSZ 100
char buf[BUFSZ];
int simulate_read(float *h, float *t)
{
  int result = 0;
  char *s;
  s = fgets(buf, BUFSZ, sensor_data_file);
  if (s) {
    *t = (float)atof(buf);
    s = fgets(buf, BUFSZ, sensor_data_file);
    *h = (float)atof(buf);
  } else {
    *t = 0.0f;
    result = 1;
  }
  return result;
}

#endif

/**
 * Attempts to get a valid temperature and humidity reading up to tries times.
 * If successful, puts the valid reading into th and returns 0.
 * If unsuccessful, puts 0 in th and returns non-zero.
*/
int get_temperature_and_humidity(struct TH* th, int tries)
{
  const int sensor = 22;
  const int pin_number = 4;
  int result = -1, i;

  th->temperature = th->humidity = 0.0f;

#if defined(USE_SIMULATED_SENSOR)
  result = simulate_read(&th->humidity, &th->temperature);
#else
  for (i = 0; i < tries; i++) {
    result = pi_2_dht_read(sensor, pin_number, &th->humidity, &th->temperature);

    /* FIXME: transformation? this should really be 'sensor_event'? */
    barectf_default_trace_transformation(
        barectf_platform_linux_fs_get_barectf_ctx(platform_ctx),
        th->temperature, th->humidity, result,
        "device_1", "DHT_22_1", "read");

    if (!result) break;
  }
#endif

  return result;
}

/* Convert the temperature from celsius to fahrenheit */
static inline void convert_C_to_F(struct TH *th)
{
  th->temperature = th->temperature * 1.8f + 32.0f;
}

/* Compare the current temperature value in th with the setpoint
 * to determine the next state. */
enum state check_setpoint(struct TH *th)
{
  const float stop_increment = 0.5f;
  const float start_increment = 0.75f;
  enum state next_state = current_state;
  if ( current_state == HEATING ) {
    if ( th->temperature > (setpoint + stop_increment) ) {
      next_state = IDLE;
    }
  } else if ( current_state == COOLING ) {
    if ( th->temperature < (setpoint - stop_increment) ) {
      next_state = IDLE;
    }
  } else if ( current_state == IDLE ) {
    if ( th->temperature < (setpoint - start_increment) ) {
      next_state = HEATING;
    } else if (th->temperature > (setpoint + start_increment)) {
      next_state = COOLING;
    }
  }
  return next_state;
}

int main(void)
{
  int hum = 0, temp = 0, i;
  struct TH th;
  enum state next_state;

  initialize();

  for (i = 0; i < 10; i++) {
    int result = get_temperature_and_humidity(&th, 5);
    printf("result = %d\n", result);
    printf("H = %f%%, T = %f *C\n", th.humidity, th.temperature);

    convert_C_to_F(&th);
    /* TODO: trace the conversion? */

    printf("H = %f%%, T = %f *f\n", th.humidity, th.temperature);

    next_state = check_setpoint(&th);
    if ( next_state != current_state ) {
      printf("Actuating... %s -> %s\n", state_names[current_state],
        state_names[next_state]);
      current_state = next_state; /* simulated actuation */
      /* TODO: trace the actuation. */
    }

    temp = th.temperature;
    hum = th.humidity;
    printf("h = %d%%, t = %d *F\n", hum, temp);
    barectf_default_trace_sensor_events(
        barectf_platform_linux_fs_get_barectf_ctx(platform_ctx), temp, hum,
        "device_1", "DHT_22_1", "read");

    sleep_milliseconds(1000);
    //sleep_milliseconds(1000000); /* 1 minute sleep */
  }

  finalize();

  return 0;
}
