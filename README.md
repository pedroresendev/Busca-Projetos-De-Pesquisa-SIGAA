# Busca-Projetos-De-Pesquisa-SIGAA

Projeto concebido para extrair informações sobre as oportunidades de bolsa de pesquisa do CEFET-MG.

Seu funcionamento se dá pela autenticação no SIGAA, onde o usuário insere suas credenciais. Posteriormente, ocorre a extração de um número definido de bolsas com base no seu ID.

Após essa etapa, realiza-se uma análise dos dados obtidos. Por exemplo, verifica-se se o projeto foi removido ou se já possui um estudante vinculado. Além disso, é viável filtrar os dados conforme o nome do orientador, o campus específico e/ou a presença de bolsa de iniciação científica. Além disso, é possível salvar e exportar os dados dos projetos em um arquivo .csv e/ou .xlsx.

Esse projeto é implementado por meio de um Web Scraper, visto que o SIGAA não disponibiliza uma API pública.

*Ressalta-se que este projeto não possui qualquer vínculo com o CEFET e não foi elaborado em colaboração com a instituição.*

# ANÁLISE DOS DADOS

Ao realizar o login, os seus dados não são armazenados em nenhum lugar. Eles são apenas utilizados como parâmetros para uma função.

# VERSÃO

Essa é a primeira versão do projeto. Novas funcionalidades serão adicionadas com o passar do tempo.

# ATUALIZAÇÕES

Att 1.1 - Salvar dados
Nessa atualização, diversas alterações foram feitas. Entre elas:

- Busca de mais de 700 URLs
- Salvar os dados em um arquivo CSV após a primerar extração. Dessa forma, ao executar o código novamente, não será necessário realizar todo o processo novamente
- Exportar dados para uma 'tabela excel' (.xlsx)
- Filtrar apenas os projetos que ainda estão disponíveis para inscrição
- Correção de bugs
 
