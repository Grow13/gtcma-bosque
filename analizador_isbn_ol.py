#!/usr/bin/env python3
import requests
import sys
import re
import json

# ============================================================
# CARGA DE BASE DE CONOCIMIENTO EXTERNA
# ============================================================
def cargar_base_conocimiento():
    try:
        with open("base_conocimiento.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

BASE_CONOCIMIENTO = cargar_base_conocimiento()

# ============================================================
# CONSULTAS A FUENTES EXTERNAS
# ============================================================
def consultar_openlibrary(isbn):
    """Consulta OpenLibrary por ISBN y devuelve metadatos."""
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        key = f"ISBN:{isbn}"
        if key in data:
            libro = data[key]
            autores = [a.get("name", "") for a in libro.get("authors", [])]
            return {
                "encontrado": True,
                "titulo": libro.get("title", ""),
                "autores": autores,
                "editorial": libro.get("publishers", [{}])[0].get("name", ""),
                "anio": libro.get("publish_date", ""),
                "url": f"https://openlibrary.org/isbn/{isbn}"
            }
        else:
            return {"encontrado": False}
    except Exception as e:
        print(f"⚠️ Error en OpenLibrary: {e}")
        return {"encontrado": False}

def consultar_google_books(isbn):
    """Consulta Google Books por ISBN y devuelve metadatos (solo autores relevantes)."""
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get("totalItems", 0) > 0:
            libro = data["items"][0]["volumeInfo"]
            autores = libro.get("authors", [])
            return {"encontrado": True, "autores": autores}
    except Exception as e:
        print(f"⚠️ Error en Google Books: {e}")
    return {"encontrado": False, "autores": []}

def es_abreviatura(abrev, completo):
    """Verifica si 'abrev' es una abreviatura plausible de 'completo'."""
    if not abrev or not completo:
        return False
    partes_abrev = abrev.split()
    partes_completo = completo.split()
    if len(partes_abrev) != len(partes_completo):
        return False
    for pa, pc in zip(partes_abrev, partes_completo):
        if re.match(r'^[A-Z]\.$', pa) and pc.startswith(pa[0]):
            continue
        elif pa.lower() != pc.lower():
            return False
    return True

def generar_acciones(isbn, datos_ol, datos_gb):
    """Genera una lista de acciones inmediatas, incluyendo corrección de autores."""
    acciones = []
    
    # Acción 1: Abrir la página de OpenLibrary
    acciones.append(f"🌐 1. Abrir en navegador: {datos_ol['url']}")
    
    # Acción 2: Buscar en Google Books
    acciones.append(f"📚 2. Buscar en Google Books: https://books.google.com/books?vid=ISBN{isbn}")
    
    # Acción 3: Corregir formato del título
    if datos_ol['titulo'] != datos_ol['titulo'].title():
        acciones.append(f"✏️ 3. Corregir título: '{datos_ol['titulo']}' → '{datos_ol['titulo'].title()}'")
    
    # Acción 4: Corregir autores (comparando con Google Books)
    if datos_gb['encontrado'] and datos_gb['autores']:
        autocorrecciones = 0
        for i, autor_ol in enumerate(datos_ol['autores']):
            for autor_gb in datos_gb['autores']:
                if es_abreviatura(autor_ol, autor_gb):
                    acciones.append(f"👤 4.{i+1} Corregir autor: '{autor_ol}' → '{autor_gb}' (según Google Books)")
                    autocorrecciones += 1
                    break
        if autocorrecciones == 0 and datos_ol['autores']:
            acciones.append(f"👤 4. Verificar autores: {', '.join(datos_ol['autores'])} (no coinciden con Google Books)")
    elif datos_ol['autores']:
        for autor in datos_ol['autores']:
            if '.' in autor or len(autor.split()) < 2:
                acciones.append(f"👤 4. Investigar nombre completo del autor: '{autor}'")
                break
    
    # Acción 5: Alerta ética para ISBN conflictivo
    if isbn in BASE_CONOCIMIENTO:
        acciones.append(f"⚠️ 5. {BASE_CONOCIMIENTO[isbn]['alerta']}")
        acciones.append(f"🔍    Acción sugerida: {BASE_CONOCIMIENTO[isbn]['accion']}")
    
    return acciones

def analizar_isbn(isbn):
    print(f"\n🔍 Analizando ISBN: {isbn}\n")
    
    datos_ol = consultar_openlibrary(isbn)
    if not datos_ol["encontrado"]:
        print("❌ ISBN no encontrado en OpenLibrary.")
        return
    
    datos_gb = consultar_google_books(isbn)
    
    # Mostrar resultados
    print(f"📚 OpenLibrary:")
    print(f"   Título: {datos_ol['titulo']}")
    print(f"   Autores: {', '.join(datos_ol['autores'])}")
    print(f"   Editorial: {datos_ol['editorial']}")
    print(f"   Año: {datos_ol['anio']}")
    
    if datos_gb['encontrado']:
        print(f"\n📚 Google Books:")
        print(f"   Autores: {', '.join(datos_gb['autores'])}")
    else:
        print(f"\n⚠️ Google Books no devolvió datos para este ISBN.")
    
    # Generar y mostrar acciones
    print("\n" + "="*60)
    print("📋 ACCIONES INMEDIATAS PARA EL GTCMA:")
    print("="*60)
    
    acciones = generar_acciones(isbn, datos_ol, datos_gb)
    for accion in acciones:
        print(accion)
    
    print("\n" + "="*60)
    print("✅ Una vez completadas las acciones, documentar el resultado.")
    print("="*60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 analizador_isbn_ol.py <ISBN>")
        sys.exit(1)
    analizar_isbn(sys.argv[1])
