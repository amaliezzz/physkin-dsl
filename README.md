# PhysKin DSL — Extensiones opcionales

Esta rama (`extension-2d-colision`) parte de `main` e implementa las dos
extensiones opcionales del proyecto: detección de colisión entre partículas
y soporte para movimiento en 2D.

Los programas 1D existentes funcionan sin ningún cambio.

---

## Detección de colisión

### Sintaxis

```
imprimir colision(p1, p2);
```

### Descripción

Calcula en qué instante dos partículas ocupan la misma posición. Partiendo
de las ecuaciones de movimiento de cada una:

```
x₁(t) = x₀₁ + v₀₁·t + ½·a₁·t²
x₂(t) = x₀₂ + v₀₂·t + ½·a₂·t²
```

Igualando `x₁(t) = x₂(t)` y reorganizando se obtiene:

```
((a₁ - a₂) / 2) · t²  +  (v₀₁ - v₀₂) · t  +  (x₀₁ - x₀₂)  =  0
```

- Si `(a₁ - a₂) = 0` la ecuación es lineal y se despeja `t` directamente.
- Si no, se aplica la fórmula cuadrática. El discriminante determina si hay
  cero, una o dos soluciones reales.
- Solo se reportan soluciones con `t ≥ 0`.

### Ejemplo

```physkin
// Se encuentran en x = 50 m
particula p1 posicion=0   velocidad=10  aceleracion=0;
particula p2 posicion=100 velocidad=-10 aceleracion=0;
imprimir colision(p1, p2);

// p3 nunca alcanza a p4
particula p3 posicion=0   velocidad=5  aceleracion=0;
particula p4 posicion=100 velocidad=10 aceleracion=20;
imprimir colision(p3, p4);
```

### Ejecución

```bash
python src/main.py tests/prueba_colision.pk --eval
```

Salida esperada:

```
[COLISION] p1 y p2 colisionan en t=5.00s
[COLISION] p3 y p4 nunca colisionan
```

---

## Movimiento 2D

### Sintaxis

```
particula p posicion=(x, y) velocidad=(vx, vy) aceleracion=(ax, ay);
```

### Descripción

Extiende la declaración de partículas para aceptar vectores `(x, y)` en
lugar de escalares. Cada componente se evalúa de forma independiente con
las mismas fórmulas MRU/MRUA:

```
x(t) = x₀ + vx₀·t + ½·ax·t²
y(t) = y₀ + vy₀·t + ½·ay·t²
```

Para la velocidad:

```
vx(t) = vx₀ + ax·t
vy(t) = vy₀ + ay·t
```

El movimiento es MRU si ambas componentes de la aceleración son cero
(`ax = 0` y `ay = 0`), y MRUA en caso contrario.

Las consultas `posicion` y `velocidad` funcionan igual que en 1D e imprimen
ambas componentes:

```
[MRUA] posicion(p) en t=2s: (6.00, 0.40) m
[MRUA] velocidad(p) en t=2s: (3.00, -9.60) m/s
```

### Regla semántica

Posición, velocidad y aceleración deben ser todas del mismo tipo: o todas
escalares (1D) o todas vectores (2D). Mezclarlas es un error semántico.

### Ejemplo

```physkin
// Proyectil: velocidad horizontal constante, gravedad en y
particula p1 posicion=(0, 0) velocidad=(3, 10) aceleracion=(0, -9.8);

// Partícula 1D en el mismo programa (retrocompatibilidad)
particula p2 posicion=100 velocidad=-5 aceleracion=0;

imprimir posicion(p1) en 2;
imprimir velocidad(p1) en 2;
imprimir posicion(p2) en 2;
```

### Ejecución

```bash
python src/main.py tests/prueba_2d.pk --eval
```

Salida esperada:

```
[MRUA] posicion(p1) en t=2s: (6.00, 0.40) m
[MRUA] velocidad(p1) en t=2s: (3.00, -9.60) m/s
[MRU] posicion(p2) en t=2s: 90.00 m
```
