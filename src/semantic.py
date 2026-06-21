from ast_nodes import (
    Programa, Bloque, DeclaracionParticula, DeclaracionNumero,
    Asignacion, ConsultaPosicion, ConsultaVelocidad, ConsultaColision, ImprimirConsulta,
    ImprimirCadena, If, While, For, BinOp, UnaryOp, Numero, Vector2D,
    Identificador, NodoError
)

# Tabla de símbolos con scopes anidados

class SymbolTable:
    """Maneja scopes anidados para variables y partículas."""
    def __init__(self):
        # La pila de scopes: cada scope es un diccionario nombre -> info
        self.scope_stack = [{}]

    def enter_scope(self):
        """Entra en un nuevo ámbito."""
        self.scope_stack.append({})

    def exit_scope(self):
        """Sale del ámbito actual."""
        self.scope_stack.pop()

    def declare(self, name, tipo, linea, col):
        """Declara un símbolo en el scope actual. Retorna False si ya existe."""
        if name in self.scope_stack[-1]:
            return False
        self.scope_stack[-1][name] = {
            'tipo': tipo,            # particula o numero
            'initialized': False,
            'linea': linea,
            'col': col
        }
        return True

    def lookup(self, name):
        """Busca un símbolo desde el scope más interno al global"""
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        return None

    def mark_initialized(self, name):
        """Marca una variable como ya inicializada"""
        info = self.lookup(name)
        if info:
            info['initialized'] = True

    def is_initialized(self, name):
        """Comprueba si una variable existe y está inicializada."""
        info = self.lookup(name)
        return info is not None and info['initialized']


