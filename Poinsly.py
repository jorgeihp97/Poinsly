from sly import Lexer, Parser
import cmath

class PoinLexer(Lexer):
    tokens = { NUMBER, ADD, EXP, TOKEN_X } #,SUB,
    ignore = ' \t'

    # Tokens
    NUMBER =r'\d+'
    ADD = r'\+'
    #SUB = r'-'
    EXP = r'\^'
    TOKEN_X = r'[xX]'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character: '%s'" % t.value[0])
        self.index += 1

class PoinParser(Parser):
    debugfile = 'Pparser.txt'
    tokens = PoinLexer.tokens

    precedence = (
        ('left', 'TOKEN_X', 'ADD'),
        ('left', 'EXP'),
        #('right', 'UMINUS'),
        )

    def __init__(self):
        self.names = { }
    
   #Intermediate Code v
    @_('linear_term')
    def number(self, p):
        return p.linear_term

    @_('quadratic_term')
    def number(self, p):
        return p.quadratic_term

    @_('number TOKEN_X')
    def linear_term(self, p):
        return p.number

    @_('number TOKEN_X EXP number')
    def quadratic_term(self, p):
        if p.number1 == 2:
            return p.number0
        else:
            print("Illegal character: ", p.number1)
    
    @_('quadratic_term ADD linear_term ADD number') 
    def number(self, p):
        print('\nQuadratic formula is ax^2 + bx +c = 0 \n' , 'a = ', p.quadratic_term, ', b = ', p.linear_term,
        ', c = ', p.number, '\n')
        #if p.number1 != 2:
            #print("Illegal character: ", p.quadratic_term.number1)
        #else:
        discriminant = (p.linear_term ** 2) - (4 * p.quadratic_term * p.number)
        print('Discriminant = ', discriminant)
        if discriminant > 0:
                print('Real and different roots\n')
                solution1 = (-p.linear_term + cmath.sqrt(discriminant))/(2*p.quadratic_term)
                solution2 = (-p.linear_term - cmath.sqrt(discriminant))/(2*p.quadratic_term)
                return solution1 , solution2
        elif discriminant == 0:
                print('Real and same roots\n')
                solution3 = (-p.linear_term /(2*p.quadratic_term))
                return solution3
        else:
                print('No real solutions\n')

        
    #Intermediate Code ^
    @_('NUMBER')
    def number(self, p):
        return p.NUMBER

    # @_('SUB number %prec UMINUS')
    #  def number(self, p):
    #    return p.number 

if __name__ == '__main__':
    lexer = PoinLexer()
    parser = PoinParser()
    print('Poinsly Language\n')
    while True:
        try:
            text = input('--> ')
            result = parser.parse(lexer.tokenize(text))
            print(result)
        except EOFError:
            break
            
