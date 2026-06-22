import sys
from antlr4 import *
from cantor_pairing import encode_list
from visitor import CantorVisitor
from cantorLexer import cantorLexer
from cantorParser import cantorParser


def run(script, encoded):
    try:
        input_stream = FileStream(script, encoding='utf-8')
        lexer = cantorLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = cantorParser(stream)

        tree = parser.root()

        # Si hi ha cap error de sintaxi, no visitar
        if parser.getNumberOfSyntaxErrors() > 0:
            return

        visitor = CantorVisitor(script)
        main_func = visitor.visit(tree)

        # Escriure per stdout l'evalució del main amb l'input
        print(main_func(encoded))

    # Capturar les excepcions
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 cantor.py [script.cantor]")
        sys.exit(1)

    script = sys.argv[1]

    raw = input().split()
    numbers = [int(x) for x in raw]
    encoded = encode_list(numbers)

    run(script, encoded)


if __name__ == '__main__':
    main()
