# Raspberry-Pi-OLED-2-
Control OLED 2" display for Raspberry Pi (even for cheap displays)

Drivers and use scripts are mirrored from Waveshare: https://www.waveshare.com/wiki/2inch_LCD_Module

![screenshot](https://github.com/vitasrutek/Raspberry-Pi-OLED-2-/blob/main/PIN.png)

### 
```
sudo raspi-config
Choose Interfacing Options -> SPI -> Yes  to enable the SPI interface
```

```
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install spidev
```

```
sudo apt-get install unzip -y
sudo wget https://files.waveshare.com/upload/8/8d/LCD_Module_RPI_code.zip
sudo unzip ./LCD_Module_RPI_code.zip 
cd LCD_Module_RPI_code/RaspberryPi/
```
Or download drivers from repo.

```
sudo python3 clock.py  # for clock and other info
# or
sudo python3 /python/example/2inch_LCD_test.py
```
