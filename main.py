import requests
import random
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- 1. CONFIGURACIÓN ---
GENIUS_TOKEN = "O7OfEum-vvEj9xEvfzYoj0gUQH25ke_ofenHXUOovVJgI2jEL-MNt9dQC8UixpwF"

# Añadimos un "User-Agent" para identificarnos correctamente ante el servidor de Genius
HEADERS = {
    "Authorization": f"Bearer {GENIUS_TOKEN}",
    "User-Agent": "AdivinaElAlbumApp/1.0"
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SongInfo(BaseModel):
    title: str
    artist_name: str
    album_name: str
    album_cover_url: str


# --- 2. LA NUEVA LÓGICA DEL JUEGO ---
@app.get("/api/juego/{artista}", response_model=SongInfo)
async def obtener_cancion_para_jugar(artista: str):
    url_busqueda = f"https://api.genius.com/search?q={artista}"
    respuesta_busqueda = requests.get(url_busqueda, headers=HEADERS)

    # --- AQUÍ ESTÁ EL CAMBIO DE DEPURACIÓN ---
    if respuesta_busqueda.status_code != 200:
        print("\n" + "=" * 40)
        print("¡ERROR REPORTADO POR LA API DE GENIUS!")
        print(f"Código HTTP: {respuesta_busqueda.status_code}")
        print(f"Detalle del error: {respuesta_busqueda.text}")
        print("=" * 40 + "\n")
        raise HTTPException(status_code=500, detail="Error en la puerta principal. Revisa la terminal de PyCharm.")
    # -----------------------------------------

    resultados = respuesta_busqueda.json().get("response", {}).get("hits", [])
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron canciones.")

    ids_canciones = [hit["result"]["id"] for hit in resultados if hit["type"] == "song"]
    random.shuffle(ids_canciones)

    for id_cancion in ids_canciones:
        url_cancion = f"https://api.genius.com/songs/{id_cancion}"
        respuesta_cancion = requests.get(url_cancion, headers=HEADERS)

        if respuesta_cancion.status_code == 200:
            datos_cancion = respuesta_cancion.json().get("response", {}).get("song", {})
            album = datos_cancion.get("album")

            if album and album.get("cover_art_url"):
                nombre_album = album.get("name", "")

                if nombre_album and not re.search(r'(?i)\(single\)', nombre_album):
                    return SongInfo(
                        title=datos_cancion.get("title"),
                        artist_name=datos_cancion.get("primary_artist", {}).get("name"),
                        album_name=nombre_album,
                        album_cover_url=album.get("cover_art_url")
                    )

    raise HTTPException(status_code=404, detail="Este artista no tiene canciones con álbumes válidos para jugar.")