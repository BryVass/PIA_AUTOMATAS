# Tipos de tokens

from os import error


ENTERO = 'ENTERO'
MAS    = 'MAS'
MENOS  = 'MENOS'
MUL    = 'MUL'
DIV    = 'DIV'
FINCADENA = 'FINCADENA'
FIN    = 'FIN'

class Token(object):
    
    def __init__(self, tipo, valor):
        self.tipo = tipo

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

    def error(self, tipo_error):
        Error = 'Error: {}'.format(tipo_error)
        print(Error)
        exit()

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
                    # Esto esta para que todo este 
                    # alineado a la izquierda
                    return self.error("todo debe estar alineado a la izquierda")
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
                return Token(FINCADENA, ';')
            else:
                self.error("caracter ilegal")
        return Token(FIN, None)
    
    def consumir_token(self, tipo_token):
        # Esta funcion va consumiendo los Tokens de la cadena
        # Se llama cuando se quiere consumir el token en el que
        # se encuentra, si el tipo que se indica consumir y el tipo del token
        # actual coinciden entonces lo consume

        if self.token_actual.tipo == tipo_token:
            self.token_actual = self.conseguir_siguiente_token()
        else:
            self.error("cadena invalida")

    def termino(self):
        # Se consume un token ENTERO y se consigue el siguiente token
        self.consumir_token(ENTERO)


 
    def expresion(self):
        """expresion -> ENTERO MAS ENTERO"""
        # Define el token actual como el primer token que se saco de la
        # cadena de entrada
        self.token_actual = self.conseguir_siguiente_token()

        # Se consume un token ENTERO
        self.termino()
        while self.token_actual.tipo in (MAS, MENOS, MUL, DIV):
            token = self.token_actual
            if token.tipo == MAS:
                # Se consume un token MAS y se consume un token ENTERO
                self.consumir_token(MAS)
                self.termino()
            elif token.tipo == MENOS:
                # Se consume un token MENOS y se consume un token ENTERO
                self.consumir_token(MENOS)
                self.termino()
            elif token.tipo == MUL:
                self.consumir_token(MUL)
                self.termino()
            elif token.tipo == DIV:
                self.consumir_token(DIV)
                self.termino()
        if self.token_actual.tipo == FINCADENA and self.pos == len(self.texto) - 1:
            self.consumir_token(FINCADENA)
            return 'Cadena aceptada'
        else:
            self.error("Cadena invalida")



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
