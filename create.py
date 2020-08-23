from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
import random
import string
from PIL import ImageGrab, Image
from win32api import GetSystemMetrics
import time
import os

class CreateAccount:

    browser = ''
    screen_coords = ()
    image_directory = os.path.dirname(__file__)
    def __init__(self):
        my_url = 'http://dblots.org.pl/new.php?lang=en&s=classic'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.maximize_window()
        browser.get(my_url)
        browser.find_element_by_id('submit').click()
        CreateAccount.browser = browser

    def fill_the_form(self):
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        my_password = 'qwerty12345'
        self.browser.find_element_by_id('password').send_keys(my_password)
        self.browser.find_element_by_id('confirm').send_keys(my_password)
        random_email = ''.join(random.choice(string.ascii_letters) for i in range(10))
        self.browser.find_element_by_id('email').send_keys(Keys.CONTROL + "a")
        self.browser.find_element_by_id('email').send_keys(f'{random_email}@gmail.com')
        self.browser.find_element_by_id('rules').click()

    def grab_captcha_image(self):
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        # get the x and y of captcha image
        # width 252 to round to whole numbers per letter
        captcha_x_pos = self.browser.find_element_by_id('captcha-image').location.get('x')
        captcha_y_pos = GetSystemMetrics(1)

        bbox = (captcha_x_pos,
                captcha_y_pos - 422,
                captcha_x_pos + 252,
                captcha_y_pos - 382)
        image_captcha = ImageGrab.grab(bbox = bbox)

        image_captcha.save(f'{self.image_directory}/my_captcha.png')

        image_to_change = Image.open(f'{self.image_directory}/my_captcha.png')
        image_width, image_height = image_to_change.size
        image_each_pixel = image_to_change.load()

        for width in range(image_width):
            for height in range(image_height):
                if image_each_pixel[width, height] != (4, 103, 149):
                    image_each_pixel[width, height] = (0, 0, 0)
        
        image_to_change.save(f'{self.image_directory}/my_captcha_black.png')

        return image_to_change


    def slice_image(self):
        image_to_slice = Image.open(f'{self.image_directory}/my_captcha_black.png')
        for i in range(6):
            box = (i*42, 0, (i+1) * 42, 40)
            image_slice = image_to_slice.crop(box)
            image_slice.save(f'{self.image_directory}/0000_{i}.png')
