"""БД на хранение 500 записей."""
_CONST_1 = 523
_CONST_2 = 7


def hash_string(string):
    hash_str = abs(string.encode('ascii')[0] + string.encode('ascii')[len(string) - 1] * _CONST_2) % _CONST_1
    return hash_str

#
# if __name__ == "__main__":
#     test = "qwer"
#     letter = d.encode('ascii')[0]
#     hash = hash_string(d)
#     print()
