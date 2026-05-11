import re

class Ethalgor:
    @staticmethod
    def validar(original, expansion):
        if not expansion or len(expansion) < 2:
            return False, "Expansión vacía o muy corta"
        
        if len(expansion) > len(original) * 8:
            return False, "Expansión excesivamente larga"
        
        if expansion.lower() == original.lower():
            return True, "Sin cambios reales"
        
        palabras_prohibidas = ["hitler", "fascista", "nazi", "violencia"]
        for p in palabras_prohibidas:
            if p in expansion.lower():
                return False, f"Contiene: {p}"
        
        return True, "Válida"
    
    @staticmethod
    def limpiar(texto):
        if not texto or len(texto) <= 100:
            return texto
        import re
        match = re.match(r'^[^.;]+', texto)
        return match.group(0).strip() if match else texto
    
    @staticmethod
    def corregir_formato(nombre):
        if not nombre:
            return nombre
        if nombre.isupper():
            nombre = nombre.title()
        return re.sub(r'\s+', ' ', nombre).strip()
    
    @staticmethod
    def procesar(original, expansion):
        expansion = Ethalgor.limpiar(expansion)
        valido, motivo = Ethalgor.validar(original, expansion)
        
        if not valido:
            return {
                "original": original,
                "corregido": original,
                "estado": "rechazado",
                "motivo": motivo,
                "confianza": 0.0
            }
        
        expansion = Ethalgor.corregir_formato(expansion)
        confianza = 0.95
        if expansion == original:
            confianza = 0.3
        elif "ORCID" in expansion or "ResearchGate" in expansion:
            confianza = 0.85
        elif len(expansion) > len(original) * 2:
            confianza = 0.75
        
        return {
            "original": original,
            "corregido": expansion,
            "estado": "aceptado",
            "confianza": confianza
        }
