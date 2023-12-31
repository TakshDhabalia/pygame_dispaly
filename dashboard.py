#!/usr/bin/env python3

import obd
import pygame
import time
import os
import paho.mqtt.client as mqtt
import json as json
# obd.logger.setLevel(obd.logging.DEBUG)
startTime = time.time()
# MQTT settings dont fuck with these unless you know them
MQTT_BROKER = "localhost"  # Change this to your MQTT broker address
MQTT_TOPIC_SPEED = "Speed"    # Change this to your MQTT topic
MQTT_TOPIC_VOLATGE = 'voltage'
MQTT_TOPIC_HELMET = 'helmet'
MQTT_TOPIC_TEMP = 'temperature'
MQTT_TOPIC = 'your'

# Create a variable to store the received MQTT data

# globals
oil_change_interval = 0
oil_change_count = 0
transmission_oil_change_interval = 0
brake_change_interval = 0
oil_mileage = 0
transmission_oil_mileage = 0
brake_mileage = 0
trip_distance = 0
prev_trip_distance = 0

rpm_target = 0
voltage = 0
inst_mpg = 0
maf_reading = 0
throttle_position = 0
load = 0
fuel_pressure = 0
intake_temp = 0
temp_value = 0

limit = False
speed_limit = False
temp_limit = False
current_page = 1
sports_button_press = False
back_button_press = False
reset_button_press = False
interval_button_press = False
three_thousand_press = False
five_thousand_press = False
seven_thousand_five_press = False
ten_thousand_press = False
fifteen_thousand_press = False
clear_dtc_press = False
dtc_code_present = False
dtc_code = ''
current_maintenance = 1
increment_press = False
decrement_press = False
colors_button_press = False
red_press = False
blue_press = False
green_press = False
grey_press = False
mint_press = False
pink_press = False
purple_press = False
current_color = 1
colors = {1: 'Red', 2: 'Blue', 3: 'Green', 4: 'Grey', 5: 'Mint', 6: 'Pink', 7: 'Purple'}
yes_press = False
no_press = False
exit_press = False
shutdown_press = False

#boot boolenas 
initial_boot_complete = False
initialized = False
# Create a variable to store the received MQTT data
mqtt_data = 0 #basically

# MQTT client setup
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with code " + str(rc))
    client.subscribe(MQTT_TOPIC_VOLATGE)
    client.subscribe(MQTT_TOPIC_HELMET)
    client.subscribe(MQTT_TOPIC_SPEED)
    client.subscribe(MQTT_TOPIC)



def on_message(client, userdata, message):
    global mqtt_data
    global mqtt_data_voltage
    try:
        mqtt_data = json.loads(message.payload.decode("utf-8"))
        print("Received MQTT Data on :", mqtt_data)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", str(e))

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect(MQTT_BROKER, 9999, 60)


# initialize the interface
pygame.init()

# clock
clock = pygame.time.Clock()

# create screen
infoObject = pygame.display.Info()
display_width = infoObject.current_w
display_height = infoObject.current_h

#screen = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1024, 600) )


# Title of app
pygame.display.set_caption("Dashboard 2.0")

# logo and project heading
logo_img = pygame.image.load('logos_headings/bolt bg.jpeg')
project_heading_img = pygame.image.load('logos_headings/Dashboard 2.0.png')

#bootup screen
boot_img = pygame.image.load('logos_headings/Bootscreen.png')

def display_logos():
    screen.blit(logo_img, (910, 450))
    screen.blit(project_heading_img, (390, 25))

def display_bootscreen():
    screen.blit(boot_img, (0, 0))


# Tachometer
tachometerX = 184
tachometerY = 0 - 20

tachometer_0 = [pygame.image.load('tach/norm/0/tach1.png'), pygame.image.load('tach/norm/0/tach2.png'), pygame.image.load('tach/norm/0/tach3.png'), pygame.image.load('tach/norm/0/tach4.png'), pygame.image.load('tach/norm/0/tach5.png'),pygame.image.load('tach/norm/0/tach6.png'), pygame.image.load('tach/norm/0/tach7.png')]
tachometer_1 = [pygame.image.load('tach/norm/1000/tach1.png'), pygame.image.load('tach/norm/1000/tach2.png'), pygame.image.load('tach/norm/1000/tach3.png'), pygame.image.load('tach/norm/1000/tach4.png'), pygame.image.load('tach/norm/1000/tach5.png'),pygame.image.load('tach/norm/1000/tach6.png')]
tachometer_2 = [pygame.image.load('tach/norm/2000/tach1.png'), pygame.image.load('tach/norm/2000/tach2.png'), pygame.image.load('tach/norm/2000/tach3.png'), pygame.image.load('tach/norm/2000/tach4.png'), pygame.image.load('tach/norm/2000/tach5.png'),pygame.image.load('tach/norm/2000/tach6.png')]
tachometer_3 = [pygame.image.load('tach/norm/3000/tach1.png'), pygame.image.load('tach/norm/3000/tach2.png'), pygame.image.load('tach/norm/3000/tach3.png'), pygame.image.load('tach/norm/3000/tach4.png'), pygame.image.load('tach/norm/3000/tach5.png'),pygame.image.load('tach/norm/3000/tach6.png')]
tachometer_4 = [pygame.image.load('tach/norm/4000/tach1.png'), pygame.image.load('tach/norm/4000/tach2.png'), pygame.image.load('tach/norm/4000/tach3.png'), pygame.image.load('tach/norm/4000/tach4.png'), pygame.image.load('tach/norm/4000/tach5.png'),pygame.image.load('tach/norm/4000/tach6.png')]
tachometer_5 = [pygame.image.load('tach/norm/5000/tach1.png'), pygame.image.load('tach/norm/5000/tach2.png'), pygame.image.load('tach/norm/5000/tach3.png'), pygame.image.load('tach/norm/5000/tach4.png'), pygame.image.load('tach/norm/5000/tach5.png'),pygame.image.load('tach/norm/5000/tach6.png')]
tachometer_6 = [pygame.image.load('tach/norm/6000/tach1.png'), pygame.image.load('tach/norm/6000/tach2.png'), pygame.image.load('tach/norm/6000/tach3.png'), pygame.image.load('tach/norm/6000/tach4.png'), pygame.image.load('tach/norm/6000/tach5.png'),pygame.image.load('tach/norm/6000/tach6.png')]
tachometer_7 = [pygame.image.load('tach/norm/7000/tach1.png'), pygame.image.load('tach/norm/7000/tach2.png'), pygame.image.load('tach/norm/7000/tach3.png'), pygame.image.load('tach/norm/7000/tach4.png'), pygame.image.load('tach/norm/7000/tach5.png'),pygame.image.load('tach/norm/7000/tach6.png')]
tachometer_8 = [pygame.image.load('tach/norm/8000/tach1.png'), pygame.image.load('tach/norm/8000/tach2.png'), pygame.image.load('tach/norm/8000/tach3.png'), pygame.image.load('tach/norm/8000/tach4.png'), pygame.image.load('tach/norm/8000/tach5.png'),pygame.image.load('tach/norm/8000/tach6.png')]

