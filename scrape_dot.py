from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER, logging
import json
import re
import sys
LOGGER.setLevel(logging.WARNING)


edge_options = Options()
edge_options.use_chromium = True
edge_options.add_argument('headless')
edge_options.add_argument('disable-gpu')
driver = webdriver.Edge(executable_path='./msedgedriver', options=edge_options)

spell_array=[]

sp_name='//*[@id="skrollr-body"]/div[3]/div[1]/main/div/div/div/div/div[1]/span'
sp_source='//*[@id="page-content"]/p[1]'
sp_lvl='//*[@id="page-content"]/p[2]/em'
sp_crcd='//*[@id="page-content"]/p[3]'
sp_desc='//*[@id="page-content"]/p[4]'

cl=sys.argv[1]

driver.get('http://dnd5e.wikidot.com/spells:'+cl)
el=driver.find_elements(By.XPATH,'//a[@href]')
spells=[elem.get_attribute('href') for elem in el if elem.get_attribute('href').find('spell:')!=-1]


for spell in spells:
    spell_obj={}
    driver.get(spell)
    if (len(driver.find_elements(By.XPATH,sp_name)[0].text.split("("))==1):
        spell_obj['class']=cl
        spell_obj['name']=driver.find_elements(By.XPATH,sp_name)[0].text.split("(")[0].strip()
        spell_obj['source']=driver.find_elements(By.XPATH,sp_source)[0].text.split(":")[1].strip()
        spell_obj['level']=int((re.split("nd|st|rd|th",driver.find_elements(By.XPATH,sp_lvl)[0].text)[0],0)[driver.find_elements(By.XPATH,sp_lvl)[0].text.find("cantrip")!=-1])
        spell_obj['casting'],spell_obj['range'],spell_obj['components'],spell_obj['duration']=[s.split(":")[1].strip() for s in driver.find_elements(By.XPATH,sp_crcd)[0].text.split("\n")]
        spell_obj['description']=driver.find_elements(By.XPATH,sp_desc)[0].text.strip()
        spell_array.append(spell_obj)



with open(cl+"_spells.json", "w") as outfile:
    json.dump(spell_array,outfile)
driver.close()
