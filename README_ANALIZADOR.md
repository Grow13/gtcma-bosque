# 📚 Analizador de ISBN para el GTCMA

**Herramienta de código abierto para la validación y corrección de metadatos académicos.**

Este script (`analizador_isbn_ol.py`) permite analizar un ISBN consultando **OpenLibrary** y genera **acciones inmediatas** para que un miembro del **GTCMA** (Grupo de Trabajo para la Corrección de Metadatos Académicos) pueda:

1.  Verificar la calidad de los metadatos.
2.  Detectar anomalías conocidas (alertas éticas).
3.  Documentar los hallazgos en el repositorio.

---

## 🚀 Uso

```bash
python3 analizador_isbn_ol.py <ISBN>