stachometer_0 = [pygame.image.load('tach/sport/0/tach1.png'), pygame.image.load('tach/sport/0/tach2.png'), pygame.image.load('tach/sport/0/tach3.png'), pygame.image.load('tach/sport/0/tach4.png'), pygame.image.load('tach/sport/0/tach5.png'),pygame.image.load('tach/sport/0/tach6.png'), pygame.image.load('tach/sport/0/tach7.png')]
stachometer_1 = [pygame.image.load('tach/sport/1000/tach1.png'), pygame.image.load('tach/sport/1000/tach2.png'), pygame.image.load('tach/sport/1000/tach3.png'), pygame.image.load('tach/sport/1000/tach4.png'), pygame.image.load('tach/sport/1000/tach5.png'),pygame.image.load('tach/sport/1000/tach6.png')]
stachometer_2 = [pygame.image.load('tach/sport/2000/tach1.png'), pygame.image.load('tach/sport/2000/tach2.png'), pygame.image.load('tach/sport/2000/tach3.png'), pygame.image.load('tach/sport/2000/tach4.png'), pygame.image.load('tach/sport/2000/tach5.png'),pygame.image.load('tach/sport/2000/tach6.png')]
stachometer_3 = [pygame.image.load('tach/sport/3000/tach1.png'), pygame.image.load('tach/sport/3000/tach2.png'), pygame.image.load('tach/sport/3000/tach3.png'), pygame.image.load('tach/sport/3000/tach4.png'), pygame.image.load('tach/sport/3000/tach5.png'),pygame.image.load('tach/sport/3000/tach6.png')]
stachometer_4 = [pygame.image.load('tach/sport/4000/tach1.png'), pygame.image.load('tach/sport/4000/tach2.png'), pygame.image.load('tach/sport/4000/tach3.png'), pygame.image.load('tach/sport/4000/tach4.png'), pygame.image.load('tach/sport/4000/tach5.png'),pygame.image.load('tach/sport/4000/tach6.png')]
stachometer_5 = [pygame.image.load('tach/sport/5000/tach1.png'), pygame.image.load('tach/sport/5000/tach2.png'), pygame.image.load('tach/sport/5000/tach3.png'), pygame.image.load('tach/sport/5000/tach4.png'), pygame.image.load('tach/sport/5000/tach5.png'),pygame.image.load('tach/sport/5000/tach6.png')]
stachometer_6 = [pygame.image.load('tach/sport/6000/tach1.png'), pygame.image.load('tach/sport/6000/tach2.png'), pygame.image.load('tach/sport/6000/tach3.png'), pygame.image.load('tach/sport/6000/tach4.png'), pygame.image.load('tach/sport/6000/tach5.png'),pygame.image.load('tach/sport/6000/tach6.png')]
stachometer_7 = [pygame.image.load('tach/sport/7000/tach1.png'), pygame.image.load('tach/sport/7000/tach2.png'), pygame.image.load('tach/sport/7000/tach3.png'), pygame.image.load('tach/sport/7000/tach4.png'), pygame.image.load('tach/sport/7000/tach5.png'),pygame.image.load('tach/sport/7000/tach6.png')]
stachometer_8 = [pygame.image.load('tach/sport/8000/tach1.png'), pygame.image.load('tach/sport/8000/tach2.png'), pygame.image.load('tach/sport/8000/tach3.png'), pygame.image.load('tach/sport/8000/tach4.png'), pygame.image.load('tach/sport/8000/tach5.png'),pygame.image.load('tach/sport/8000/tach6.png')]


def tachometer():
    # 0-1000
    if rpm_target == 0:
        screen.blit(tachometer_0[0], (tachometerX, tachometerY))
    elif rpm_target > 0 and rpm_target <= 167:
        screen.blit(tachometer_0[1], (tachometerX, tachometerY))
    elif rpm_target > 167 and rpm_target <= 334:
        screen.blit(tachometer_0[2], (tachometerX, tachometerY))
    elif rpm_target > 334 and rpm_target <= 501:
        screen.blit(tachometer_0[3], (tachometerX, tachometerY))
    elif rpm_target > 501 and rpm_target <= 800:
        screen.blit(tachometer_0[4], (tachometerX, tachometerY))
    elif rpm_target > 800 and rpm_target <= 950:
        screen.blit(tachometer_0[5], (tachometerX, tachometerY))
    elif rpm_target > 950 and rpm_target <= 1000:
        screen.blit(tachometer_0[6], (tachometerX, tachometerY))

    # 1000-2000
    if rpm_target > 1000 and rpm_target <= 1167:
        screen.blit(tachometer_1[0], (tachometerX, tachometerY))
    elif rpm_target > 1167 and rpm_target <= 1334:
        screen.blit(tachometer_1[1], (tachometerX, tachometerY))
    elif rpm_target > 1334 and rpm_target <= 1501:
        screen.blit(tachometer_1[2], (tachometerX, tachometerY))
    elif rpm_target > 1501 and rpm_target <= 1800:
        screen.blit(tachometer_1[3], (tachometerX, tachometerY))
    elif rpm_target > 1800 and rpm_target <= 1950:
        screen.blit(tachometer_1[4], (tachometerX, tachometerY))
    elif rpm_target > 1950 and rpm_target <= 2000:
        screen.blit(tachometer_1[5], (tachometerX, tachometerY))

    # 2000-3000
    if rpm_target > 2000 and rpm_target <= 2167:
        screen.blit(tachometer_2[0], (tachometerX, tachometerY))
    elif rpm_target > 2167 and rpm_target <= 2334:
        screen.blit(tachometer_2[1], (tachometerX, tachometerY))
    elif rpm_target > 2334 and rpm_target <= 2501:
        screen.blit(tachometer_2[2], (tachometerX, tachometerY))
    elif rpm_target > 2501 and rpm_target <= 2800:
        screen.blit(tachometer_2[3], (tachometerX, tachometerY))
    elif rpm_target > 2800 and rpm_target <= 2950:
        screen.blit(tachometer_2[4], (tachometerX, tachometerY))
    elif rpm_target > 2950 and rpm_target <= 3000:
        screen.blit(tachometer_2[5], (tachometerX, tachometerY))

    # 3000-4000
    if rpm_target > 3000 and rpm_target <= 3167:
        screen.blit(tachometer_3[0], (tachometerX, tachometerY))
    elif rpm_target > 3167 and rpm_target <= 3334:
        screen.blit(tachometer_3[1], (tachometerX, tachometerY))
    elif rpm_target > 3334 and rpm_target <= 3501:
        screen.blit(tachometer_3[2], (tachometerX, tachometerY))
    elif rpm_target > 3501 and rpm_target <= 3800:
        screen.blit(tachometer_3[3], (tachometerX, tachometerY))
    elif rpm_target > 3800 and rpm_target <= 3950:
        screen.blit(tachometer_3[4], (tachometerX, tachometerY))
    elif rpm_target > 3950 and rpm_target <= 4000:
        screen.blit(tachometer_3[5], (tachometerX, tachometerY))

    # 4000-5000
    if rpm_target > 4000 and rpm_target <= 4167:
        screen.blit(tachometer_4[0], (tachometerX, tachometerY))
    elif rpm_target > 4167 and rpm_target <= 4334:
        screen.blit(tachometer_4[1], (tachometerX, tachometerY))
    elif rpm_target > 4334 and rpm_target <= 4501:
        screen.blit(tachometer_4[2], (tachometerX, tachometerY))
    elif rpm_target > 4501 and rpm_target <= 4800:
        screen.blit(tachometer_4[3], (tachometerX, tachometerY))
    elif rpm_target > 4800 and rpm_target <= 4950:
        screen.blit(tachometer_4[4], (tachometerX, tachometerY))
    elif rpm_target > 4950 and rpm_target <= 5000:
        screen.blit(tachometer_4[5], (tachometerX, tachometerY))

    # 5000-6000
    if rpm_target > 5000 and rpm_target <= 5167:
        screen.blit(tachometer_5[0], (tachometerX, tachometerY))
    elif rpm_target > 5167 and rpm_target <= 5334:
        screen.blit(tachometer_5[1], (tachometerX, tachometerY))
    elif rpm_target > 5334 and rpm_target <= 5501:
        screen.blit(tachometer_5[2], (tachometerX, tachometerY))
    elif rpm_target > 5501 and rpm_target <= 5800:
        screen.blit(tachometer_5[3], (tachometerX, tachometerY))
    elif rpm_target > 5800 and rpm_target <= 5950:
        screen.blit(tachometer_5[4], (tachometerX, tachometerY))
    elif rpm_target > 5950 and rpm_target <= 6000:
        screen.blit(tachometer_5[5], (tachometerX, tachometerY))

    # 6000-7000
    if rpm_target > 6000 and rpm_target <= 6167:
        screen.blit(tachometer_6[0], (tachometerX, tachometerY))
    elif rpm_target > 6167 and rpm_target <= 6334:
        screen.blit(tachometer_6[1], (tachometerX, tachometerY))
    elif rpm_target > 6334 and rpm_target <= 6501:
        screen.blit(tachometer_6[2], (tachometerX, tachometerY))
    elif rpm_target > 6501 and rpm_target <= 6800:
        screen.blit(tachometer_6[3], (tachometerX, tachometerY))
    elif rpm_target > 6800 and rpm_target <= 6950:
        screen.blit(tachometer_6[4], (tachometerX, tachometerY))
    elif rpm_target > 6950 and rpm_target <= 7000:
        screen.blit(tachometer_6[5], (tachometerX, tachometerY))

    # 7000-8000
    if rpm_target > 7000 and rpm_target <= 7167:
        screen.blit(tachometer_7[0], (tachometerX, tachometerY))
    elif rpm_target > 7167 and rpm_target <= 7334:
        screen.blit(tachometer_7[1], (tachometerX, tachometerY))
    elif rpm_target > 7334 and rpm_target <= 7501:
        screen.blit(tachometer_7[2], (tachometerX, tachometerY))
    elif rpm_target > 7501 and rpm_target <= 7800:
        screen.blit(tachometer_7[3], (tachometerX, tachometerY))
    elif rpm_target > 7800 and rpm_target <= 7950:
        screen.blit(tachometer_7[4], (tachometerX, tachometerY))
    elif rpm_target > 7950 and rpm_target <= 8000:
        screen.blit(tachometer_7[5], (tachometerX, tachometerY))

    # 8000-9000
    if rpm_target > 8000 and rpm_target <= 8167:
        screen.blit(tachometer_8[0], (tachometerX, tachometerY))
    elif rpm_target > 8167 and rpm_target <= 8334:
        screen.blit(tachometer_8[1], (tachometerX, tachometerY))
    elif rpm_target > 8334 and rpm_target <= 8501:
        screen.blit(tachometer_8[2], (tachometerX, tachometerY))
    elif rpm_target > 8501 and rpm_target <= 8800:
        screen.blit(tachometer_8[3], (tachometerX, tachometerY))
    elif rpm_target > 8800 and rpm_target <= 8950:
        screen.blit(tachometer_8[4], (tachometerX, tachometerY))
    elif rpm_target > 8950 and rpm_target <= 9000:
        screen.blit(tachometer_8[5], (tachometerX, tachometerY))


