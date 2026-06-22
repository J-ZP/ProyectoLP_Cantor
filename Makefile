all:
	antlr4 -Dlanguage=Python3 -no-listener -visitor cantor.g4

clean:
	rm -f *.interp *.tokens cantorLexer.py cantorParser.py cantorVisitor.py