import pandas as pd  # Importa a biblioteca pandas e a apelida de 'pd' para facilitar o uso.
import json  # Importa o módulo json, que é usado para trabalhar com dados JSON.
import requests  # Importa a biblioteca requests, usada para fazer solicitações HTTP.
import openai
import boto3

'''
O Pandas é uma biblioteca de código aberto em Python que fornece estruturas de dados e ferramentas de análise de dados eficazes e flexíveis. Ele é amplamente utilizado para manipular e analisar dados tabulares, 
como planilhas e bancos de dados, tornando mais fácil a realização de tarefas como limpeza, transformação, análise e visualização de dados. O Pandas é essencial para cientistas de dados e analistas de dados que .
trabalham com dados numéricos e tabulares. Ele oferece estruturas de dados poderosas, como DataFrames e Series, que simplificam a manipulação e análise de dados.
'''

# Especifique o caminho completo para o arquivo CSV na sua máquina
caminho_arquivo = 'caminho do aquivo CSV'

# Use o pandas para ler o arquivo CSV e carregar os dados em um DataFrame
clientes_df = pd.read_csv(caminho_arquivo)


# Converta o DataFrame para JSON com a codificação UTF-8
json_data = clientes_df.to_json(orient='records', indent=4, force_ascii=False, default_handler=str)



# Filtrar clientes com status "Pendente"
clientes_pendentes_df = clientes_df[clientes_df['Status'] == 'Pendente']


# Exibir os clientes com pendências após a transformação
# print(clientes_pendentes_df)

# Defina sua chave de API do ChatGPT
openai.api_key = 'SUA_CHAVE_DE_API_DO_CHATGPT'
openai.api_key = openai.api_key

def generate_ai_news(cliente):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em relacionamento com os clientes, tome cuidado com palavras diretas para o cliente não se sentir ofendido com a cobrança e seja sempore conrdial. obs não use a palavra devolver ou Precisamos dos equipamentos é ofensivo "
            },
            {
                "role": "user",
                "content": f"Crie uma mensagem de cobrança para {cliente['Nome']} sobre a importância da devolução dos equipamentos em atraso (máximo de 100 caracteres)"
            }
        ]
    )
    return completion.choices[0].message.content.strip('\"')

# for index, cliente in clientes_pendentes_df.iterrows():
#     news = generate_ai_news(cliente)
#     print(news)


# Configure as credenciais da AWS
aws_access_key_id = 'SUA_ACCESS_KEYID_DA_AWS'
aws_secret_access_key = 'SUA_SECRET_ACCESS_KEY_DA_AWS'
aws_region = 'REGIAO_AWS'  # Por exemplo, 'us-east-1'

# Crie um cliente SNS
sns_client = boto3.client('sns', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

# Loop pelos clientes com status "Pendente"
for index, cliente in clientes_pendentes_df.iterrows():
    nome_cliente = cliente['Nome']
    numero_telefone = str(cliente['contato']) # Converte o número de telefone para uma string
    
    # Gere uma mensagem usando a função generate_ai_news
    mensagem = generate_ai_news(cliente)

    # Envie a mensagem SMS usando o Amazon SNS
    response_sns = sns_client.publish(
        PhoneNumber=numero_telefone,  # Número de telefone de destino
        Message=mensagem,
    )

    print(f"Mensagem enviada para {nome_cliente} em {numero_telefone}: {response_sns['MessageId']}")