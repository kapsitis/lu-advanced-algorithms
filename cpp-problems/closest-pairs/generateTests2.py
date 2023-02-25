import random

def main():
    # Test01...Test03 - Manual

    # Test04:
    lines = list()
    vv = list()
    for i in range(0, 20):
        vv.append(random.randint(1, 99))
    vv.append(0)
    lines.append(' '.join(list(map(lambda x: str(x), vv))))
#    with open('test2.04.txt', mode='w') as myfile:
#        myfile.write('\n'.join(lines))
#        myfile.write('\n')

    # Test05:
    lines = list()
    vv = list()
    for i in range(0, 200):
        vv.append(random.randint(1, 9999))
    vv.append(0)
    lines.append(' '.join(list(map(lambda x: str(x), vv))))
#    with open('test2.05.txt', mode='w') as myfile:
#        myfile.write('\n'.join(lines))
#        myfile.write('\n')

    # Test06:
    lines = list()
    vv = list()
    for i in range(0, 2000):
        vv.append(random.randint(1, 999999))
    vv.append(0)
    lines.append(' '.join(list(map(lambda x: str(x), vv))))
#    with open('test2.06.txt', mode='w') as myfile:
#        myfile.write('\n'.join(lines))
#        myfile.write('\n')

    # Test07:
    lines = list()
    vv = random.sample(list(range(1, 101)), 20)
    vv.append(0)
    lines.append(' '.join(list(map(lambda x: str(x), vv))))
#    with open('test2.07.txt', mode='w') as myfile:
#        myfile.write('\n'.join(lines))
#        myfile.write('\n')

    # Test08:
    lines = list()
    vv = random.sample(list(range(1, 1001)), 200)
    vv.append(0)
    lines.append(' '.join(list(map(lambda x: str(x), vv))))
#    with open('test2.08.txt', mode='w') as myfile:
#        myfile.write('\n'.join(lines))
#        myfile.write('\n')

    # Test09:
    lines = list()
    vv = random.sample(list(range(1, 2001)), 2000)
    vv.append(0)
    lines.append(' '.join(list(map(lambda x: str(x), vv))))
#    with open('test2.09.txt', mode='w') as myfile:
#        myfile.write('\n'.join(lines))
#        myfile.write('\n')

    # Test10:
    lines = list()
    vv = list()
    for i in range(0, 2000):
        vv.append(random.randint(1, 1000000001))
    vv.append(0)
    lines.append(' '.join(list(map(lambda x: str(x), vv))))
    with open('test2.10.txt', mode='w') as myfile:
        myfile.write('\n'.join(lines))
        myfile.write('\n')


if __name__ == '__main__':
    main()