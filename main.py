import re
import time
import csv
from typing import List, Dict, Optional

import pandas as pd
import requests
from requests import Session
from bs4 import BeautifulSoup

DADOS_BOLSA_PESQUISA: List[Dict[str, str]] = []

URL_LOGIN_SIGAA: str = 'https://sig.cefetmg.br/sigaa/verTelaLogin.do'
URL_SIGAA: str = 'https://sig.cefetmg.br/sigaa/portais/discente/discente.jsf'
URL_BOLSAS: str = 'https://sig.cefetmg.br/sigaa/pesquisa/planoTrabalho/wizard.do?dispatch=view&obj.id=9837{}'

def req(url: str) -> str:
    """Essa função faz uma requisição GET para a url passada como parâmetro e retorna o conteúdo HTML da página."""
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta.text
        else:
            print('Erro ao fazer requisição')
    except:
        print('Erro ao tentar realizar a aquisição')
        
def parsing(resposta_html: str) -> BeautifulSoup:
    """Essa função faz o parsing do conteúdo HTML da página e retorna um objeto BeautifulSoup."""
    try:
        soup = BeautifulSoup(resposta_html, 'html.parser')
        return soup
    except Exception as error:
        print('Erro ao fazer o parsing HTML')
        print(error)
        

def fazer_login(session: Session, soup: BeautifulSoup, username: str, password: str) -> None:
    """Essa função faz o login no sistema SIGAA automaticamente e retorna a sessão."""
    try:
        logon = soup.find('div', class_='logon')
        form = logon.find('form', {'name': 'loginForm'})
        action_url = form['action']
        table = form.find('table')
        inputs = table.find_all('input')
        
        form_data = {}
        for input_tag in inputs:
            if input_tag.get('name'):
                form_data[input_tag['name']] = input_tag.get('value', '')
                
        form_data['user.login'] = username
        form_data['user.senha'] = password

        response = session.post('https://sig.cefetmg.br' + action_url, data=form_data)
        if response.status_code == 200:
            if response.url == URL_SIGAA:
                response.url = URL_BOLSAS
                print('Login realizado com sucesso')
                return session
            else:
                print('Email e/ou senha incorretos.')
        else:
            print('Algo deu errado.')
    except Exception as error:
        print('Erro ao fazer login')
        print(error)

def remove_scripts_and_css(soup: BeautifulSoup) -> BeautifulSoup:
    """Essa função remove todos os scripts e css do objeto BeautifulSoup."""
    try:
        for script in soup(["script", "style", "link"]):
            script.decompose()  # remove a tag do objeto BeautifulSoup
        return soup
    except Exception as error:
        print('Erro ao remover scripts e css')
        print(error)

def buscar_trabalhos_de_pesquisa(session) -> List[Dict[str, str]]:
    """Essa função busca todos os trabalhos de pesquisa disponíveis no SIGAA e retorna uma lista de dicionários com os dados dos trabalhos."""
    try:
        lista_bolsas: List[Dict[str, str]] = []
        lista_bolsas_formatada: List[Dict[str, str]] = []
        
        for i in range(1, 700):
            url_bolsas: str = 'https://sig.cefetmg.br/sigaa/pesquisa/planoTrabalho/wizard.do?dispatch=view&obj.id=98370{}'.format(f'{i:03d}')
            soup_login: BeautifulSoup = parsing(session.get(url_bolsas).text)
            
            if i % 100 == 0:  # A cada 150 requisições, faça uma pausa
                print('Aguardando 10 segundos...')
                time.sleep(10)
            

            tabela = soup_login.find('table', class_='formulario')
            if tabela:
                dados_bolsa_th: List[str] = []
                dados_bolsa_td: List[str] = []
                for row in range (9):
                    th_elements = tabela.find_all('tr')[row].find_all('th')
                    td_elements = tabela.find_all('tr')[row].find_all('td')
                    if th_elements and td_elements:  # Verifica se as listas não estão vazias
                        cell_text_th: str = th_elements[0].text
                        cell_text_td: str = td_elements[0].text
                        
                        # Remove os (diversos) caracteres de tabulação e quebra de linha
                        cleaned_text_th: str = cell_text_th.replace("\t", "").replace("\n", "")
                        cleaned_text_td: str = cell_text_td.replace("\t", "").replace("\n", "")
                        
                        dados_bolsa_th.append(cleaned_text_th)
                        dados_bolsa_td.append(cleaned_text_td)
                
                # Cria um dicionário com os dados da bolsa de pesquisa, em que a chave é o texto do th e o valor é o texto do td
                dados_bolsa_pesquisa: Dict[str, str] = dict(pair for pair in zip(dados_bolsa_th, dados_bolsa_td))
                dados_bolsa_pesquisa['ID'] = ('98370{}'.format(f'{i:03d}'))
                dados_bolsa_pesquisa['URL'] = ('https://sig.cefetmg.br/sigaa/pesquisa/planoTrabalho/wizard.do?dispatch=view&obj.id=98370{}'.format(f'{i:03d}'))
                print('###### 98370{}'.format(f'{i:03d}'))
                
                lista_bolsas.append(dados_bolsa_pesquisa)
                
            else:
                print('Não foi possível encontrar a tabela no id: 983700{}'.format(f'{i:02d}'))
                
                
        lista_bolsas_formatada = filtragem_de_dados(lista_bolsas)
    except Exception as error:
        print('Erro ao buscar trabalhos de pesquisa')
        print(error)
        
    return lista_bolsas_formatada

