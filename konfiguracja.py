import configparser

filename = 'settings.ini'

def konfiguracja(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    # print(config.sections())
    # print(config.options('sciezki'))
    path_source = config.get('sciezki', 'path_source')
    path_destination = config.get('sciezki', 'path_destination')
    # print(path_source)
    # print(path_destination)
    return path_source, path_destination


