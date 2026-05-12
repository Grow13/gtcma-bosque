# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import os
import random
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

# ============ ALMAS 1-30 (simplificadas) ============
def alma_1(autor): return {"J. Thompson": "John Thompson", "M. Garcia": "Maria Garcia"}.get(autor, autor)
def alma_2(autor): return autor.upper().replace(".", "").strip()
def alma_3(autor): return autor[::-1]
def alma_4(autor):
    if not DEEPSEEK_API_KEY:
        return autor
    try:
        client = openai.OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")
        resp = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=[{"role": "user", "content": f"Devuelve SOLO el nombre completo de {autor}"}],
            temperature=0.1,
            max_tokens=25
        )
        return resp.choices[0].message.content.strip() or autor
    except:
        return autor

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
            return f"{nombre} ({nacimiento}) - {obras} obras, {promedio:.2f} estrellas. Obra destacada: {top}"
        return nombre
    except:
        return autor

# Almas 5-30 (simplificadas)
for i in range(5, 31):
    def make_func(i):
        return lambda autor: f"Alma{i}: {autor}"
    globals()[f'alma_{i}'] = make_func(i)

ALMAS = {i: globals()[f'alma_{i}'] for i in range(1, 32)}

@app.route('/expandir', methods=['POST'])
def expandir():
    data = request.json
    autor = data.get('autor', '')
    alma_id = data.get('alma', random.randint(1, 31))
    if alma_id not in ALMAS:
        return jsonify({'error': 'Alma no existe'})
    corregido = ALMAS[alma_id](autor)
    return jsonify({'alma': alma_id, 'original': autor, 'corregido': corregido})

@app.route('/salud', methods=['GET'])
def salud():
    return jsonify({'almas': len(ALMAS)})

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    app.run(host='0.0.0.0', port=port)
