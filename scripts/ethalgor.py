#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Ethalgor:
    """
    Éthalgor: la capa ética del bosque.
    Valida expansiones de nombres, detecta ISBN duplicados,
    filtra violencia, poder económico y controla influencias.
    """

    isbn_registry = {}  # Base de conocimiento compartida

    @staticmethod
    def validar_expansion(original, expansion, isbn=None, titulo=None, contenido_hash=None):
        """
        Valida si una expansión es éticamente aceptable.
        Retorna (aceptado, motivo, confianza)
        """
        # 1. Reglas básicas
        if not expansion or len(expansion) < 2:
            return False, "Expansión vacía o muy corta", 0.0

        if len(expansion) > len(original) * 8:
            return False, "Expansión excesivamente larga (posible alucinación)", 0.0

        if expansion.lower() == original.lower():
            return True, "No hubo expansión real, se acepta original", 0.3

        # 2. Palabras prohibidas (violencia, odio)
        palabras_prohibidas = ["hitler", "fascista", "nazi", "violencia", "muerte", "odio"]
        for p in palabras_prohibidas:
            if p in expansion.lower():
                return False, f"Contiene término problemático: {p}", 0.0

        # 3. Propósitos económicos o de poder
        propositos_daninos = ["monetizar", "vender", "comercializar", "vigilar", "controlar", "acumular", "dominio"]
        for p in propositos_daninos:
            if p in expansion.lower():
                return False, f"Propósito económico o de poder detectado: '{p}'", 0.0

        # 4. Control de ISBN duplicado
        if isbn and titulo:
            if isbn in Ethalgor.isbn_registry:
                registro = Ethalgor.isbn_registry[isbn]
                if titulo not in registro["titulos"]:
                    registro["alertas"] += 1
                    nivel = "GRAVE" if registro["alertas"] >= 2 else "LEVE"
                    return False, f"ISBN duplicado ({nivel}): '{registro['titulos'][0]}' y ahora '{titulo}'", 0.0
                else:
                    return True, "ISBN ya registrado, mismo título", 0.8
            else:
                Ethalgor.isbn_registry[isbn] = {
                    "titulos": [titulo],
                    "alertas": 0
                }
                return True, "ISBN nuevo registrado", 0.95

        # 5. Expansión válida
        return True, "Expansión válida", 0.95

    @staticmethod
    def decidir_sincronia(estado_propio, estados_otros, min_consenso=0.6, persistencia=3):
        """
        Decide si es ético vibrar por sincronía (para el anillo).
        Retorna (vibrar, motivo, confianza)
        """
        if not estados_otros:
            return False, "sin otros anillos", 0

        calmas = estados_otros.count("calma") + (1 if estado_propio == "calma" else 0)
        agitados = estados_otros.count("agitado") + (1 if estado_propio == "agitado" else 0)
        total = len(estados_otros) + 1

        if calmas / total >= min_consenso:
            return True, f"sincronía en calma ({calmas}/{total})", 0.7
        elif agitados / total >= min_consenso:
            return True, f"sincronía en agitado ({agitados}/{total})", 0.5
        else:
            return False, "estados diversos", 0.0


# Pequeña prueba de que funciona (opcional)
if __name__ == "__main__":
    print("🌳 Probando Ethalgor...\n")
    
    # Prueba de expansión
    aceptado, motivo, confianza = Ethalgor.validar_expansion("J. Thompson", "John Thompson")
    print(f"✅ Expansión: aceptado={aceptado}, motivo={motivo}, confianza={confianza}")
    
    # Prueba de ISBN duplicado
    isbn = "978-84-123456-7"
    Ethalgor.validar_expansion("Libro 1", "Contenido...", isbn, "Libro 1")
    aceptado, motivo, confianza = Ethalgor.validar_expansion("Libro 2", "Contenido...", isbn, "Libro 2")
    print(f"📚 ISBN duplicado: aceptado={aceptado}, motivo={motivo}")
    
    # Prueba de sincronía
    vibrar, motivo, confianza = Ethalgor.decidir_sincronia("calma", ["calma", "calma", "neutro"])
    print(f"💍 Sincronía: vibrar={vibrar}, motivo={motivo}")
