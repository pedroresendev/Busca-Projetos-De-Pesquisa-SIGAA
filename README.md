# BuscaProjetosDePesquisaSIGAA

Projeto concebido para extrair informações sobre as oportunidades de bolsa de pesquisa do CEFET-MG.

Seu funcionamento se dá pela autenticação no SIGAA, onde o usuário insere suas credenciais. Posteriormente, ocorre a extração de um número definido de bolsas com base no seu ID.

Após essa etapa, realiza-se uma análise dos dados obtidos. Por exemplo, verifica-se se o projeto foi removido ou se já possui um estudante vinculado. Além disso, é viável filtrar os dados conforme o nome do orientador, o campus específico e/ou a presença de bolsa de iniciação científica.

Esse projeto é implementado por meio de um Web Scraper, visto que o SIGAA não disponibiliza uma API pública.

Ressalta-se que este projeto não possui qualquer vínculo com o CEFET e não foi elaborado em colaboração com a instituição.

# ANÁLISE DOS DADOS

Ao realizar o login, os seus dados não são armazenados em nenhum lugar. Eles são apenas utilizados como parâmetros para uma função.

#VERSÃO

Essa é a primeira versão do projeto. Novas funcionalidades serão adicionadas com o passar do tempo.
 
