from ast_nodes import (
    Programa, DeclaracionParticula,
    ImprimirConsulta, ImprimirCadena,
    ConsultaPosicion, ConsultaVelocidad,
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


def evaluate(ast):
    Evaluator().run(ast)