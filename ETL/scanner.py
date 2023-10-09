from google.cloud import bigquery
from google.oauth2 import service_account
import numpy as np
import csv
import os
import keyboard
import pandas as pd
import epaper
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from signal import pause
import requests
from datetime import date
import time

##### DRIVERS AND INITIALIZING DISPLAY########
epd = epaper.epaper("epd2in7").EPD() # get the display
epd.init()           # initialize the display
print("Clearing display...")    # prints to console, not the display, for debugging
epd.Clear(0xFF)      # clear the display
#######
### DEFINING BUTTONS
key1 = Button(5)
key2 = Button(6)
key3 = Button(13)
key4 = Button(19)

##### defining variables
barcode_data = ""
restart_requested = False
value = 1
today_date = date.today().strftime("%Y-%m-%d")
font = ImageFont.truetype("path/to/fonts", 25)
font_data = ImageFont.truetype("path/to/fonts", 15)
hourglass = """
          +===+
          |  (::)  |
          |   )(   |
          |  (..)  |
          +===+
"""
### API VARIABLES
### EAN Data
key = "api-key-for-ean-codes-here"

# Google Bigquery variables
project_id = "project-id-here"
dataset_id = "data-set-id-here"
table_id = "table-id-here"

credentials_data = {
	"type": "service_account",
	"project_id": "project-id-here",
	"private_key_id": "private-key-id-here",
	"private_key": "private-key-here",
	"client_email": "client-mail-here",
	"client_id": "client-id-here",
	"auth_uri": "https://accounts.google.com/o/oauth2/auth",
	"token_uri": "https://oauth2.googleapis.com/token",
	"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
	"client_x509_cert_url": "email-here",
	"universe_domain": "googleapis.com"
	}

credentials = service_account.Credentials.from_service_account_info(credentials_data)
client = bigquery.Client(project=project_id, credentials=credentials)
schema = [
	bigquery.SchemaField("barcode", "STRING"),
	bigquery.SchemaField("brand", "STRING"),
	bigquery.SchemaField("quantity", "STRING"),
	bigquery.SchemaField("name", "STRING"),
	bigquery.SchemaField("category", "STRING"),
	bigquery.SchemaField("amount", "INTEGER"),
	bigquery.SchemaField("date", "DATE")
        ]
table_ref = client.dataset(dataset_id).table(table_id)


#########
### DEFINING FUNCTIONS
## for button action ###
def save_to_local_file():
	global barcode_data, value
	print(barcode_data, value)
	if barcode_data:
		csv_file = "barcode.csv"
		file_exists = os.path.isfile(csv_file)
		with open(csv_file, "a", newline="") as file:
			fieldnames = ["barcode", "value"]
			writer = csv.DictWriter(file, fieldnames=fieldnames)
			if not file_exists:
				writer.writeheader()
			writer.writerow({"barcode": barcode_data, "value": value})

	print("Saved to local file...")
	value_str = str(value)
	final_scan(barcode_data, value_str)
	key1.when_pressed = button_a_callback
	key2.when_pressed = push_to_gbq
	value = 1


def push_to_gbq():
	global barcode_data, value
	data_list = []
	with open("barcode.csv", mode="r") as file:
		csv_reader = csv.reader(file)
		next(csv_reader)
		print(csv_reader)
		for row in csv_reader:
			barcode = row[0]
			category = ""
			amount = row[1]
			api_url = f"https://api.upcdatabase.org/product/{barcode}?apikey={key}"
			response = requests.get(api_url)
			if response.status_code == 200:
				try:
					response_json = response.json()
					brand = response_json.get("brand", "")
					quantity = response_json.get("metadata", {}).get("quantity", "")
					name = response_json.get("title", "")
					#append to list
					data_list.append({"barcode": barcode, "brand": brand, "quantity": quantity, "name": name, "category": category, "amount": amount, "date": today_date})

				except (ValueError, AttributeError) as e:
					print(f"Error for barcode: {barcode}. Error: {e}")
					data_list.append({"barcode": barcode, "brand": "", "quantity": "", "name": "", "category": "", "amount": amount, "date": today_date})
			else:
				print(f"API request failed for barcode: {barcode}")
	columns = ["barcode", "brand", "quantity", "name", "category", "amount", "date"]
	df_ean_api = pd.DataFrame(data_list, columns=columns)
	print(df_ean_api)
	errors = client.insert_rows_json(table_ref, data_list)
	if not errors:
		print("Pushed to Google Big Query")
		os.remove("barcode.csv")
	else:
		print(f"Errors encountered while inserting data: {errors}")

	print("barcode.csv successfully removed")
	home_screen(hourglass)
	key1.when_pressed = button_a_callback
	key2.when_pressed = button_b_callback


