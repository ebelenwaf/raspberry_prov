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

int main(void)
{
  const int sensor = 22;
  const int pin_number = 4;
  float humidity = 0.0f, temperature = 0.0f;
  int hum = 0, temp = 0, i;
  struct barectf_platform_linux_fs_ctx *platform_ctx;

  /* initialize platform */
  platform_ctx = barectf_platform_linux_fs_init(1024, "ctf", 1, 2, 20);

  for (i = 0; i < 10; i++) {
    int result = pi_2_dht_read(sensor, pin_number, &humidity, &temperature);

    printf( "result = %d\n", result);
    printf( "Humidity = %f%, Temperature = %f*C \n", humidity, temperature);

    temp = temperature;
    hum = humidity;
    barectf_default_trace_sensor_events(
        barectf_platform_linux_fs_get_barectf_ctx(platform_ctx), temp, hum,
        "device_1", "DHT_22_1", "read");

    sleep_milliseconds(1000);
  }

  barectf_platform_linux_fs_fini(platform_ctx);

  return 0;
}
