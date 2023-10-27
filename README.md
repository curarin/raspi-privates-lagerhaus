# raspi-privates-lagerhaus
Dashboard for inventory of own food warehouse.

## Why?
Our home has a cellar where we store longer-lasting food. When I stand in the kitchen and cook, it can happen that the flour has run out. So that I don't have to go to the cellar "on the off chance" to check whether there is still flour in stock, I would like to check the stock level in a web app on my cell phone.

This way I can see at a glance whether it's worth going to the cellar.

## How?
Food products have a barcode. As soon as we buy longer-lasting food, the packaging is scanned using a Raspberry Pi-powered barcode scanner. Subsequently, product information is obtained via an API, which in turn is pushed to Google BigQuery.

The Streamlit Web App then pulls current inventory information from Google BigQuery and displays it to me.

## Modules
Using this:
- https://pypi.org/project/waveshare-epaper/
