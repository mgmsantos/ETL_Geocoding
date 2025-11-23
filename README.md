# ETL_Geocoding

```python
CHAVE_API_GOOGLE = "____" ## INSIRA UMA CHAVE API GEOCODING
try:
    gmaps = googlemaps.Client(key=CHAVE_API_GOOGLE)
except Exception as e:
    print(f"Erro ao iniciar o cliente Google Maps: {e}")
    gmaps = None

def get_coordenadas_google(query_completa):
    if gmaps is None: return pd.Series([None, None])
    try:
        geocode_result = gmaps.geocode(query_completa)
        if geocode_result:
            lat = geocode_result[0]['geometry']['location']['lat']
            lon = geocode_result[0]['geometry']['location']['lng']
            return pd.Series([lat, lon])
        else:
            return pd.Series([None, None]) 
    except Exception as e:
        print(f"Erro na API: {e} | Query: {query_completa}")
        return pd.Series([None, None])
# -------------------------------------------------

df[["latitude", "longitude"]] = df['ENDERECO_FULL'].apply(get_coordenadas_google)

df_coord = df
```
