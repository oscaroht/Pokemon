import urllib
from selenium import webdriver
import requests
from sqlalchemy import create_engine
import os
from configparser import ConfigParser

def config(filename, section, item = 'all'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    if item == 'all':
        return db
    else:
        return db[item]

os.chdir(os.path.dirname(os.path.realpath(__file__)))
engine = create_engine(
    f"postgresql+psycopg2://postgres:{config('../users.ini', 'postgres', 'password')}@localhost/pokemon")

with engine.connect() as con:
    pokemon_dict = {}
    temp = {}
    for row in con.execute(f"select * from mappings.pokemon;"):
        # get all the atributes in a dict instead of a tuple
        temp = dict((key, value) for key, value in row._mapping.items())
        # create 2 keys on pokemon_id and on pokemon_name
        # pokemon_dict[row['pokemon_id']] = temp
        pokemon_dict[row['pokemon_name']] = temp

driver = webdriver.Chrome()
for p, value in pokemon_dict.items():
    name = value['pokemon_name']
    if name in ['nidoran_f', 'nidoran_m', "farfetch'd"]:
        continue
    url = name.title().replace(' ', '_')+'_(Pok%C3%A9mon)'


    driver.get(f'https://bulbapedia.bulbagarden.net/wiki/{url}')
    # get the image source

    xp = '//*[@id="mw-content-text"]/div/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/a/img'

    img = driver.find_element_by_xpath(xp)
    src = img.get_attribute('src')

    r = requests.get(src)
    with open(f'pics\\{name}.png', 'wb') as file:
        file.write(r.content)


