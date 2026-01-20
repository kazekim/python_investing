print(['hello' for x in [1,2,3,4,5] if x <= 3])

for i in [1,2,3,4,5]:
    if i <= 3:
        print('hello')

print(['hello' if x == 1 else 'nothing' for x in [1,2,3,4,5]])

for i in [1,2,3,4,5]:
    if i == 1:
        print('hello')
    else:
        print('nothing')

for i in [1,2,3,4,5]:
    if i == 1:
        print('hello')
    elif i == 2:
        print('hello 2')
    else:
        print('nothing')

print(['hello' if x == 1 else ('hello 2' if x == 2 else 'nothing') for x in [1,2,3,4,5]])