# API Recomendação
 Este repositório contém uma aplicação em Python usando Flask para recomendação de produtos com base em avaliações de clientes. O sistema utiliza um modelo de filtragem colaborativa implementado com a biblioteca Surprise para gerar recomendações personalizadas para clientes com base em seus históricos de compras e avaliações.

# Funcionalidades:
Treinamento do Modelo: Endpoint (/treinar_modelo) para treinar o modelo de recomendação utilizando dados de um arquivo CSV contendo informações de clientes, produtos e avaliações.

Recomendações Personalizadas: Endpoint (/recomendacao/<cliente_id>) para obter recomendações específicas para um cliente, considerando os produtos mais adquiridos por esse cliente e gerando previsões de avaliações para recomendar os principais produtos.

# Tecnologias Utilizadas:
Python

Flask

Surprise (biblioteca de recomendação)

Pandas (manipulação de dados)

# Como Utilizar:
Clone o repositório.
Instale as dependências necessárias listadas no arquivo requirements.txt.
Execute a aplicação com python nome_do_arquivo.py.
Acesse os endpoints (/treinar_modelo e /recomendacao/<cliente_id>) para treinar o modelo e obter recomendações para um cliente específico.

# Observações:
Certifique-se de ter o arquivo CSV com os dados de compras e avaliações conforme o esperado para o treinamento do modelo e para gerar recomendações personalizadas.
