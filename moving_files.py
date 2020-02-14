import glob
import os
import shutil



# poniższe kody są tylko do testów
kody_zapytan = {'92873500070009427230000010': '4b48e-867j8mk',
                '56105000861000002293400848': 'bf2hk-867j8nb',
                '49219000023000004625800101': '2em41-867j8nn'}



def moving_files(kody_zapytan, path_source, path_destination):
    """funkcja do zmiany nazw pobranych potwierdzeń i do zapisania ich we właściwym miejscu"""

    # ściezki zapisuję w pliku konfiguracyjnym, żeby łatwiej było je modyfikować


    # lista plikow do przeniesienia

    os.chdir(path_source)
    pliki_pdf = glob.glob('potwierdzenie-' + '*.pdf')

    print(pliki_pdf)

    # namierzenie wlasciwych plikow
    for plik in pliki_pdf:
        for rachunek, kod in kody_zapytan.items():
            if kod in plik:
                source = plik
                print('do przeniesienia:\n', source)
                plik = plik.replace('potwierdzenie', rachunek)
                print('zmieniona nazwa', plik)
                destination = path_destination + plik
                print('po przeniesieniu\n', destination)
                shutil.move(source, destination)

