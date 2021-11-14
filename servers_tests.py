import unittest
from collections import Counter

from servers_skeleton import *

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    # Czy wyniki zwrócone przez serwer przechowujący dane w liście są poprawnie posortowane?
    def test_get_entries_returns_sorted_list_data(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        server = ListServer(products)
        entries = server.get_entries(2)
        self.assertEqual([products[2], products[1]], entries)

    # Czy przekroczenie maksymalnej liczby znalezionych produktów powoduje rzucenie wyjątku?
    def test_get_entries_raise_too_many_products_exception(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)] * Server.n_max_returned_entries
        server = ListServer(products)
        with self.assertRaises(TooManyProductsFoundError):
            server.get_entries(2)


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    # Czy funkcja obliczająca łączną cenę produktów zwraca poprawny wynik w przypadku rzucenia wyjątku oraz\
    # braku produktów pasujących do kryterium wyszukiwania?
    def test_total_price_raise_exception_or_no_product_found_error(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(0, client.get_total_price(1))


if __name__ == '__main__':
    unittest.main()
