from dataclasses import dataclass
from typing import List, Optional, Union

class NodoAST:
    pass

@dataclass
class Programa(NodoAST):
    """programa = { instruccion } ;"""
    instrucciones: List[NodoAST]

@dataclass
class Bloque(NodoAST):
    """bloque = "{", {instruccion}, "}"; """
    instrucciones: List[NodoAST]
    linea: int
    col: int

@dataclass
class DeclaracionParticula(NodoAST):
    """declaracion_particula = "particula", ID, "posicion", "=", numero_real,
         "velocidad", "=", numero_real, [ "aceleracion", "=", numero_real ], ";" ; """
    nombre: str
    posicion: "Numero"
    velocidad: "Numero"
    aceleracion: Optional["Numero"]
    linea: int
    col: int

@dataclass
class DeclaracionNumero(NodoAST):
    """declaracion_numero = "numero", ID, ["=", expr], ";"; """
    nombre: str
    expr: Optional[NodoAST]
    linea: int
    col: int

@dataclass
class Asignacion(NodoAST):
    """asignacion = ID, "=", expr, ";" ;"""
    nombre: str
    expr: NodoAST
    linea: int
    col: int

@dataclass
class ConsultaPosicion(NodoAST):
    """consulta_posicion = "posicion", "(", ID, ")", "en", numero_real; """
    particula: str
    tiempo: "Numero"
    linea: int
    col: int

@dataclass
class ConsultaVelocidad(NodoAST):
    """consulta_velocidad = "velocidad", "(", ID, ")", "en", numero_real;"""
    particula: str
    tiempo: "Numero"
    linea: int
    col: int

@dataclass
class ImprimirConsulta(NodoAST):
    """consulta = "imprimir", (consulta_posicion | consulta_velocidad), ";"; """
    consulta: Union[ConsultaPosicion, ConsultaVelocidad]
    linea: int
    col: int

@dataclass
class ImprimirCadena(NodoAST):
    """imprimir_cadena = "imprimir", STRING, ";" ;"""
    valor: str
    linea: int
    col: int

@dataclass
class If(NodoAST):
    """if_stmt    = "if",    "(", expr, ")", bloque, [ "else", bloque ] ;"""
    condicion: NodoAST
    then: Bloque
    else_: Optional[Bloque]
    linea: int
    col: int

@dataclass
class While(NodoAST):
    """while_stmt = "while", "(", expr, ")", bloque;"""
    condicion: NodoAST
    cuerpo: Bloque
    linea: int
    col: int

@dataclass
class For(NodoAST):
    """for_stmt = "for", "(", ID, "=", expr, ";", expr, ";", ID, "=", expr, ")", bloque ;"""
    var_ini: str
    expr_ini: NodoAST
    condicion: NodoAST
    var_paso: str
    expr_paso: NodoAST
    cuerpo: Bloque
    linea: int
    col: int

@dataclass
class BinOp(NodoAST):
    """Operacion binaria producida por comparacion | suma | termino."""
    left: NodoAST
    operador: str
    right: NodoAST
    linea: int
    col: int

@dataclass
class UnaryOp(NodoAST):
    """menos unario sobre una expresion."""
    operador: str
    operando: NodoAST
    linea: int
    col: int

@dataclass
class Numero(NodoAST):
    """NUM, o numero_real con el signo ya resuelto"""
    valor: Union[int, float]
    linea: int
    col: int

@dataclass
class Identificador(NodoAST):
    nombre: str
    linea: int
    col: int

@dataclass
class NodoError(NodoAST):
    linea: int
    col: int


