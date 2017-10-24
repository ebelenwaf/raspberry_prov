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
#include <string.h>

//#define DEBUG

#define USE_SIMULATED_SENSOR
#if defined(USE_SIMULATED_SENSOR)
FILE *sensor_data_file;
char *sensor_data_filename = "temperature.csv"; /* TODO: parameterize */
#endif

enum state {
  OFF = 0,
  HEATING = 1,
  COOLING = 2
};
const char *state_names[3] = {"OFF", "HEATING", "COOLING"};

struct thermostat_ctx {
  float temperature;
  float humidity;
  float cooling_setpoint;
  float heating_setpoint;
  enum state current_state;
  enum state current_mode;
};


struct barectf_platform_linux_fs_ctx *platform_ctx;

void initialize(struct thermostat_ctx *th)
{
  /* initialize platform */
  platform_ctx = barectf_platform_linux_fs_init(1024, "ctf", 1, 2, 20);
  th->cooling_setpoint = 72.5f;
  th->heating_setpoint = 72.5f;
  th->current_state = OFF;
  th->current_mode = COOLING; /* TODO: parameterize? */

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
int simulate_read(float *h, float *t, float *csp, float *hsp)
{
  int result = 1;
  char *s;
  float *outputs[4] = {t,h,csp,hsp};
  float **p = outputs;
  *t = 0.0f;
  *h = 0.0f;
  
  s = fgets(buf, BUFSZ, sensor_data_file);
  if (s) {
    s = strtok(s, ", ");
    while (s) {
      **p++ = (float)atof(s);
      s = strtok(NULL, ", ");
      result = 0;
    }
  }
  return result;
}

#endif

/**
 * Attempts to get a valid temperature and humidity reading up to tries times.
 * If successful, puts the valid reading into th and returns 0.
 * If unsuccessful, puts 0 in th and returns non-zero.
*/
int get_temperature_and_humidity(struct thermostat_ctx* th, int tries)
{
  int result = -1;
#if !defined(USE_SIMULATED_SENSOR)
  const int sensor = 22;
  const int pin_number = 4;
  int i;
#endif

  th->temperature = th->humidity = 0.0f;

#if defined(USE_SIMULATED_SENSOR)
  result = simulate_read(
      &th->humidity, &th->temperature, &th->cooling_setpoint,
      &th->heating_setpoint);

  barectf_default_trace_th_sensor_reading(
      barectf_platform_linux_fs_get_barectf_ctx(platform_ctx),
      th->temperature, th->humidity, result,
      "device_1", "DHT_22_1", "read");
#else
  for (i = 0; i < tries; i++) {
    result = pi_2_dht_read(sensor, pin_number, &th->humidity, &th->temperature);

    barectf_default_trace_th_sensor_reading(
        barectf_platform_linux_fs_get_barectf_ctx(platform_ctx),
        th->temperature, th->humidity, result,
        "device_1", "DHT_22_1", "read");

    if (!result) break;
  }
#endif

  return result;
}

/* Convert the temperature from celsius to fahrenheit */
static inline void convert_C_to_F(struct thermostat_ctx *th)
{
  th->temperature = th->temperature * 1.8f + 32.0f;
  th->cooling_setpoint = th->cooling_setpoint * 1.8f + 32.0f;
  th->heating_setpoint = th->heating_setpoint * 1.8f + 32.0f;
}

/* Compare the current temperature value in th with the setpoint
 * to determine the next state. */
enum state check_setpoint(struct thermostat_ctx *th)
{
  const float stop_increment = 1.00f;
  const float start_increment = 1.00f;

  enum state next_state = th->current_state;

  if ( th->current_mode == HEATING ) {
    if ( th->temperature > (th->heating_setpoint + stop_increment) ) {
      next_state = OFF;
    } else if (th->temperature < (th->heating_setpoint - start_increment) ) {
      next_state =  HEATING;
    }
  } else if ( th->current_mode == COOLING ) {
    if ( th->temperature < (th->cooling_setpoint - stop_increment) ) {
      next_state = OFF;
    } else if (th->temperature > (th->cooling_setpoint + start_increment) ) {
      next_state = COOLING;
    }
  } else if ( th->current_mode == OFF ) {
      next_state = OFF;
  }
  return next_state;
}

int main(int argc, char *argv[])
{
  int hum = 0, temp = 0, i;
  struct thermostat_ctx th;
  enum state next_state;

  if (argc > 1) {
#if defined(USE_SIMULATED_SENSOR)
    sensor_data_filename = argv[1]; /* FIXME: better arg processing */
#endif
  }

  initialize(&th);

  /* TODO: parametrize the runs */
  for (i = 0; i < 1440; i++) {
    int result = get_temperature_and_humidity(&th, 5);

#if defined(DEBUG)
    printf("H = %f%%, T = %f *C\n", th.humidity, th.temperature);
#endif

    convert_C_to_F(&th);

    barectf_default_trace_transformation(
        barectf_platform_linux_fs_get_barectf_ctx(platform_ctx),
        th.temperature, th.humidity, result,
        "device_1", "DHT_22_1", "read");

    printf("H = %f%%, T = %f *f, CSP = %f *f, HSP = %f *f\n",
        th.humidity, th.temperature, th.cooling_setpoint, th.heating_setpoint);

    next_state = check_setpoint(&th);
    if ( next_state != th.current_state ) {
      printf("Actuating... %s -> %s\n", state_names[th.current_state],
        state_names[next_state]);
      th.current_state = next_state; /* simulated actuation */

    barectf_default_trace_actuation(
        barectf_platform_linux_fs_get_barectf_ctx(platform_ctx),
        state_names[th.current_state], "device_1", "DHT_22_1", "actuate");

    }

    temp = th.temperature;
    hum = th.humidity;
#if defined(DEBUG)
    printf("h = %d%%, t = %d *F\n", hum, temp);
#endif

    /* TODO: what is this event? */
    barectf_default_trace_sensor_events(
        barectf_platform_linux_fs_get_barectf_ctx(platform_ctx), temp, hum,
        "device_1", "DHT_22_1", "read");

#if defined(USE_SIMULATED_SENSOR)
    //sleep_milliseconds(1000);
#else
    sleep_milliseconds(1000000); /* 1 minute sleep */
#endif
  }

  finalize();

  return 0;
}
