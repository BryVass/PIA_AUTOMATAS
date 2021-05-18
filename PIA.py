# Tipos de tokens

ENTERO = 'ENTERO'
MAS = 'MAS'
MENOS = 'MENOS'
FIN = 'FIN'
MUL = 'MUL'
DIV = 'DIV'
PARI = '('
PARD = ')'



class Token(object):
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        return 'Token({tipo}, {valor})'.format(
            tipo=self.tipo, valor=repr(self.valor))
    
    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.caracter_actual = self.texto[self.pos]

    def error(self):
        raise Exception('Caracter invalido')

    def ignorar_espacios(self):
        while self.caracter_actual is not None and self.caracter_actual.isspace():
            self.avanzar()
    
    def avanzar(self):
        self.pos += 1
        if self.pos > len(self.texto) - 1:
            self.caracter_actual = None
        else:
            self.caracter_actual = self.texto[self.pos]
    
    def entero(self):
        num = ''
        while self.caracter_actual is not None and self.caracter_actual.isdigit():
            num += self.caracter_actual
            self.avanzar()
        return int(num)

    def sig_token(self):

        while self.caracter_actual is not None:
            
            if self.caracter_actual.isspace():
                self.ignorar_espacios()
                continue
            elif self.caracter_actual.isdigit():
                return Token(ENTERO, self.entero())
            elif self.caracter_actual == '+':
                self.avanzar()
                return Token(MAS, '+')
            elif self.caracter_actual == '-':
                self.avanzar()
                return Token(MENOS, '-')
            elif self.caracter_actual == '*':
                self.avanzar()
                return Token(MUL, '*')
            elif self.caracter_actual == '/':
                self.avanzar()
                return Token(DIV, '/')
            elif self.caracter_actual == '(':
                self.avanzar()
                return Token(PARI, '(')
            elif self.caracter_actual == ')':
                self.avanzar()
                return Token(PARD, ')')
            
            self.error()
        return Token(FIN, None)



class Interprete(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_actual = self.lexer.sig_token()
        self.parentesis = False

    def error(self):
        raise Exception('Error de sintaxis')

    def consumir(self, tipo_token):
        if self.token_actual.tipo == tipo_token:
            self.token_actual = self.lexer.sig_token()
        else:
            self.error()


    def factor(self):
        token = self.token_actual
        if token.tipo == ENTERO:
            self.consumir(ENTERO)
        elif token.tipo == MENOS:
            self.consumir(MENOS)
            self.consumir(ENTERO)
        elif token.tipo == PARI:
            self.consumir(PARI)
            self.parentesis = True
            self.expresion()
            self.consumir(PARD)
        else:
            self.error()

    def termino(self):
        self.factor()
        while self.token_actual.tipo in (MUL, DIV):
            token = self.token_actual
            if token.tipo == MUL:
                self.consumir(MUL)  
                self.factor()
            elif token.tipo == DIV:
                self.consumir(DIV)
                self.factor()
            else:
                self.error()

    def expresion(self):
        # Expresion -> termino ((*|/)termino)*
        self.termino()
        while self.token_actual.tipo in (MAS, MENOS):
            token = self.token_actual
            if token.tipo == MAS:
                self.consumir(MAS)
                self.termino()
            elif token.tipo == MENOS:
                self.consumir(MENOS)
                self.termino()
            else:
                self.error()
        if self.token_actual.tipo == PARD and self.parentesis is False:
            self.error()

def main():
    while True:
        try:
            texto = input('calc> ')
        except EOFError:
            break
        if not texto:
            continue
        lexer = Lexer(texto)
        interprete = Interprete(lexer)
        resultado = interprete.expresion()
        if resultado is None:
            print('Cadena Valida')

if __name__ == '__main__':
    main()