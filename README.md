# telegram_bot_url_to_image

This bot makes a screenshot from the URL you enter.

## Install

### Install ChromeDriver
	
	wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip
	unzip chromedriver_linux64.zip

You may choose your variant https://sites.google.com/a/chromium.org/chromedriver/downloads

	sudo mv chromedriver /usr/bin/chromedriver
	sudo chown root:root /usr/bin/chromedriver
	sudo chmod +x /usr/bin/chromedriver

### Install ChromiumBrowser
	
	sudo apt-get install -y chromium-browser

## Create .env file

	TELEGRAM_BOT_TOKEN= # your telegram bot token
	DEVELOPER_CHAT_ID= # admin chat_id, to receive error messages
	IMAGE_SAVE_PATH=/home/path_to_project/telegram_bot_url_to_image/images/
	DEFAULT_HIDE_ELEMENTS= # css element identifier separated by divider "," for e.g.: div,jdiv,.cookie-consent,#alert-message

DEFAULT_HIDE_ELEMENTS - this element will hide on the screenshot

## Set up envirment

	virtualenv -p python3.7 --no-site-packages env_py37

	source env_py37/bin/activate
	pip install -r requirements.txt

## Run

### Local

	python3 conversation.py

### Server

Start Screen:
	screen -S mybot

Run:
	python3 conversation.py

Exit screen:
	Ctr + A + D

Reattach to screen:
	screen -r mybot