def stachometer():
    # 0-1000
    if rpm_target == 0:
        screen.blit(stachometer_0[0], (tachometerX, tachometerY))
    elif rpm_target > 0 and rpm_target <= 167:
        screen.blit(stachometer_0[1], (tachometerX, tachometerY))
    elif rpm_target > 167 and rpm_target <= 334:
        screen.blit(stachometer_0[2], (tachometerX, tachometerY))
    elif rpm_target > 334 and rpm_target <= 501:
        screen.blit(stachometer_0[3], (tachometerX, tachometerY))
    elif rpm_target > 501 and rpm_target <= 800:
        screen.blit(stachometer_0[4], (tachometerX, tachometerY))
    elif rpm_target > 800 and rpm_target <= 950:
        screen.blit(stachometer_0[5], (tachometerX, tachometerY))
    elif rpm_target > 950 and rpm_target <= 1000:
        screen.blit(stachometer_0[6], (tachometerX, tachometerY))

    # 1000-2000
    if rpm_target > 1000 and rpm_target <= 1167:
        screen.blit(stachometer_1[0], (tachometerX, tachometerY))
    elif rpm_target > 1167 and rpm_target <= 1334:
        screen.blit(stachometer_1[1], (tachometerX, tachometerY))
    elif rpm_target > 1334 and rpm_target <= 1501:
        screen.blit(stachometer_1[2], (tachometerX, tachometerY))
    elif rpm_target > 1501 and rpm_target <= 1800:
        screen.blit(stachometer_1[3], (tachometerX, tachometerY))
    elif rpm_target > 1800 and rpm_target <= 1950:
        screen.blit(stachometer_1[4], (tachometerX, tachometerY))
    elif rpm_target > 1950 and rpm_target <= 2000:
        screen.blit(stachometer_1[5], (tachometerX, tachometerY))

    # 2000-3000
    if rpm_target > 2000 and rpm_target <= 2167:
        screen.blit(stachometer_2[0], (tachometerX, tachometerY))
    elif rpm_target > 2167 and rpm_target <= 2334:
        screen.blit(stachometer_2[1], (tachometerX, tachometerY))
    elif rpm_target > 2334 and rpm_target <= 2501:
        screen.blit(stachometer_2[2], (tachometerX, tachometerY))
    elif rpm_target > 2501 and rpm_target <= 2800:
        screen.blit(stachometer_2[3], (tachometerX, tachometerY))
    elif rpm_target > 2800 and rpm_target <= 2950:
        screen.blit(stachometer_2[4], (tachometerX, tachometerY))
    elif rpm_target > 2950 and rpm_target <= 3000:
        screen.blit(stachometer_2[5], (tachometerX, tachometerY))

    # 3000-4000
    if rpm_target > 3000 and rpm_target <= 3167:
        screen.blit(stachometer_3[0], (tachometerX, tachometerY))
    elif rpm_target > 3167 and rpm_target <= 3334:
        screen.blit(stachometer_3[1], (tachometerX, tachometerY))
    elif rpm_target > 3334 and rpm_target <= 3501:
        screen.blit(stachometer_3[2], (tachometerX, tachometerY))
    elif rpm_target > 3501 and rpm_target <= 3800:
        screen.blit(stachometer_3[3], (tachometerX, tachometerY))
    elif rpm_target > 3800 and rpm_target <= 3950:
        screen.blit(stachometer_3[4], (tachometerX, tachometerY))
    elif rpm_target > 3950 and rpm_target <= 4000:
        screen.blit(stachometer_3[5], (tachometerX, tachometerY))

    # 4000-5000
    if rpm_target > 4000 and rpm_target <= 4167:
        screen.blit(stachometer_4[0], (tachometerX, tachometerY))
    elif rpm_target > 4167 and rpm_target <= 4334:
        screen.blit(stachometer_4[1], (tachometerX, tachometerY))
    elif rpm_target > 4334 and rpm_target <= 4501:
        screen.blit(stachometer_4[2], (tachometerX, tachometerY))
    elif rpm_target > 4501 and rpm_target <= 4800:
        screen.blit(stachometer_4[3], (tachometerX, tachometerY))
    elif rpm_target > 4800 and rpm_target <= 4950:
        screen.blit(stachometer_4[4], (tachometerX, tachometerY))
    elif rpm_target > 4950 and rpm_target <= 5000:
        screen.blit(stachometer_4[5], (tachometerX, tachometerY))

    # 5000-6000
    if rpm_target > 5000 and rpm_target <= 5167:
        screen.blit(stachometer_5[0], (tachometerX, tachometerY))
    elif rpm_target > 5167 and rpm_target <= 5334:
        screen.blit(stachometer_5[1], (tachometerX, tachometerY))
    elif rpm_target > 5334 and rpm_target <= 5501:
        screen.blit(stachometer_5[2], (tachometerX, tachometerY))
    elif rpm_target > 5501 and rpm_target <= 5800:
        screen.blit(stachometer_5[3], (tachometerX, tachometerY))
    elif rpm_target > 5800 and rpm_target <= 5950:
        screen.blit(stachometer_5[4], (tachometerX, tachometerY))
    elif rpm_target > 5950 and rpm_target <= 6000:
        screen.blit(stachometer_5[5], (tachometerX, tachometerY))

    # 6000-7000
    if rpm_target > 6000 and rpm_target <= 6167:
        screen.blit(stachometer_6[0], (tachometerX, tachometerY))
    elif rpm_target > 6167 and rpm_target <= 6334:
        screen.blit(stachometer_6[1], (tachometerX, tachometerY))
    elif rpm_target > 6334 and rpm_target <= 6501:
        screen.blit(stachometer_6[2], (tachometerX, tachometerY))
    elif rpm_target > 6501 and rpm_target <= 6800:
        screen.blit(stachometer_6[3], (tachometerX, tachometerY))
    elif rpm_target > 6800 and rpm_target <= 6950:
        screen.blit(stachometer_6[4], (tachometerX, tachometerY))
    elif rpm_target > 6950 and rpm_target <= 7000:
        screen.blit(stachometer_6[5], (tachometerX, tachometerY))

    # 7000-8000
    if rpm_target > 7000 and rpm_target <= 7167:
        screen.blit(stachometer_7[0], (tachometerX, tachometerY))
    elif rpm_target > 7167 and rpm_target <= 7334:
        screen.blit(stachometer_7[1], (tachometerX, tachometerY))
    elif rpm_target > 7334 and rpm_target <= 7501:
        screen.blit(stachometer_7[2], (tachometerX, tachometerY))
    elif rpm_target > 7501 and rpm_target <= 7800:
        screen.blit(stachometer_7[3], (tachometerX, tachometerY))
    elif rpm_target > 7800 and rpm_target <= 7950:
        screen.blit(stachometer_7[4], (tachometerX, tachometerY))
    elif rpm_target > 7950 and rpm_target <= 8000:
        screen.blit(stachometer_7[5], (tachometerX, tachometerY))

    # 8000-9000
    if rpm_target > 8000 and rpm_target <= 8167:
        screen.blit(stachometer_8[0], (tachometerX, tachometerY))
    elif rpm_target > 8167 and rpm_target <= 8334:
        screen.blit(stachometer_8[1], (tachometerX, tachometerY))
    elif rpm_target > 8334 and rpm_target <= 8501:
        screen.blit(stachometer_8[2], (tachometerX, tachometerY))
    elif rpm_target > 8501 and rpm_target <= 8800:
        screen.blit(stachometer_8[3], (tachometerX, tachometerY))
    elif rpm_target > 8800 and rpm_target <= 8950:
        screen.blit(stachometer_8[4], (tachometerX, tachometerY))
    elif rpm_target > 8950 and rpm_target <= 9000:
        screen.blit(stachometer_8[5], (tachometerX, tachometerY))

# Speed
speed_value = 0
speed_font = pygame.font.Font('Fonts/LeelUIsl.ttf', 50)
mphfont = pygame.font.Font('Fonts/LeelUIsl.ttf', 25)

