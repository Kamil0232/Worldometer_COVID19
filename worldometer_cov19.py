import requests
from bs4 import BeautifulSoup

#funkcja find_country() pobiera dane z Worldometers, odpowiednio konwertuje liczby na float (pozbywa się obecnego na stronie przecinka)
#i zwraca listę w postaci ['Kraj', Liczba zachorowań, Liczba zmarłych, Liczba wyzdrowiałych, Liczba aktualnie chorych] dla danego kraju, w momencie wykonywania skryptu.
#Konieczne są pakiety bs4 oraz requests, inaczej dane z html nie pobiorą się w odpowiedni sposób


def find_country(country):
    #parsowanie źródła strony z html
    finding = []
    website = requests.get("https://www.worldometers.info/coronavirus/")
    soup = BeautifulSoup(website.text, 'html.parser')
    table = soup.find("table", attrs={"id": "main_table_countries_today"})
    find_verses = table.find_all("tr")
    lista = []
    for x in find_verses:
        lista.append(str(x))


    #pobieranie danych kraju i wrzucanie ich do listy final
    elements = ['Kraj:', 'Liczba zachorowań:', 'Liczba zmarłych:', 'Liczba wyzdrowiałych:', 'Liczba aktualnie chorych:', 'Liczba testów:']
    matching = [s for s in lista if country in s] #szukanie odpowiedniego kraju
    matching = str(matching[0])
    finding.append(matching)
    if len(finding) != 0:
        f = finding[0]
        soup2 = BeautifulSoup(f, 'html.parser')
        proba2 = soup2.find_all("td")
        country = proba2[0].next_element.next_element
        total_cases = proba2[1].next_element.replace(" ", "")
        total_deaths = proba2[3].next_element.replace(" ", "")
        total_recovered = proba2[5].next_element.replace(" ", "")
        active_cases = proba2[6].next_element.replace(" ", "")
        total_tests = proba2[10].next_element.replace(" ", "")
        if proba2[0].next_element == " ":
            country = proba2[0].next_element.next_element.next_element
        final = [country, total_cases, total_deaths, total_recovered, active_cases, total_tests]

        for checking_empty in range(len(final)):
            if final[checking_empty] == "":
                final[checking_empty] = '0' #zerowanie pustych elementów dla danego kraju (np. gdy nie ma żadnych wyzdrowiałych)

        total_cases = int(final[1].replace(",", ""))
        total_deaths = int(final[2].replace(",", ""))
        total_recovered = int(final[3].replace(",", ""))
        active_cases = int(final[4].replace(",", ""))
        total_tests = int(final[5].replace(",", ""))

        final = [country, total_cases, total_deaths, total_recovered, active_cases, total_tests]

        for element in range(len(elements)):
            print('{} {}'.format(elements[element], final[element]))


        return final

find_country('Germany')






