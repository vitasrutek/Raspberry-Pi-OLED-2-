#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
#import sys_info
import os
import sys
import time
from datetime import datetime
import locale
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch
from PIL import Image,ImageDraw,ImageFont
import random
import subprocess as sp
import socket
import psutil

#locale.setlocale(locale.LC_TIME, 'cs_CZ.UTF-8')

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level=logging.DEBUG)

def random_color():
    return tuple(random.randint(0, 255) for _ in range(3))

def get_temp():
    temp = float(sp.getoutput("vcgencmd measure_temp").split("=")[1].split("'")[0])
    return temp

def get_cpu():
    return psutil.cpu_percent()

def get_mem():
    return psutil.virtual_memory().percent

def get_disk_usage():
    usage = psutil.disk_usage("/")
    return usage.used / usage.total * 100


def get_uptime():
    uptime = ("%s" % (datetime.now() - datetime.fromtimestamp(psutil.boot_time()))).split(".")[0]
    return "UpTime: %s" % (uptime)


def find_single_ipv4_address(addrs):
    for addr in addrs:
        if addr.family == socket.AddressFamily.AF_INET:  # IPv4
            return addr.address


def get_ipv4_address(interface_name=None):
    if_addrs = psutil.net_if_addrs()

    if isinstance(interface_name, str) and interface_name in if_addrs:
        addrs = if_addrs.get(interface_name)
        address = find_single_ipv4_address(addrs)
        return address if isinstance(address, str) else ""
    else:
        if_stats = psutil.net_if_stats()
        # remove loopback
        if_stats_filtered = {key: if_stats[key] for key, stat in if_stats.items() if "loopback" not in stat.flags}
        # sort interfaces by
        # 1. Up/Down
        # 2. Duplex mode (full: 2, half: 1, unknown: 0)
        if_names_sorted = [stat[0] for stat in sorted(if_stats_filtered.items(), key=lambda x: (x[1].isup, x[1].duplex), reverse=True)]
        if_addrs_sorted = OrderedDict((key, if_addrs[key]) for key in if_names_sorted if key in if_addrs)

        for _, addrs in if_addrs_sorted.items():
            address = find_single_ipv4_address(addrs)
            if isinstance(address, str):
                return address

        return ""


def get_ip(network_interface_name):
    return "IP: %s" % (get_ipv4_address(network_interface_name))


def format_percent(percent):
    return "%5.1f" % (percent)

network_interface_name = "wlan0"

try:

    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_2inch.LCD_2inch()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    #Set the backlight to 100
    disp.bl_DutyCycle(100)

    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.height, disp.width ), "BLACK")
    #image1=image1.rotate(180)
    draw = ImageDraw.Draw(image1)


    #logging.info("draw point")

    draw.rectangle((5,10,6,11), fill = "RED")
    draw.rectangle((5,25,7,27), fill = "YELLOW")
    draw.rectangle((5,40,8,43), fill = "GREEN")
    draw.rectangle((5,55,9,59), fill = "BLUE")
    while True:
        draw.rectangle((0,0, 320, 240), fill = "BLACK")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime ('%d. %B %Y')
        #logging.info(current_time)
        #logging.info(current_date)
        Font1 = ImageFont.truetype("../Font/Font02.ttf", 55)
        Font2 = ImageFont.truetype("../Font/Font02.ttf", 75)
        Font3 = ImageFont.truetype("../Font/Font02.ttf", 15)

        W, H = (320, 240)
        _, _, w, h = draw.textbbox((0, 0), str(current_date), font=Font1)
        draw.text(((W-w)/2,0), str(current_date), font=Font1, fill="white")
        _, _, w, h = draw.textbbox((0, 0), str(current_time), font=Font2)
        draw.text(((W-w)/2,40), str(current_time), font=Font2, fill=random_color()) #bylo "white"

        #draw.text((10, 10), 'AHOJ :)', fill = "RED", font=Font1)

        #image1=image1.rotate(180)

        draw.text((5, 120), str(get_temp()), font=Font3, fill="white")
        draw.text((5, 140), str(get_cpu()), font=Font3, fill="white")
        draw.text((5, 160), str(get_mem()), font=Font3, fill="white")
        #draw.text((5, 180), str(get_ipv4_address(interface_name=network_interface_name)), font=Font3, fill="white")
        draw.text((5, 200), str(get_ip(network_interface_name)), font=Font3, fill="white")
        #draw.text((5, 220), XY, font=Font3, fill="white")

        disp.ShowImage(image1)
        '''
        logging.info("draw line")
        draw.line([(20, 10),(70, 60)], fill = "RED",width = 1)
        draw.line([(70, 10),(20, 60)], fill = "RED",width = 1)
        draw.line([(170,15),(170,55)], fill = "RED",width = 1)
        draw.line([(150,35),(190,35)], fill = "RED",width = 1)

        logging.info("draw rectangle")
        draw.rectangle([(20,10),(70,60)],fill = "WHITE",outline="BLUE")
        draw.rectangle([(85,10),(130,60)],fill = "BLUE")

        logging.info("draw circle")
        draw.arc((150,15,190,55),0, 360, fill =(0,255,0))
        draw.ellipse((150,65,190,105), fill = (0,255,0))

        logging.info("draw text")
        Font1 = ImageFont.truetype("../Font/Font01.ttf",25)
        Font2 = ImageFont.truetype("../Font/Font01.ttf",35)
        Font3 = ImageFont.truetype("../Font/Font02.ttf",32)

        draw.rectangle([(0,65),(140,100)],fill = "WHITE")
        draw.text((5, 68), 'Hello world', fill = "BLACK",font=Font1)
        draw.rectangle([(0,115),(190,160)],fill = "RED")
        draw.text((5, 118), 'WaveShare', fill = "WHITE",font=Font2)
        draw.text((5, 160), '1234567890', fill = "GREEN",font=Font3)
        text= u"微雪电子"
        draw.text((5, 200),text, fill = "BLUE",font=Font3)
        image1=image1.rotate(0)
        disp.ShowImage(image1)
        time.sleep(1)
        logging.info("show image")
        image = Image.open('../pic/LCD_2inch4.jpg')
        image = image.rotate(0)
        disp.ShowImage(image)'''
        #time.sleep(5)
        #disp.module_exit()
        #logging.info("quit:")
        time.sleep(1)
except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()