rpm_font = pygame.font.Font('Fonts/pirulen rg.ttf', 34)
srpmfont = pygame.font.Font('Fonts/pirulen rg.ttf', 25)

speedtextX0 = 500  # one's place
speedtextY0 = 255

speedtextX10 = 489  # ten's place
speedtextY10 = 255

speedtextX100 = 480  # hundredth's place
speedtextY100 = 255

mphtextX = 488
mphtextY = 325


def display_speed():
    speed = speed_font.render(str(speed_value), True, (255, 255, 255))
    mph = mphfont.render("MPH", True, (255, 255, 255))

    if speed_value <= 9:
        screen.blit(speed, (speedtextX0, speedtextY0))
    elif speed_value >= 10 and speed_value <= 99:
        screen.blit(speed, (speedtextX10, speedtextY10))
    elif speed_value >= 100:
        screen.blit(speed, (speedtextX100, speedtextY100))

    screen.blit(mph, (mphtextX, mphtextY))


def sdisplay_rpm():
    srpm = rpm_font.render(str(rpm_target), True, (255, 255, 255))
    rpm_text = srpmfont.render("RPM", True, (255, 255, 255))

    if rpm_target <= 9:
        screen.blit(srpm, (speedtextX0, speedtextY0 + 15))
    elif rpm_target >= 10 and rpm_target <= 99:
        screen.blit(srpm, (speedtextX10 - 5, speedtextY10 + 15))
    elif rpm_target >= 100 and rpm_target <= 999:
        screen.blit(srpm, (speedtextX10 - 20, speedtextY10 + 15))
    elif rpm_target >= 1000 and rpm_target <= 1999:
        screen.blit(srpm, (speedtextX10 - 22, speedtextY10 + 15))
    elif rpm_target >= 2000:
        screen.blit(srpm, (speedtextX100 - 25, speedtextY100 + 15))

    screen.blit(rpm_text, (mphtextX - 10, mphtextY - 10))

main_page_check_engine_img = pygame.image.load('diagnostics/engine_check.png')

# main display information
def display_more_info():
    info_font = pygame.font.Font('Fonts/LeelUIsl.ttf', 30)

    rpm_norm = info_font.render('Tach ' + str(rpm_target) + ' RPM', True, (255, 255, 255))
    screen.blit(rpm_norm, (775, 330))

    mpg_inst_norm = info_font.render('MPG ' + str(inst_mpg), True, (255, 255, 255))
    screen.blit(mpg_inst_norm, (775, 370))

    mpg_avg_norm = info_font.render('Voltage ' + str(voltage) + ' V', True, (255, 255, 255))
    screen.blit(mpg_avg_norm, (775, 410))


    if dtc_code_present == True:
        screen.blit(main_page_check_engine_img, (830, 175))



# sport display information
def display_more_info_sport():
    info_font = pygame.font.Font('Fonts/pirulen rg.ttf', 25)

    maf_sport = info_font.render('MAF ' + str(maf_reading) + ' g/s', True, (255, 255, 255))
    screen.blit(maf_sport, (755, 150))

    throttle_sport = info_font.render('Throttle ' + str(throttle_position) + '%', True, (255, 255, 255))
    screen.blit(throttle_sport, (755, 190))

    load_sport = info_font.render('Load ' + str(load) + '%', True, (255, 255, 255))
    screen.blit(load_sport, (755, 230))

    speed_sport = info_font.render('Speed ' + str(speed_value) + ' MPH', True, (255, 255, 255))
    screen.blit(speed_sport, (745, 380))


# temperature guages
temp_indicator_img = pygame.image.load('temp_gauge/indicator.png')
temp_gauge_img = pygame.image.load('temp_gauge/Temp Gauge.png')
temp_indicatorX = 140  # 135 = middle, 240 = max, 30 = min
temp_indicatorY = 399
temp_font = pygame.font.Font('Fonts/LeelUIsl.ttf', 25)
stemp_font = pygame.font.Font('Fonts/pirulen rg.ttf', 20)
stemp_font_fuel = pygame.font.Font('Fonts/pirulen rg.ttf', 18)

temp_txt_X = 30
temp_txt_Y = 420


# Intake Temp Gauge
def intake_temp_gauge():
    turbo_icon_img = pygame.image.load('sport_mode/turbo.png')
    temp_intake = stemp_font.render(('Intake Temp ' + str(intake_temp) + ' °F'), True, (255, 255, 255))
    screen.blit(temp_intake, (temp_txt_X - 22, 245))

    screen.blit(temp_gauge_img, (19, 220))

    if intake_temp >= 60 and intake_temp <= 80:
        screen.blit(temp_indicator_img, (temp_indicatorX, 220))
    elif intake_temp >= 40 and intake_temp < 60:
        screen.blit(temp_indicator_img, (temp_indicatorX - 10, 220))
    elif intake_temp >= 20 and intake_temp < 40:
        screen.blit(temp_indicator_img, (temp_indicatorX - 50, 220))
    elif intake_temp >= 0 and intake_temp < 20:
        screen.blit(temp_indicator_img, (temp_indicatorX - 105, 220))
    elif intake_temp > 80 and intake_temp <= 120:
        screen.blit(temp_indicator_img, (temp_indicatorX + 10, 220))
    elif intake_temp > 120 and intake_temp <= 150:
        screen.blit(temp_indicator_img, (temp_indicatorX + 70, 220))
    elif intake_temp > 150:
        screen.blit(temp_indicator_img, (temp_indicatorX + 95, 220))

    pressure_fuel = stemp_font_fuel.render(('Fuel Pressure ' + str(fuel_pressure) + ' PSI'), True, (255, 255, 255))
    screen.blit(pressure_fuel, (temp_txt_X - 20, 185))

    screen.blit(turbo_icon_img, (120, 135))


# Coolant Temp Gauge
def temp_gauge():
    if temp_value >= 200 and temp_value <= 220:
        screen.blit(temp_indicator_img, (temp_indicatorX, temp_indicatorY))
    elif temp_value >= 180 and temp_value < 200:
        screen.blit(temp_indicator_img, (temp_indicatorX - 10, temp_indicatorY))
    elif temp_value >= 100 and temp_value < 180:
        screen.blit(temp_indicator_img, (temp_indicatorX - 50, temp_indicatorY))
    elif temp_value >= 0 and temp_value < 100:
        screen.blit(temp_indicator_img, (temp_indicatorX - 105, temp_indicatorY))
    elif temp_value > 195 and temp_value <= 225:
        screen.blit(temp_indicator_img, (temp_indicatorX + 10, temp_indicatorY))
    elif temp_value > 225 and temp_value <= 275:
        screen.blit(temp_indicator_img, (temp_indicatorX + 70, temp_indicatorY))
    elif temp_value > 275:
        screen.blit(temp_indicator_img, (temp_indicatorX + 95, temp_indicatorY))


def display_temp():
    temp = temp_font.render(('Coolant Temp ' + str(temp_value) + ' °F'), True, (255, 255, 255))

    screen.blit(temp, (temp_txt_X, temp_txt_Y))


def sdisplay_temp():
    temp = stemp_font.render(('Coolant ' + str(temp_value) + ' °F'), True, (255, 255, 255))

    screen.blit(temp, (temp_txt_X - 5, temp_txt_Y + 5))


# Framework
framework_img = pygame.image.load('framework.png')
frameworkX = 8
frameworkY = 95

sframework_img = pygame.image.load('sport_mode/framework/Framework.png')


def framework():
    screen.blit(framework_img, (frameworkX, frameworkY))


def sframework():
    screen.blit(sframework_img, (frameworkX, frameworkY))


# Background colors
gradient_img = pygame.image.load('backgrounds/Gradient.png')
gradientX = 0
gradientY = 0

red_color = pygame.image.load('backgrounds/Gradient_red.png')
blue_color = pygame.image.load('backgrounds/Gradient_blue.png')
green_color = pygame.image.load('backgrounds/gradient green.png')
grey_color = pygame.image.load('backgrounds/gradient grey.png')
mint_color = pygame.image.load('backgrounds/gradient mint.png')
pink_color = pygame.image.load('backgrounds/gradient pink.png')
purple_color = pygame.image.load('backgrounds/gradient purple.png')

def gradient():
    screen.blit(gradient_img, (gradientX, gradientY))


def sports():
    if current_color == 1:
        screen.blit(red_color, (gradientX, gradientY))
    elif current_color == 2:
        screen.blit(blue_color, (gradientX, gradientY))
    elif current_color == 3:
        screen.blit(green_color, (gradientX, gradientY))
    elif current_color == 4:
        screen.blit(grey_color, (gradientX, gradientY))
    elif current_color == 5:
        screen.blit(mint_color, (gradientX, gradientY))
    elif current_color == 6:
        screen.blit(pink_color, (gradientX, gradientY))
    elif current_color == 7:
        screen.blit(purple_color, (gradientX, gradientY))

