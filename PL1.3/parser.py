print('PoopityScoopLang Parser 1.2Dev 0300')
from lark import Lark, Transformer, Tree
from lark.reconstruct import Reconstructor
from math import sqrt

psl_grammer_ebnf = '''
statement = (block | if_stmt | end_stmt | poopyscoop_stmt | get_stmt, put_stmt), ";";

block = {statement}

if_stmt = 'if', expressision, ";", block, ["else",block];

poopyscoop_stmt = indentifier, "is:",expression;

get_stmt = 'read:',indentifier

put_stmt = 'put:', expression

'''









psl_grammer = '''
?start: value
?value: WORD
      | ifexpr
      | expr
      | stmt
      | numstmt
      | varstmt
      | gvarstmt
      | prtstmt
      | modulestmt
      | longst
      | newline
      | STRING
      | pyexpr
valst: stmt
newline: "fs" WORD value
longst: newline value
pyexpr: "py" STRING
fview: "fview" value
ifexpr: "if" value ":"
stmt: "=>"
numstmt: expr valst expr
expr: add
    | subtract
    | divide
    | multiply
    | expon
    | sqrt
    | NUMBER

add:  expr "+" expr
subtract: expr "-" expr 
divide: expr "/" expr
multiply: expr "*" expr
expon: expr "**" expr
sqrt: expr "//"
gvarstmt: WORD ">>"
varstmt: WORD "=" value
prtstmt: "view" value

modulestmt: "import" WORD

%import common.NUMBER
%import common.WORD
%import common.ESCAPED_STRING   -> STRING
%ignore " "

%declare _INDENT _DEDENT
'''

p = Lark(psl_grammer, parser='lalr')

prsd = p.parse('1+2+1+1-2*2/2*2//')
#print(prsd)

prsd2 = p.parse('if 1 => 2+2:')

prsd3 = p.parse('hello=if 2+2 => 4+0:')

prsd4 = p.parse('hello >>')

prsd5 = p.parse('view hello >>')

prsd6 = p.parse('import viewstmt')

prsd7 = p.parse('fs helloww view 1+1')

prsd8 = p.parse('py "print(hello)"')

NAMESPACE = {}
FNAMESPACE = {}
class PSTransformer(Transformer):
    def __init__(self):
        self.tsum = 0
        self.glob = {}
    def expr(self, numbers):
        
        addo = []
        subo = []
        mulo = []
        divo = []
        
        try:
            #print(numbers)
            rt = float(numbers[0])
            #print(rt)
            return rt
        except:
            
            if numbers[0].data == 'add':
                self.tsum = numbers[0].children[1] + numbers[0].children[0] #Embrace the communitve property!
            elif numbers[0].data == 'subtract':
                self.tsum = numbers[0].children[0] - numbers[0].children[1]
            elif numbers[0].data == 'multiply':
                self.tsum = numbers[0].children[1] * numbers[0].children[0] #Embrace the communitve property!
            elif numbers[0].data == 'divide':
                self.tsum = numbers[0].children[0] / numbers[0].children[1] #Embrace the communitve property!
            elif numbers[0].data == 'expon':
                self.tsum = numbers[0].children[0] ** numbers[0].children[1]
            else:
                self.tsum = sqrt(float(numbers[0].children[0]))
            rt = self.tsum
        return rt
    def ifexpr(self,exp):
        print(exp)
        if exp[0].data == 'numstmt':
            for i in exp[0].children:
                if type(i) == type(1.0):
                    try:
                        self.glob['NUMSTMT_TESTCONDS'].append(i)
                    except KeyError:
                        self.glob['NUMSTMT_TESTCONDS'] = [i]


                else:
                    pass
            if self.glob['NUMSTMT_TESTCONDS'][0] == self.glob['NUMSTMT_TESTCONDS'][1]:
                return True
            else:
                return False
                
        else:
            print('Well, that\'s stinky! That\'s not something that\'s supported!')
            return True
    def varstmt(self,vstmt):
        global NAMESPACE
        #print('Hi!')
        #print(vstmt)
        NAMESPACE[str(vstmt[0])] = vstmt[1]
    def gvarstmt(self,vstmt):
        #print('Hi')
        #print(str(vstmt[0]))
        
        return NAMESPACE[str(vstmt[0])]
    def prtstmt(self,stmt):
        #print(type(stmt[0]))
        #print('Hiiiii!')
        #print(str(stmt[0]))
        try:
            str(stmt[0])
            tryexceptblock = True
        except:
            tryexceptblock = False
        if not str(type(stmt[0])) == '<class \'lark.tree.Tree\'>' and not str(type(stmt[0])) == "<class 'lark.lexer.Token'>" :
            
            print(str(stmt[0]))
        elif tryexceptblock:
            print(str(stmt[0])[1:-1])
        
        
    def explword(self,wd):
        return str(wd[0])
    def modulestmt(self,fi):
        #print(fi)
        for i in open(str(fi[0]) + '.poopy').readlines():
            prs = p.parse(i)
            self.transform(prs)
    def fview(self,s):
        return str('fview ' + s[0])
    def newline(self,stmt):
        global FNAMESPACE
        #print(stmt)
        #print(str(stmt[0]))
        tempo = []
        for i in stmt:
            tempo.append(str(i))
        #print(tempo)
        if type(tempo[0]) == type('poopy stinky'):
            self.cname = str(tempo[0])
            FNAMESPACE[self.cname] = []
        
        return stmt
        
    def pyexpr(self,expr):
        #print(str(expr[0]))
        return eval(str(expr[0])[1:-1],NAMESPACE)
            
                
        
        
    
'''        
print(PSTransformer().transform(prsd))
print(PSTransformer().transform(prsd2))
print(PSTransformer().transform(prsd3))
print(PSTransformer().transform(prsd4))
PSTransformer().transform(prsd5)
PSTransformer().transform(prsd6)
PSTransformer().transform(prsd7)
PSTransformer().transform(prsd8)
'''
