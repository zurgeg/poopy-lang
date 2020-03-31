print('PoopyLang Parser 0.1.0.0')
from lark import Lark, Transformer, Tree
from lark.reconstruct import Reconstructor

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
      | explword
      | ifexpr
      | expr
      | stmt
      | numstmt
      | varstmt
      | gvarstmt
      | prtstmt
explword: "'" value "'"
ifexpr: "if" value ":"
stmt: "=>"
numstmt: expr stmt expr
expr: add
    | subtract
    | divide
    | multiply
    | NUMBER
add:  expr "+" expr
subtract: expr "-" expr 
divide: expr "/" expr
multiply: expr "*" expr
gvarstmt: WORD ">>"
varstmt: WORD "=" value
prtstmt: "view" value

%import common.NUMBER
%import common.WORD
%ignore " "
'''

p = Lark(psl_grammer, parser='lalr')

'''
prsd = p.parse('1+2+1+1-2*2/2')
print(prsd)

prsd2 = p.parse('if 1 => 2+2:')

prsd3 = p.parse('hello=if 2+2 => 4+0:')

prsd4 = p.parse('hello >>')

prsd5 = p.parse('view hello >>')
'''
NAMESPACE = {}
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
            #return rt
        except:
            
            if numbers[0].data == 'add':
                self.tsum = numbers[0].children[1] + numbers[0].children[0] #Embrace the communitve property!
            elif numbers[0].data == 'subtract':
                self.tsum = numbers[0].children[0] - numbers[0].children[1]
            elif numbers[0].data == 'multiply':
                self.tsum = numbers[0].children[1] * numbers[0].children[0] #Embrace the communitve property!
            if numbers[0].data == 'divide':
                self.tsum = numbers[0].children[0] / numbers[0].children[1] #Embrace the communitve property!
            rt = self.tsum
        return rt
    def ifexpr(self,exp):
        #print(exp)
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
        if not str(type(stmt[0])) == '<class \'lark.tree.Tree\'>' and not str(type(stmt[0])) == "<class 'lark.lexer.Token'>":
            
            print(str(stmt[0]))
    def explword(self,wd):
      return str(wd[0])
'''
print(PSTransformer().transform(prsd))
print(PSTransformer().transform(prsd2))
print(PSTransformer().transform(prsd3))
print(PSTransformer().transform(prsd4))
PSTransformer().transform(prsd5)
'''
