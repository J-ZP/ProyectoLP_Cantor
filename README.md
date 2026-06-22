# ProjecteLP_Cantor

Aquesta pràctica implementa un intèrpret d'un llenguatge de programació minimalista que té com a base funcions simples d'un únic paràmetre i les [funcions d'aparellament de Cantor](https://en.wikipedia.org/wiki/Pairing_function) utilitzant Python i Antlr. 

## Requeriments

- Python 3
- Antlr4 (versió 4.13.2)
- Antlr4-python3-runtime (versió 4.13.2)

## Funcionament

Només cal fer servir la comanda make per generar els fitxes d'antlr necesaris.

```
make
```

Un cop generats, es pot fer servir la següent comanda per interpretar un script.

```
echo "1 2 3" | python3 cantor.py script.cantor
```

L'entrada/sortida de l'intèrpret es fa via stdin/stdout, per tant, també admet l'ús d'operadors de redirecció i pipes.

```
python3 cantor.py exemple.cantor < entrada.txt > sortida.txt
```

## Elements implementats en el llenguatge cantorià

### Nucli base

És a dir, el llenguatge treballa internament amb la funció d'aparellament de Cantor. Disposa de les següents funcions bàsiques: `k_1`, `id`, `add`, `mul`, `diff`. Consideració important: No es pot redefinir aquestes funcions, perquè podria trencar el funcionament d'altres scripts. La sintaxi dels scripts consisteix la definició d'un main i de funcions auxiliars mitjançant les directives:

```
main nom_func
```

```
define nom_funció
    [documentació de la funció en llenguatge natural]
    pair_o_comp funció_1 funció_2
```

### Importació

És a dir, el llenguatge admet la funcionalitat d'importar scripts mitjançant la següent directiva:

```
import nom_sense_extensió
```

### Funció compair i Mode Extended

És a dir, el llenguatge permet activar un mode extès mitjançant la directiva:

```
extended
```

En aquest mode, es pot fer servir la funció `compair`, que és la composició de `comp` i `pair`.

A més, també es poden fer servir les funcions `fst` i `snd` per accedir als elements codificats per la funció d'aparellament de Cantor.

### Recursivitat en Mode Basic

És a dir, el llenguatge admet recursivitat en base a la minimització μ. 

L'operador de minimització rep un predicat com a paràmetre i crea una funció `h = mu f` que implementa una cerca lineal sobre `f`. Concretament, `h(x)` va calculant iterativament la seqüència `f(<x.0>)`, `f(<x.1>)`, `f(<x.2>)` fins trobar un valor `k` que satisfà `f(<x.k>)`: aleshores `h(x)=k`. Com a consideració adicional, aquest procés pot no acabar.

### Recursivitat en Mode Extended

És a dir, el llenguatge permet definir funcions recursives mitjançant la funció `primrec`, que donat funcions `f`, `g`, `h`, retorna una funció `s` on `f` és un predicat que ens diu si estem davant del cas base, `g` representa la funció de cas_base i `h` el pas del cas_recursiu. La funció `s` retorna una tupla que conté els valors `s(x)`, `s(x-1)`, `s(x-2)`, ..., `s(1)`, `s(0)` on s'ha aplicat les funcions `g` o `h` a cada valor en funció de si és un cas base o no (si satisfà el predicat `f`). Cal destacar que pel correcte funcionament, f(0) sempre hauria de ser evaluat a True.

## Estructura de fitxers

- La carpeta `tests` que conté els jocs de proves per les diferents funcionalitats i els exercicis proposats. 
- `cantor_pairing.py` conté funcions auxiliars que implementen l'aparellament de Cantor. 
- `cantor.g4` conté la gramàtica del llenguatge. 
- `cantor.py` conté el codi amb el programa principal de l'intèrpret. 
- `Makefile` és el makefile que permet generar els fitxers d'antlr. 
- `visitor.py` conté el codi del visitor que es fa servir.
- `README.md` és aquest propi fitxer.

## Jocs de prova

Els jocs de prova consisteixen en 3 fitxers: un `.cantor` que conté l'script a executar, un `.inp` amb l'input a provar i un `.out` amb l'output esperat.

En general, els jocs de prova es poden separar en 2 grups: funcionalitats i exercicis proposats. No obstant això, per comoditat, estan tots situats a la mateixa carpeta. Els jocs de prova de funcionalitat comproven que els exemples de l'enunciat, les funcions *builtin* i certs aspectes tècnics es comportin de manera esperada. Per exemple, el test `import_loop` comprova que l'intèrpret no es quedi penjat si existeix un cicle en els imports.

Per altra banda, els fitxers que implementen els exercicis proposats son els següents: `booleans`, `relacionals`, `mod_even`, `fibonacci`, `max`, `min`, `cond`, `max2` .

## Decisions de disseny

### Intèrpret i visitor

- Las funciones es guarden en un diccionari intern del visitor. Les funcions `builtin` simplement es guarden com a lambdes, mentres que las funciones compostas: `comp`, `pair`, `compair`, `mu`, `primrec` produeixen clausures que capturen les funcions que utilitzen.

És important destacar que per implementar els `imports`, he decidit simplement fer servir el mateix visitor per fer el recorregut, tenint en compte no visitar el main dels scripts importats i mantenir el flag del mode extès local. 

No obstant això, això vol dir que pot haver problemes si l'usuari redefineix funcions que els scripts importats utilitzen. A més, un altre aspecte rellevant és que no dono suport a les *forward references*. He considerat aquests problemes fora de l'*scope* de la pràctica.

- Les funcions `compair` i `primrec` son part del mode extès, però les funcions `builtin`: `fst` i `snd` es poden fer servir en el mode bàsic pel que he entès de l'enunciat.

- Els errors i excepcions es capturen tots al bloc *try except* situat a la crida del visitor a cantor.py. Com a *fallback*, `compair` i `primrec` retornen la funció `id` en cas de no estar en mode extès.

- Per facilitar la creació dels tests, el visitor quan està important un script busca automàticament l'script amb el nom del import en el directori de l'script principal. No he implementat la funcionalitat de buscar en subdirectoris perquè em semblava fora de l'*scope* de la pràctica.

- L'atribut `imported` serveix per mantenir un set dels scripts importats per tal d'evitar bucles a l'hora d'importar scripts.

- L'atribut `extended` serveix per saber si l'script en qüestió té o no activat el mode extès. He implementat el mode extès per tal que sigui local, és a dir, per exemple, si l'script principal no té el activat el mode extès, però un script importat sí que el té, llavors el mode extès només s'aplica a les funcions d'aquell script importat.

- He implementat l'stack a primrec, com un "stack" codificat per la funció d'aparellament de Cantor, és a dir, el primer element és el top i el segon és la resta.

### Gramática

- He declarat les paraules clau del llenguatge (`main`, `pair`, `import`, etc...) com a tokens explícits per sobre dels identificadors en el lexer per tal que els prioritzi, i com a conseqüència, evitar que l'usuari els redefineixi.

- La regla per funcCall conté tants les funcions *builtin* com les definides per l'usuari. Això permet de manera senzilla utilizar tant funcions *builtin* com les definides per l'usuari en les funcions compostes. 

- D'acord amb la implementació feta a classe, he fet servir etiquetes per separar els diferents casos de les regles. Això permet evitar tenir una cadena de if's al visitor.

- He marcat docString com a opcional, perquè considero que tècnicament, no és realment necesari tenir aquest element a l'hora de programar en aquest llenguatge, encara que és bastant recomanable.

- He marcat mainDirective com a opcionals al root per tal de permetre scripts sense main, és a dir, que només inclouen definicions, per facilitar la creació de tests. 
