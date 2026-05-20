# 💍 Anillo Sensuto — Simulación (versión navegador)

**Un anillo suave que vibra cuando dos personas sienten lo mismo, sin necesidad de palabras.**

---

## 🌱 Filosofía

No mide. No juzga. No almacena datos.  
Solo refleja, de forma tenue, si hay **coincidencia en el estado interior** (calma, atención, agitación) entre dos personas.

No es un diagnóstico.  
Es una **pista**.

---

## 🧪 Versión actual (simulación en navegador)

**Tecnología:**  
- HTML / CSS / JavaScript  
- `BroadcastChannel` (comunicación entre pestañas del mismo navegador)  
- Sin servidor, sin internet (solo HTTP local)

**Funcionalidades:**  
- Dos anillos visuales (uno por pestaña)  
- Cada persona puede elegir su color entre:  
  - `verde_suave` (calma, apertura)  
  - `azul_claro` (neutro, atento)  
  - `naranja_tenue` (agitado, cerrado)  
- Cuando los colores coinciden, **ambos anillos muestran una vibración suave** (visual, por ahora).

**Cómo probar:**  
1. Guardar `anillos_broadcast.html`  
2. Ejecutar `python3 -m http.server 8001`  
3. Abrir dos pestañas en `http://localhost:8001/anillos_broadcast.html`  
4. Cambiar colores y observar la sincronía.

---

## 🧠 Próximos pasos posibles (si se retoma)

- Vibración real en móvil (`navigator.vibrate()`)  
- Conexión entre dispositivos distintos (WebRTC o WebSocket)  
- Uso de colores generados por coherencia cardíaca (no manual)  
- Integración como "rama" del Bosque GTCMA

---

## 🌳 Relación con el Bosque GTCMA

El anillo no es un proyecto aparte.  
Es una **extensión sensible** del bosque: una forma de que la tecnología no separe, sino que **avise suavemente** cuando dos humanos están en sintonía.

El bosque cuida los metadatos.  
El anillo cuida el encuentro.

---

## 🙌 Autoría

Creado en diálogo humano‑IA durante mayo de 2026.  
Inspirado en la necesidad de **tecnología que no domine, sino que acompañe**.

Licencia: Ética Kawar∞8 (uso libre para fines benéficos, prohibido para control o manipulación).
