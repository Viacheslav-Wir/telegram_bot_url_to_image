import os
import time
from selenium import webdriver
from dotenv import load_dotenv


load_dotenv()
image_path = os.getenv("IMAGE_SAVE_PATH")


def show_file_names():
	files_names = [file for file in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, file))]

	return files_names


def collect_hiden_elements():
	default_hide_elements = os.getenv("DEFAULT_HIDE_ELEMENTS")
	hide_elements = default_hide_elements.split(',')

	return hide_elements


def url_to_filename(url):
	name = url.split('//')[1]
	length = len(name)
	if name[length - 1] == '/':
		name = name[:length - 1]

	file_name = '{}{}.png'.format(image_path, name.replace('/','-'))

	return file_name


def get_screenshot(url):
	# Gets the path to the right chromedriver
	path = "/usr/bin/chromedriver"

	options = webdriver.ChromeOptions()
	options.add_argument("--headless")
	options.add_argument('--ignore-certificate-errors')
	options.add_argument("--disable-extensions")
	options.add_argument("--disable-gpu")
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("--disable-popup-blocking")
	options.add_argument("--no-sandbox")

	options.add_experimental_option("excludeSwitches", ["enable-automation"])
	options.add_experimental_option('useAutomationExtension', False)

	# must install linux browser 'sudo apt-get install -y chromium-browser'
	options.binary_location = '/usr/bin/chromium-browser'

	with webdriver.Chrome(path, options=options) as driver:
		file_name = url_to_filename(url)
		driver.get(url)
		page_sizes = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
		driver.set_window_size(1920, page_sizes('Height'))

		driver.get(url)
		time.sleep(2)

		js_script = "{}.forEach(identifier => [...document.querySelectorAll(identifier)].forEach(ele => ele.style.display = 'none'));".format(collect_hiden_elements())
		driver.execute_script(js_script)

		maked_sreen = driver.save_screenshot(file_name)
		print('FIN', maked_sreen)
		return maked_sreen, file_name
