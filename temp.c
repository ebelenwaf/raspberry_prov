#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <barectf-platform-linux-fs.h>
#include <barectf.h>
#include<sys/stat.h>


#define MAXTIMINGS	85
#define DHTPIN		13
int dht11_dat[5] = { 0, 0, 0, 0, 0 };

enum state_t {
	ACTIVATED,
	DEACTIVATED
	
};


void trace_stuff(struct barectf_default_ctx *ctx)
{
	int i;
	const char *str;

	 //record 40000 events 
	
		barectf_trace_simple_uint32(ctx, i * 1500);
		barectf_trace_simple_int16(ctx, -i * 2);
		barectf_trace_simple_float(ctx, (float) i / 1.23);

		
	   // str = "hello there!";
	

		barectf_trace_trace_sensor(ctx, "hello");
		barectf_trace_context_no_payload(ctx, i, "ctx");
		barectf_trace_simple_enum(ctx, ACTIVATED);
		
		barectf_trace_bit_packed_integers(ctx, 1, -1, 3,
							    -2, 2, 7, 23,
							    -55, 232);
		barectf_trace_no_context_no_payload(ctx);
		barectf_trace_simple_enum(ctx, DEACTIVATED);

}


 
void read_dht11_dat()
{
	uint8_t laststate	= HIGH;
	uint8_t counter		= 0;
	uint8_t j		= 0, i;
	float	f; /* fahrenheit */
 
	dht11_dat[0] = dht11_dat[1] = dht11_dat[2] = dht11_dat[3] = dht11_dat[4] = 0;
	pinMode (7, OUTPUT) ;
	

	
 
	/* pull pin down for 18 milliseconds */
	pinMode( DHTPIN, OUTPUT );
	digitalWrite( DHTPIN, LOW );
	delay( 18 );
	/* then pull it up for 40 microseconds */
	digitalWrite( DHTPIN, HIGH );
	delayMicroseconds( 40 );
	/* prepare to read the pin */
	pinMode( DHTPIN, INPUT );
 
	/* detect change and read data */
	for ( i = 0; i < MAXTIMINGS; i++ )
	{
		counter = 0;
		while ( digitalRead( DHTPIN ) == laststate )
		{
			counter++;
			delayMicroseconds( 1 );
			if ( counter == 255 )
			{
				break;
			}
		}
		laststate = digitalRead( DHTPIN );
 
		if ( counter == 255 )
			break;
 
		/* ignore first 3 transitions */
		if ( (i >= 4) && (i % 2 == 0) )
		{
			/* shove each bit into the storage bytes */
			dht11_dat[j / 8] <<= 1;
			if ( counter > 16 )
				dht11_dat[j / 8] |= 1;
			j++;
		}
	}
 
	/*
	 * check we read 40 bits (8bit x 5 ) + verify checksum in the last byte
	 * print it out if data is good
	
	if ( (j >= 40) &&
	     (dht11_dat[4] == ( (dht11_dat[0] + dht11_dat[1] + dht11_dat[2] + dht11_dat[3]) & 0xFF) ) )
	{ */
		f = dht11_dat[2] * 9. / 5. + 32;
		printf( "Humidity = %d.%d %% Temperature = %d.%d *C (%.1f *F)\n",
			dht11_dat[0], dht11_dat[1], dht11_dat[2], dht11_dat[3], f );


		
	
		//barectf_trace_simple_string(barectf_platform_linux_fs_get_barectf_ctx(platform_ctx), "Humidity");

//trace_stuff(barectf_platform_linux_fs_get_barectf_ctx(platform_ctx));
/*}else  {
		printf( "Data not good, skip\n" );
	} */

	
}

int fsize(FILE *fp)
{
	int prev = ftell(fp);
	fseek(fp, 0L, SEEK_END);
	int sz= ftell(fp);
	fseek(fp, prev, SEEK_SET);
	
	return sz;
}
 
int main( void )
{	struct stat st;
	FILE *fp = fopen("experiment.txt", "w+");

	
	time_t rawtime;
	struct tm * timeinfo;
	struct barectf_platform_linux_fs_ctx *platform_ctx;

	/* initialize platform */
	platform_ctx = barectf_platform_linux_fs_init(1024, "ctf", 1, 2, 20);

	printf( "Raspberry Pi wiringPi DHT11 Temperature test program\n" );

	
	



	if(fp== NULL)
	{
		printf("Error opening file!\n");
		exit(1);
	}
		
	
 
	if ( wiringPiSetup() == -1 )
		exit( 1 );
 
	for ( int i = 0; i < 5; i++ )
	{

		fstat(fp, &st);
		int size = st.st_size;
		read_dht11_dat();

		time( &rawtime);
	    timeinfo = localtime(&rawtime);
		//barectf_trace_trace_sensor(barectf_platform_linux_fs_get_barectf_ctx(platform_ctx), "hello");

		
		delay( 1000 ); /* wait 1secls to refresh */


		//trace_stuff(barectf_platform_linux_fs_get_barectf_ctx(platform_ctx));

		//printf("No of packets discarded: %d, time: %s \n",barectf_packet_events_discarded(platform_ctx), asctime(timeinfo));
		//fprintf(fp, "No of packets discarded: %d, time: %s \n",barectf_packet_events_discarded(platform_ctx), asctime(timeinfo));  
		fprintf(fp, "%d, %s \n",fsize(fp), asctime(timeinfo)); 
		printf("%d, %s \n",fsize(fp), asctime(timeinfo));  

		  

		barectf_default_trace_sensor_readings(barectf_platform_linux_fs_get_barectf_ctx(platform_ctx), -1, 301,
						     "device_1", "sensor_1");

		pinMode( 7, INPUT );
		
		
		digitalWrite (7, HIGH) ; 
		printf( "Blinker activated \n" );
		//barectf_trace_simple_enum(barectf_platform_linux_fs_get_barectf_ctx(platform_ctx), ACTIVATED);
		delay (500) ;
		
        digitalWrite (7,  LOW) ; 
		printf( "Blinker activated \n" );
		//barectf_trace_simple_enum(barectf_platform_linux_fs_get_barectf_ctx(platform_ctx), DEACTIVATED);
		

	}

	time_t rawtime1;
	struct tm * timeinfo1;

	time( &rawtime1);
	timeinfo1 = localtime(&rawtime1);

    /* finalize platform */
	barectf_platform_linux_fs_fini(platform_ctx);

	fprintf(fp, "Final time: %s\n", asctime(timeinfo1)); 

	fclose(fp);
 
	return(0);
}
