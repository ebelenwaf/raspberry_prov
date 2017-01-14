#include <stdio.h>    // Used for printf() statements
#include <wiringPi.h> // Include WiringPi library!
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include "barectf-platform-linux-fs.h"
#include "barectf.h"

// Pin number declarations. We're using the Broadcom chip pin numbers.
const int pwmPin = 18; // PWM LED - Broadcom pin 18, P1 pin 12
const int ledPin = 23; // Regular LED - Broadcom pin 23, P1 pin 16
const int butPin = 17; // Active-low button - Broadcom pin 17, P1 pin 11

const int pwmValue = 75; // Use this to set an LED brightness

enum state_t {
	NEW,
	TERMINATED,
	READY,
	RUNNING,
	WAITING,
};

static void trace_stuff(struct barectf_default_ctx *ctx, int argc,
			char *argv[])
{
	int i;
	const char *str;

	/* record 40000 events */
	for (i = 0; i < 5000; ++i) {
		barectf_trace_simple_uint32(ctx, i * 1500);
		barectf_trace_simple_int16(ctx, -i * 2);
		barectf_trace_simple_float(ctx, (float) i / 1.23);

		if (argc > 0) {
			str = argv[i % argc];
		} else {
			str = "hello there!";
		}

		barectf_trace_simple_string(ctx, str);
		barectf_trace_context_no_payload(ctx, i, "ctx");
		barectf_trace_simple_enum(ctx, RUNNING);
		barectf_trace_a_few_fields(ctx, -1, 301, -3.14159,
						     str, NEW);
		barectf_trace_bit_packed_integers(ctx, 1, -1, 3,
							    -2, 2, 7, 23,
							    -55, 232);
		barectf_trace_no_context_no_payload(ctx);
		barectf_trace_simple_enum(ctx, TERMINATED);
	}
}


int main(int argc, char *argv[])
{

	struct barectf_platform_linux_fs_ctx *platform_ctx;

		/* initialize platform */
		platform_ctx = barectf_platform_linux_fs_init(1028, "ctf", 1, 2, 7);

		if (!platform_ctx) {
			fprintf(stderr, "Error: could not initialize platform\n");
			return 1;
	}

    // Setup stuff:
    wiringPiSetupGpio(); // Initialize wiringPi -- using Broadcom pin numbers
    pinMode(pwmPin, PWM_OUTPUT); // Set PWM LED as PWM output
    pinMode(ledPin, OUTPUT);     // Set regular LED as output
    pinMode(butPin, INPUT);      // Set button as INPUT
    pullUpDnControl(butPin, PUD_UP); // Enable pull-up resistor on button

    printf("Blinker is running! Press CTRL+C to quit.\n");

		//for (int i = 0; i < 5000; ++i) {
		
	

		 barectf_default_trace_trace_sensor(barectf_platform_linux_fs_get_barectf_ctx(platform_ctx), "Hello");
		
		
	//}

	barectf_platform_linux_fs_fini(platform_ctx);

   

    return 0;
}
