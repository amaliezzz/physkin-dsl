## Gramática EBNF de PhysKin

### Notación
- Los terminales (tokens) van entre comillas dobles: `"particula"`
- Los no terminales se escriben sin comillas: `declaracion_particula`

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
                        "posicion", "=", NUM,
                        "velocidad", "=", NUM,
                        [ "aceleracion", "=", NUM ],
                        ";" ;

declaracion_numero = "numero", ID, [ "=", expr ], ";" ;

asignacion = ID, "=", expr, ";" ;

consulta = "imprimir", ( consulta_posicion | consulta_velocidad ), ";" ;
consulta_posicion = "posicion", "(", ID, ")", "en", NUM ;
consulta_velocidad = "velocidad", "(", ID, ")", "en", NUM ;

imprimir_cadena = "imprimir", STRING, ";" ;


if_stmt = "if", "(", expr, ")", instruccion, [ "else", instruccion ] ;
while_stmt = "while", "(", expr, ")", instruccion ;
for_stmt = "for", "(", ID, "=", expr, ";", expr, ";", ID, "=", expr, ")", instruccion ;

expr = comparacion ;
comparacion = suma { ("<" | ">" | "<=" | ">=" | "==" | "!=") suma } ;
suma = termino { ("+" | "-") termino } ;
termino = factor { ("*" | "/") factor } ;
factor = NUM | ID | STRING | "(", expr, ")" | "-", factor ;


ID = letra (letra | digito | "_")* ;
NUM = ["-"], digito+, [".", digito+] ;
STRING = '"' , { carácter - '"' | escape } , '"' ;