# Buttons
normal_font = pygame.font.Font('Fonts/LeelUIsl.ttf', 25)
sports_font = pygame.font.Font('Fonts/pirulen rg.ttf', 13)

# Button Text
sports_txt_X = 98
sports_txt_Y = 530
normal_txt_X = 97
normal_txt_Y = 530


def sports_button():
    if sports_button_press is True:
        button_img = pygame.image.load('buttons/Sport Button Pressed (no label).png')
    else:
        button_img = pygame.image.load('buttons/Sport button not pressed (no label).png')
    screen.blit(button_img, (45, 450))
    # Checks the state and changes the text accordingly
    if current_page != 2:
        button_label = sports_font.render('Sports', True, (255, 255, 255))
        screen.blit(button_label, (sports_txt_X, sports_txt_Y))
    else:
        button_label = sports_font.render('Normal', True, (255, 255, 255))
        screen.blit(button_label, (normal_txt_X, normal_txt_Y))

def exit_button():
    if exit_press is True:
        exit_img = pygame.image.load('buttons/exit button pressed.png')
    else:
        exit_img = pygame.image.load('buttons/exit button not pressed.png')
    screen.blit(exit_img, (785, 450))

def shutdown_button():
    if shutdown_press is True:
        shutdown_img = pygame.image.load('buttons/power button pressed.png')
    else:
        shutdown_img = pygame.image.load('buttons/power button not pressed.png')
    screen.blit(shutdown_img, (675, 450))

def back_button():
    if back_button_press is True:
        back_img = pygame.image.load('buttons/Back Button Pressed.png')
    else:
        back_img = pygame.image.load('buttons/Back Button.png')
    screen.blit(back_img, (10, 425))


def reset_button():
    if reset_button_press is True:
        reset_img = pygame.image.load('buttons/Reset Interval Button Pressed.png')
    else:
        reset_img = pygame.image.load('buttons/Reset Interval Button.png')
    screen.blit(reset_img, (700, 425))


def interval_button():
    if interval_button_press is True:
        interval_img = pygame.image.load('buttons/Interval Button Pressed.png')
    else:
        interval_img = pygame.image.load('buttons/Interval Button.png')
    screen.blit(interval_img, (825, 425))

def colors_button():
    if colors_button_press is True:
        colors_img = pygame.image.load('buttons/color shift pressed.png')
    else:
        colors_img = pygame.image.load('buttons/color shift not pressed.png')
    screen.blit(colors_img, (754, 450))

# Current interval text
interval_txt_X = 220
interval_txt_Y = 200
interval_font = pygame.font.Font('Fonts/LeelUIsl.ttf', 40)


def interval_text(interval_string, maintenance_interval, offset):
    interval_message = interval_font.render(interval_string + str(maintenance_interval), True, (255, 255, 255))

    screen.blit(interval_message, (interval_txt_X + offset, interval_txt_Y))


# Oil change interval buttons
def three_thousand():
    if three_thousand_press is True:
        three_thousand_img = pygame.image.load('buttons/3000_P.png')
    else:
        three_thousand_img = pygame.image.load('buttons/3000_NP.png')
    screen.blit(three_thousand_img, (115, 260))


def five_thousand():
    if five_thousand_press is True:
        five_thousand_img = pygame.image.load('buttons/5000_P.png')
    else:
        five_thousand_img = pygame.image.load('buttons/5000_NP.png')
    screen.blit(five_thousand_img, (265, 260))


def seven_thousand_five():
    if seven_thousand_five_press is True:
        seven_thousand_five_img = pygame.image.load('buttons/7500_P.png')
    else:
        seven_thousand_five_img = pygame.image.load('buttons/7500_NP.png')
    screen.blit(seven_thousand_five_img, (415, 260))


def ten_thousand():
    if ten_thousand_press is True:
        ten_thousand_img = pygame.image.load('buttons/10000_P.png')
    else:
        ten_thousand_img = pygame.image.load('buttons/10000_NP.png')
    screen.blit(ten_thousand_img, (565, 260))


def fifteen_thousand():
    if fifteen_thousand_press is True:
        fifteen_thousand_img = pygame.image.load('buttons/15000_P.png')
    else:
        fifteen_thousand_img = pygame.image.load('buttons/15000_NP.png')
    screen.blit(fifteen_thousand_img, (715, 260))


def increment():
    if increment_press is True:
        increment_img = pygame.image.load('buttons/Plus button Pressed.png')
    else:
        increment_img = pygame.image.load('buttons/Plus Button Not Pressed.png')
    screen.blit(increment_img, (600, 260))


def decrement():
    if decrement_press is True:
        decrement_img = pygame.image.load('buttons/Subtract Button Pressed.png')
    else:
        decrement_img = pygame.image.load('buttons/Subtract button Not pressed.png')
    screen.blit(decrement_img, (250, 260))


# Maintenance Display

# File Objects and Maintenance and Mileage Tracking
with open('maintenance/interval.txt', 'r+') as int_file:
    oil_change_string = int_file.readline()
    oil_change_interval = int(oil_change_string)

with open('maintenance/transmission_interval.txt', 'r+') as int_file:
    transmission_change_string = int_file.readline()
    transmission_oil_change_interval = int(transmission_change_string)

with open('maintenance/brake_interval.txt', 'r+') as int_file:
    brake_change_string = int_file.readline()
    brake_change_interval = int(brake_change_string)

with open('maintenance/mileage.txt', 'r+') as mileage_file:
    oil_mileage_string = mileage_file.readline()
    oil_mileage = int(oil_mileage_string)

with open('maintenance/transmission_mileage.txt', 'r+') as mileage_file:
    transmission_mileage_string = mileage_file.readline()
    transmission_oil_mileage = int(transmission_mileage_string)

with open('maintenance/brake_mileage.txt', 'r+') as mileage_file:
    brake_mileage_string = mileage_file.readline()
    brake_mileage = int(brake_mileage_string)


def maintenance_counter(mileage, interval):
    maintenance_count = interval - mileage
    return maintenance_count


oil_change_count = maintenance_counter(oil_mileage, oil_change_interval)
transmission_oil_change_count = maintenance_counter(transmission_oil_mileage, transmission_oil_change_interval)
brake_change_count = maintenance_counter(brake_mileage, brake_change_interval)


def display_maintenance_distance(maintenance_string, past_due_string, maintenance_count, offset, offset_due):
    maintenance_font = pygame.font.Font('Fonts/LeelUIsl.ttf', 40)
    txt_X = 255
    txt_Y = 330

    if maintenance_count > 0:
        maintenance_change = maintenance_font.render((maintenance_string + str(maintenance_count) + ' Miles'), True,
                                                     (255, 255, 255))
        screen.blit(maintenance_change, (txt_X + offset, txt_Y))
    elif maintenance_count < 0:
        maintenance_past_due = maintenance_font.render((past_due_string + str(maintenance_count * -1) + ' Miles'), True,
                                                       (255, 255, 255))
        screen.blit(maintenance_past_due, (txt_X + offset_due, txt_Y))


# Warning Indicator

def display_warning_indicator(maintenance_count, maintenance_page):
    warning_big_img = pygame.image.load('maintenance/warning_big.png')
    brake_img = pygame.image.load('maintenance/brake.png')
    transmission_img = pygame.image.load('maintenance/gearbox.png')
    oil_img = pygame.image.load('maintenance/oil_white_big.png')

    warning_bigX = 470
    warning_bigY = 235

    if maintenance_count < 500:
        screen.blit(warning_big_img, (warning_bigX, warning_bigY))
    else:
        if maintenance_page == 1:
            screen.blit(oil_img, (warning_bigX - 20, warning_bigY))
        elif maintenance_page == 2:
            screen.blit(transmission_img, (warning_bigX, warning_bigY - 15))
        elif maintenance_page == 3:
            screen.blit(brake_img, (warning_bigX, warning_bigY - 15))


# Main Page Maintenance Indicators

warning_small_img = pygame.image.load('maintenance/warning_small.png')
everything_ok_img = pygame.image.load('maintenance/maintenance ok.png')


def display_warning_indicator_small(oil_change_count, transmission_change_count, brake_change_count):
    warning_smallX = 120
    warning_smallY = 230

    maintenance_txt_X = 45
    maintenance_txt_Y = 175

    if oil_change_count < 500 or transmission_change_count < 500 or brake_change_count < 500:
        screen.blit(warning_small_img, (warning_smallX, warning_smallY))
        maintenance_change_font = pygame.font.Font('Fonts/LeelUIsl.ttf', 25)
        maintenance_line1 = maintenance_change_font.render(('Maintenance Due'), True, (255, 255, 255))
        screen.blit(maintenance_line1, (maintenance_txt_X, maintenance_txt_Y))
    else:
        screen.blit(everything_ok_img, (15, 200))


