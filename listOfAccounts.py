import glob
import pandas as pd


# data = '2020-01-17' # tylko do testów. w pliku blp_wydruk stosowana jest data today lub yesterday
def make_list_of_accounts(data):
    """pobiera listę rachunków z raportów excel z danego dnia"""
    path = '\\\\plrudfps01\\data\\Rudniki\\archiwizacja_faktur\\BLP_REPORTS\\EXCEL_Reports\\'
    pliki_blp = glob.glob(path + 'BLP_' + data + '*.xlsx')
    print(pliki_blp)
    ile_blp = len(pliki_blp)
    print(f'liczba plików z rachunkami: {ile_blp}.')
    if ile_blp > 0:
        tabela = pd.concat(map(lambda file: pd.read_excel(file, usecols=['rachunek','Czy odszukał po rachunku?'], dtype = str), pliki_blp))

        # print(tabela)
        tabela = tabela[tabela['Czy odszukał po rachunku?']=='True']
        tabela = tabela.drop_duplicates()
        tabela = tabela.reset_index()
        # print(tabela)
        rach = tabela['rachunek']
        # print(type(rach))
        lista_rach = rach.tolist()
        return lista_rach

    else:
        lista_rach = []
        return lista_rach