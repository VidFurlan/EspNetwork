#include <LiquidCrystal_I2C.h>

int lcdColumns = 16;
int lcdRows = 2;

LiquidCrystal_I2C lcd(0x27, lcdColumns, lcdRows);  

void start_lcd_debuging()
{
    lcd.init();
    lcd.backlight();
}

void update_debug_lcd()
{
    lcd.setCursor(0, 0);
    lcd.print("Hello, World!");
}