def button_pressed_while_scanning(button):
	global value
	if button == key1:
		value += 1
	elif button == key2:
		value -= 1
	elif button == key3:
		value += 10
	scan_new_items(barcode_data, value)
	return barcode_data, value


#### GENERIC BUTTON FUNCTIONS
def button_a_callback():
	global barcode_data
	value = 1
	barcode_data = scan()
	scan_new_items(barcode_data, value)
	key1.when_pressed = button_pressed_while_scanning
	key2.when_pressed = button_pressed_while_scanning
	key3.when_pressed = button_pressed_while_scanning
	key4.when_pressed = save_to_local_file


def button_b_callback():
	print("Button 2", barcode_data)

def button_c_callback():
	print("Button 3", barcode_data)

def button_d_callback():
	print("Button 4", barcode_data)

####### FUNCTIONS #######
def scan():
	barcode_data = ""
	listen = True
	try:
		print("Listening for barcode scanner input...")
		while True:
			event = keyboard.read_event()
			if event.event_type == keyboard.KEY_DOWN:
				if event.name == "enter":
					if barcode_data:
                        # Print and reset the barcode data when the "Enter" key is pressed
						print(f"Barcode data: {barcode_data}")
						return barcode_data
					barcode_data = ""
				else:
					barcode_data += event.name  # Append the keypress to the barcode data
	except KeyboardInterrupt:
		print("Barcode scanner input listening stopped.")
	finally:
		listen = False

def home_screen(barcode_data):
	HImage = Image.new("1", (epd.height, epd.width), 255)
	draw = ImageDraw.Draw(HImage)

	#draw lines
	draw.line([(0,40),(255,40)], fill = 0, width = 1)
	draw.line([(0,85),(130,85)], fill = 0, width = 1)
#	draw.line([(0,130),(130,130)], fill = 0, width = 1)
	draw.line([(130,40),(265,40)], fill = 0, width = 3)
	draw.line([(130,0),(130,255)], fill = 0, width = 3)

	#Text
	draw.text((5, 5), "    Scan", font = font, fill = 0)
	draw.text((5, 50), "    Delete", font = font, fill = 0)

	draw.text((140, 5), "Barcode", font = font, fill = 0)
	draw.text((140, 50), barcode_data, font = font_data, fill = 0)

	#push to display
	epd.display(epd.getbuffer(HImage))
	time.sleep(2)

def final_scan(barcode_data, value):
	HImage = Image.new("1", (epd.height, epd.width), 255)
	draw = ImageDraw.Draw(HImage)

        #draw lines
	draw.line([(0,40),(255,40)], fill = 0, width = 1)
	draw.line([(0,85),(130,85)], fill = 0, width = 1)
	draw.line([(130,40),(265,40)], fill = 0, width = 3)
	draw.line([(130,0),(130,255)], fill = 0, width = 3)

        #Text
	draw.text((5, 5), "New Scan", font = font, fill = 0)
	draw.text((5, 50), "Finalize", font = font, fill = 0)
	draw.text((140, 5), "Barcode", font = font, fill = 0)
	draw.text((140, 50), "Last Scan:", font = font, fill = 0)
	draw.text((140, 80), barcode_data, font = font_data, fill = 0)
	draw.text((140, 100), "Amount:", font = font, fill = 0)
	draw.text((140, 130), value, font = font, fill = 0)

        #push to display
	epd.display(epd.getbuffer(HImage))
	time.sleep(2)

def scan_new_items(barcode_data, counter):
	HImage = Image.new("1", (epd.height, epd.width), 255)
	draw = ImageDraw.Draw(HImage)

        #draw lines
	draw.line([(0,40),(255,40)], fill = 0, width = 1)
	draw.line([(0,85),(130,85)], fill = 0, width = 1)
	draw.line([(0,130),(130,130)], fill = 0, width = 1)
	draw.line([(130,40),(265,40)], fill = 0, width = 3)
	draw.line([(130,0),(130,255)], fill = 0, width = 3)
        #Text
	draw.text((5, 5), "       +1", font = font, fill = 0)
	draw.text((5, 50), "        -1", font = font, fill = 0)
	draw.text((5, 95), "        +10 ", font = font, fill = 0) 
	draw.text((5, 140), "        OK", font = font, fill = 0)

	draw.text((140, 5), "Barcode", font = font, fill = 0)
	draw.text((140, 50), barcode_data, font = font_data, fill = 0)
	draw.text((140, 95), f"Counter: {counter}", font = font_data, fill = 0)
        #push to display
	epd.display(epd.getbuffer(HImage))
	time.sleep(2)

############################

home_screen(hourglass)
key1.when_pressed = button_a_callback
key2.when_pressed = button_b_callback
key3.when_pressed = button_c_callback
key4.when_pressed = button_d_callback

pause()
