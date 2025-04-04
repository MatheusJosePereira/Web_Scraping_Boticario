from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime

# Pergunta ao usuário qual produto deseja procurar
produto = input('Qual produto você deseja procurar na Boticário: ')

# Configuração do WebDriver
navegador = webdriver.Chrome()

# Maximiza a janela
navegador.maximize_window()

# URL da busca com o produto
url = f'https://www.boticario.com.br/busca?q={produto}'

# Abre a URL no navegador
navegador.get(url)

# Aceita cookies
try:
    wait = WebDriverWait(navegador, 10)
    botao_aceitar_cookies = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    botao_aceitar_cookies.click()
except Exception as e:
    print('Não foi possível aceitar os cookies.')

# Encontra todos os elementos de classe 'showcase-image'
elementos_produtos = navegador.find_elements(By.CLASS_NAME, 'showcase-image')

# Lista para armazenar os resultados
resultados = []

# Itera sobre os elementos para obter informações
for i in range(len(elementos_produtos)):
    try:
        elemento = elementos_produtos[i]
        url_imagem = elemento.get_attribute('src')

        # Clicar na imagem para abrir detalhes do produto
        elemento.click()

        # Aguarda a visibilidade do título (h1)
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
        elemento_h1 = navegador.find_element(By.TAG_NAME, 'h1')
        titulo_h1 = elemento_h1.text

        # Aguarda a visibilidade do preço
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'nproduct-price-value')))
        elemento_preco = navegador.find_element(By.CLASS_NAME, 'nproduct-price-value')
        preco_texto = elemento_preco.text.replace('R$', '').replace(',', '.').strip()

        # Converte para float e depois para inteiro
        preco = int(float(preco_texto))

        # Adiciona os resultados à lista
        resultados.append({
            'titulo': titulo_h1,
            'preco': preco,
            'avaliacao': i,  # Adicione a avaliação real, se disponível
            'link_imagem': url_imagem
        })

        # Voltar para a página de resultados
        navegador.back()

        # Aguarde a visibilidade dos elementos novamente
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'showcase-image')))
        elementos_produtos = navegador.find_elements(By.CLASS_NAME, 'showcase-image')

    except IndexError:
        print(f"Erro: Não foi possível acessar o índice {i} na lista. Provavelmente, não há mais elementos.")
        break

indices = []
titulos = []
precos = []
avaliacoes = []
links_imagem = []

# Loop para iterar sobre os resultados
for idx, resultado in enumerate(resultados, start=1):
    # Seu código para extrair os dados...

    
    titulo = resultado.get('titulo', 'N/A') 
    preco = resultado.get('preco', 'N/A') 
    avaliacao = resultado.get('avaliacao', 'N/A')  
    url_imagem = resultado.get('link_imagem', 'N/A')

    # Adicionar dados às listas
    indices.append(idx)
    titulos.append(titulo)
    precos.append(preco)
    avaliacoes.append(avaliacao)
    links_imagem.append(url_imagem)

    # Exibir os dados
    print(f'{idx}: {titulo}, {preco}, {avaliacao}, {url_imagem}')

# Criar DataFrame a partir das listas
tabela = pd.DataFrame({
    'Índice': indices,
    'Título': titulos,
    'Preço': precos,
    'Avaliação': avaliacoes,
    'Link da Imagem': links_imagem
})

# Salvar o DataFrame em um arquivo Excel
data_atual = datetime.now().strftime("%Y-%m-%d")
nome_arquivo = f'{produto}_resultados_{data_atual}.xlsx'
tabela.to_excel(nome_arquivo, index=False)

# Exibir o DataFrame
print(tabela)

navegador.quit()
