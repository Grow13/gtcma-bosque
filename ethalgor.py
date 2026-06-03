#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

class Ethalgor:
    """
    Éthalgor: el árbitro ético del bosque.
    Valida expansiones, recuerda decisiones pasadas y propone acciones.
    """

    MEMORIA_FILE = "ethalgor_memoria.json"
    
    def __init__(self):
        self.cargar_memoria()
        self.acciones_propuestas = []
    
    def cargar_memoria(self):
        """Carga el historial de decisiones pasadas."""
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
        """Guarda el historial para futuras ejecuciones."""
        with open(self.MEMORIA_FILE, "w") as f:
            json.dump(self.memoria, f, indent=2)
    
    def recordar(self, isbn):
        """Recuerda si este ISBN ya ha tenido problemas."""
        return self.memoria["isbn_registry"].get(isbn)
    
    def aprender(self, isbn, titulo, anomalia):
        """Aprende de una nueva anomalía y la registra."""
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
    
    def validar_expansion(self, original, expansion, isbn=None, titulo=None):
        """Valida una expansión (versión mejorada con memoria)."""
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
        
        # 4. ISBN duplicado (con memoria)
        if isbn and titulo:
            registro = self.recordar(isbn)
            if registro and titulo not in registro["titulos"]:
                nivel = "GRAVE" if registro["alertas"] >= 2 else "LEVE"
                self.aprender(isbn, titulo, f"Intento de duplicado ({nivel})")
                return False, f"ISBN duplicado ({nivel}): libro previamente registrado", 0.0
            elif not registro:
                self.aprender(isbn, titulo, "Primer registro")
                return True, "ISBN nuevo registrado", 0.95
        
        # 5. Expansión válida
        return True, "Expansión válida", 0.95
    
    def proponer_accion(self, isbn, datos=None):
        """Propone acciones concretas basadas en el análisis."""
        acciones = []
        registro = self.recordar(isbn)
        
        if registro and registro["alertas"] > 0:
            acciones.append(f"⚠️ ALERTA: Este ISBN ({isbn}) tiene {registro['alertas']} anomalías registradas.")
            acciones.append(f"   Última: {registro['historial'][-1]['anomalia']}")
            
            if registro["alertas"] >= 2:
                acciones.append("🔴 ACCIÓN SUGERIDA: Marcar este ISBN para revisión manual obligatoria.")
                acciones.append("   Una vez revisado, si es correcto, resetear el contador de alertas.")
        
        return acciones


# Pequeña prueba integrada
if __name__ == "__main__":
    e = Ethalgor()
    
    print("\n🌳 Probando Ethalgor con ISBN conflictivo\n")
    isbn = "9789814696333"
    
    # Primera consulta (registra el ISBN)
    e.validar_expansion("Modeling Love Dynamics", "Modeling Love Dynamics", isbn, "Modeling Love Dynamics")
    
    # Segunda consulta (debe generar alerta)
    aceptado, motivo, confianza = e.validar_expansion(
        "Algoritmos del corazón", 
        "Algoritmos del corazón", 
        isbn, 
        "Algoritmos del corazón"
    )
    print(f"Resultado: {'✅ ACEPTADO' if aceptado else '❌ RECHAZADO'} - {motivo} (confianza: {confianza})")
    
    # Proponer acciones
    acciones = e.proponer_accion(isbn)
    for accion in acciones:
        print(accion)
