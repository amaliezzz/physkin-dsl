import sys
from lexer import lexer
from parser import parser
from semantic import analyze
from evaluator import evaluate

def main():
    args = sys.argv[1:]
    run_eval = '--eval' in args
    files = [a for a in args if not a.startswith('--')]

    if not files:
        return

    with open(files[0], encoding='utf-8') as f:
        source = f.read()

    lexer.lineno = 1
    ast = parser.parse(source, lexer=lexer)

    if ast is None:
        return

    errors = analyze(ast)
    if errors:
        for e in errors:
            print(e)
        return

    if run_eval:
        evaluate(ast)


if __name__ == '__main__':
    main()
