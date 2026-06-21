import ply.yacc as yacc
from lexer import tokens, lexer
import sys
import re
from ast_nodes import (
    Programa, Bloque, DeclaracionParticula, DeclaracionNumero,
    Asignacion, ConsultaPosicion, ConsultaVelocidad, ConsultaColision,
    ImprimirConsulta, ImprimirCadena, If, While, For, BinOp, UnaryOp, Numero,
    Identificador, NodoError
)

precedence = (
    ('left', 'MENOR', 'MAYOR', 'MENORIGUAL', 'MAYORIGUAL', 'IGUALDAD', 'DISTINTO'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULT', 'DIV'),
    ('right', 'UMINUS'),   # menos unario
)

# Funciones auxiliares para obtener línea/columna de un token
def token_line(tok):
    return tok.lineno

def token_column(tok):
    lexdata = lexer.lexdata
    line_start = lexdata.rfind('\n', 0, tok.lexpos) + 1
    return tok.lexpos - line_start + 1

# programa = { instruccion }
def p_programa(p):
    'programa : instrucciones'
    p[0] = Programa(p[1])

def p_instrucciones_lista(p):
    'instrucciones : instrucciones instruccion'
    p[0] = p[1] + [p[2]]

def p_instrucciones_vacio(p):
    'instrucciones : '
    p[0] = []

def p_instruccion(p):
    '''instruccion : declaracion_particula
                   | declaracion_numero
                   | asignacion
                   | consulta
                   | imprimir_cadena
                   | if_stmt
                   | while_stmt
                   | for_stmt
                   | bloque'''
    p[0] = p[1]

def p_instruccion_error(p):
    'instruccion : error PUNTOCOMA'
    linea = token_line(p.slice[2])
    col = token_column(p.slice[2])
    p[0] = NodoError(linea, col)

def p_bloque(p):
    'bloque : LLAVE_IZQ instrucciones LLAVE_DER'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = Bloque(p[2], linea, col)


def p_declaracion_particula_con_acel(p):
    '''declaracion_particula : PARTICULA ID POSICION ASIGN numero_real \
                               VELOCIDAD ASIGN numero_real \
                               ACELERACION ASIGN numero_real PUNTOCOMA'''
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = DeclaracionParticula(p[2], p[5], p[8], p[11], linea, col)


def p_declaracion_particula_sin_acel(p):
    '''declaracion_particula : PARTICULA ID POSICION ASIGN numero_real \
                               VELOCIDAD ASIGN numero_real PUNTOCOMA'''
    linea = token_line(p.slice[1])
    col   = token_column(p.slice[1])
    p[0]  = DeclaracionParticula(p[2], p[5], p[8], None, linea, col)


def p_declaracion_numero_con_inic(p):
    'declaracion_numero : NUMERO ID ASIGN expr PUNTOCOMA'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = DeclaracionNumero(p[2], p[4], linea, col)

def p_declaracion_numero_sin_inic(p):
    'declaracion_numero : NUMERO ID PUNTOCOMA'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = DeclaracionNumero(p[2], None, linea, col)

def p_asignacion(p):
    'asignacion : ID ASIGN expr PUNTOCOMA'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = Asignacion(p[1], p[3], linea, col)


def p_imprimir_consulta(p):
    'consulta : IMPRIMIR consulta_cuerpo PUNTOCOMA'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    # p[2] es un nodo ConsultaPosicion o ConsultaVelocidad
    p[0] = ImprimirConsulta(p[2], linea, col)

def p_consulta_posicion(p):
    'consulta_cuerpo : POSICION PAREN_IZQ ID PAREN_DER EN numero_real'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = ConsultaPosicion(p[3], p[6], linea, col)

def p_consulta_velocidad(p):
    'consulta_cuerpo : VELOCIDAD PAREN_IZQ ID PAREN_DER EN numero_real'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = ConsultaVelocidad(p[3], p[6], linea, col)

def p_consulta_colision(p):
    'consulta : IMPRIMIR COLISION PAREN_IZQ ID COMA ID PAREN_DER PUNTOCOMA'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = ConsultaColision(p[4], p[6], linea, col)

def p_imprimir_cadena(p):
    'imprimir_cadena : IMPRIMIR STRING PUNTOCOMA'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = ImprimirCadena(p[2], linea, col)

def p_if_sin_else(p):
    'if_stmt : IF PAREN_IZQ expr PAREN_DER bloque'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = If(p[3], p[5], None, linea, col)

def p_if_con_else(p):
    'if_stmt : IF PAREN_IZQ expr PAREN_DER bloque ELSE bloque'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = If(p[3], p[5], p[7], linea, col)


def p_while(p):
    'while_stmt : WHILE PAREN_IZQ expr PAREN_DER bloque'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = While(p[3], p[5], linea, col)


def p_for(p):
    'for_stmt : FOR PAREN_IZQ ID ASIGN expr PUNTOCOMA expr PUNTOCOMA ID ASIGN expr PAREN_DER bloque'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = For(p[3], p[5], p[7], p[9], p[11], p[13], linea, col)

# numero_real = ["-"], NUM
def p_numero_real_positivo(p):
    'numero_real : NUM'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = Numero(p[1], linea, col)

def p_numero_real_negativo(p):
    'numero_real : MENOS NUM'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    valor = -p[2]   # p[2] es el valor numérico
    p[0] = Numero(valor, linea, col)


def p_expr(p):
    'expr : comparacion'
    p[0] = p[1]

# comparacion = suma { ("<" | ">" | "<=" | ">=" | "==" | "!=") suma }
def p_comparacion_unica(p):
    'comparacion : suma'
    p[0] = p[1]

def p_comparacion_binaria(p):
    '''comparacion : suma MENOR suma
                   | suma MAYOR suma
                   | suma MENORIGUAL suma
                   | suma MAYORIGUAL suma
                   | suma IGUALDAD suma
                   | suma DISTINTO suma'''
    linea = token_line(p.slice[2])
    col = token_column(p.slice[2])
    p[0] = BinOp(p[1], p[2], p[3], linea, col)

# suma = termino { ("+" | "-") termino }
def p_suma_unica(p):
    'suma : termino'
    p[0] = p[1]

def p_suma_binaria(p):
    '''suma : suma MAS termino
            | suma MENOS termino'''
    linea = token_line(p.slice[2])
    col = token_column(p.slice[2])
    p[0] = BinOp(p[1], p[2], p[3], linea, col)

# termino = factor { ("*" | "/") factor }
def p_termino_unico(p):
    'termino : factor'
    p[0] = p[1]

def p_termino_binario(p):
    """termino : termino MULT factor
               | termino DIV factor"""
    linea = token_line(p.slice[2])
    col = token_column(p.slice[2])
    p[0] = BinOp(p[1], p[2], p[3], linea, col)

# factor = NUM | ID | "(", expr, ")" | "-", factor
def p_factor_num(p):
    'factor : NUM'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = Numero(p[1], linea, col)

def p_factor_id(p):
    'factor : ID'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = Identificador(p[1], linea, col)

def p_factor_parentesis(p):
    'factor : PAREN_IZQ expr PAREN_DER'
    p[0] = p[2]

def p_factor_unario(p):
    'factor : MENOS factor %prec UMINUS'
    linea = token_line(p.slice[1])
    col = token_column(p.slice[1])
    p[0] = UnaryOp('-', p[2], linea, col)

def p_error(p):
    if p is None:
        print("Error sintáctico: fin de archivo inesperado")
        return

    col = token_column(p)

    if p.type == 'ID':
        encontrado = f"identificador '{p.value}'"
    elif p.type == 'NUM':
        encontrado = f"número {p.value}"
    elif p.type == 'STRING':
        encontrado = f'cadena "{p.value}"'
    else:
        encontrado = f"'{p.value}'"

    def display(tipo):
        if tipo == 'ID': return 'un identificador'
        if tipo == 'NUM': return 'un número'
        if tipo == 'STRING': return 'una cadena'
        attr = getattr(sys.modules['lexer'], f't_{tipo}', None)
        if isinstance(attr, str):
            return "'" + re.sub(r'\\(.)', r'\1', attr) + "'"
        return "'" + tipo.lower() + "'"

    estado = parser.statestack[-1]
    acciones = parser.action.get(estado, {})
    esperados = sorted({
        display(t) for t in acciones
        if t not in ('error', '$end') })

    # Evita mostrar '-' solo, lo integra al número para mayor claridad
    if set(esperados) == {"'-'", 'un número'}:
        esperados = ['un número']

    if esperados:
        print(
            f"Error sintáctico [línea {p.lineno}, columna {col}]: "
            f"se esperaba {' o '.join(esperados)}, "
            f"pero se encontró {encontrado}")
    else:
        print(
            f"Error sintáctico [línea {p.lineno}, columna {col}]: "
            f"token inesperado {encontrado}")

# Construccion del parser
parser = yacc.yacc(errorlog=yacc.NullLogger())
