# Importações necessárias
from flask import Flask, jsonify
import pandas as pd
from surprise import Dataset, Reader, KNNWithMeans
from surprise.model_selection import train_test_split
from surprise import accuracy

# Inicialização da aplicação Flask
app = Flask(__name__)
trained_model = None  # Inicialização do modelo treinado como nulo


# Endpoint para treinar o modelo
@app.route('/treinar_modelo', methods=['GET'])
def treinar_modelo():
    global trained_model  # Uso da variável global para armazenar o modelo treinado

    # Carregar dados do arquivo CSV e preparar para o modelo
    data = pd.read_csv("D:\\Pessoal\\Academico\\SOFTEX\\cronosIA\\tabela_compras_avaliacao.csv", encoding='latin1')
    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(data[['Cliente ID', 'Produto', 'Avaliacao']], reader)

    # Dividir o conjunto de dados em treino e teste
    trainset, testset = train_test_split(dataset, test_size=0.2)
    
    # Configurar e treinar o algoritmo
    algo = KNNWithMeans()
    algo.fit(trainset)
    
    # Testar o modelo e calcular a raiz do erro quadrático médio (RMSE)
    predictions = algo.test(testset)
    rmse = accuracy.rmse(predictions)

    trained_model = algo  # Armazenar o modelo treinado para uso posterior
    
    # Responder com uma mensagem de sucesso e o valor do RMSE
    return jsonify({"message": "Modelo treinado com sucesso!", "RMSE": rmse})


# Endpoint para obter recomendações para um cliente específico usando o modelo treinado
@app.route('/recomendacao/<int:cliente_id>', methods=['GET'])
def obter_recomendacoes(cliente_id):
    global trained_model  # Uso da variável global para acessar o modelo treinado

    if trained_model is None:
        return jsonify({"message": "Por favor, treine o modelo antes de fazer recomendações."})

    # Carregar dados do arquivo CSV e preparar para o modelo
    data = pd.read_csv("D:\\Pessoal\\Academico\\SOFTEX\\cronosIA\\tabela_compras_avaliacao.csv", encoding='latin-1')
    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(data[['Cliente ID', 'Produto', 'Avaliacao']], reader)

    trainset = dataset.build_full_trainset()
    
    algo = trained_model  # Usar o modelo treinado armazenado
    
    # Identificar os produtos mais comprados pelo cliente
    produtos_mais_comprados = data[data['Cliente ID'] == cliente_id]['Produto'].value_counts().index.tolist()
    dados_recomendacao = [(cliente_id, produto, 4) for produto in produtos_mais_comprados]

    # Obter previsões de avaliações para os produtos mais comprados pelo cliente
    previsoes = algo.test(dados_recomendacao)

    # Ordenar as previsões para obter os principais produtos recomendados
    top_n = 5
    produtos_top = sorted(previsoes, key=lambda x: x.est, reverse=True)[:top_n]

    # Criar uma resposta JSON com os produtos recomendados
    produtos_recomendados = [{"Produto": produto.iid, "Avaliacao_Prevista": produto.est} for produto in produtos_top]

    return jsonify({"cliente_id": cliente_id, "produtos_recomendados": produtos_recomendados})

# Executar a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)