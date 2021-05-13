from sly import Lexer, Parser
import cmath
import numpy as np
import matplotlib.pyplot as plt

class PoinLexer(Lexer):
    tokens = { NUMBER, ADD, EXP, TOKEN_X} 
    ignore = ' \t'

    # Tokens
    NUMBER =r'-?\d+'
    ADD = r'\+'
    EXP = r'\^'
    TOKEN_X = r'[xX]'

    @_(r'-?\d+')
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
        )

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
            print("Illegal character: X^", p.number1, "Only enter number'2' ")
    
    @_('linear_term ADD number') 
    def number(self, p):
     try:
        a = (-p.number)/p.linear_term
        print("Solving for x solution: \n", a)
        print("Linear equation graph: \n")
        x = np.linspace(-5, 5, 100)
        y = p.linear_term * x + p.number
        plt.title("graph",) 
        plt.xlabel("x axis") 
        plt.ylabel("y axis")
        plt.plot(x,y)
        plt.grid() 
        plt.show()
        return a
     except:
          print('Illegal character entered please try again, variable must be x or X')

    @_('quadratic_term ADD linear_term ADD number') 
    def number(self, p):
        print('\nQuadratic formula is ax^2 + bx +c = 0 \n' , 'a = ', p.quadratic_term, ', b = ', p.linear_term,
        ', c = ', p.number, '\n')
        try:
            a = p.quadratic_term
            b = p.linear_term
            c = p.number
            discriminant = (b ** 2) - (4 * a * c)
            if discriminant > 0:
                print('Real and different roots\n')
                solution1 = (-b+ cmath.sqrt(discriminant))/(2*a)
                solution2 = (-b- cmath.sqrt(discriminant))/(2*a)
                print(solution1 , solution2)
                x = np.linspace(-20,20,50)
                y = a*x**2+b*x+c
                plt.title("Parabola") 
                plt.xlabel("x axis") 
                plt.ylabel("y axis") 
                plt.plot(x,y)
                plt.axhline(y=0, color='black', linestyle='-')
                plt.axvline(x=0, color='black', linestyle='-')
                plt.plot(solution1, 0, marker="o", color='green')
                plt.plot(solution2, 0, marker="o", color='green')
                plt.grid()
                plt.show()
                return 
            elif discriminant == 0:
                print('Real and same roots\n')
                solution3 = (-b /(2*a))
                print(solution3)
                x = np.linspace(-20,20,50)
                y = a*x**2+b*x+c
                plt.title("Parabola") 
                plt.xlabel("x axis") 
                plt.ylabel("y axis") 
                plt.plot(x,y)
                plt.axhline(y=0, color='black', linestyle='-')
                plt.axvline(x=0, color='black', linestyle='-')
                plt.plot(solution3, 0, marker="o", color='green')
                plt.grid()
                plt.show()
                return
            else:
                print('No real solutions\n')
                
        except:
          print('Error: Illegal character was entered in aX^2, bX or C, Suggest looking at input')

    @_('NUMBER')
    def number(self, p):
        return p.NUMBER

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
