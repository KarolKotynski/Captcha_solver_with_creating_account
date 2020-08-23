import json
from time import time

import cv2
import numpy as np
import selenium

from create import CreateAccount


def resize(img):
    height, width = (img.shape[0], img.shape[1])
    img = cv2.resize(img, (width * 4, height * 4))
    return img

def process_image(original_img):
    img_gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    img_canny = cv2.Canny(img_blur, 10, 150)
    kernel = np.ones((2, 2))
    img_dilation = cv2.dilate(img_canny, kernel, iterations=2)
    img_threshold = cv2.erode(img_dilation, kernel, iterations=2)
    #img_contour = original_img.copy()
    return img_threshold

def get_contours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    pelimeter_list = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:
            pelimeter = cv2.arcLength(contour, True)
            #cv2.drawContours(img_contour, contour, -1, (255, 0, 0), 2)
            intersection_points = cv2.approxPolyDP(contour, pelimeter, True)
            amount_points = len(intersection_points)
            #print(f'Amount of points: {amount_points} coords_points: {intersection_points} \npelimeter: {pelimeter}')
            pelimeter_list.append(pelimeter)
    return pelimeter_list

def compare_pelimeter(pelimeter_contours):
    solution = 'None'
    letters_list = []
    occurence_list = []
    for each in data:
        get_length = len((set(pelimeter_contours) & set(each['pelimeter'])))
        if get_length != 0:
            letters_list.append(str(each['letter']))
            occurence_list.append(get_length)
    most_occur = occurence_list.index(max(occurence_list))
    return letters_list[most_occur]

def find_solution(number_of_char):
    #global img_contour
    img = cv2.imread(f'0000_{number_of_char}.png')
    img = resize(img)
    #img_contour = img.copy()
    img_threshold = process_image(img)
    pelimeter_contours = get_contours(img_threshold)
    letter = compare_pelimeter(pelimeter_contours)
    return letter

def main():
    how_many_accounts = int(input('Write down how many accounts to create: '))
    time_start = time()
    a = CreateAccount()
    for _ in range(how_many_accounts):
        try:
            a.fill_the_form()
            a.grab_captcha_image()
            a.slice_image()
            numbers = (0, 1, 2, 3, 4, 5)
            letters = list(map(find_solution, numbers))
            solved_captcha = ''.join(str(each) for each in letters)
            a.browser.find_element_by_id('captcha').send_keys(solved_captcha)
        except:
            pass

        a.browser.find_element_by_id('submit').click()

    time_stop = time()
    print(f'{how_many_accounts} accounts created in: {time_stop - time_start} seconds')

if __name__ == '__main__':
    with open('letter_pelimeter.json') as json_file:
        data = json.load(json_file)
    main()
