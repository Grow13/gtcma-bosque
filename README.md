# 🌳 Bosque GTCMA

**Sistema descentralizado para corrección y enriquecimiento de metadatos académicos**

El Bosque GTCMA es una arquitectura de árboles API conectados entre sí que permite extraer, corregir y enriquecer metadatos de documentos académicos (PDFs) utilizando IA local, OpenLibrary y servicios externos como DeepSeek API.

---

## 📋 Características

- ✅ Extracción de título, autores y año desde PDFs académicos
- ✅ Expansión de iniciales de autores (ej: `J. Thompson → John Thompson`)
- ✅ Arquitectura descentralizada tipo "bosque" (múltiples árboles que se consultan)
- ✅ Cliente inteligente que elige la mejor respuesta entre árboles
- ✅ Integración con DeepSeek API para expansión avanzada (Alma 4)
- ✅ Integración con OpenLibrary para datos biográficos de autores (Almas 31, 32)
- ✅ Capa ética **Éthalgor** que valida, limpia y asigna confianza a cada respuesta
- ✅ Preparado para ejecutarse con Docker o localmente

---

## 🗂️ Estructura del proyecto

```bash
gtcma-bosque/
├── README.md                 # Este archivo
├── ANILLO.md                 # Documentación del Anillo Sensuto
├── anillos_broadcast.html    # Simulación funcional del anillo
├── Dockerfile                # Para construir la imagen Docker
├── scripts/
│   ├── api_arbol.py          # Servidor Flask con 31 almas
│   ├── ethalgor.py           # Capa ética (validación y confianza)
│   ├── alma_openlibrary.py   # Alma 31 (OpenLibrary completa)
│   └── alma_openlibrary32.py # Alma 32 (OpenLibrary resumida)
└── (otros archivos históricos)



....
