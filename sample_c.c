#include "pi_2_dht_read.h"
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include "pi_2_mmio.h"
#include <stdint.h>
#include <time.h>
#include <barectf-platform-linux-fs.h>
#include <barectf.h>
#include<sys/stat.h>


int main(void)
{

struct barectf_platform_linux_fs_ctx *platform_ctx;

/* initialize platform */
platform_ctx = barectf_platform_linux_fs_init(1024, "ctf", 1, 2, 20);


int sensor = 22;

int pin_number = 4;

float humidity = 0; 
float temperature = 0;

int hum = 0;

int temp = 0;


for (int i= 0; i < 100; i++)
{

int result = pi_2_dht_read(sensor, pin_number, &humidity, &temperature);
if(humidity!= 0 && temperature !=0){
	printf( "Humidity = %f%, Temperature = %f*C \n", humidity, temperature);
    temp = temperature;
    hum = humidity;
    barectf_default_trace_sensor_events(barectf_platform_linux_fs_get_barectf_ctx(platform_ctx), temp, hum, "device_1", "DHT_22_1", "read");

	

}



sleep_milliseconds(500);

}



barectf_platform_linux_fs_fini(platform_ctx);

return 0;

}
