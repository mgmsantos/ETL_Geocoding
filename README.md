# Batch Geocoding: Pandas & Google Maps

## Visão Geral do Projeto

Este projeto consiste em uma solução Python para realizar a geocodificação em lote (*batch geocoding*) de endereços, nomes de locais e pontos de interesse, convertendo-os em coordenadas geográficas (Latitude e Longitude).

O código é tecnicamente versátil, sendo aplicável a qualquer setor que trabalhe com grandes bases de dados geográficos e necessite de precisão na localização.

---

### Funcionalidades Chave:

* **API Geocoding:** Utilização do client `googlemaps` para consultas eficientes.
* **Integração Pandas:** Aplicação direta da função em `DataFrames` do Pandas para processamento em lote.
* **Robustez:** Implementação de `try/except Exception as e` para gerenciamento de falhas de API (limites de uso, erros de rede, etc.).

---

## Stack Técnico e Configuração

### Requisitos

* **Linguagem:** Python.
* **Bibliotecas:** `os`, `googlemaps`, `pandas`
* **API:** Google Maps Geocoding API

---

### Código Python

1. Importação das bibliotecas necessárias
```python
# %%
# ----------------------------------------------------------------------
# 1. IMPORTAÇÃO DAS BIBLIOTÉCAS NECESSÁRIAS
# ----------------------------------------------------------------------

import googlemaps
import googlemaps.exceptions
import pandas as pd

```

2. Inicialização do client e tratamento em caso de erro
```python
# %%
# ----------------------------------------------------------------------
# 2. CONFIGURAÇÃO DO CLIENTE GOOGLE MAPS
# ----------------------------------------------------------------------

CHAVE_API_GOOGLE = "DIGITE SUA API AQUI"

try:
    if CHAVE_API_GOOGLE:
        gmaps = googlemaps.Client(key = CHAVE_API_GOOGLE)
        print("Cliente Google Maps inicializado com sucesso.")
except Exception as e:
    print(f"Erro ao iniciar o cliente Google Maps: {e}")
    gmaps = None
```

3. Função `get_coordenadas_google`
- A funçao utiliza `try/except` para garantir que o código não crash em falhas da API
```python
# %%
# ----------------------------------------------------------------------
# 3. FUNÇÃO DE GEOCODIFICAÇÃO
# ----------------------------------------------------------------------

geobatch_cache = {} ## cachê para armazenar resultados já consultados em caso de múltiplas consultas iguais

def get_coordenadas_google(query):

    """
    Converte um endereço de texto em coordenadas geográficas (Lat/Long) usando 
    a API do Google Maps.
    
    Args:
        query (str): O endereço ou nome do local a ser geocodificado.
        
    Returns:
        pd.Series: Uma série do Pandas contendo [latitude, longitude].
                   Retorna [None, None] em caso de falha.
    """
    
    # Se o cliente não foi inicializado (gmaps é None), não prossegue
    if gmaps is None:
        print("Erro: Cliente Google Maps não inicializado.")
        return pd.Series([None, None])
    
    # Checar se a consulta é válida, caso não, não prossegue
    if not query or pd.isna(query):
        print("Aviso: Consulta inválida ou vazia.")
        return pd.Series([None, None])
    
    # checar se a consulta já está no cachê
    if query in geobatch_cache:
        return pd.Series(geobatch_cache[query])
    
    try:
        # Realiza a chamada à API
        geocode_result = gmaps.geocode(query)
        
        if geocode_result:
            # Extrai as coordenadas do primeiro resultado
            lat = geocode_result[0]['geometry']['location']['lat']
            long = geocode_result[0]['geometry']['location']['lng']

            # Armazena no cachê
            geobatch_cache[query] = [lat, long]
            return pd.Series([lat, long])
        else:
            # Armazena no cache e retorna None se a API não encontrar o endereço
            geobatch_cache[query] = [None, None]
            print(f"AVISO: Endereço não encontrado pela API. Consulta: {query}")
            return pd.Series([None, None]) 

    # Tratativa de erros específicos da API
    except googlemaps.exceptions.ApiError as e:
        print(f"Erro API Google Maps: {e} | Consulta: {query}")
        return pd.Series([None, None])     
    
    # Tratativa de erros de timeout/rede
    except (googlemaps.exceptions.Timeout, googlemaps.exceptions.TransportError) as e:
        print(f"Erro de rede/timeout: {e} | Consulta: {query}")
        return pd.Series([None, None])
    
    # Tratativa de outros tipos de erro
    except Exception as e:
        # Trata erros inesperados da API
        print(f"Outro tipo de erro: {e} | Consulta: {query}")
        return pd.Series([None, None])
```

