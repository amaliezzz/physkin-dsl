import math
from ast_nodes import (
    Programa, DeclaracionParticula,
    ImprimirConsulta, ImprimirCadena,
    ConsultaPosicion, ConsultaVelocidad, ConsultaColision, Vector2D
)

class Evaluator:
    def __init__(self):
        self.particles = {}

    def run(self, ast_root):
        for stmt in ast_root.instrucciones:
            self._exec(stmt)

    def _exec(self, node):
        if isinstance(node, DeclaracionParticula):
            def val(nodo):
                return (nodo.x, nodo.y) if isinstance(nodo, Vector2D) else nodo.valor

            x0 = val(node.posicion)
            v0 = val(node.velocidad)
            if node.aceleracion is not None:
                a = val(node.aceleracion)
            else:
                a = (0, 0) if isinstance(x0, tuple) else 0
            self.particles[node.nombre] = {'x0': x0, 'v0': v0, 'a': a}

        elif isinstance(node, ImprimirConsulta):
            self._eval_query(node.consulta)

        elif isinstance(node, ImprimirCadena):
            print(node.valor)

        elif isinstance(node, ConsultaColision):
            self._eval_colision(node)

    def _eval_query(self, consulta):
        p = self.particles.get(consulta.particula)
        if p is None:
            return

        t = consulta.tiempo.valor
        x0 = p['x0']
        v0 = p['v0']
        a = p['a']

        es_2d = isinstance(x0, tuple)

        if es_2d:
            es_mru = (a[0] == 0 and a[1] == 0)
            mov = "MRU" if es_mru else "MRUA"

            if isinstance(consulta, ConsultaPosicion):
                px = x0[0] + v0[0] * t + 0.5 * a[0] * t ** 2
                py = x0[1] + v0[1] * t + 0.5 * a[1] * t ** 2
                print(f"[{mov}] posicion({consulta.particula}) en t={t}s: ({px:.2f}, {py:.2f}) m")

            elif isinstance(consulta, ConsultaVelocidad):
                vx = v0[0] + a[0] * t
                vy = v0[1] + a[1] * t
                print(f"[{mov}] velocidad({consulta.particula}) en t={t}s: ({vx:.2f}, {vy:.2f}) m/s")

        else:
            es_mru = (a == 0)
            mov = "MRU" if es_mru else "MRUA"

            if isinstance(consulta, ConsultaPosicion):
                pos = x0 + v0 * t if es_mru else x0 + v0 * t + 0.5 * a * t ** 2
                print(f"[{mov}] posicion({consulta.particula}) en t={t}s: {pos:.2f} m")

            elif isinstance(consulta, ConsultaVelocidad):
                vel = v0 if es_mru else v0 + a * t
                print(f"[{mov}] velocidad({consulta.particula}) en t={t}s: {vel:.2f} m/s")

    def _eval_colision(self, node):
        p1 = self.particles.get(node.particula1)
        p2 = self.particles.get(node.particula2)
        if p1 is None or p2 is None:
            return

        # x1(t) = x2(t)  =>  A*t² + B*t + C = 0
        A = 0.5 * (p1['a'] - p2['a'])
        B = p1['v0'] - p2['v0']
        C = p1['x0'] - p2['x0']

        soluciones = []

        if A == 0:
            # Ecuación lineal: B*t + C = 0
            if B == 0:
                if C == 0:
                    print(f"[COLISION] {node.particula1} y {node.particula2} siempre coinciden")
                else:
                    print(f"[COLISION] {node.particula1} y {node.particula2} nunca colisionan")
                return
            soluciones = [-C / B]
        else:
            # Ecuación cuadrática
            disc = B ** 2 - 4 * A * C
            if disc < 0:
                print(f"[COLISION] {node.particula1} y {node.particula2} nunca colisionan")
                return
            raiz = math.sqrt(disc)
            t1 = (-B + raiz) / (2 * A)
            t2 = (-B - raiz) / (2 * A)
            soluciones = sorted(set([t1, t2]))

        validas = [t for t in soluciones if t >= 0]
        if not validas:
            print(f"[COLISION] {node.particula1} y {node.particula2} nunca colisionan (solo t < 0)")
        else:
            for t in validas:
                print(f"[COLISION] {node.particula1} y {node.particula2} colisionan en t={t:.2f}s")


def evaluate(ast):
    Evaluator().run(ast)