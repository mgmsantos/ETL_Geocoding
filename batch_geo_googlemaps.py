# %%

# ----------------------------------------------------------------------
# 1. IMPORTAÇÃO DAS BIBLIOTÉCAS NECESSÁRIAS
# ----------------------------------------------------------------------

import googlemaps
import googlemaps.exceptions
import pandas as pd

# %%

# ----------------------------------------------------------------------
# 2. CONFIGURAÇÃO DO CLIENTE GOOGLE MAPS
# ----------------------------------------------------------------------

CHAVE_API_GOOGLE = "AIzaSyATYR0DBO9spMMce_XxlgGJ7EFV62teYYw"

try:
    if CHAVE_API_GOOGLE:
        gmaps = googlemaps.Client(key = CHAVE_API_GOOGLE)
        print("Cliente Google Maps inicializado com sucesso.")
except Exception as e:
    print(f"Erro ao iniciar o cliente Google Maps: {e}")
    gmaps = None

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
df_teste

# %%
# ----------------------------------------------------------------------
# 5. GERANDO UM MAPA TESTE
# ----------------------------------------------------------------------

import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
from shapely.geometry import Point

CRS_WEBMERCARTOR = "EPSG:3857"

def gerar_mapa_teste(df, archive = "mapa.png"):
    """
    Gera um mapa estático geográfico utilizando Matplotlib, GeoPandas e Contextily.
    
    A função reprojeta os pontos de latitude/longitude (EPSG:4326) para o sistema 
    Web Mercator (EPSG:3857), que é compatível com o mapa base do OpenStreetMap, 
    e salva o resultado como um arquivo de imagem.

    Args:
        df (pd.DataFrame): O DataFrame de entrada, que deve conter as colunas 
                           'latitude' e 'longitude' com as coordenadas geocodificadas.
        archive (str, optional): O nome do arquivo onde o mapa será salvo. 
                                 Deve ser uma extensão de imagem válida (ex: .png, .jpg).
                                 Padrão é "mapa.png".
                                 
    Returns:
        None: A função salva o mapa como um arquivo e não retorna nenhum objeto.
    """
    df = df.dropna(subset=['latitude', 'longitude']).drop_duplicates(subset=['latitude', 'longitude'])
    if df.empty:
        print("Não há coordenadas para geraro mapa")
        return
    
    gdf = gpd.GeoDataFrame(
        df,
        geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])],
        crs = "EPSG:4326"
    )

    gdf_web = gdf.to_crs(CRS_WEBMERCARTOR)

    fig, ax = plt.subplots(figsize = (5, 5,))
    gdf_web.plot(ax = ax, color = 'red', markersize = 40, edgecolor = 'black', linewidth = 1)

    try:
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    except Exception as e:
        print(f"⚠️ Erro ao adicionar Contextily: {e}")
    
    ax.set_axis_off()
    ax.set_title("Mapa Teste")
    plt.tight_layout()
    plt.savefig(archive,
                dpi = 400,
                bbox_inches = 'tight',
                pad_inches = 0.1)

gerar_mapa_teste(df_teste, "mapa_teste")