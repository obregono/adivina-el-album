// Aquí guardaremos la respuesta correcta de forma invisible
let albumCorrecto = "";

async function buscarCancion() {
    const artista = document.getElementById('input-artista').value;
    const mensajeDiv = document.getElementById('mensaje');

    if (!artista) return;

    // Mensaje de carga usando el color blanco del CSS
    mensajeDiv.style.color = "var(--text-main)";
    mensajeDiv.innerText = "Buscando en tu API de Python... ⏳";

    try {
        const respuesta = await fetch(`https://adivina-el-album.onrender.com/api/juego/${artista}`);

        if (!respuesta.ok) {
            throw new Error("No se encontraron canciones para jugar.");
        }

        const datos = await respuesta.json();

        // Guardamos la respuesta secreta
        albumCorrecto = datos.album_name.toLowerCase();

        // Actualizamos la interfaz
        document.getElementById('titulo-cancion').innerText = datos.title;
        document.getElementById('nombre-artista').innerText = datos.artist_name;

        const img = document.getElementById('portada-album');
        img.src = datos.album_cover_url;
        img.style.display = "block";

        // Cambiamos de pantalla
        document.getElementById('fase-busqueda').style.display = "none";
        document.getElementById('fase-juego').style.display = "block";
        mensajeDiv.innerText = "";

    } catch (error) {
        mensajeDiv.style.color = "var(--danger-color)";
        mensajeDiv.innerText = "Error: " + error.message;
    }
}

function comprobarRespuesta() {
    const intento = document.getElementById('input-adivinanza').value.toLowerCase().trim();
    const mensajeDiv = document.getElementById('mensaje');

    if (intento === albumCorrecto) {
        mensajeDiv.style.color = "var(--accent-color)";
        mensajeDiv.innerText = "¡CORRECTO! 🎉 El álbum es: " + albumCorrecto.toUpperCase();
    } else {
        mensajeDiv.style.color = "var(--danger-color)";
        mensajeDiv.innerText = "¡Fallaste! ❌ Sigue intentando.";
    }
}

function reiniciarJuego() {
    document.getElementById('fase-busqueda').style.display = "block";
    document.getElementById('fase-juego').style.display = "none";
    document.getElementById('portada-album').style.display = "none";
    document.getElementById('input-artista').value = "";
    document.getElementById('input-adivinanza').value = "";
    document.getElementById('mensaje').innerText = "";
}