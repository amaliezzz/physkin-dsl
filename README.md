### PhysKin DSL
PhysKin es un mini-lenguaje de dominio específico (DSL) diseñado para modelar partículas con posición, velocidad y aceleración, y calcular su estado en cualquier instante mediante las fórmulas del MRU y MRUA. El analizador cubre las tres fases clásicas — **léxico, sintáctico y semántico** — y reporta cada error con línea y columna. La gramática formal del lenguaje se encuentra en [`docs/grammar.md`](docs/grammar.md).

---

#### Requisitos
- Python 3.10 o superior
- PLY 3.11

#### Instalación

**1. Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd physkin-dsl
```

**2. Crear y activar el entorno virtual**
```bash
python -m venv venv
```
```bash
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

**3. Instalar dependencias**
```bash
pip install ply==3.11
```

---

#### Cómo ejecutar

El punto de entrada es `src/main.py`. Recibe como argumento el archivo .pk a analizar.
```bash
python src/main.py tests/programa_valido.pk
```
El analizador ejecuta las fases en orden: léxico → sintáctico → semántico.
Si todas las fases son correctas, el programa termina sin salida (comportamiento esperado de un compilador).
Si se encuentra un error en alguna fase, se reporta y la ejecución se detiene antes de pasar a la siguiente.

#### Errores

Los errores se reportan con el formato:
```
Error <fase> [línea X, columna Y]: <mensaje>
```
Donde `<fase>` puede ser léxico, sintáctico o semántico.

Ejemplos:
```
Error léxico     [línea 4, columna 12]: carácter inesperado '@'
Error sintáctico [línea 7, columna 3]: se esperaba un número, pero se encontró ';'
Error semántico  [línea 10, columna 1]: el tiempo debe ser ≥ 0, se recibió -5
```

#### Archivos de prueba

| Archivo | Qué contiene |
|---|---|
| `tests/programa_valido.pk` | Programa correcto en las tres fases |
| `tests/error_sintactico.pk` | Errores sintácticos aislados |
| `tests/error_semantico.pk` | Errores semánticos con sintaxis correcta |

```bash
python src/main.py tests/programa_valido.pk
python src/main.py tests/error_sintactico.pk
python src/main.py tests/error_semantico.pk
```

#### Flag `--eval`

El flag `--eval` activa el evaluador. Solo tiene efecto si el programa es válido en las tres fases. Calcula y muestra la posición o velocidad de cada partícula usando las fórmulas de MRU y MRUA.
```bash
python src/main.py tests/programa_valido.pk --eval
```
```
[MRUA] posicion(p1) en t=5s: 75.00 m
[MRUA] velocidad(p1) en t=5s: 20.00 m/s
[MRU]  posicion(p2) en t=10s: 50.00 m
```

---

#### Extensiones opcionales

La detección de colisiones entre partículas y el soporte 2D están disponibles en la rama `extension-2d-colision`.