import functools as fntls
import operator as op


def cmp_to_op(cmp):
    return lambda vs: int(cmp(*(vs[:2])))


class Pkt:
    VERSION_LEN = 3
    TYPE_ID_LEN = 3
    HEADER_LEN = VERSION_LEN + TYPE_ID_LEN
    LITERAL_GROUP_SIZE = 4

    LITERAL_DO_CONTINUE_FLAG = "1"

    LITERAL_TYPE_ID = 4

    SUBPKTSLEN_BITLEN_TYPE_ID = "0"
    SUBPKTSLEN_NUMPKTS_TYPE_ID = "1"

    SUBPKTSLEN_BITLEN_FIELD_WIDTH = 15
    SUBPKTSLEN_NUMPKTS_FIELD_WIDTH = 11

    OPERATORS = [
        sum,
        fntls.partial(fntls.reduce, op.mul),
        min,
        max,
        "literal",
        cmp_to_op(op.gt),
        cmp_to_op(op.lt),
        cmp_to_op(op.eq),
    ]

    def __init__(self, version, type_id, payload):
        self.version = version
        self.type_id = type_id
        self.is_operator = type_id != self.LITERAL_TYPE_ID
        if self.is_operator:
            self.subpkts = payload
            value = self.__evaluate()
        else:
            value = payload
        self.value = value

    def __evaluate(self):
        return self.OPERATORS[self.type_id]([p.value for p in self.subpkts])

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
        version = int(bits[si:si + cls.VERSION_LEN], base=2)
        type_id = int(bits[si + cls.VERSION_LEN:si + cls.HEADER_LEN], base=2)
        if type_id == cls.LITERAL_TYPE_ID:
            lit_bits_sc = si + cls.HEADER_LEN
            lit_bits = []
            more_groups = True
            while more_groups:
                more_groups = bits[lit_bits_sc] == cls.LITERAL_DO_CONTINUE_FLAG
                lit_bits_sc += 1
                lit_bits += bits[lit_bits_sc:lit_bits_sc +
                                 cls.LITERAL_GROUP_SIZE]
                lit_bits_sc += cls.LITERAL_GROUP_SIZE
            value = int(''.join(lit_bits), base=2)
            return Pkt(version, type_id, value), lit_bits_sc
        else:
            data_idx = si + cls.HEADER_LEN
            len_type = bits[data_idx]
            data_idx += 1
            if len_type == cls.SUBPKTSLEN_BITLEN_TYPE_ID:
                start_sub_i = data_idx + cls.SUBPKTSLEN_BITLEN_FIELD_WIDTH
                len_subs = int(bits[data_idx:start_sub_i], base=2)
                end_sub_i = start_sub_i + len_subs
                subs = []
                while start_sub_i < end_sub_i:
                    pkt, start_sub_i = cls.__from_bits(bits, start_sub_i)
                    subs.append(pkt)
                return Pkt(version, type_id, subs), start_sub_i
            else:
                start_sub_i = data_idx + cls.SUBPKTSLEN_NUMPKTS_FIELD_WIDTH
                num_subs = int(bits[data_idx:start_sub_i], base=2)
                subs = []
                for _ in range(num_subs):
                    pkt, start_sub_i = cls.__from_bits(bits, start_sub_i)
                    subs.append(pkt)
                return Pkt(version, type_id, subs), start_sub_i


def solve():
    pkt = Pkt.from_hex(input())
    print(pkt.value)


if __name__ == '__main__':
    solve()
