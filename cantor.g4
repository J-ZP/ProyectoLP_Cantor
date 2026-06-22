grammar cantor;

root          : mainDirective? EXTENDED? importDirective* defineBlock* EOF ;
mainDirective : MAIN funcCall ;
importDirective : IMPORT IDENTIFIER ;
defineBlock   : DEFINE IDENTIFIER docString? funcBody ;
docString     : DOC_STRING ;
funcBody      : PAIR f=funcCall g=funcCall    # PairExpr
              | COMP f=funcCall g=funcCall    # CompExpr
              | COMPAIR f=funcCall g=funcCall h=funcCall # CompairExpr
              | MU f=funcCall                 # MuExpr
              | PRIMREC f=funcCall g=funcCall h=funcCall # PrimrecExpr
              ;
funcCall      : IDENTIFIER               # UserFunc
              | K_1                      # KOne
              | ID                       # Identity
              | ADD                      # Add
              | MUL                      # Mul
              | DIFF                     # Diff
              | FST                      # Fst
              | SND                      # Snd
              ;

MAIN    : 'main' ;
IMPORT  : 'import' ;
DEFINE  : 'define' ;
PAIR    : 'pair' ;
COMP    : 'comp' ;
K_1     : 'k_1' ;
ID      : 'id' ;
ADD     : 'add' ;
MUL     : 'mul' ;
DIFF    : 'diff' ;
FST     : 'fst' ;
SND     : 'snd' ;
EXTENDED: 'extended' ;
COMPAIR : 'compair' ;
MU      : 'mu';
PRIMREC : 'primrec' ;

IDENTIFIER  : [a-zA-Z][a-zA-Z0-9_]* ;
DOC_STRING  : '[' ~[\]]* ']' ;
COMMENT     : '#' ~[\n]* -> skip ;
WS          : [ \t\n\r]+ -> skip ;