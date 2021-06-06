#####################################################
# keep script running, every time car is uploaded   #
# email will be sent.                               #
#####################################################

import requests #allows us to download html
from bs4 import BeautifulSoup #allows us to scrape html
import re
from emailcar import send_email
import time
from pytimedinput import timedInput #pip3 install pytimedinput

#Create file containing all desired cars
current_dc = ''
with open('dream_cars.txt', mode = 'r') as my_file:
    file_contents = my_file.read().splitlines()
    for content in file_contents:
        current_dc = current_dc + f' {content}\n'
    inp1 = input(f'The current cars you want are:\n {current_dc}' + '\n Would you like to add more (y/n/reset): ')
    response = inp1.lower()
    if response == 'y':
        with open('dream_cars.txt', mode = 'a') as my_file:
            while True:
                car = input('Enter a car you would like to look for. (If done type \'done\'): ')
                if car == 'done':
                    break
                else:
                    my_file.write(car + '\n')
    elif response == 'reset':
        with open('dream_cars.txt', mode = 'w') as my_file:
            while True:
                car = input('Enter a car you would like to look for. (If done type \'done\'): ')
                if car == 'done':
                    break
                else:
                    my_file.write(car + '\n')

dream_cars = []
with open('dream_cars.txt', mode = 'r') as my_file:
    file_contents = my_file.read().splitlines()
    for content in file_contents:
        dream_cars.append(content.lower())

receiving_email = input('Receiving Email: ')
senders_email = input('Sender\'s Email: ')
password = input('Password: ')

cars = []
def create_custom_CL(carinfo, receiving_email):
    for idx, item in enumerate(carinfo):
        name = item.getText().lower()
        href = item.get('href', None)
        carid = item.get('id')

        for car in dream_cars:
            #check if the craigslist ad is a desired car
            match = re.search(car, name)
            #if the vehicle does not already exist in the list, append
            if match: 
                duplicate = 0
                for x in cars:
                    if carid == x['id']:
                        duplicate += 1
                if not duplicate:
                    cardict = {'name':name,'link':href,'id':carid}
                    cars.append(cardict)
                    #every time a new car enters list, email sends.
                    send_email(receiving_email, cardict, senders_email, password)
    return

#scrape data of cars from craigslist

while True:
    res = requests.get('https://vancouver.craigslist.org/d/cars-trucks-by-owner/search/cto?auto_transmission=1')
    soup = BeautifulSoup(res.text, 'html.parser')
    carinfo = soup.select('.result-title')

    create_custom_CL(carinfo, receiving_email)
    #email sends approximately once an hour
    time.sleep(1800)

    ### Timed Input
        #if timedout, default the loop to continue
    answer, timedOut = timedInput(f'end? (y/n): ',timeOut = 60) #one minute to input a value
    if timedOut:
        answer = 'n'

    response = answer.lower()
    if response == 'y':
        break
    else:
        continue
