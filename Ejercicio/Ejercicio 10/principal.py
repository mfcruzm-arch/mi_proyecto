import importlib.util
from pathlib import Path


_ruta_banco = Path(__file__).with_name('09banco.py')
_especificacion = importlib.util.spec_from_file_location('banco', _ruta_banco)
_banco = importlib.util.module_from_spec(_especificacion)
_especificacion.loader.exec_module(_banco)

Cliente = _banco.Cliente
Cuenta = _banco.Cuenta
Movimiento = _banco.Movimiento


antonio = Cliente('12345678A', 'Antonio', 'Martínez')

cuenta_1 = Cuenta('ES0001', antonio)
cuenta_1.anadir_movimiento(Movimiento('Nómina', 1500))
cuenta_1.anadir_movimiento(Movimiento('Alquiler', -700))
cuenta_1.anadir_movimiento(Movimiento('Compra', -120))

cuenta_2 = Cuenta('ES0002', antonio)
cuenta_2.anadir_movimiento(Movimiento('Ingreso', 800))
cuenta_2.anadir_movimiento(Movimiento('Recibo', -200))
cuenta_2.anadir_movimiento(Movimiento('Transferencia', 100))

print(f'Saldo de la cuenta {cuenta_1.numero}: {cuenta_1.saldo} euros')
print(f'Saldo de la cuenta {cuenta_2.numero}: {cuenta_2.saldo} euros')