def filtragem_de_dados(lista_bolsas: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Essa função filtra os dados das bolsas de pesquisa e retorna uma lista de dicionários com os dados de bolsas que não foram excluídas ou desaprovadas."""
    try:
        lista: List[Dict[str, str]] = []
        for dicionario in lista_bolsas:
            if (dicionario.get(' Status do Plano: ') != 'EXCLUÍDO' and 
                dicionario.get(' Status do Plano: ') != 'PROJETO NÃO APROVADO' and 
                ' Discente: ' not in dicionario):
                    lista.append(dicionario)
        return lista
    except Exception as error:
        print('Erro ao filtrar dados')
        print(error)
    

def exibir_projetos() -> None:
    """Essa função exibe todos os projetos de pesquisa disponíveis no SIGAA."""
    try:
        for dicionario in DADOS_BOLSA_PESQUISA:
                    for chave, valor in dicionario.items():
                        print(f'{chave} {valor}')
                    print("\n")
    except Exception as error:
        print('Erro ao exibir todos os projetos')
        print(error)

def filtragem_de_dados_por_campus() -> List[Dict[str, str]]:
    """Essa função filtra os dados das bolsas de pesquisa por campus e retorna uma lista de dicionários com os dados das bolsas que não foram excluídas."""
    try:
        print('OPÇÕES DE CAMPUS: \n\n')
        print('ARAXÁ')
        print('CONTAGEM')
        print('CURVELO')
        print('DIVINÓPOLIS')
        print('LEOPOLDINA')
        print('NEPOMUCENO')
        print('NOVA GAMELEIRA - BELO HORIZONTE')
        print('NOVA LIMA')
        print('NOVA SUÍÇA - BELO HORIZONTE')
        print('TIMÓTEO')
        print('VARGINHA')
        
        opcao: str = input('Digite o nome do campus que deseja filtrar: ')
        opcao_bolsa: str = input('Deseja filtrar por bolsa? (S/N): ')
        
        for dicionario in DADOS_BOLSA_PESQUISA:
            if dicionario['Centro:'].strip() == ('DIRETORIA DO CAMPUS ' + opcao):
                    
                    if opcao_bolsa.upper() == 'S':
                        #Verifica se o projeto não é voluntário
                        if not dicionario[' Tipo de Bolsa: '] == ' VOLUNTÁRIO (IC)':
                            for chave, valor in dicionario.items():
                                print(f'{chave} {valor}')
                            print("\n")
                    elif opcao_bolsa.upper() == 'N':
                        for chave, valor in dicionario.items():
                            print(f'{chave} {valor}')
                        print("\n")
                    else:
                        print('Valor inválido. Digite S ou N.')
                        
    except Exception as error:
        print('Erro ao filtrar dados por campus')
        print(error)

def filtragem_de_dados_por_orientador() -> List[Dict[str, str]]:
    """Essa função filtra os dados das bolsas de pesquisa por orientador e retorna uma lista de dicionários com os dados das bolsas que não foram excluídas."""
    try:
        opcao = input('Digite o nome completo do orientador que deseja filtrar:')
        opcao_bolsa = input('Deseja filtrar por bolsa? (S/N): ')
        
        for dicionario in DADOS_BOLSA_PESQUISA:
            if dicionario['Orientador:'].strip() == opcao.upper():
                    
                    if opcao_bolsa.upper() == 'S':
                        if not dicionario[' Tipo de Bolsa: '] == ' VOLUNTÁRIO (IC)':
                            for chave, valor in dicionario.items():
                                print(f'{chave} {valor}')
                            print("\n")
                    elif opcao_bolsa.upper() == 'N':
                        for chave, valor in dicionario.items():
                            print(f'{chave} {valor}')
                        print("\n")
                        
                    else:   
                        print('Valor inválido. Digite S ou N.')
                    
    except Exception as error:
        print('Erro ao filtrar dados por orientador')
        print(error)
        
def salvar_dados():
    #salva os dados extraídos em um arquivo CSV
    try:
        lista_de_dicionarios = DADOS_BOLSA_PESQUISA
        
        nomes_das_colunas = set(key for dicionario in lista_de_dicionarios for key in dicionario)

        # Escrevendo no arquivo CSV
        with open('database.csv', 'w', newline='', encoding='utf-8') as arquivo_csv:
            writer = csv.DictWriter(arquivo_csv, fieldnames=nomes_das_colunas)
            writer.writeheader()
            writer.writerows(lista_de_dicionarios)
            
    except Exception as error:
        print('Erro ao salvar os dados')
        print(error)
        
def carregar_dados():
    #carrega os dados salvos no arquivo CSV
    global DADOS_BOLSA_PESQUISA
    try:
        with open('database.csv', 'r', encoding='utf-8') as arquivo_csv:
            reader = csv.DictReader(arquivo_csv)
            DADOS_BOLSA_PESQUISA = [row for row in reader]
            
    except FileNotFoundError:
        print("Nenhum dado foi salvo. Por favor, faça o processo de busca novamente.")
        
def exportar_dados():
    #exporta os dados salvos no arquivo CSV para um arquivo .xlsx (Excel)
    global DADOS_BOLSA_PESQUISA
    try:
        df = pd.read_csv('database.csv')
        df.to_excel('database.xlsx', index=False)
    except Exception as error:
        print('Erro ao exportar dados')
        print(error)
        
def imprimir_menu():
    print('================================================')
    print('MENU')
    print('1 -Atualizar os dados de bolsas de pesquisa')
    print('2 - Buscar todos os trabalhos de pesquisa')
    print('3 - Filtrar trabalhos disponíveis por campus')
    print('4 - Filtrar trabalhos disponíveis por orientador')
    print('5 - Salvar os dados em uma tabela')
    print('0 - Sair')
    print('================================================')
    
def buscar_e_filtrar_dados():
        
    global DADOS_BOLSA_PESQUISA
        
    resposta_busca = req(URL_LOGIN_SIGAA)
    if resposta_busca:
        soup_busca = parsing(resposta_busca)
        if soup_busca:
            cpf: str = input('Digite o seu CPF(Apenas números): ')
            senha_sigaa: str = input('Digite a sua senha do SIGAA: ')
            session = fazer_login(requests.session(), soup_busca, cpf, senha_sigaa)
            if session:
                DADOS_BOLSA_PESQUISA = buscar_trabalhos_de_pesquisa(session)
                salvar_dados()
            
if __name__ == '__main__': 
    carregar_dados()
    
    while True:
        imprimir_menu()
        opcao = input('Escolha uma opção para o menu: ')
        
        if opcao == '1':
            buscar_e_filtrar_dados()
        elif opcao == '2':  
            exibir_projetos()
        elif opcao == '3':
            filtragem_de_dados_por_campus()
        elif opcao == '4':
            filtragem_de_dados_por_orientador()
        elif opcao == '5':
            exportar_dados()
        elif opcao == '0':
            break