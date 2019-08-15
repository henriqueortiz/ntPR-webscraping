'''
Criado por: Henrique Ortiz

'''


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import pandas as pd


# Abrindo navegador
driver = webdriver.Chrome()

# Função para logar no site
def site_login(url,cpf,senha):
    driver.get(url)
    driver.find_element_by_id('attribute').send_keys(cpf)
    driver.find_element_by_id ('password').send_keys(senha)      
    driver.find_element_by_css_selector('.action-button').send_keys(Keys.RETURN)

# Função para navegar pelo site e coletar informações do mês atual
def nt_mes(url):

    # Acessa página informada, url do extrato.
    driver.get(url)
    
    # Coleta todos os links da tabela com as notas. 
    elems = driver.find_element_by_css_selector('.grid-verde')
    links = elems.find_elements_by_xpath("//*[@href]")
    
    # Adiciona somentes os links das notas em uma lista
    links_notas = []
    for i in links:
        if 'NotaFiscalHtml' in i.get_attribute("href"):
            links_notas.append(i.get_attribute("href"))
    # Listas que serão populadas com as informações das notas
    list_html_prod = []
    list_html_cab = []
    list_cobr = []
    list_places = []
    list_dates = []
    list_nr_nota = []

    # Acessa cada link na lista 'links_notas' e garimpa as informações da nota.
    for i in links_notas:
        driver.get(i)
        list_html_prod.append(driver.find_element_by_id('Prod').get_attribute('innerHTML'))
        list_html_cab.append(driver.find_element_by_id('NFe').get_attribute('innerHTML'))
        list_places.append(driver.find_element_by_xpath('/html[1]/body[1]/div[2]/div[1]/div[1]/fieldset[2]/table[1]/tbody[1]/tr[1]/td[2]/span[1]').get_attribute('innerHTML'))
        list_dates.append(driver.find_element_by_xpath('/html[1]/body[1]/div[2]/div[1]/div[1]/fieldset[1]/table[1]/tbody[1]/tr[1]/td[4]/span[1]').get_attribute('innerHTML'))
        list_cobr.append(driver.find_element_by_xpath('/html[1]/body[1]/div[2]/div[6]/div[1]/fieldset[1]/table[1]/tbody[1]/tr[1]/td[2]/span[1]').get_attribute('innerHTML'))
        list_nr_nota.append(driver.find_element_by_xpath('/html[1]/body[1]/div[2]/div[1]/div[1]/fieldset[1]/table[1]/tbody[1]/tr[1]/td[3]/span[1]').get_attribute('innerHTML'))
    
    # Itera sobre lista de htmls coletando informações dos itens da nota
    itens_notas = []
    for html in list_html_prod:
        soup = bs(html, 'html.parser')
        a = soup.find_all('table', attrs={'class':'toggle box'})
        b = []
        for i in a:
            x = []
            for j in i.find_all('span'):
                x.append(j.text)
            b.append(x)
        itens_notas.append(b)

    # Adiciona informações do cabeçalho na lista de itens
    for i in range(len(itens_notas)):
        for j in itens_notas[i]:
            j.append(list_places[i])
            j.append(list_dates[i].split()[0])
            j.append(list_dates[i].split()[1])
            j.append(list_cobr[i].strip())
            j.append(list_nr_nota[i])

    # trata lista para criação do dataframe
    final_list = []
    for i in range(len(itens_notas)):
        for j in itens_notas[i]:
            final_list.append(j)


    # Cria e trata o DataFrame para gerar csv
    df = pd.DataFrame(final_list,columns=['item_nota','produto','qtd','unidade','preço','local','data','hora','pagamento','nr_nota'])
    columns_order = ['local','nr_nota','item_nota','produto','qtd','unidade','preço','data','hora','pagamento']
    df = df.reindex(columns=columns_order)
    df.to_csv('notas_ntPR_atual.csv',sep=';')

    # Volta para página do extrato e efetua o logoff
    driver.get('https://notaparana.pr.gov.br/nfprweb/Extrato')
    driver.find_element_by_id('user-logout').click()



# Everything happens here!!!
def main():

    # Solicita cpf e senha para acessar site!
    cpf   = input('Informe seu cpf (sem pontos ou traços): ')
    senha = input('informe sua senha: ' ) 

    # Urls de acesso às paginas necessárias.
    url     = 'https://notaparana.pr.gov.br/nfprweb'
    url_ext = 'https://notaparana.pr.gov.br/nfprweb/Extrato'

    # Executa função para acessar o site.
    site_login(url,cpf,senha)
    
    # Executa função para coletar os dados das notas fiscais.
    nt_mes(url_ext)

main()