4. Exemplo de aplicação em DataFrame
```python
# %%
# ----------------------------------------------------------------------
# 4. EXECUÇÃO DA FUNÇÃO
# ----------------------------------------------------------------------
data = {
    'ENDERECO': [
        "Av. Paulista, 1578 - Bela Vista, São Paulo - SP, 01310-200",
        "R. Cantareira, 306 - Centro Histórico de São Paulo, São Paulo - SP, 01024-000",
        "Praça da Sé, s/n - Sé, São Paulo - SP, 01001-000", # Primeira ocorrência
        "Av. Pedro Álvares Cabral, s/n - Vila Mariana, São Paulo - SP, 04094-050",
        "R. Oscar Freire, 1100 - Cerqueira César, São Paulo - SP, 05409-010",
        "Praça da Sé, s/n - Sé, São Paulo - SP, 01001-000"  # Segunda ocorrência (Cache Test)
    ]
}

df_teste = pd.DataFrame(data)

# Considerando que 'df' é um DataFrame carregado com a coluna de texto a ser geocodificada.
df_teste[["latitude", "longitude"]] = df_teste['ENDERECO'].apply(get_coordenadas_google)

# %%

# Exibe o DataFrame resultante e o conteúdo do cache
print(df_teste)
print(geobatch_cache)
```
### 5. Mapa teste com as coordenadas geocodificadas
<div align = "center">
    <img src="/mapa_teste.png" alt="Mapa de localização dos pontos geocodificados" width="400"/>
</div>
---

### Aplicações e versatilidade
O motor de geocodificação construído pode ser aplicado em diversos setores que necessitem de análise espacial de grandes volumes de dados, por exemplo:
- **AgTech (Agricultura e Tecnologia):**
  - Integração de pontos geocodificados com dados de sensor ou mapas de colheita para análises de geoprocessamento;
  - Mapeamento de fornecedores e rotas para otimizar a distribuição e aplicação de fertilizantes e defensivos;
  - Criação de shapefiles e camadas vetoriais para modelagem de dados territoriais.
- **Business Intelligence (BI):**
  - Mapeamento de clientes e fornecedores para otimizar logística, distribuição e análise de mercado;
  - Criação de indicadores de desempenho (KPIs) baseados em localização geográfica.
- **Análise Urbana e Geomarketing:**
  - Conversão de endereços para planejamento urbano, definição de zonas de serviço e análise de geomarketing.

---

## Conecte-se Comigo

*Siga os links abaixo para saber mais sobre minha trajetória profissional e me contatar:*

<div> 
  <a href="mailto:miguel.gms31@gmail.com"><img src="https://img.shields.io/badge/-Gmail-%23333?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
  <a href="https://www.linkedin.com/in/miguelgms31/" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a>
  <a href="http://lattes.cnpq.br/2943203054995050" target="_blank"><img src="https://img.shields.io/badge/-Lattes-%230077B5?style=for-the-badge&logo=google-scholar&logoColor=white" target="_blank"></a>
</div>

---

## Próximos Passos e Contribuições

Este projeto pode ser expandido com as seguintes funcionalidades:

* Implementação de rotinas de validação de endereços antes da geocodificação.
* Adição de suporte para outras APIs de geocodificação (como HERE ou OpenCage).
* Criação de um *wrapper* para processamento assíncrono (otimizando a velocidade do *batch geocoding*).

Sinta-se à vontade para *favoritar* esse repositório com uma estrela e promor melhorias, abrir *issues* ou enviar *pull requests*!

---
