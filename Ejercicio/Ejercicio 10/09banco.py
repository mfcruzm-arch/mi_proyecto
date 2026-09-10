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

    def get_numero(self):
        return self.__numero

    def get_saldo(self):
        return self.__saldo

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
cuentas:list[Cuenta] = []

cuentas.append(Cuenta(clientes[0]))
print(f'El saldo de {cuentas[0].get_titular().get_nombre()} es de {cuentas[0].get_saldo()} €')

cuentas[0].set_movimiento(Movimiento('Ingreso inicial',1000))
cuentas[0].set_movimiento(Movimiento('Ingreso ',30))
cuentas[0].set_movimiento(Movimiento('Retirada ',-500))
print(f'El saldo de {cuentas[0].get_titular().get_nombre()} es de {cuentas[0].get_saldo()} €')

# Listar las cuentas de clientes[0]
print(clientes[0].get_dni())
print(cuentas[0].get_titular().get_dni())
for cuenta in cuentas:
    if cuentas[0].get_titular().get_dni() == clientes[0].get_dni() :
        print(f'D. {cuenta.get_titular().get_nombre()} es titular de la cuenta {cuenta.get_numero()} con un saldo de {cuenta.get_saldo()}') 

