

import requests
from bs4 import BeautifulSoup
from numpy.core import long
#from RPLCD import CharLCD
#import RPi.GPIO as GPIO
from time import *
import datetime

'''GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23], numbering_mode=GPIO.BOARD)
lcd.clear()
lcd.cursor_pos = (0, 0)
lcd.write_string(u'Chorzy:')
lcd.cursor_pos = (1, 0)
lcd.write_string(u'Zmarli:')
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)'''


def find_country(country, finding, lista, elements, lista_do_rpi):
    matching = [s for s in lista if country in s]
    matching = str(matching[0])
    finding.append(matching)
    if len(finding) != 0:
        f = finding[0]
        soup2 = BeautifulSoup(f, 'html.parser')
        proba2 = soup2.find_all("td")
        country = proba2[0].next_element
        total_cases = proba2[1].next_element.replace(" ", "")
        total_deaths = proba2[3].next_element.replace(" ", "")
        total_recovered = proba2[5].next_element.replace(" ", "")
        active_cases = proba2[6].next_element.replace(" ", "")
        if proba2[0].next_element == " ":
            country = proba2[0].next_element.next_element.next_element
        final = [country, total_cases, total_deaths, total_recovered, active_cases]

        for checking_empty in range(len(final)):
            if final[checking_empty] == "":
                final[checking_empty] = '0'

        total_cases = float(final[1].replace(",", "."))
        total_deaths = float(final[2].replace(",", "."))
        total_recovered = float(final[3].replace(",", "."))
        active_cases = float(final[4].replace(",", "."))

        final = [country, total_cases, total_deaths, total_recovered, active_cases]
        for element in range(len(elements)):
            print('{} {}'.format(elements[element], final[element]))
        lista_do_rpi[0] = final[1]
        lista_do_rpi[1] = final[2]
        lista_do_rpi[2] = final[3]
        lista_do_rpi[3] = final[4]
        return lista_do_rpi

porownanie_chorych = []
porownanie_chorych.append(0)
while(1):

    website = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(website.text, 'html.parser')
    table = soup.find("table", attrs={"id": "main_table_countries_today"})

    find_verses = table.find_all("tr")

    elements_ar = ['Kraj:', 'Liczba zachorowań:', 'Liczba zmarłych:', 'Liczba wyzdrowiałych:', 'Liczba chorych:']
    lista_do_rpi_ar = []
    for wydruk in range(1, 5):
        lista_do_rpi_ar.append(0)

    lista_ar = []
    for x in find_verses:
        lista_ar.append(str(x))

    finding_ar = []

    odczyt = find_country('USA', finding_ar, lista_ar, elements_ar, lista_do_rpi_ar)
    if odczyt[0] > porownanie_chorych[0]:
        #GPIO.output(21, GPIO.HIGH)
        #sleep(0.5)
        #GPIO.output(21, GPIO.LOW)
        porownanie_chorych[0] = odczyt[0]
        print('UWAGA - Zmiana')
        #lcd.cursor_pos = (0, 8)
        #lcd.write_string(u'{}'.format(odczyt[0]))
        #lcd.cursor_pos = (1, 8)
        #lcd.write_string(u'{}'.format(odczyt[1]))
    #n = n + 1
    #lcd.cursor_pos = (1, 14)
    #lcd.write_string(u'{}'.format(n))
    print(datetime.datetime.now())
    sleep(60)