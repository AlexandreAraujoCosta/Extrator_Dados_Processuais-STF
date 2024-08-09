## Extrair as informacoes dos arquivos

import requests
import dsl
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd



from selenium.webdriver.chrome.options import Options
 
# Define a custom user agent
my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
 
# Set the custom User-Agent
chrome_options.add_argument(f"--user-agent={my_user_agent}")

# Create a new instance of ChromeDriver with the desired options
driver = webdriver.Chrome(options=chrome_options)

# Set an implicit wait
driver.implicitly_wait(20)



def waitForLoad(inputXPath): 

    Wait = WebDriverWait(driver, 20)       
    Wait.until(EC.presence_of_element_located((By.XPATH, inputXPath)))
    
def xpath_get (xpath):
    
    waitForLoad(xpath)
    dados = driver.find_element(By.XPATH, xpath).get_attribute('innerHTML')
    
    return dados

lista = []

processo = 1000
classe = "ADI"

url = 'https://portal.stf.jus.br/processos/listarProcessos.asp?classe=' + classe + '&numeroProcesso=' + str(processo)

dados = driver.get(url)

resumo = xpath_get('//*[@id="texto-pagina-interna"]')

andamentos = xpath_get('//*[@id="texto-pagina-interna"]')

dados_processuais = xpath_get('//*[@id="informacoes"]')

partes = xpath_get('//*[@id="partes"]')

decisoes = xpath_get('//*[@id="decisoes"]')

sessaovirtual = xpath_get('//*[@id="sessao-virtual"]')

deslocamentos = xpath_get('//*[@id="deslocamentos"]')

peticoes = xpath_get('//*[@id="peticoes"]')

recursos = xpath_get('//*[@id="recursos"]')

pautas = xpath_get('//*[@id="pautas"]')


dados_a_gravar = [classe + str(processo), 
          resumo,
          andamentos,
          dados_processuais,
          partes,
          decisoes, 
          sessaovirtual, 
          deslocamentos, 
          peticoes, 
          recursos,
          pautas]
        
colunas = ['processo', 
          'resumo',
          'andamentos',
          'dados_processuais',
          'partes',
          'decisoes', 
          'sessaovirtual', 
          'deslocamentos', 
          'peticoes', 
          'recursos',
          'pautas']

lista.append(dados_a_gravar)

df = pd.DataFrame(lista, columns = colunas)
df.to_csv('Dados_processuais.csv', index=False)
