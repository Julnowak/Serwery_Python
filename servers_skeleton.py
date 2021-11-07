#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional
from abc import ABC, abstractmethod  #interfejsy i klasy


class Product:
    def __init__(self, name: str, price: float):
        self.name: str = name
        self.price: float = price
    # DONE
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)

    def __eq__(self, other):
        return self.name == other.name  # FIXME: zwróć odpowiednią wartość
    
    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass



class Server(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod  # tutaj wymuszamy implementację tej metody w klasach pochodnych
    def nazwa_gatunku(self):
        pass

# FIXME: Każda z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania


OurServerType = TypeVar('Server', bound=Server)   # HelperType for our serwer


class ListServer(Server):
    n_max_returned_entries: int = 10

    def __init__(self, products: List[Product]) -> None:
        super().__init__()
        self.products: List[Product] = products

    def get_entries(self, n_letters: int) -> List[Product]:
        return self.products


class MapServer(Server):
    n_max_returned_entries: int = 10

    def __init__(self, products: List[Product]) -> None:
        super().__init__()
        d = dict()
        for product in products:
            d[product.name] = product
        self.products: Dict[str, Product] = d

    def get_entries(self, n_letters: int) -> List[Product]:
        return list(self.products.values())


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, serwer: OurServerType):   ## Czy to jest dobrze?
        self.serwer: OurServerType = serwer

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        raise NotImplementedError()