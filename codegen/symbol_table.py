from collections import namedtuple


Symbol = namedtuple('Symbol', 'name type address size')


class SymbolTable:
    class Types:
        VARIABLE = 'VARIABLE'
        ARRAY = 'ARRAY'

    def __init__(self):
        self.symbols = []
        self.last_address = 100

    def get_address(self, var):
        # print('SymT: lookup', var)
        for symbol in self.symbols[::-1]:
            if symbol.name == var:
                return symbol.address
        return 'NaN'

    def get_temp(self):
        return self.insert_var('')

    def insert_var(self, var):
        self.symbols.append(Symbol(
            var,
            SymbolTable.Types.VARIABLE,
            self.last_address,
            1,
        ))
        self.last_address += 4
        return self.symbols[-1].address

    def insert_arr(self, var, size):
        # print(f'SymT: arr insert {var}')
        self.symbols.append(Symbol(
            var,
            SymbolTable.Types.ARRAY,
            self.last_address,
            size,
        ))
        self.last_address += 4 * size
        return self.symbols[-1].address