class SemanticAnalyzer:
    """Recorre el AST y aplica las reglas de tipo y del dominio."""
    def __init__(self):
        self.symbols = SymbolTable()
        self.errors = []

    def _error(self, linea, col, msg):
        self.errors.append(f"Error semántico [línea {linea}, columna {col}]: {msg}")


    def analyze(self, ast_root):
        """Analiza el AST desde la raíz y devuelve la lista de errores."""
        self._process(ast_root)
        return self.errors


    def _process(self, node):
        if node is None:
            return
        # Los nodos de error sintáctico ya se reportaron, los ignoramos
        if isinstance(node, NodoError):
            return

        # Diccionario que asocia cada tipo de nodo con su función de análisis
        handlers = {
            Programa: self._analyze_program,
            Bloque: self._analyze_block,
            DeclaracionParticula: self._analyze_particle_decl,
            DeclaracionNumero: self._analyze_number_decl,
            Asignacion: self._analyze_assignment,
            ConsultaPosicion: self._analyze_position_query,
            ConsultaVelocidad: self._analyze_velocity_query,
            ConsultaColision: self._analyze_collision_query,
            ImprimirConsulta: self._analyze_print_query,
            ImprimirCadena: self._analyze_print_string,
            If: self._analyze_if,
            While: self._analyze_while,
            For: self._analyze_for,
            BinOp: self._analyze_binop,
            UnaryOp: self._analyze_unaryop,
            Numero: self._analyze_number,
            Vector2D: self._analyze_vector2d,
            Identificador: self._analyze_identifier,
        }
        handler = handlers.get(type(node))
        if handler:
            handler(node)
        else:
            raise TypeError(f"Nodo AST no manejado: {type(node).__name__}")

    def _analyze_program(self, node):
        for stmt in node.instrucciones:
            self._process(stmt)

    def _analyze_block(self, node):
        # Cada bloque crea un nuevo ámbito
        self.symbols.enter_scope()
        for stmt in node.instrucciones:
            self._process(stmt)
        self.symbols.exit_scope()

    def _analyze_particle_decl(self, node):
        # Teniendo en cuenta no redeclarar partículas
        if self.symbols.lookup(node.nombre) is not None:
            self._error(node.linea, node.col, f"'{node.nombre}' ya está declarado")
            return

        # posición y velocidad obligatorias
        if node.posicion is None or node.velocidad is None:
            self._error(node.linea, node.col,"falta 'posicion' o 'velocidad' en la declaración")
            return

        # posicion, velocidad y aceleracion deben ser todas 1D o todas 2D
        es_2d = isinstance(node.posicion, Vector2D)
        if isinstance(node.velocidad, Vector2D) != es_2d:
            self._error(node.linea, node.col,
                        "posicion y velocidad deben ser ambas 1D o ambas 2D")
            return
        if node.aceleracion is not None and isinstance(node.aceleracion, Vector2D) != es_2d:
            self._error(node.linea, node.col,
                        "aceleracion debe ser del mismo tipo que posicion y velocidad")
            return

        # Declaramos la partícula y la marcamos como inicializada
        self.symbols.declare(node.nombre, 'particula', node.linea, node.col)
        self.symbols.mark_initialized(node.nombre)

        # procesamos los numeros
        self._process(node.posicion)
        self._process(node.velocidad)
        if node.aceleracion is not None:
            self._process(node.aceleracion)

    def _analyze_number_decl(self, node):
        # No se puede redeclarar en el mismo ámbito
        if node.nombre in self.symbols.scope_stack[-1]:
            self._error(node.linea, node.col,f"variable '{node.nombre}' ya declarada en este ámbito")
            return

        self.symbols.declare(node.nombre, 'numero', node.linea, node.col)
        if node.expr is not None:
            self._process(node.expr)
            self.symbols.mark_initialized(node.nombre)

    def _analyze_assignment(self, node):
        info = self.symbols.lookup(node.nombre)
        if info is None:
            self._error(node.linea, node.col, f"variable '{node.nombre}' no declarada")
            return
        if info['tipo'] != 'numero':
            self._error(node.linea, node.col,f"'{node.nombre}' es una partícula, no se puede asignar")
            return

        self._process(node.expr)
        self.symbols.mark_initialized(node.nombre)

    def _analyze_position_query(self, node):
        self._check_particle_and_time(node.particula, node.tiempo, node.linea, node.col)

    def _analyze_velocity_query(self, node):
        self._check_particle_and_time(node.particula, node.tiempo, node.linea, node.col)

    def _analyze_collision_query(self, node):
        for nombre in (node.particula1, node.particula2):
            info = self.symbols.lookup(nombre)
            if info is None:
                self._error(node.linea, node.col, f"partícula '{nombre}' no declarada")
            elif info['tipo'] != 'particula':
                self._error(node.linea, node.col, f"'{nombre}' no es una partícula")

    def _check_particle_and_time(self, name, time_node, line, col):
        """para consultas de posición y velocidad"""
        info = self.symbols.lookup(name)
        if info is None:
            self._error(line, col, f"partícula '{name}' no declarada")
            return
        if info['tipo'] != 'particula':
            self._error(line, col, f"'{name}' no es una partícula")
            return

        # Verificar que el tiempo sea ≥ 0
        self._process(time_node)

        if time_node.valor < 0:
            self._error(time_node.linea, time_node.col, f"el tiempo debe ser ≥ 0, se recibió {time_node.valor}")

    def _analyze_print_query(self, node):
        self._process(node.consulta)

    def _analyze_print_string(self, node):
        # Las cadenas son literales, no hay nada que comprobar
        pass

    def _analyze_if(self, node):
        self._process(node.condicion)
        self._process(node.then)
        if node.else_ is not None:
            self._process(node.else_)

    def _analyze_while(self, node):
        self._process(node.condicion)
        self._process(node.cuerpo)

    def _analyze_for(self, node):
        # La variable de inicio y paso deben ser la misma
        if node.var_ini != node.var_paso:
            self._error(node.linea, node.col,
                        f"variables de inicio y paso deben coincidir: '{node.var_ini}' vs '{node.var_paso}'")

        # Si la variable no existe, se declara
        info = self.symbols.lookup(node.var_ini)
        if info is None:
            self.symbols.declare(node.var_ini, 'numero', node.linea, node.col)
        elif info['tipo'] != 'numero':
            self._error(node.linea, node.col,
                        f"'{node.var_ini}' no es numérica")

        # tres expresiones del for
        self._process(node.expr_ini)
        self.symbols.mark_initialized(node.var_ini)
        self._process(node.condicion)
        self._process(node.expr_paso)

        # cuerpo se procesa en su propio ámbito (el nodo Bloque ya lo maneja)
        self._process(node.cuerpo)

    def _analyze_binop(self, node):
        # Visitamos los hijos; la verificación de tipos la hace _analyze_identifier
        self._process(node.left)
        self._process(node.right)

    def _analyze_unaryop(self, node):
        self._process(node.operando)

    def _analyze_number(self, node):
        pass

    def _analyze_vector2d(self, node):
        pass  # literal 2D, nada que validar

    def _analyze_identifier(self, node):
        info = self.symbols.lookup(node.nombre)
        if info is None:
            self._error(node.linea, node.col,f"variable '{node.nombre}' no declarada")
            return
        # Las partículas no pueden aparecer en expresiones aritméticas
        if info['tipo'] != 'numero':
            self._error(node.linea, node.col,f"'{node.nombre}' es una partícula, no se puede usar en expresiones")
            return
        # Verificar que la variable haya sido inicializada antes de usarla
        if not info['initialized']:
            self._error(node.linea, node.col,
                        f"variable '{node.nombre}' usada antes de ser inicializada")

def analyze(ast):
    return SemanticAnalyzer().analyze(ast)