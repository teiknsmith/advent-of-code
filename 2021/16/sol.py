import functools as fntls
import operator as op

def cmp_to_op(cmp):
    return lambda vs: int(cmp(*(vs[:2])))

class Pkt:

    OPERATORS = [
        sum,
        fntls.partial(fntls.reduce, op.mul),
        min,
        max,
        None,
        cmp_to_op(op.gt),
        cmp_to_op(op.lt),
        cmp_to_op(op.eq),
    ]

    def __init__(self, version, type_id, payload):
        self.version = version
        self.type_id = type_id
        self.is_operator = type_id != 4
        if self.is_operator:
            self.subpkts = payload
            value = self.__evaluate()
        else:
            value = payload
        self.value = value

    def __evaluate(self):
        return Pkt.OPERATORS[self.type_id]([p.value for p in self.subpkts])

    @staticmethod
    def hex_to_bits(hex):
        return str(bin(int(hex, base=16)))[2:].zfill(len(hex) * 4)

    @classmethod
    def from_bits(cls, bits):
        pkt, _ = cls.__from_bits(bits, 0)
        return pkt

    @classmethod
    def from_hex(cls, hex):
        return cls.from_bits(cls.hex_to_bits(hex))

    @classmethod
    def __from_bits(cls, bits, si):
        version = int(bits[si:si + 3], base=2)
        type_id = int(bits[si + 3:si + 6], base=2)
        if type_id == 4:
            lit_bits_sc = si + 6
            lit_bits = []
            while bits[lit_bits_sc] == "1":
                lit_bits += bits[lit_bits_sc + 1:lit_bits_sc + 5]
                lit_bits_sc += 5
            lit_bits += bits[lit_bits_sc + 1:lit_bits_sc + 5]
            lit_bits_sc += 5
            value = int(''.join(lit_bits), base=2)
            return Pkt(version, type_id, value), lit_bits_sc
        else:
            len_type = bits[si + 6]
            if len_type == "0":
                len_subs = int(bits[si + 7:si + 7 + 15], base=2)
                subs = []
                start_sub_i = si + 7 + 15
                while start_sub_i < si + 7 + 15 + len_subs:
                    pkt, start_sub_i = Pkt.__from_bits(bits, start_sub_i)
                    subs.append(pkt)
                return Pkt(version, type_id, subs), start_sub_i
            else:
                num_subs = int(bits[si + 7:si + 7 + 11], base=2)
                subs = []
                start_sub_i = si + 7 + 11
                for _ in range(num_subs):
                    pkt, start_sub_i = Pkt.__from_bits(bits, start_sub_i)
                    subs.append(pkt)
                return Pkt(version, type_id, subs), start_sub_i


def solve():
    pkt = Pkt.from_hex(input())
    print(pkt.value)


if __name__ == '__main__':
    solve()
