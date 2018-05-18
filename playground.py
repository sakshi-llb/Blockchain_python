# For the fill_block algo

a = [1, 2, 3, 4, 5, 6, 7, 8]
v = []
# v[1] = a.pop()
# print(v, a)
v.append(a.pop(0))
# print(v, a)
v.append(a.pop())
# print(v, a)


# print(v, a)

block = {
    'transactions': []
}
block['transactions'] = [1, 2, 3]

# print(block['transactions'][0])
import hashlib
from uuid import uuid4
print(uuid4().hex)
