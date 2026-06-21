## Gramática EBNF de PhysKin 

### Notación

- Los **terminales** (tokens) van entre comillas dobles: `"particula"`
- Los **no terminales** se escriben sin comillas: `declaracion_particula`

### Gramática

```ebnf
programa = { instruccion } ;

instruccion = declaracion_particula
            | declaracion_numero
            | asignacion
            | consulta
            | imprimir_cadena
            | if_stmt
            | while_stmt
            | for_stmt
            | bloque ;

bloque = "{" , { instruccion } , "}" ;

declaracion_particula = "particula", ID,
                        "posicion", "=", valor_cinematico,
                        "velocidad", "=", valor_cinematico,
                        [ "aceleracion", "=", valor_cinematico ],
                        ";" ;

declaracion_numero = "numero", ID, [ "=", expr ], ";" ;

asignacion = ID, "=", expr, ";" ;

consulta = "imprimir", ( consulta_posicion | consulta_velocidad ), ";" ;
consulta_posicion = "posicion", "(", ID, ")", "en", numero_real ;
consulta_velocidad = "velocidad", "(", ID, ")", "en", numero_real ;
consulta_colision  = "colision",  "(", ID, ",", ID, ")" ;

imprimir_cadena = "imprimir", STRING, ";" ;

if_stmt    = "if",    "(", expr, ")", bloque, [ "else", bloque ] ;
while_stmt = "while", "(", expr, ")", bloque ;
for_stmt   = "for",   "(", ID, "=", expr, ";", expr, ";", ID, "=", expr, ")", bloque ;

(* valor escalar (1D) o vector (2D) para posicion, velocidad y aceleracion *)
valor_cinematico = numero_real
                 | "(", numero_real, ",", numero_real, ")" ;

numero_real = ["-"], NUM ;

expr = comparacion ;
comparacion = suma , { ("<" | ">" | "<=" | ">=" | "==" | "!=") , suma } ;
suma = termino , { ("+" | "-") , termino } ;
termino = factor , { ("*" | "/") , factor } ;
factor = NUM | ID | "(", expr, ")" | "-", factor ;

(* Terminales (definidos en el analizador léxico) *)
ID = (letra | "_") , (letra | digito | "_")* ;
NUM = digito+ , [ "." , digito+ ] ;
STRING = '"' , { caracter_valido } , '"' ;
caracter_valido = "\\" , ("n" | "t" | '"' | "\\")
                | ( carácter - ('"' | "\\") ) ;