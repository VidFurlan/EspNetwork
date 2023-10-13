#include <network.h>
#include <lcd_debug.h>

void setup()
{
    Serial.begin(115200);
    start_ap_sta_network();
    start_lcd_debuging();
}

void loop()
{
    display_connected_devices();
    update_debug_lcd();
    delay(5000);
}