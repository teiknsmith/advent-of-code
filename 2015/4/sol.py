import hashlib


def solve():
    o = input()
    for i in range(int(1e7)):
        to_hash = (o + str(i)).encode('utf-8')
        front_of_hash = hashlib.md5(to_hash).hexdigest()[:6]
        if front_of_hash == "000000":
            print(i)
            break


if __name__ == '__main__':
    solve()
