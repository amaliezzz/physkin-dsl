import math
from ast_nodes import (
    Programa, DeclaracionParticula,
    ImprimirConsulta, ImprimirCadena,
    ConsultaPosicion, ConsultaVelocidad, ConsultaColision
)

class Evaluator:
    def __init__(self):
        self.particles = {}

    def run(self, ast_root):
        for stmt in ast_root.instrucciones:
            self._exec(stmt)

    def _exec(self, node):
        if isinstance(node, DeclaracionParticula):
            a = node.aceleracion.valor if node.aceleracion is not None else 0
            self.particles[node.nombre] = {
                'x0': node.posicion.valor, 'v0': node.velocidad.valor, 'a':  a,
            }

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

        es_mru = (a == 0)
        mov = "MRU" if es_mru else "MRUA"

        if isinstance(consulta, ConsultaPosicion):
            if es_mru:
                pos = x0 + v0 * t
            else:
                pos = x0 + v0 * t + 0.5 * a * t ** 2
            print(f"[{mov}] posicion({consulta.particula}) en t={t}s: {pos:.2f} m")

        elif isinstance(consulta, ConsultaVelocidad):
            if es_mru:
                vel = v0
            else:
                vel = v0 + a * t
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