# Maintenance Headings
vehicle_maint_heading_img = pygame.image.load('maintenance/maintenance_heading.png')
maint_headingX = 210
maint_headingY = 65
next_maintenance = pygame.image.load('buttons/next.png')
previous_maintenance = pygame.image.load('buttons/back.png')

oil_change_int_heading_img = pygame.image.load('maintenance/oil_change_interval_heading.png')
transmission_oil_change_int_heading_img = pygame.image.load('maintenance/transmission_interval_heading.png')
brake_change_int_heading_img = pygame.image.load('maintenance/brake_interval_heading.png')


def display_maint_heading():
    screen.blit(vehicle_maint_heading_img, (maint_headingX, maint_headingY))
    screen.blit(next_maintenance, (765, 75))
    screen.blit(previous_maintenance, (210, 75))


def display_int_heading(maintenance_heading_img):
    screen.blit(maintenance_heading_img, (maint_headingX, maint_headingY))


# Diagnostic Display
diag_heading_img = pygame.image.load('diagnostics/vehicle_diagnostics_heading.png')


def display_diag_heading():
    screen.blit(diag_heading_img, (maint_headingX, maint_headingY))


# Diagnostics Display
clear_dtc_font = pygame.font.Font('Fonts/LeelUIsl.ttf', 20)
clear_dtc_button_label = clear_dtc_font.render('Clear DTC', True, (255, 255, 255))


def clear_dtc_button():
    if clear_dtc_press is False:
        clear_dtc = pygame.image.load('buttons/Sport button not pressed (no label).png')
    else:
        clear_dtc = pygame.image.load('buttons/Sport Button Pressed (no label).png')
    screen.blit(clear_dtc, (840, 425))
    screen.blit(clear_dtc_button_label, (888, 500))


diagnostic_font = pygame.font.Font('Fonts/LeelUIsl.ttf', 30)
no_error_msg = diagnostic_font.render('No DTC Codes Detected', True, (255, 255, 255))
no_error_symbol = pygame.image.load('car.png')

error_symbol_small = pygame.image.load('engine_check_small.png')
error_symbol = pygame.image.load('engine_check.png')


# Display functions for UI(MQTT connectriviy cant be implemetted rn )
def displays():
    sports_button()
    tachometer()
    framework()
    temp_gauge()
    display_temp()
    display_warning_indicator_small(oil_change_count, transmission_oil_change_count, brake_change_count)
    display_speed()
    display_more_info()
    display_logos()
    exit_button()
    shutdown_button()


def sports_display():
    stachometer()
    sports_button()
    sframework()
    sdisplay_rpm()
    temp_gauge()
    sdisplay_temp()
    display_more_info_sport()
    intake_temp_gauge()
    display_logos()
    colors_button()

def maintenance_display():
    reset_button()
    interval_button()
    back_button()
    display_maint_heading()
    # Changes maintenance information
    if current_maintenance == 1:
        display_maintenance_distance('Oil Change Due In ', 'Oil Change Past Due by ', oil_change_count, 0, -50)
        display_warning_indicator(oil_change_count, 1)
    elif current_maintenance == 2:
        display_maintenance_distance('Transmission Oil Change Due In ', 'Transmission Oil Change Past Due by ',
                                     transmission_oil_change_count, -100, -150)
        display_warning_indicator(transmission_oil_change_count, 2)
    elif current_maintenance == 3:
        display_maintenance_distance('Brake Change Due In ', 'Brake Change Past Due by ', brake_change_count, -30, -60)
        display_warning_indicator(brake_change_count, 3)


def interval_display():
    if current_maintenance == 1:
        display_int_heading(oil_change_int_heading_img)
        three_thousand()
        five_thousand()
        seven_thousand_five()
        ten_thousand()
        fifteen_thousand()
        interval_text('Current Oil Change Interval: ', oil_change_interval, 0)
    elif current_maintenance == 2:
        increment()
        decrement()
        interval_text('Current Transmission Oil Change Interval: ', transmission_oil_change_interval, -100)
        display_int_heading(transmission_oil_change_int_heading_img)
    elif current_maintenance == 3:
        increment()
        decrement()
        interval_text('Current Brake Change Interval: ', brake_change_interval, -20)
        display_int_heading(brake_change_int_heading_img)
    # all pages
    back_button()


error_font = pygame.font.Font('Fonts/LeelUIsl.ttf', 30)


def diag_display():
    display_diag_heading()
    back_button()
    if current_page == 5:
        screen.blit(no_error_symbol, (435, 175))
        screen.blit(no_error_msg, (340, 300))


    elif current_page == 6:
        screen.blit(error_symbol_small, (465, 155))
        error_num_list = []
        error_description_list = []
        # Separates tuples into two lists
        for i in range(len(dtc_code)):
            error_num, error_description = dtc_code[i]
            error_num_list.append(error_num)
            error_description_list.append(error_description)
        # Iterates through the two lists and prints list contents
        for j in range(len(dtc_code)):
            error_label = error_font.render(error_num_list[j] + ' ' + error_description_list[j], True, (255, 255, 255))
            screen.blit(error_label, (200, 250 + (j * 40)))
        clear_dtc_button()

# Change background colors page
color_heading = pygame.image.load('logos_headings/Background Colors Heading.png')
color_font = pygame.font.Font('Fonts/pirulen rg.ttf', 25)
with open('backgrounds/current_background.txt', 'r+') as background_file:
    background_color_string = background_file.readline()
    if background_color_string:
        current_color = int(background_color_string)
    # Defaults to red if text file is empty
    else:
        current_color = 1

def display_color_heading():
    screen.blit(color_heading, (maint_headingX, maint_headingY))

def display_current_color(current_color):
    color_label = color_font.render('Current color: ' + colors.get(current_color), True, (255, 255, 255))
    screen.blit(color_label, (300, 170))

def red_button():
    if red_press is True:
        red = pygame.image.load('buttons/Red P.png')
    else:
        red = pygame.image.load('buttons/Red NP.png')
    screen.blit(red, (190, 200))

def blue_button():
    if blue_press is True:
        blue = pygame.image.load('buttons/Blue P.png')
    else:
        blue = pygame.image.load('buttons/Blue NP.png')
    screen.blit(blue, (340, 200))

def green_button():
    if green_press is True:
        green = pygame.image.load('buttons/Green P.png')
    else:
        green = pygame.image.load('buttons/Green NP.png')
    screen.blit(green, (490, 200))

def grey_button():
    if grey_press is True:
        grey = pygame.image.load('buttons/Grey P.png')
    else:
        grey = pygame.image.load('buttons/Grey NP.png')
    screen.blit(grey, (640, 200))

def mint_button():
    if mint_press is True:
        mint = pygame.image.load('buttons/Mint P.png')
    else:
        mint = pygame.image.load('buttons/Mint NP.png')
    screen.blit(mint, (265, 320))

def pink_button():
    if pink_press is True:
        pink = pygame.image.load('buttons/Pink P.png')
    else:
        pink = pygame.image.load('buttons/Pink NP.png')
    screen.blit(pink, (415, 320))

def purple_button():
    if purple_press is True:
        purple = pygame.image.load('buttons/Purple P.png')
    else:
        purple = pygame.image.load('buttons/Purple NP.png')
    screen.blit(purple, (565, 320))

def color_display():
    display_color_heading()
    display_current_color(current_color)
    back_button()
    red_button()
    blue_button()
    green_button()
    grey_button()
    mint_button()
    pink_button()
    purple_button()

# Confirm reset page
reset_heading = pygame.image.load('maintenance/Confirm Reset Heading.png')
reset_font = pygame.font.Font('Fonts/LeelUIsl.ttf', 35)

def confirm_reset_heading():
    screen.blit(reset_heading, (maint_headingX, maint_headingY))

def confirm_reset_message(current_maintenance):
    if current_maintenance == 1:
        reset_message = reset_font.render('Do you want to reset the oil maintenance interval?', True, (255, 255, 255))
        screen.blit(reset_message, (140, 180))
    elif current_maintenance == 2:
        reset_message = reset_font.render('Do you want to reset the transmission maintenance interval?', True, (255, 255, 255))
        screen.blit(reset_message, (70, 180))
    elif current_maintenance == 3:
        reset_message = reset_font.render('Do you want to reset the brake maintenance interval?', True, (255, 255, 255))
        screen.blit(reset_message, (120, 180))

def yes_button():
    if yes_press is True:
        yes = pygame.image.load('buttons/Yes P.png')
    else:
        yes = pygame.image.load('buttons/Yes NP.png')
    screen.blit(yes, (250, 260))

def no_button():
    if no_press is True:
        no = pygame.image.load('buttons/No P.png')
    else:
        no = pygame.image.load('buttons/No NP.png')
    screen.blit(no, (600, 260))

