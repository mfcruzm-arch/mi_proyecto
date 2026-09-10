import random

class Cliente:
    __dni: str
    __nombre:str
    __apellidos:str

    def __init__(self, dni, nombre, apellidos):
        self.__dni= dni
        self.__nombre = nombre
        self.__apellidos = apellidos

    def get_nombre(self):
        return(f'{self.__nombre}, {self.__apellidos}')

    def get_dni(self):
        return self.__dni

class Movimiento:
    __concepto:str
    __cantidad:float

    def __init__(self, concepto, cantidad):
        self.__concepto = concepto
        self.__cantidad = cantidad

    def get_cantidad(self):
        return self.__cantidad

class Cuenta:
    __numero:int
    __titular:Cliente
    __movimientos:list[Movimiento]

    def __init__(self, titular:Cliente):
        self.__titular = titular
        self.__numero = int("".join([str(random.randint(0, 9)) for _ in range(10)]))
        self.__saldo = 0
        self.__movimientos = []

    def get_saldo(self):
        return self.__saldo

    def get_titular(self):
        return self.__titular

    def set_movimiento(self, movimiento):
        self.__movimientos.append(movimiento)
        self.__saldo += movimiento.get_cantidad()

    
# Creación de clientes
clientes = []

clientes.append(Cliente('12345678Z','José Antonio','Ribera Ordóñez'))
clientes.append(Cliente('98765M','María de la O', 'Pérez Serrano'))

for cliente in clientes:
    print(cliente.get_nombre(),' DNI:',cliente.get_dni())

# Creación de cuentas
cuentaPepe = Cuenta(clientes[0])
print(f'El saldo de {cuentaPepe.get_titular().get_nombre()} es de {cuentaPepe.get_saldo()} €')

cuentaPepe.set_movimiento(Movimiento('Ingreso inicial',1000))
print(f'El saldo de {cuentaPepe.get_titular().get_nombre()} es de {cuentaPepe.get_saldo()} €') 