import configparser

filename = 'blp_settings.ini'


def konfiguracja(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    path_source = config.get('sciezki', 'path_source')
    path_destination = config.get('sciezki', 'path_destination')
    path_chrome_driver = config.get('sciezki', 'path_chrome_driver')

    return path_source, path_destination, path_chrome_driver