def confirm_display():
    confirm_reset_heading()
    confirm_reset_message(current_maintenance)
    yes_button()
    no_button()

# Redraw
def RedrawWindow():
    # Checks which background image to use
    if current_page == 2:
        sports()

    else:
        gradient()

    # Checks if the current screen needs the gauges and normal information
    if current_page < 3 and current_page != 2:
        displays()
    else:
        if current_page == 2:
            sports_display()
        elif current_page == 3:
            maintenance_display()
        elif current_page == 4:
            interval_display()
        elif current_page == 7:
            color_display()
        elif current_page == 8:
            confirm_display()
        else:
            diag_display()

    pygame.display.update()

def drawBootscreen():
    display_bootscreen()
    pygame.display.update()

# OBD Callback Definitions to be replaced by mqtt callbacks 
def get_rpm(rpmRaw):
    if not rpmRaw.is_null():
        global rpm_target
        rpm_target = mqtt_data


def get_speed(speedRaw):
    if not speedRaw.is_null():
        global speed_value
        speed_value = mqtt_data  # to MPH instead of KMH need to be implemeted 
        


def get_temp(tempRaw):
    if not tempRaw.is_null():
        global temp_value
        temp_value = mqtt_data

def get_throttle_position(throttlepositionRaw):
    if not throttlepositionRaw.is_null():
        global throttle_position
        throttle_position = int(throttlepositionRaw.value.magnitude)


def get_maf(mafRaw):
    if not mafRaw.is_null():
        global maf_reading
        maf_reading = mqtt_data


def get_load(loadRaw):
    if not loadRaw.is_null():
        global load
        load = int(loadRaw.value.magnitude)


def get_fuel_pressure(fuelpressureRaw):
    if not fuelpressureRaw.is_null():
        global fuel_pressure
        fuel_pressure = int(fuelpressureRaw.value.magnitude * 0.14503)


def get_intake_temp(intaketempRaw):
    if not intaketempRaw.is_null():
        global intake_temp
        intake_temp = int((intaketempRaw.value.magnitude * 1.8) + 32)


def get_trip_distance(tripdistanceRaw):
    if not tripdistanceRaw.is_null():
        global trip_distance
        trip_distance = int(tripdistanceRaw.value.magnitude * 0.621371)


def get_dtc_codes(dtcRaw):
    global dtc_code
    dtc_code = mqtt_data

def clear_dtc_codes(clearRaw):
    global dtc_code

def get_elm_voltage(voltageRaw):
    if not voltageRaw.is_null():
        global voltage
        voltage = mqtt_data

# OBD Connection Callbacks
def initialize():
    connection.watch(obd.commands.RPM, callback=get_rpm)
    connection.watch(obd.commands.SPEED, callback=get_speed)
    connection.watch(obd.commands.COOLANT_TEMP, callback=get_temp)
    connection.watch(obd.commands.THROTTLE_POS, callback=get_throttle_position)
    connection.watch(obd.commands.MAF, callback=get_maf)
    connection.watch(obd.commands.ENGINE_LOAD, callback=get_load)
    connection.watch(obd.commands.FUEL_PRESSURE, callback=get_fuel_pressure)
    connection.watch(obd.commands.INTAKE_TEMP, callback=get_intake_temp)
    connection.watch(obd.commands.DISTANCE_SINCE_DTC_CLEAR, callback=get_trip_distance)
    connection.watch(obd.commands.GET_DTC, callback=get_dtc_codes)
    connection.watch(obd.commands.ELM_VOLTAGE, callback=get_elm_voltage)
    connection.start()

def clearDTC():
    
    connection.stop()
    connection.watch(obd.commands.CLEAR_DTC, callback=clear_dtc_codes)
    connection.watch(obd.commands.RPM, callback=get_rpm)
    connection.watch(obd.commands.SPEED, callback=get_speed)
    connection.watch(obd.commands.COOLANT_TEMP, callback=get_temp)
    connection.watch(obd.commands.THROTTLE_POS, callback=get_throttle_position)
    connection.watch(obd.commands.MAF, callback=get_maf)
    connection.watch(obd.commands.ENGINE_LOAD, callback=get_load)
    connection.watch(obd.commands.FUEL_PRESSURE, callback=get_fuel_pressure)
    connection.watch(obd.commands.INTAKE_TEMP, callback=get_intake_temp)
    connection.watch(obd.commands.DISTANCE_SINCE_DTC_CLEAR, callback=get_trip_distance)
    connection.watch(obd.commands.GET_DTC, callback=get_dtc_codes)
    connection.watch(obd.commands.ELM_VOLTAGE, callback=get_elm_voltage)
    connection.start()

# Game Loop
app_running = True
pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))

