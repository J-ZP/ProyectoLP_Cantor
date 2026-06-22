from cantorVisitor import cantorVisitor
from cantorLexer import cantorLexer
from cantorParser import cantorParser
from cantor_pairing import unpi, pi
from antlr4 import *
import os


class CantorVisitor(cantorVisitor):
    def __init__(self, script):
        # Per buscar scripts per importar en el mateix directori
        self.current_dir = os.path.dirname(os.path.abspath(script))
        # Per evitar problemes amb bucles d'import
        self.imported = set()
        # Flag per saber si el mode extès està activat
        self.extended = False
        self.functions = {
            'k_1': lambda x: 1,
            'id': lambda x: x,
            'add': lambda x: unpi(x)[0] + unpi(x)[1],
            'mul': lambda x: unpi(x)[0] * unpi(x)[1],
            'diff': lambda x: max(0, unpi(x)[0] - unpi(x)[1]),
            'fst': lambda x: unpi(x)[0],
            'snd': lambda x: unpi(x)[1]
        }

    def visitRoot(self, ctx, is_import=False):
        if ctx.EXTENDED():
            self.extended = True
        for imp in ctx.importDirective():
            self.visit(imp)
        for block in ctx.defineBlock():
            self.visit(block)
        # No visitar el main dels imports
        if not is_import and ctx.mainDirective():
            return self.visit(ctx.mainDirective())

    def visitMainDirective(self, ctx):
        f = self.visit(ctx.funcCall())
        return f

    def visitImportDirective(self, ctx):
        # Construir el path dels fitxers script dels imports
        script_name = ctx.IDENTIFIER().getText() + '.cantor'
        script_path = os.path.abspath(os.path.join(self.current_dir, script_name))

        if script_path in self.imported:
            return
        self.imported.add(script_path)

        input_stream = FileStream(script_path, encoding='utf-8')
        lexer = cantorLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = cantorParser(stream)

        tree = parser.root()

        if parser.getNumberOfSyntaxErrors() > 0:
            return

        # Mantenir el flag extended de manera local
        extended_before = self.extended
        self.visitRoot(tree, is_import=True)
        self.extended = extended_before

    def visitDefineBlock(self, ctx):
        name = ctx.IDENTIFIER().getText()
        f = self.visit(ctx.funcBody())
        self.functions[name] = f

    def visitPairExpr(self, ctx):
        f = self.visit(ctx.f)
        g = self.visit(ctx.g)
        return lambda x: pi(f(x), g(x))

    def visitCompExpr(self, ctx):
        f = self.visit(ctx.f)
        g = self.visit(ctx.g)
        return lambda x: f(g(x))

    def visitCompairExpr(self, ctx):
        if not self.extended:
            print("Mode Extended no activat")
            # Fallback
            return self.functions['id']

        f = self.visit(ctx.f)
        g = self.visit(ctx.g)
        h = self.visit(ctx.h)
        return lambda x: f(pi(g(x), h(x)))

    def visitMuExpr(self, ctx):
        f = self.visit(ctx.f)

        def h(x):
            k = 0
            while not f(pi(x, k)):
                k += 1
            return k

        return h

    def visitPrimrecExpr(self, ctx):
        if not self.extended:
            print("Mode Extended no activat")
            # Fallback
            return self.functions['id']

        f = self.visit(ctx.f)
        g = self.visit(ctx.g)
        h = self.visit(ctx.h)

        def s(x):
            stack = 0
            for i in range(x + 1):
                if f(i):
                    value = g(i)
                else:
                    value = h(pi(i, stack))
                # Fer servir l'aparellament de Cantor com a stack
                stack = pi(value, stack)
            return unpi(stack)[0]

        return s

    def visitUserFunc(self, ctx):
        name = ctx.IDENTIFIER().getText()
        return self.functions[name]

    def visitKOne(self, ctx):
        return self.functions['k_1']

    def visitIdentity(self, ctx):
        return self.functions['id']

    def visitAdd(self, ctx):
        return self.functions['add']

    def visitMul(self, ctx):
        return self.functions['mul']

    def visitDiff(self, ctx):
        return self.functions['diff']

    def visitFst(self, ctx):
        return self.functions['fst']

    def visitSnd(self, ctx):
        return self.functions['snd']
