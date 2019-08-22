from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from getpass import getpass
from ntPR_functions import site_login
from ntPR_functions import coleta


# Abrindo navegador
chrome_options = Options()  
chrome_options.add_argument("--headless") 

driver = webdriver.Chrome(chrome_options=chrome_options)  

# Everything happens here!!!
def main():

    # Solicita cpf e senha para acessar site!
    cpf   = input('Informe seu cpf (sem pontos ou traços): ')
    senha = getpass('Informe sua senha: ')
    opt =   int(input('\nDigite o número da opção desejada?: \n 1 - Mês Atual\n 2 - Mês anterior\n'))    

    # Urls de acesso às paginas necessárias.
    url     = 'https://notaparana.pr.gov.br/nfprweb'
    url_ext = 'https://notaparana.pr.gov.br/nfprweb/Extrato'

    # Executa função para acessar o site.
    site_login(driver,url,cpf,senha)
    
    # Executa função para coletar os dados das notas fiscais.
    coleta(driver,url_ext,cpf,opt)

main()

driver.close()