while app_running:
    clock.tick(60)
    mqtt_client.loop()
    # screen fill
    screen.fill((0, 0, 0))

    mouse = pygame.mouse.get_pos()
    #print(mouse)
    #############MQTT callbacks#############################
    voltage = mqtt_data
    speed_value = mqtt_data

    #boot sequence
    if initialized == False:
        drawBootscreen()
        endTime = time.time()
        if (endTime - startTime > 7) and initial_boot_complete == False:
            initial_boot_complete = True
        elif initial_boot_complete == True:
            # OBD Initilization
            connection = obd.Async(fast=False, check_voltage=False)
            initialize()
            initialized = True


    elif initialized == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                connection.stop()
                connection.close()
                app_running = False

            # Checks for when we press the mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checks if the mouse click was where the button is
                # mouse[0] is the x coordinate, mouse[1] is the y
                if 90 < mouse[0] < 180 and 495 < mouse[1] < 585 and current_page < 3:
                    sports_button_press = True
                elif 800 < mouse[0] < 890 and 495 < mouse[1] < 585 and current_page == 2:
                        colors_button_press = True
                elif 830 < mouse[0] < 920 and 495 < mouse[1] < 585 and current_page == 1:
                    exit_press = True
                elif 720 < mouse[0] < 810 and 495 < mouse[1] < 585 and current_page == 1:
                    shutdown_press = True
                elif 56 < mouse[0] < 146 and 471 < mouse[1] < 561 and current_page > 2:
                    back_button_press = True
                elif 745 < mouse[0] < 835 and 471 < mouse[1] < 561 and current_page == 3:
                    reset_button_press = True
                elif 870 < mouse[0] < 960 and 471 < mouse[1] < 561 and current_page == 3:
                    interval_button_press = True
                elif 885 < mouse[0] < 975 and 470 < mouse[1] < 560 and current_page == 6:
                    clear_dtc_press = True
                    # clearDTC()
                elif current_page == 4:
                    if current_maintenance == 1:
                        if 160 < mouse[0] < 250 and 305 < mouse[1] < 395:
                            three_thousand_press = True
                        elif 310 < mouse[0] < 400 and 305 < mouse[1] < 395:
                            five_thousand_press = True
                        elif 460 < mouse[0] < 550 and 305 < mouse[1] < 395:
                            seven_thousand_five_press = True
                        elif 610 < mouse[0] < 700 and 305 < mouse[1] < 395:
                            ten_thousand_press = True
                        elif 760 < mouse[0] < 850 and 305 < mouse[1] < 395:
                            fifteen_thousand_press = True
                    elif current_maintenance == 2 or current_maintenance == 3:
                        if 295 < mouse[0] < 385 and 305 < mouse[1] < 395:
                            decrement_press = True
                        elif 645 < mouse[0] < 735 and 305 < mouse[1] < 395:
                            increment_press = True
                elif current_page == 7:
                    if 235 < mouse[0] < 325 and 245 < mouse[1] < 335:
                        red_press = True
                    elif 385 < mouse[0] < 475 and 245 < mouse[1] < 335:
                        blue_press = True
                    elif 535 < mouse[0] < 625 and 245 < mouse[1] < 335:
                        green_press = True
                    elif 685 < mouse[0] < 775 and 245 < mouse[1] < 335:
                        grey_press = True
                    elif 310 < mouse[0] < 400 and 365 < mouse[1] < 455:
                        mint_press = True
                    elif 460 < mouse[0] < 550 and 365 < mouse[1] < 455:
                        pink_press = True
                    elif 610 < mouse[0] < 700 and 365 < mouse[1] < 455:
                        purple_press = True
                elif current_page == 8:
                    if 295 < mouse[0] < 385 and 305 < mouse[1] < 395:
                        yes_press = True
                    elif 645 < mouse[0] < 735 and 305 < mouse[1] < 395:
                        no_press = True

            # Checks for when we let go of the mouse button
            if event.type == pygame.MOUSEBUTTONUP:
                interval_button_press = reset_button_press = diagnostic_press = maintenance_press = back_button_press = sports_button_press = False
                three_thousand_press = five_thousand_press = seven_thousand_five_press = ten_thousand_press = fifteen_thousand_press = False
                decrement_press = increment_press = False
                clear_dtc_press = False
                colors_button_press = False
                red_press = blue_press = green_press = grey_press = mint_press = pink_press = purple_press = False
                yes_press = no_press = False
                exit_press = False
                shutdown_press = False
                # current_page condition is used to prevent users from going to pages in the wrong order
                # ex. Going from maintenance to sports mode
                if 90 < mouse[0] < 180 and 495 < mouse[1] < 585 and current_page < 3:
                    if current_page != 2:
                        current_page = 2
                    else:
                        current_page = 1
                elif 800 < mouse[0] < 890 and 495 < mouse[1] < 585 and current_page == 2:
                    # Goes to change background color page
                    current_page = 7
                #Exit program
                elif 830 < mouse[0] < 920 and 495 < mouse[1] < 585 and current_page == 1:
                    connection.stop()
                    connection.close()
                    app_running = False
                #Shutdown System
                elif 720 < mouse[0] < 810 and 495 < mouse[1] < 585 and current_page == 1:
                    connection.stop()
                    connection.close()
                    os.system("sudo shutdown -h now")
                # Goes to vehicle maintenance
                elif 10 < mouse[0] < 270 and 130 < mouse[1] < 300 and current_page == 1:
                    current_page = 3
                # Navigates through the different maintenances
                # Previous maintenance
                elif 210 < mouse[0] < 260 and 65 < mouse[1] < 135 and current_page == 3:
                    if current_maintenance == 1:
                        current_maintenance = 3
                    else:
                        current_maintenance -= 1
                # Next maintenance
                elif 765 < mouse[0] < 810 and 65 < mouse[1] < 135 and current_page == 3:
                    if current_maintenance == 3:
                        current_maintenance = 1
                    else:
                        current_maintenance += 1
                # Goes to vehicle diagnostics
                elif 754 < mouse[0] < 1016 and 130 < mouse[1] < 300 and current_page < 2:
                    # Page 6 if there is an error
                    if dtc_code_present is True:
                        current_page = 6
                    else:
                        current_page = 5
                # Back button
                elif 56 < mouse[0] < 146 and 471 < mouse[1] < 561:
                    if current_page == 3 or current_page == 5 or current_page == 6:
                        current_page = 1
                    elif current_page == 7:
                        current_page = 2
                    else:
                        current_page -= 1
                # Reset button
                elif 745 < mouse[0] < 835 and 471 < mouse[1] < 561 and current_page == 3:
                    current_page = 8
                # Yes button
                elif 295 < mouse[0] < 385 and 305 < mouse[1] < 395 and current_page == 8:
                    if current_maintenance == 1:
                        oil_mileage = 0
                    elif current_maintenance == 2:
                        transmission_oil_mileage = 0
                    elif current_maintenance == 3:
                        brake_mileage = 0
                    current_page = 3
                # No button
                elif 645 < mouse[0] < 735 and 305 < mouse[1] < 395 and current_page == 8:
                    current_page = 3
                # Interval button
                elif 870 < mouse[0] < 960 and 471 < mouse[1] < 561 and current_page == 3:
                    current_page = 4
                if current_maintenance == 1 and current_page == 4:
                    if 160 < mouse[0] < 250 and 305 < mouse[1] < 395:
                        oil_change_interval = 3000
                        with open('maintenance/interval.txt', 'w') as interval_file:
                            interval_file.write(str(oil_change_interval))
                    elif 310 < mouse[0] < 400 and 305 < mouse[1] < 395:
                        oil_change_interval = 5000
                        with open('maintenance/interval.txt', 'w') as interval_file:
                            interval_file.write(str(oil_change_interval))
                    elif 460 < mouse[0] < 550 and 305 < mouse[1] < 395:
                        oil_change_interval = 7500
                        with open('maintenance/interval.txt', 'w') as interval_file:
                            interval_file.write(str(oil_change_interval))
                    elif 610 < mouse[0] < 700 and 305 < mouse[1] < 395:
                        oil_change_interval = 10000
                        with open('maintenance/interval.txt', 'w') as interval_file:
                            interval_file.write(str(oil_change_interval))
                    elif 760 < mouse[0] < 850 and 305 < mouse[1] < 395:
                        oil_change_interval = 15000
                        with open('maintenance/interval.txt', 'w') as interval_file:
                            interval_file.write(str(oil_change_interval))
                elif current_maintenance == 2 and current_page == 4:
                    if 295 < mouse[0] < 385 and 305 < mouse[1] < 395:
                        transmission_oil_change_interval = transmission_oil_change_interval - 500
                        with open('maintenance/transmission_interval.txt', 'w') as interval_file:
                            interval_file.write(str(transmission_oil_change_interval))
                    elif 645 < mouse[0] < 735 and 305 < mouse[1] < 395:
                        transmission_oil_change_interval = transmission_oil_change_interval + 500
                        with open('maintenance/transmission_interval.txt', 'w') as interval_file:
                            interval_file.write(str(transmission_oil_change_interval))
                elif current_maintenance == 3 and current_page == 4:
                    if 295 < mouse[0] < 385 and 305 < mouse[1] < 395:
                        brake_change_interval = brake_change_interval - 500
                        with open('maintenance/brake_interval.txt', 'w') as interval_file:
                            interval_file.write(str(brake_change_interval))
                    elif 645 < mouse[0] < 735 and 305 < mouse[1] < 395:
                        brake_change_interval = brake_change_interval + 500
                        with open('maintenance/brake_interval.txt', 'w') as interval_file:
                            interval_file.write(str(brake_change_interval))
                elif current_page == 7:
                    if 235 < mouse[0] < 325 and 245 < mouse[1] < 335:
                        current_color = 1
                        with open('backgrounds/current_background.txt', 'w') as background_file:
                            background_file.write(str(current_color))
                    elif 385 < mouse[0] < 475 and 245 < mouse[1] < 335:
                        current_color = 2
                        with open('backgrounds/current_background.txt', 'w') as background_file:
                            background_file.write(str(current_color))
                    elif 535 < mouse[0] < 625 and 245 < mouse[1] < 335:
                        current_color = 3
                        with open('backgrounds/current_background.txt', 'w') as background_file:
                            background_file.write(str(current_color))
                    elif 685 < mouse[0] < 775 and 245 < mouse[1] < 335:
                        current_color = 4
                        with open('backgrounds/current_background.txt', 'w') as background_file:
                            background_file.write(str(current_color))
                    elif 310 < mouse[0] < 400 and 365 < mouse[1] < 455:
                        current_color = 5
                        with open('backgrounds/current_background.txt', 'w') as background_file:
                            background_file.write(str(current_color))
                    elif 460 < mouse[0] < 550 and 365 < mouse[1] < 455:
                        current_color = 6
                        with open('backgrounds/current_background.txt', 'w') as background_file:
                            background_file.write(str(current_color))
                    elif 610 < mouse[0] < 700 and 365 < mouse[1] < 455:
                        current_color = 7
                        with open('backgrounds/current_background.txt', 'w') as background_file:
                            background_file.write(str(current_color))

        # Mileage/Oil Change Interval Functions

        oil_change_count = maintenance_counter(oil_mileage, oil_change_interval)
        transmission_oil_change_count = maintenance_counter(transmission_oil_mileage, transmission_oil_change_interval)
        brake_change_count = maintenance_counter(brake_mileage, brake_change_interval)

        convert_oil_mileage = str(oil_mileage)
        convert_trans_oil_mileage = str(transmission_oil_mileage)
        convert_brake_mileage = str(brake_mileage)

        with open('maintenance/mileage.txt', 'w') as mileage_file:
            mileage_file.write(convert_oil_mileage)

        with open('maintenance/transmission_mileage.txt', 'w') as mileage_file:
            mileage_file.write(convert_trans_oil_mileage)

        with open('maintenance/brake_mileage.txt', 'w') as mileage_file:
            mileage_file.write(convert_brake_mileage)

        # Redraw UI
        RedrawWindow()

        # instant mpg value updation left 
        if speed_value < 1:
            inst_mpg = mqtt_data
        elif speed_value >= 1 and maf_reading > 0.5:
            if ((710.7 + speed_value) / maf_reading) > 100:
                inst_mpg = 99
            else:
                inst_mpg = round((710.7 + speed_value) / maf_reading)
        else:
            inst_mpg = 0

        # Where mileage should increment
        if trip_distance > prev_trip_distance + 1:
            oil_mileage = oil_mileage + 1
            transmission_oil_mileage = transmission_oil_mileage + 1
            brake_mileage = brake_mileage + 1
            prev_trip_distance = trip_distance

        # dtc boolean handling
        if dtc_code:
            dtc_code_present = True
        else:
            dtc_code_present = False