# Tipos de tokens

ENTERO, MAS, MENOS, MUL, DIV, FIN = 'ENTERO', 'MAS', 'MUL', 'DIV', 'MENOS', 'FIN'

class Token(object):
    
    def __init__(self, tipo, valor):
        # Tipo del token, ENTERO, MAS, FIN
        self.tipo = tipo

        # Valor del token: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, +, o None
        self.valor = valor

    def __str__(self):
        """Representacion en forma de cadena del objeto de esta clase.

        Ejemplos
        Token(ENTERO, 3)
        Token(MAS, '+')
        """
        return 'Token({tipo}, {valor})'.format(
            tipo = self.tipo,
            valor = repr(self.valor)
        )

    def __repr__(self):
        """ "Respuesta Print", esta funcion ejecuta este codigo
            cuando llamas a la funcion print con una instancia
            de este codigo como argumento print(token)
        """
        return self.__str__()


class Interprete(object):
    def __init__(self, texto):
        # Cadena de entrada, por ejemplo 3+5
        self.texto = texto
        # Self.pos es un indice dentro de self.texto
        self.pos = 0
        # Token en el que se encuentra actualmente
        self.token_actual = None
        self.caracter_actual = self.texto[self.pos]

    def error(self):
        raise Exception('Error analizando la entrada')

    def avanzar(self):
        """Avanza en la "pos" y establece la variable "caracter_actual" """
        self.pos += 1
        if self.pos > len(self.texto) - 1:
            self.caracter_actual = None # Indica el final de la entrada
        else:
            self.caracter_actual = self.texto[self.pos]
        
    def ignorar_espacios(self):
        while self.caracter_actual is not None and self.caracter_actual.isspace():
            self.avanzar()

    def entero(self):
        """Regresa un entero de varios digitos consumidos de la entrada"""
        resultado = ''
        while self.caracter_actual is not None and self.caracter_actual.isdigit():
            resultado += self.caracter_actual
            self.avanzar()
        return int(resultado)

    
    def conseguir_siguiente_token(self):
        """Analizador lexico (Tokenizador o escaner le dicen)
        
        Este metodo se encarga de separar la cadena de entrada
        en tokens. Un token a la vez
        """
        while self.caracter_actual is not None:
            
            if self.caracter_actual.isspace():
                if self.pos == 0:
                    return self.error()
                else:
                    self.ignorar_espacios()
                    continue
            
            if self.caracter_actual.isdigit():
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
            elif self.caracter_actual == ';':
                return Token(FIN, None)
            else:
                self.error()
    
    def consumir(self, tipo_token):
        # Compara el tipo del token actual con el tipo del token anterior
        # y si son iguales se "come" al token actual y asigna el siguiente
        # token a self.token_actual, de otra manera, crea una excepcion
        if self.token_actual is not None:
            if self.token_actual.tipo == tipo_token:
                self.token_actual = self.conseguir_siguiente_token()
            else:
                self.error()
        else:
            self.error()

    def termino(self):
        self.consumir(ENTERO)
        
            
    def expresion(self):
        """expresion -> ENTERO MAS ENTERO"""
        # Define el token actual como el primer token que se saco de la
        # cadena de entrada
        self.token_actual = self.conseguir_siguiente_token()
        self.termino()
        # Se espera que el token actual sea un solo digito entero
        try:
            while self.token_actual.tipo in (MAS, MENOS):
                token = self.token_actual
                if token.tipo == MAS:
                    self.consumir(MAS)
                    self.termino()
                elif token.tipo == MENOS:
                    self.consumir(MENOS)
                    self.termino()     ##########Checar por aqui algo anda raro
            return 'Cadena Valida'
        except AttributeError:
            self.error()

def main():
    while True:
        try:
            texto = input('calc> ')
        except EOFError:
            break
        if not texto:
            continue
        interprete = Interprete(texto)
        resultado = interprete.expresion()
        print(resultado)

if __name__ == '__main__':
    main()
