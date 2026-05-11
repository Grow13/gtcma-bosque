#!/usr/bin/env python3
import os
import random
import openai
from alma_openlibrary import alma_31 as alma_31_func
from alma_openlibrary32 import alma_32 as lib32
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
            model="deepseek-v4-pro",  # Modelo mas estable para respuestas directas
            messages=[
                {"role": "system", "content": "Eres un asistente academico. Responde SOLO con el nombre completo, sin explicaciones, sin puntos, sin comillas."},
                {"role": "user", "content": f"Nombre original: {autor}. Devuelve unicamente el nombre completo expandido."}
            ],
            temperature=0.1,
            max_tokens=25
        )
        resultado = resp.choices[0].message.content or ""
        # Limpiar caracteres no deseados
        resultado = resultado.replace('"', '').replace('.', '').strip()
        return resultado if resultado else {"J. Thompson": "John Thompson", "M. Garcia": "Maria Garcia"}.get(autor, autor)
    except Exception as e:
        return {"J. Thompson": "John Thompson", "M. Garcia": "Maria Garcia"}.get(autor, autor)
def alma_5(autor): return f"{autor} PhD"
def alma_6(autor): return f"Dr. {autor}"
def alma_7(autor): return f"{autor} (Universidad del Bosque)"
def alma_8(autor): return f"{autor} (Investigador)"
def alma_9(autor): return f"{autor} [DOI: 10.1000/xyz]"
def alma_10(autor): return f"{autor} (2024)"

# ============ ALMAS 11-20 ============
def alma_11(autor): return {"J. Thompson": "Jonathan Thompson", "M. Garcia": "Mariana Garcia"}.get(autor, f"Alma11: {autor}")
def alma_12(autor): return f"{autor}, A. (2024). Título del trabajo."
def alma_13(autor): return f"Ilustre {autor}"
def alma_14(autor): return f"{autor}, PhD"
def alma_15(autor): return f"{autor} | Universidad Nacional"
def alma_16(autor): return f"{autor} (Proyecto GTCMA)"
def alma_17(autor): return f"{autor} (Becario)"
def alma_18(autor): return f"{autor} (Premio 2024)"
def alma_19(autor): return f"{autor} en colaboración con MIT"
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
def alma_31(autor):
    return alma_31_func(autor)
def alma_32(autor):
    return lib32(autor)
ALMAS = {i: globals()[f'alma_{i}'] for i in range(1, 33)}

@app.route('/expandir', methods=['POST'])
def expandir():
    data = request.json
    autor = data.get('autor', '')
    alma_id = data.get('alma', random.randint(1, 32))
    raw = ALMAS[alma_id](autor)
    resultado = Ethalgor.procesar(autor, raw)
    resultado['alma'] = alma_id
    return jsonify(resultado)

@app.route('/salud', methods=['GET'])
def salud():
    return jsonify({'almas': len(ALMAS), 'ethalgor': 'activo'})

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    app.run(host='0.0.0.0', port=port)

EOF
