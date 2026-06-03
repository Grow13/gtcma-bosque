#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random
import openai
from flask import Flask, request, jsonify
from ethalgor import Ethalgor

app = Flask(__name__)
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

# ============ ALMAS 1-10 ============
def alma_1(autor): return {"J. Thompson": "John Thompson", "M. Garcia": "Maria Garcia"}.get(autor, f"Alma1: {autor}")
def alma_2(autor): return autor.upper().replace(".", "").strip()
def alma_3(autor): return autor[::-1]

def alma_4(autor):
    if not DEEPSEEK_API_KEY:
        return {"J. Thompson": "John Thompson", "M. Garcia": "Maria Garcia"}.get(autor, autor)
    try:
        client = openai.OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")
        resp = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=[{"role": "user", "content": f"Devuelve SOLO el nombre completo de {autor}"}],
            temperature=0.1,
            max_tokens=25
        )
        resultado = resp.choices[0].message.content or ""
        resultado = resultado.replace('"', '').strip()
        return resultado if resultado else autor
    except:
        return autor

def alma_5(autor): return f"{autor} PhD"
def alma_6(autor): return f"Dr. {autor}"
def alma_7(autor): return f"{autor} (Universidad del Bosque)"
def alma_8(autor): return f"{autor} (Investigador)"
def alma_9(autor): return f"{autor} [DOI: 10.1000/xyz]"
def alma_10(autor): return f"{autor} (2024)"

# ============ ALMAS 11-20 ============
def alma_11(autor): return {"J. Thompson": "Jonathan Thompson", "M. Garcia": "Mariana Garcia"}.get(autor, f"Alma11: {autor}")
def alma_12(autor): return f"{autor}, A. (2024). Titulo del trabajo."
def alma_13(autor): return f"Ilustre {autor}"
def alma_14(autor): return f"{autor}, PhD"
def alma_15(autor): return f"{autor} | Universidad Nacional"
def alma_16(autor): return f"{autor} (Proyecto GTCMA)"
def alma_17(autor): return f"{autor} (Becario)"
def alma_18(autor): return f"{autor} (Premio 2024)"
def alma_19(autor): return f"{autor} en colaboracion con MIT"
def alma_20(autor): return f"{autor} (Investigador Senior)"

# ============ ALMAS 21-30 ============
def alma_21(autor): return f"{autor} (Universidad de Oxford)"
def alma_22(autor): return f"{autor}, Ph.D."
def alma_23(autor): return f"Prof. {autor}"
def alma_24(autor): return f"{autor} (Premio Nobel 2025)"
def alma_25(autor): return f"{autor} | ORCID: 0000-0000-0000"
def alma_26(autor): return f"{autor} (Scopus: 12345678)"
def alma_27(autor): partes = autor.split(); return f"{partes[0][0].upper()}. {partes[-1]}" if len(partes) >= 2 else autor
def alma_28(autor): return f"{autor} (h-index: 42)"
def alma_29(autor): return f"{autor} (Google Scholar)"
def alma_30(autor): return f"{autor} | ResearchGate"

# ============ ALMA 31 (OpenLibrary) ============
def alma_31(autor):
    import requests
    nombre = autor.replace('.', '').replace(' ', '+')
    url = f"https://openlibrary.org/search/authors.json?q={nombre}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if not data.get('docs'):
            return autor
        a = data['docs'][0]
        nombre = a.get('name', autor)
        nacimiento = a.get('birth_date', '')
        obras = a.get('work_count', 0)
        promedio = a.get('ratings_average', 0)
        top = a.get('top_work', '')
        if nacimiento and top:
            return f"{nombre} ({nacimiento}) - {obras} obras, ⭐{promedio:.2f}. Obra destacada: {top}"
        elif nacimiento:
            return f"{nombre} ({nacimiento})"
        return nombre
    except:
        return autor

# ============ DICCIONARIO DE ALMAS ============
ALMAS = {i: globals()[f'alma_{i}'] for i in range(1, 32)}

# ============ ENDPOINTS ============
@app.route('/expandir', methods=['POST'])
def expandir():
    data = request.json
    autor = data.get('autor', '')
    alma_id = data.get('alma', random.randint(1, 31))
    isbn = data.get('isbn', None)
    titulo = data.get('titulo', None)
    
    # Obtener expansión del alma correspondiente
    raw = ALMAS[alma_id](autor)
    
    # Pasar por Éthalgor (filtro ético)
    aceptado, motivo, confianza = Ethalgor.validar_expansion(
        original=autor,
        expansion=raw,
        isbn=isbn,
        titulo=titulo
    )
    
    if not aceptado:
        return jsonify({
            'error': 'Expansión rechazada por Éthalgor',
            'motivo': motivo,
            'original': autor,
            'expansion_intentada': raw,
            'alma': alma_id
        }), 400
    
    return jsonify({
        'original': autor,
        'corregido': raw,
        'alma': alma_id,
        'confianza': confianza,
        'ethalgor_motivo': motivo
    })

@app.route('/salud', methods=['GET'])
def salud():
    return jsonify({'almas': len(ALMAS), 'ethalgor': 'activo'})

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    app.run(host='0.0.0.0', port=port)
