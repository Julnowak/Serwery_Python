# 3b: Nowak (407203), Malatyński (403420), Huczek (408378)
# !/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, TypeVar, List, Dict
from abc import ABC, abstractmethod  # interfejsy i klasy
import re


class Product:
    def __init__(self, name: str, price: float) -> None:
        pat = f'^[a-zA-Z]+[0-9]+$'
        if price > 0 and re.fullmatch(pat, name):
            self.name: str = name
            self.price: float = price
        else:
            raise ValueError

    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu\
    #  (typu str) i\ jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str)\
    #  oraz `price` (typu float)

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price  # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


class ServerError(Exception):
    """Ogólna klasa błędów serwera"""


class TooManyProductsFoundError(ServerError):
    """Znaleziono zbyt dużą liczbę produktów"""


class Server(ABC):
    n_max_returned_entries: int = 10

    def __init__(self) -> None:
        super().__init__()

    def get_entries(self, n_letters: int = 1):
        if n_letters > 0 and isinstance(n_letters, int):
            lista = []
            wzor = f'^[a-zA-Z]{{{n_letters}}}\\d{{2,3}}$'
            for entry in self._get_entries(n_letters):
                if re.fullmatch(wzor, entry.name):
                    lista.append(entry)
            if Server.n_max_returned_entries < len(lista):
                raise TooManyProductsFoundError
            else:
                return sorted(lista, reverse=False, key=lambda x: x.price)
        else:
            raise ValueError

    @abstractmethod  # tutaj wymuszamy implementację tej metody w klasach pochodnych
    def _get_entries(self, n_letters: int):
        raise NotImplementedError


# FIXME: Każda z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products`\
#   zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną\
#   dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających\
#   kryterium wyszukiwania


OurServerType = TypeVar('OurServerType', bound=Server)  # HelperType for our server


class ListServer(Server):

    def __init__(self, products: List[Product]) -> None:
        super().__init__()
        self.products: List[Product] = products

    def _get_entries(self, n_letters: int = 1) -> List[Product]:
        return self.products


class MapServer(Server):

    def __init__(self, products: List[Product]) -> None:
        super().__init__()
        d = dict()
        for product in products:
            d[product.name] = product
        self.products: Dict[str, Product] = d

    def _get_entries(self, n_letters: int = 1) -> List[Product]:
        return list(self.products.values())


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, serwer: OurServerType) -> None:
        self.serwer: OurServerType = serwer

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            suma = 0
            if n_letters is None:
                n_letters = 1
            entries = self.serwer.get_entries(n_letters)
            for entry in entries:
                suma += entry.price
            return suma
        except TooManyProductsFoundError:
            return 0

# 3b: Nowak (407203), Malatyński (403420), Huczek (408378)
