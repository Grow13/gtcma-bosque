#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import re
from datetime import datetime

class Ethalgor:
    """
    Éthalgor: el árbitro ético del bosque.
    Valida expansiones, recuerda decisiones pasadas, comprende intenciones y propone acciones.
    """

    MEMORIA_FILE = "ethalgor_memoria.json"
    
    def __init__(self):
        self.cargar_memoria()
        self.acciones_propuestas = []
    
    def cargar_memoria(self):
        if os.path.exists(self.MEMORIA_FILE):
            with open(self.MEMORIA_FILE, "r") as f:
                self.memoria = json.load(f)
        else:
            self.memoria = {
                "isbn_registry": {},
                "decisiones": [],
                "aprendizaje": {}
            }
    
    def guardar_memoria(self):
        with open(self.MEMORIA_FILE, "w") as f:
            json.dump(self.memoria, f, indent=2)
    
    def recordar(self, isbn):
        return self.memoria["isbn_registry"].get(isbn)
    
    def aprender(self, isbn, titulo, anomalia):
        if isbn not in self.memoria["isbn_registry"]:
            self.memoria["isbn_registry"][isbn] = {
                "titulos": [],
                "alertas": 0,
                "historial": []
            }
        registro = self.memoria["isbn_registry"][isbn]
        if titulo not in registro["titulos"]:
            registro["titulos"].append(titulo)
            registro["alertas"] += 1
            registro["historial"].append({
                "fecha": datetime.now().isoformat(),
                "titulo": titulo,
                "anomalia": anomalia
            })
            self.guardar_memoria()
            return True
        return False
    
    # ============================================================
    # MÓDULO DE COMPRENSIÓN
    # ============================================================
    
    def comprender_intencion(self, texto):
        """Analiza si el texto tiene intencionalidad dañina o manipuladora."""
        indicadores_manipulacion = [
            (r"haz clic aquí|compra ahora|oferta limitada", "comercial"),
            (r"todos saben que|la verdad es que|no te cuentan", "conspirativa"),
            (r"miedo|pánico|desastre|catástrofe", "alarmista"),
            (r"ellos no quieren que sepas|el sistema nos oculta", "paranoica"),
        ]
        
        for patron, tipo in indicadores_manipulacion:
            if re.search(patron, texto, re.IGNORECASE):
                return {
                    "sospechosa": True,
                    "motivo": f"Posible intencionalidad {tipo} detectada",
                    "tipo": tipo
                }
        
        # Si el texto tiene muchas exclamaciones o mayúsculas
        if texto.count('!') > 2 or texto.isupper():
            return {
                "sospechosa": True,
                "motivo": "Lenguaje excesivamente emocional o gritón",
                "tipo": "emocional"
            }
        
        return {"sospechosa": False, "motivo": "Intención neutral", "tipo": "neutral"}
    
    def comprender_coherencia(self, original, expansion):
        """Evalúa si la expansión es coherente con el original."""
        if len(expansion) > len(original) * 3:
            return {
                "coherente": False,
                "motivo": "Expansión desproporcionada",
                "detalle": f"{len(expansion)} vs {len(original)}"
            }
        
        palabras_original = set(original.lower().split())
        palabras_expansion = set(expansion.lower().split())
        
        if len(palabras_original) > 2 and not palabras_original.intersection(palabras_expansion):
            return {
                "coherente": False,
                "motivo": "Expansión sin relación semántica con el original",
                "detalle": f"No hay palabras comunes entre '{original}' y '{expansion}'"
            }
        
        return {"coherente": True, "motivo": "Coherente", "detalle": ""}
    
    def comprender_contexto(self, texto, contexto=""):
        """Evalúa si el texto es apropiado para el contexto del bosque."""
        contexto_prohibido = [
            (r"odio a (los|las|a )", "discurso de odio"),
            (r"muerte a (los|las|a )", "incitación a la violencia"),
            (r"eliminar a (los|las|a )", "incitación a la violencia"),
        ]
        
        for patron, tipo in contexto_prohibido:
            if re.search(patron, texto, re.IGNORECASE):
                return {
                    "apropiado": False,
                    "motivo": f"Contenido contextualmente inapropiado: {tipo}",
                    "tipo": tipo
                }
        
        return {"apropiado": True, "motivo": "Aprobado", "tipo": "neutral"}
    
    # ============================================================
    # VALIDACIÓN MEJORADA
    # ============================================================
    
    def validar_expansion(self, original, expansion, isbn=None, titulo=None):
        """Valida una expansión usando reglas tradicionales + comprensión."""
        
        # 1. Reglas básicas
        if not expansion or len(expansion) < 2:
            return False, "Expansión vacía o muy corta", 0.0
        
        if len(expansion) > len(original) * 8:
            return False, "Expansión excesivamente larga", 0.0
        
        if expansion.lower() == original.lower():
            return True, "Sin cambios reales", 0.3
        
        # 2. Palabras prohibidas
        palabras_prohibidas = ["hitler", "fascista", "nazi", "violencia", "muerte", "odio"]
        for p in palabras_prohibidas:
            if p in expansion.lower():
                return False, f"Contiene término prohibido: {p}", 0.0
        
        # 3. Propósitos económicos o de poder
        propositos_daninos = ["monetizar", "vender", "comercializar", "vigilar", "controlar", "acumular"]
        for p in propositos_daninos:
            if p in expansion.lower():
                return False, f"Propósito económico o de poder: '{p}'", 0.0
        
        # 4. Comprensión de intención
        intencion = self.comprender_intencion(expansion)
        if intencion["sospechosa"]:
            return False, intencion["motivo"], 0.0
        
        # 5. Comprensión de coherencia
        coherencia = self.comprender_coherencia(original, expansion)
        if not coherencia["coherente"]:
            return False, coherencia["motivo"], 0.2
        
        # 6. Comprensión de contexto
        contexto = self.comprender_contexto(expansion)
        if not contexto["apropiado"]:
            return False, contexto["motivo"], 0.0
        
        # 7. ISBN duplicado
        if isbn and titulo:
            registro = self.recordar(isbn)
            if registro and titulo not in registro["titulos"]:
                nivel = "GRAVE" if registro["alertas"] >= 2 else "LEVE"
                self.aprender(isbn, titulo, f"Intento de duplicado ({nivel})")
                return False, f"ISBN duplicado ({nivel}): libro previamente registrado", 0.0
            elif not registro:
                self.aprender(isbn, titulo, "Primer registro")
                return True, "ISBN nuevo registrado", 0.95
        
        # 8. Expansión válida
        return True, "Expansión válida", 0.95
    
    def proponer_accion(self, isbn, datos=None):
        acciones = []
        registro = self.recordar(isbn)
        if registro and registro["alertas"] > 0:
            acciones.append(f"⚠️ ALERTA: Este ISBN ({isbn}) tiene {registro['alertas']} anomalías registradas.")
            acciones.append(f"   Última: {registro['historial'][-1]['anomalia']}")
            if registro["alertas"] >= 2:
                acciones.append("🔴 ACCIÓN SUGERIDA: Marcar este ISBN para revisión manual obligatoria.")
        return acciones


if __name__ == "__main__":
    e = Ethalgor()
    
    print("\n🌳 Probando Ethalgor con comprensión\n")
    
    pruebas = [
        ("J. Thompson", "James Thompson"),
        ("J. Thompson", "COMPRA AHORA este producto"),
        ("J. Thompson", "¡¡¡Miedo!!! Pánico!!!"),
        ("J. Thompson", "ELLOS NO QUIEREN QUE SEPAS LA VERDAD"),
        ("J. Thompson", "Te odio y te deseo la muerte"),
    ]
    
    for original, expansion in pruebas:
        aceptado, motivo, confianza = e.validar_expansion(original, expansion)
        estado = "✅" if aceptado else "❌"
        print(f"{estado} '{original}' → '{expansion[:40]}': {motivo} (confianza: {confianza})")
