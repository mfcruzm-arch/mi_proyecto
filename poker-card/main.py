# Here you have the suits symbols:
# ♣ ◆ ❤ ♠

# TODO
import os


class InvalidCardError(Exception):
    """Excepción personalizada para errores de cartas inválidas."""
    def __init__(self, message: str = ''):
        if message:
            super().__init__(f"Invalid card: {message}")
        else:
            super().__init__("Invalid card")


class Card:
    SUITS = {'♣', '♦', '♠', '♥'}
    VALID_STR_VALUES = {'A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'}
    _glyphs_cache = None

    def __init__(self, value: int | str, suit: str):
        # Validación del palo (suit)
        if suit not in self.SUITS:
            raise InvalidCardError(f"{repr(suit)} is not a supported suit")
        self.suit = suit

        # Validación del valor
        if isinstance(value, int):
            if not (1 <= value <= 13):
                raise InvalidCardError(f"{repr(value)} is not a supported value")
            self.value = value
        elif isinstance(value, str):
            if value not in self.VALID_STR_VALUES:
                raise InvalidCardError(f"{repr(value)} is not a supported symbol")
            self.value = value
        else:
            raise InvalidCardError(f"{repr(value)} is not a supported value")

    @classmethod
    def _load_glyphs(cls) -> dict:
        """Carga los glifos desde el fichero data/glyphs.dat si existe."""
        if cls._glyphs_cache is not None:
            return cls._glyphs_cache
        
        cls._glyphs_cache = {}
        path = "data/glyphs.dat"
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split(":")
                        if len(parts) == 2:
                            cls._glyphs_cache[parts[0]] = parts[1]
            except Exception:
                pass
        return cls._glyphs_cache

    def __repr__(self) -> str:
        glyphs = self._load_glyphs()
        key = f"{self.value}{self.suit}"
        if key in glyphs:
            return glyphs[key]
        return f"{self.value}{self.suit}"

    def _to_numeric_value(self) -> int:
        """Convierte la carta a un valor numérico para comparaciones (As = 14)."""
        if self.value == 'A' or self.value == 1:
            return 14
        if isinstance(self.value, int):
            return self.value
        mapping = {'J': 11, 'Q': 12, 'K': 13, '10': 10}
        return mapping.get(str(self.value), 0)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self._to_numeric_value() == other._to_numeric_value()

    def __lt__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self._to_numeric_value() < other._to_numeric_value()

    def __gt__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self._to_numeric_value() > other._to_numeric_value()

    def __add__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        
        def raw_val(v):
            if v == 'A' or v == 1:
                return 1
            if isinstance(v, int):
                return v
            return {'J': 11, 'Q': 12, 'K': 13}.get(v, 1)

        suma = raw_val(self.value) + raw_val(other.value)
        nuevo_valor = 'A' if suma > 13 else suma

        if other > self:
            nuevo_palo = other.suit
        else:
            nuevo_palo = self.suit

        return Card(nuevo_valor, nuevo_palo)

    @classmethod
    def get_available_suits(cls) -> str:
        return "".join(cls.SUITS)

    @classmethod
    def get_cards_by_suit(cls, suit: str):
        if suit not in cls.SUITS:
            return
        for val in ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']:
            yield Card(val, suit)


# comprobacion a partir de aqui, no tocar nada de lo anterior
if __name__ == "__main__":
    print("--- 1. Pruebas de Creación y Excepciones ---")
    try:
        c1 = Card('A', '♠')
        print(f"Carta creada correctamente: {c1}")
    except InvalidCardError as e:
        print(e)

    try:
        # Probando un valor entero fuera de rango (debe saltar la excepción)
        c_err1 = Card(15, '♥')
    except InvalidCardError as e:
        print(f"Excepción capturada con éxito -> {e}")

    try:
        # Probando un palo inválido (debe saltar la excepción)
        c_err2 = Card(5, 'X')
    except InvalidCardError as e:
        print(f"Excepción capturada con éxito -> {e}")

    print("\n--- 2. Pruebas de Comparación ---")
    card_10 = Card(10, '♥')
    card_king = Card('K', '♦')
    card_ace = Card('A', '♠')

    print(f"¿Es el 10 menor que la K? -> {card_10 < card_king}")
    print(f"¿Es el As mayor que la K? -> {card_ace > card_king} (¡El As vale más!)")

    print("\n--- 3. Pruebas de Suma ---")
    # 5 + 8 = 13 (Rey o valor 13)
    suma1 = Card(5, '♣') + Card(8, '♠')
    print(f"5 ♣ + 8 ♠ = Valor: {suma1.value}, Palo: {suma1.suit}")

    # 8 + 7 = 15 (Supera 13, por lo que se convierte en As 'A')
    suma2 = Card(8, '♥') + Card(7, '♦')
    print(f"8 ♥ + 7 ♦ = Valor: {suma2.value}, Palo: {suma2.suit} (Supera 13, se convierte en As)")

    print("\n--- 4. Métodos de Clase ---")
    print(f"Palos disponibles: {Card.get_available_suits()}")
    print("Cartas generadas para el palo de picas (♠):")
    for carta in Card.get_cards_by_suit('♠'):
        print(f"{carta.value}{carta.suit}", end="  ")
    print()            

    