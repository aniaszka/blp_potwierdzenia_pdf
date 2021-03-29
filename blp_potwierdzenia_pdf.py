import os
from datetime import datetime, timedelta
import time
import csv
import moving_files
import listOfAccounts
import konfiguracja
import glob

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys



def potwierdzenia_wczoraj():
    ## TODO przenieść na początek zapytanie o datę

    data_w_blp = input('Podaj datę w nazwie plików excel w formacie dd-mm-rrrr'
                       'czyli np.: 31-07-2020\n>>>>')
    # data_w_blp = data - timedelta(days=2)
    # data_w_blp = data_w_blp.strftime("%d-%m-%Y")
    data_w_nazwie_plikow_excel = data_w_blp[6:] + '-' + data_w_blp[3:5] + '-' + data_w_blp[0:2]

    opts = Options()
    opts.headless = True
    assert opts.headless  # Operating in headless mode

    # pobieram scieżki
    filename = 'blp_settings.ini'
    path_source, path_destination, path_chrome_driver = \
        konfiguracja.konfiguracja(
        filename)

    # get the path of ChromeDriverServer
    # odpowiedni chromedriver pobrany z https://chromedriver.chromium.org/downloads
    ## TODO często trzeba aktualizowach poniższy dodatek. Zrobić do tego ścieżkę w pliku settings.
    # pat_chrome_driver = r'C:\Users\aszadkowska\Documents\dodatki\chromedriver_win32_2020_12'
    chrome_driver_path = path_chrome_driver + "\chromedriver.exe"

    # create a new Chrome session
    driver = webdriver.Chrome(chrome_driver_path, options=opts)



    # funkcja która naprawia błąd z pobraniem potwierdzeń w tle.

    def enable_download_headless(browser,download_dir):
        browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        browser.execute("send_command", params)

    # ustawiam czas czekania na poprawne załadowanie strony
    # to lepsze niż time.sleep
    driver.implicitly_wait(30)
    # driver.maximize_window()

    # Navigate to the application home page
    url = 'http://www.podatki.gov.pl/wykaz-podatnikow-vat-wyszukiwarka/'
    driver.get(url)

    # ustalam miejsce zapisywania pobranych plików
    enable_download_headless(driver, path_source)

    # ustalam czas czekania na załadowanie poszczególnych elementów
    delay = 5  # seconds

    # Zepewnienie, że strona jest załadowana
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'inputType')))
        print("Main page is loaded!")
    except TimeoutException:
        print("Loading took too much time!")

    # pobieram bieżącą datę i tworzę folder z datą w nazwie
    data = datetime.now()

    parent_dir = '\\\\plrudfps01\\data\\Rudniki\\archiwizacja_faktur\\BLP_REPORTS\\screenshots\\'
    directory = 'BLP_screenshots_' + data.strftime("%Y-%m-%d_%H%M") +'\\'
    folder = os.path.join(parent_dir, directory)
    os.mkdir(folder)
    print(folder)




    # print(data_w_nazwie_plikow_excel)
    lista_rachunkow = listOfAccounts.make_list_of_accounts(data.strftime(data_w_nazwie_plikow_excel))

    # print(lista_rachunkow)
    if not lista_rachunkow:
        print('Nie ma plików excel z wczorajszą datą. Nie pobieram potwieredzeń.')
    else:
        # print(lista_rachunkow)
        print('I am on the proper page ready for searching.')

        # dla każdego rachunku poprzez pętle pobiorę zaświadczenie
        licznik = 0
        weryfikacja = {}
        list_of_id = []
        for rach in lista_rachunkow:
            licznik += 1
            print(f'Sprawdzam: {licznik} na {len(lista_rachunkow)}')
            search_field = driver.find_element_by_name("inputType")
            rachunek = (rach[:2] + ' ' + rach[2:6] + ' ' +
                        rach[6:10] + ' ' + rach[10:14] + ' ' +
                        rach[14:18] + ' ' + rach[18:22] + ' ' + rach[22:])
            print(rachunek)
            # enter search keyword and submit

            try:
                # zapewnienie, że okienko do wpisania rachunku jest aktywne
                try:
                    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'inputType')))
                    print("Okienko do wpisania rachunku jest załadowane!")
                except TimeoutException:
                    print("Nie mogę załadować okienka do wpisania rachunku!")

                search_field.send_keys(rachunek)
                time.sleep(1)

                # zapewnienie, że opcja zmiany daty jest aktywna
                try:
                    myCheck = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located((By.XPATH, "//div/div/label[@for='vertical-checkbox2']")))
                    print("checkbox do zmiany daty aktywny")
                except TimeoutException:
                    print("checkbox nie działa wciąż!")

                date_change_box = driver.find_element_by_xpath("//div/div/label[@for='vertical-checkbox2']")
                date_change_box.click()

                # zapewnienie, że okienko do wpisania nowej daty jest aktywne
                try:
                    myDateBoxCheck = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located((By.NAME, "inputType3")))
                    print("okienko do wpisania nowej daty aktywne")
                except TimeoutException:
                    print("okienko do wpisania nowej daty nie działa wciąż!")

                time.sleep(1)
                date_enter_field = driver.find_element_by_name("inputType3")
                date_enter_field.send_keys(Keys.CONTROL, 'a')
                date_enter_field.send_keys(Keys.BACKSPACE)
                time.sleep(1)
                date_enter_field.send_keys(data_w_blp)

                search_field.submit()
                time.sleep(3)

                # sprawdzam czy strona dla danego rachunku jest załadowana

                try:
                    myPrintButton = WebDriverWait(driver, delay).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                    print("Page is ready for confirmation download!")
                except TimeoutException:
                    print("Strona z potwierdzeniem nie jest gotowya!")

                content = driver.find_element_by_xpath("//div[@class='searchFooterAK toLeftBox']")
                print(content)
                id_wyszukiwania = content.text[28:]
                print(content.text)
                x = rach + '_' + id_wyszukiwania
                print(x)
                weryfikacja[rach] = id_wyszukiwania
                list_of_id.append(id_wyszukiwania)

                # zapewnienie, że PrintButton jest widzilany
                try:
                    myPringButtonCheck = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located((By.ID, "superPrintButton")))
                    print("PrintButton jest gotowy")
                except TimeoutException:
                    print("PrintButton nie działa wciąż!")

                # powyższe nie wystarcza, więc trzeba sprawdzic, czy jest klikalny

                try:
                    botton_to_click = WebDriverWait(driver, delay).until(
                        EC.element_to_be_clickable((By.ID, "superPrintButton")))
                    print("PrintButton jest klikalny")
                except TimeoutException:
                    print("PrintButton nie jest klikalny!")

                botton_to_click.click()
                time.sleep(2)
                print('klikam print\n')
                time.sleep(2)

                # odświeżęnie strony
                driver.get(url)
                time.sleep(2)

            # dodałam ten blok wyjątków, żeby jeden trefny rachunek nie spieprzył całego programu
            except Exception as e:
                print(e)
                print(f'Pobranie potwierdzenia dla {rachunek} nie powiodło się.\n')
                driver.get(url)
                time.sleep(2)


        # close the browser window
        driver.quit()

        print('\nlista id\n')
        print(list_of_id)

        print('\nlista par\n')
        print(weryfikacja)

        # tworzę plik csv zawierający pary: rachunek i id zapytania
        # plik jest zapisany w folderze do ktorego przeniesione będą pliki pdf
        print(folder)
        txt_file = folder + "weryfikacja.csv"

        w = csv.writer(open(txt_file, "w", newline=''))

        for key, val in weryfikacja.items():
            w.writerow([key, val])


        # przenoszę pliki w miejsce docelowe
        path_destination = folder
        moving_files.moving_files(weryfikacja, path_source, path_destination)

        os.chdir(path_destination)

        lista_po_przeniesieniu = glob.glob('*.pdf')
        lista_rachunkow_z_potierdzeniem = []
        for r in lista_po_przeniesieniu:
            lista_rachunkow_z_potierdzeniem.append(r[:26])

        brakuje = list(set(lista_rachunkow) - set(lista_rachunkow_z_potierdzeniem))

        with open('brakuje.txt', 'w') as raport:
            for i in brakuje:
                raport.writelines(i+'\n')

        # komunikat o zakończeniu procesu
        print('Dziś to na tyle.')

if __name__ == "__main__":
    potwierdzenia_wczoraj()
