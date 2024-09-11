import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# A classe Service é usada para iniciar uma instância do Chrome WebDriver
service = Service()

# webdriver.ChromeOptions é usada para definir a preferência para o browser do Chrome
options = webdriver.ChromeOptions()

# Iniciar a instância do Chrome Webdriver com as definidas 'options' e 'service'
driver = webdriver.Chrome(service=service, options=options)

url = 'https://books.toscrape.com/'

driver.get(url)

# Corrigir a chamada do método para find_elements e pegar o atributo title do elemento
title_elements = driver.find_elements(By.TAG_NAME, 'a')

# Verificar se há pelo menos 59 elementos antes de acessar o índice 58
if len(title_elements) > 58:
    title_attribute = title_elements[58].get_attribute('title')

# Pegar a fatia correta dos elementos
title_elements = title_elements[54:94:2]

# Obter a lista de títulos dos elementos
title_list = [title.get_attribute('title') for title in title_elements]

# Clicar no terceiro elemento da lista title_elements, se existir
if len(title_elements) > 2:
    title_elements[2].click()

    # Extrair o número de itens em estoque, removendo o texto desnecessário
    in_stock_count = int(driver.find_element(By.CLASS_NAME, 'instock').text.replace('In stock (', '').replace(' available)', ''))

    # Voltar para a página anterior
    driver.back()

# Coletar dados de estoque
stock_list = []
for title in title_elements:
    title.click()

    qtd_stock = int(driver.find_element(By.CLASS_NAME, 'instock').text.replace('In stock (', '').replace(' available)', ''))

    stock_list.append(qtd_stock)

    driver.back()

# Garantir que as listas têm o mesmo comprimento antes de criar o DataFrame
if len(title_list) == len(stock_list):
    dict_df = {'title': title_list, 'stock': stock_list}
    df = pd.DataFrame(dict_df)
    print("DataFrame:\n", df)
else:
    print("Erro: As listas 'title_list' e 'stock_list' têm comprimentos diferentes.")
    print("title_list length:", len(title_list))
    print("stock_list length:", len(stock_list))

# Fechar o navegador
driver.quit()

# Exibir os resultados (opcional)
if 'title_attribute' in locals():
    print("Title Attribute:", title_attribute)
if 'in_stock_count' in locals():
    print("In Stock Count:", in_stock_count)
