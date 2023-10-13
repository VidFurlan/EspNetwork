#include <WiFi.h>
#include "esp_wifi.h"

// Wifi to connect the Esp to
const char* wifi_network_ssid       = "pm_EXT";
const char* wifi_network_password   =  "vijavajavn";

// Esp network parameters
const char* soft_ap_ssid            = "Esp32 Hotspot";
const char* soft_ap_password        = NULL;
const int   soft_ap_channel         = 10;
const bool  soft_ap_hide_SSID       = false;
const int   soft_ap_max_connection  = 5;

IPAddress local_ip(192,168,0,1);
IPAddress gateway(192,168,0,1);
IPAddress subnet(255,255,255,0);

void start_ap_sta_network ()
{
    WiFi.mode(WIFI_AP_STA);

    Serial.println("\n[*] Creating ESP32 AP");
    WiFi.softAP(soft_ap_ssid, soft_ap_password, soft_ap_channel, soft_ap_hide_SSID, soft_ap_max_connection);
    Serial.print("[+] AP Created with IP Gateway ");
    Serial.println(WiFi.softAPIP());

    // Connect to the internet
    WiFi.begin(wifi_network_ssid, wifi_network_password);
    Serial.println("\n[*] Connecting to WiFi Network");

    while(WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(100);
    }

    Serial.print("\n[+] Connected to the WiFi network with local IP : ");
    Serial.println(WiFi.localIP());
}

void get_connected_devices()
{

}

void display_connected_devices()
{
    wifi_sta_list_t wifi_sta_list;
    tcpip_adapter_sta_list_t adapter_sta_list;
    esp_wifi_ap_get_sta_list(&wifi_sta_list);
    tcpip_adapter_get_sta_list(&wifi_sta_list, &adapter_sta_list);

    if (adapter_sta_list.num > 0)
        Serial.println("----------------------");

    for (uint8_t i = 0; i < adapter_sta_list.num; i++)
    {
        tcpip_adapter_sta_info_t station = adapter_sta_list.sta[i];
        Serial.print("\n[+] Device " + i);
        Serial.printf(" | MAC : %02X:%02X:%02X:%02X:%02X:%02X", station.mac[0], station.mac[1], station.mac[2], station.mac[3], station.mac[4], station.mac[5]);
        Serial.print(" | IP " + IPAddress(station.ip.addr).toString());
    }
}
