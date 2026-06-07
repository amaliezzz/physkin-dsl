import ply.lex as lex

tokens = [
    # Identificadores y literales
    'ID',
    'NUM',
    'STRING',
    # Operadores aritméticos
    'MAS',      # +
    'MENOS',    # -
    'MULT',     # *
    'DIV',      # /
    # Operadores relacionales
    'MENOR',        # <
    'MAYOR',        # >
    'MENORIGUAL',   # <=
    'MAYORIGUAL',   # >=
    'IGUALDAD',     # ==
    'DISTINTO',     # !=
    # Delimitadores y asignación
    'ASIGN',        # =
    'PUNTOCOMA',    # ;
    'COMA',         # ,
    'PAREN_IZQ',    # (
    'PAREN_DER',    # )
    'LLAVE_IZQ',    # {
    'LLAVE_DER',    # }
]

# Palabras reservadas
reserved = {
    # Dominio PhysKin
    'particula': 'PARTICULA',
    'posicion': 'POSICION',
    'velocidad': 'VELOCIDAD',
    'aceleracion': 'ACELERACION',
    'en': 'EN',
    'imprimir': 'IMPRIMIR',
    # Variables numéricas
    'numero': 'NUMERO',
    # Estructuras de control
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
}

tokens = list(reserved.values()) + tokens

# Tokens simples con expresiones regulares
t_ASIGN      = r'='
t_PUNTOCOMA  = r';'
t_COMA       = r','
t_PAREN_IZQ  = r'\('
t_PAREN_DER  = r'\)'
t_LLAVE_IZQ  = r'\{'
t_LLAVE_DER  = r'\}'
t_MAS        = r'\+'
t_MENOS      = r'-'
t_MULT       = r'\*'
t_DIV        = r'/'
t_MENOR      = r'<'
t_MAYOR      = r'>'
t_MENORIGUAL = r'<='
t_MAYORIGUAL = r'>='
t_IGUALDAD   = r'=='
t_DISTINTO   = r'!='

# Números (enteros y decimales, SIN signo)
def t_NUM(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

# Identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Cadenas de texto con escapes
def t_STRING(t):
    r'\"([^\\\n]|\\.)*\"'   # Soporta escapes, pero no saltos de línea sin escapar
    # Eliminar las comillas dobles del inicio y final
    raw = t.value[1:-1]
    # Procesar secuencias de escape
    escapes = {
        'n': '\n',
        't': '\t',
        '"': '"',
        '\\': '\\'
    }
    result = []
    i = 0
    length = len(raw)
    while i < length:
        if raw[i] == '\\' and i+1 < length:
            esc_char = raw[i+1]
            if esc_char in escapes:
                result.append(escapes[esc_char])
                i += 2
            else:
                # Secuencia de escape no reconocida: error léxico
                # Posición aproximada: línea actual, columna (t.lexpos + i)
                col = t.lexpos + i
                print(f"Error léxico [línea {t.lineno}, columna {col}]: secuencia de escape inválida '\\{esc_char}'")
                # No recuperamos, pero devolvemos un token dummy? Mejor parar.
                # Para continuar, ignoramos la barra y el carácter.
                result.append(raw[i])
                i += 1
        else:
            result.append(raw[i])
            i += 1
    t.value = ''.join(result)
    return t

# --- Comentarios ---
# Comentarios de línea: ignorar desde // hasta fin de línea
def t_COMMENT_LINE(t):
    r'//.*'
    # No devolver token, solo ignorar
    pass

# Comentarios de bloque: soporte anidamiento opcional, pero con regex simple sin anidar.
# Las orientaciones no exigen anidamiento. Usamos una regex que captura /* ... */
# sin anidar (la primera aparición de */). Si hubiera anidamiento, esto fallaría,
# pero es suficiente para el proyecto.
def t_COMMENT_BLOCK(t):
    r'/\*.*?\*/'
    # Contar saltos de línea dentro del comentario para actualizar lineno
    lines = t.value.count('\n')
    t.lexer.lineno += lines
    pass

# --- Seguimiento de líneas ---
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# --- Caracteres a ignorar (espacios, tabulaciones) ---
t_ignore = ' \t\r'

# --- Manejo de errores léxicos ---
def t_error(t):
    # Reportar carácter inesperado con línea y columna
    columna = t.lexpos - t.lexer.lexdata.rfind('\n', 0, t.lexpos) - 1
    if columna < 0:
        columna = t.lexpos
    print(f"Error léxico [línea {t.lineno}, columna {columna}]: carácter inesperado '{t.value[0]}'")
    # Recuperar: avanzar un carácter
    t.lexer.skip(1)

# --- Construir el lexer ---
lexer = lex.lex()
