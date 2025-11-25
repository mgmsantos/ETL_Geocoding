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

### Configuração da Chave API

Por questões de segurança, é interessante que a chave API seja lida de uma `Variável Ambiente`

```bash
# Linux/macOS
export CHAVE_API_GEOCODING_GoogleMaps = "Insira sua chave aqui"

# Windows (PowerShell)
$env:CHAVE_API_GEOCODING_GoogleMaps = "Insira sua chave aqui"
```

---

### Código Python

1. Importação das bibliotecas necessárias
```python
# ----------------------------------------------------------------------
# 1. IMPORTAÇÃO DAS BIBLIOTÉCAS NECESSÁRIAS
# ----------------------------------------------------------------------

import os
import googlemaps
import pandas as pd
```

2. Inicialização do client e tratamento em caso de erro
```python
# ----------------------------------------------------------------------
# 2. CONFIGURAÇÃO DO CLIENTE GOOGLE MAPS
# ----------------------------------------------------------------------

# A chave deve ser definida como uma variável de ambiente (ex: export CHAVE_API_GOOGLE="SUA_CHAVE")
CHAVE_API_GEOCODING_GoogleMaps = os.environ.get("CHAVE_API_GEOCODING_GoogleMaps") 
gmaps = None

try:
    if CHAVE_API_GOOGLE:
        # Tenta iniciar o cliente da API
        gmaps = googlemaps.Client(key=CHAVE_API_GOOGLE)
        print("Cliente Google Maps inicializado com sucesso.")
    else:
        print("AVISO: A variável de ambiente CHAVE_API_GOOGLE não foi definida.")
except Exception as e:
    # Captura e exibe qualquer erro de inicialização
    print(f"ERRO CRÍTICO ao iniciar o cliente Google Maps: {e}")
    gmaps = None
```

3. Função `get_coordenadas_google`
- A funçao utiliza `try/except` para garantir que o código não crash em falhas da API
```python
# ----------------------------------------------------------------------
# 3. FUNÇÃO DE GEOCODIFICAÇÃO
# ----------------------------------------------------------------------

def get_coordenadas_google(query):
    """
    Converte um endereço de texto em coordenadas geográficas (Lat/Lon) usando 
    a API do Google Maps.
    
    Args:
        query_completa (str): O endereço ou nome do local a ser geocodificado.
        
    Returns:
        pd.Series: Uma série do Pandas contendo [latitude, longitude].
                   Retorna [None, None] em caso de falha.
    """
    
    # Se o cliente não foi inicializado (gmaps é None), não prossegue
    if gmaps is None: 
        return pd.Series([None, None])
        
    try:
        # Realiza a chamada à API
        geocode_result = gmaps.geocode(query)
        
        if geocode_result:
            # Extrai as coordenadas do primeiro resultado
            lat = geocode_result[0]['geometry']['location']['lat']
            lon = geocode_result[0]['geometry']['location']['lng']
            return pd.Series([lat, lon])
        else:
            # Retorna None se a API não encontrar o endereço
            print(f"AVISO: Endereço não encontrado pela API. Consulta: {query}")
            return pd.Series([None, None]) 
            
    except Exception as e:
        # Trata erros inesperados da API (limite de uso, rede, etc.)
        print(f"ERRO na API: {e} | Consulta: {query}")
        return pd.Series([None, None])
```

4. Exemplo de aplicação em DataFrame
```python
# Considerando que 'df' é um DataFrame carregado com a coluna de texto a ser geocodificada.
df[["latitude", "longitude"]] = df['ENDERECO'].apply(get_coordenadas_google)
```

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

Sinta-se à vontade para propor melhorias, abrir *issues* ou enviar *pull requests*!

---
