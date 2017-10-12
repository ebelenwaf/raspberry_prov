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

struct TH {
  float temperature;
  float humidity;
};

float setpoint;

struct barectf_platform_linux_fs_ctx *platform_ctx;

void initialize( )
{
  /* initialize platform */
  platform_ctx = barectf_platform_linux_fs_init(1024, "ctf", 1, 2, 20);
  setpoint = 70.0f;
}

void finalize( )
{
  barectf_platform_linux_fs_fini(platform_ctx);
}

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
  for (i = 0; i < tries; i++) {
    result = pi_2_dht_read(sensor, pin_number, &th->humidity, &th->temperature);

    /* FIXME: transformation? this should really be 'sensor_event'? */
    barectf_default_trace_transformation(
        barectf_platform_linux_fs_get_barectf_ctx(platform_ctx),
        th->temperature, th->humidity, result,
        "device_1", "DHT_22_1", "read");

    if (!result) break;
  }
  return result;
}

/* Convert the temperature from celsius to fahrenheit */
static inline void convert_C_to_F(struct TH *th)
{
  th->temperature = th->temperature * 1.8f + 32.0f;
}

int main(void)
{
  int hum = 0, temp = 0, i;
  struct TH th;

  initialize();

  for (i = 0; i < 10; i++) {
    int result = get_temperature_and_humidity(&th, 5);
    printf("result = %d\n", result);
    printf("H = %f%, T = %f *C\n", th.humidity, th.temperature);

    convert_C_to_F(&th);
    /* TODO: trace the conversion? */

    temp = th.temperature;
    hum = th.humidity;
    printf("h = %d%, t = %d *F\n", hum, temp);
    barectf_default_trace_sensor_events(
        barectf_platform_linux_fs_get_barectf_ctx(platform_ctx), temp, hum,
        "device_1", "DHT_22_1", "read");

    sleep_milliseconds(1000);
  }

  finalize();

  return 0;
}
