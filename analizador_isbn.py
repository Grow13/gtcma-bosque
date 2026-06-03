#!/usr/bin/env python3
import requests
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

def consultar_openlibrary(isbn):
    """Consulta OpenLibrary por ISBN y devuelve metadatos básicos."""
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        key = f"ISBN:{isbn}"
        if key in data:
            libro = data[key]
            autores = [a.get("name", "") for a in libro.get("authors", [])]
            return {
                "fuente": "OpenLibrary",
                "titulo": libro.get("title", ""),
                "autores": autores,
                "editorial": libro.get("publishers", [{}])[0].get("name", ""),
                "anio": libro.get("publish_date", ""),
                "url": f"https://openlibrary.org/isbn/{isbn}"
            }
    except Exception as e:
        print(f"⚠️ Error en OpenLibrary: {e}")
    return None

def consultar_google_books(isbn):
    """Consulta Google Books por ISBN y devuelve metadatos básicos."""
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get("totalItems", 0) > 0:
            libro = data["items"][0]["volumeInfo"]
            return {
                "fuente": "Google Books",
                "titulo": libro.get("title", ""),
                "autores": libro.get("authors", []),
                "editorial": libro.get("publisher", ""),
                "anio": libro.get("publishedDate", "")[:4],
                "url": f"https://books.google.com/books?vid=ISBN{isbn}"
            }
    except Exception as e:
        print(f"⚠️ Error en Google Books: {e}")
    return None

def analizar_isbn(isbn):
    print(f"\n🔍 Analizando ISBN: {isbn}\n")
    
    # Consultar fuentes en paralelo
    resultados = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(consultar_openlibrary, isbn): "OpenLibrary",
            executor.submit(consultar_google_books, isbn): "Google Books"
        }
        for future in as_completed(futures):
            res = future.result()
            if res:
                resultados.append(res)
    
    if not resultados:
        print("❌ No se encontró información en ninguna fuente.")
        return
    
    # Mostrar resultados de cada fuente
    for res in resultados:
        print(f"\n📚 {res['fuente']}:")
        print(f"   Título: {res.get('titulo', 'N/D')}")
        print(f"   Autores: {', '.join(res.get('autores', [])) if res.get('autores') else 'N/D'}")
        print(f"   Editorial: {res.get('editorial', 'N/D')}")
        print(f"   Año: {res.get('anio', 'N/D')}")
        print(f"   URL: {res.get('url', 'N/D')}")
    
    # Calcular puntuación de consistencia
    puntuacion = 0
    total_comparaciones = 0
    
    # Comparar títulos
    titulos = [res.get('titulo', '').lower() for res in resultados if res.get('titulo')]
    if len(titulos) >= 2:
        total_comparaciones += 1
        if len(set(titulos)) == 1:
            puntuacion += 1
    
    # Comparar años
    años = [res.get('anio', '') for res in resultados if res.get('anio')]
    if len(años) >= 2:
        total_comparaciones += 1
        if len(set(años)) == 1:
            puntuacion += 1
    
    # Comparar primer autor (si existe)
    primeros_autores = []
    for res in resultados:
        autores = res.get('autores', [])
        if autores and len(autores) > 0:
            primeros_autores.append(autores[0].lower())
    if len(primeros_autores) >= 2:
        total_comparaciones += 1
        if len(set(primeros_autores)) == 1:
            puntuacion += 1
    
    # Mostrar alerta ética
    print("\n" + "="*50)
    if total_comparaciones == 0:
        print("⚪ No hay suficientes datos para calcular la consistencia.")
    else:
        porcentaje = (puntuacion / total_comparaciones) * 100
        print(f"📊 Puntuación de consistencia: {porcentaje:.0f}%")
        
        if porcentaje >= 80:
            print("🟢 CONFIANZA ALTA: Los metadatos coinciden entre fuentes.")
        elif porcentaje >= 50:
            print("🟡 CONFIANZA MEDIA - Revisar manualmente: Existen algunas discrepancias.")
        else:
            print("🔴 CONFIANZA BAJA - POSIBLE ANOMALÍA: Grandes discrepancias detectadas.")
            print("   (Este caso debería activar una alerta ética en Ethalgor)")
    print("="*50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 analizador_isbn.py <ISBN>")
        print("Ejemplo: python3 analizador_isbn.py 9789814696333")
        sys.exit(1)
    analizar_isbn(sys.argv[1])
