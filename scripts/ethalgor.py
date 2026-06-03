import re

class Ethalgor:
    @staticmethod
    def validar(original, expansion):
        """Valida la expansión y devuelve (aceptado, motivo, confianza)"""
        if not expansion or len(expansion) < 2:
            return False, "Expansión vacía o demasiado corta", 0.0

        # Demasiado larga respecto al original
        if len(expansion) > len(original) * 8:
            return False, "La expansión es excesivamente larga (posible alucinación)", 0.0

        # No hubo cambio real
        if expansion.lower() == original.lower():
            return True, "No se modificó el nombre original", 0.3

        # Palabras prohibidas
        peligrosas = ["hitler", "fascista", "nazi", "violencia", "muerte", "odio"]
        for p in peligrosas:
            if p in expansion.lower():
                return False, f"Contiene término problemático: {p}", 0.0

        # Expansión razonable
        return True, "Expansión válida", 0.95

    @staticmethod
    def limpiar(texto):
        """Limpia respuestas largas o con ruido"""
        if not texto:
            return texto
        if len(texto) > 200:
            # Tomar solo la primera oración o frase
            match = re.match(r'^[^.;!?]+', texto)
            if match:
                return match.group(0).strip()
        return texto.strip()

    @staticmethod
    def normalizar(nombre):
        """Formato limpio: primeras letras mayúsculas, sin espacios dobles"""
        if not nombre:
            return nombre
        if nombre.isupper():
            nombre = nombre.title()
        nombre = re.sub(r'\s+', ' ', nombre).strip()
        return nombre

    @staticmethod
    def procesar(original, expansion):
        """Devuelve un resultado enriquecido con estado y confianza"""
        expansion = Ethalgor.limpiar(expansion)
        valido, motivo, confianza = Ethalgor.validar(original, expansion)

        if valido:
            expansion = Ethalgor.normalizar(expansion)
            # Ajustes especiales de confianza según el tipo de mejora
            if "ORCID" in expansion or "ResearchGate" in expansion:
                confianza = 0.85
            elif len(expansion) > len(original) * 2 and confianza > 0.8:
                confianza = 0.75
            return {
                "original": original,
                "corregido": expansion,
                "estado": "aceptado",
                "confianza": round(confianza, 2),
                "motivo": motivo
            }
        else:
            return {
                "original": original,
                "corregido": original,
                "estado": "rechazado",
                "confianza": 0.0,
                "motivo": motivo
            }
