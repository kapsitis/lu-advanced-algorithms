import random

def main():

    # Test01...Test03 - Manual

    # Test04:
    lines = list()
    for i in range(0, 3):
        vv = list()
        for j in range(0, 5):
            vv.append(random.randint(3, 4))
        lines.append(' '.join(list(map(lambda x: str(x), vv))))
    #    with open('test1.04.txt', mode='w') as myfile:
    #        myfile.write('\n'.join(lines))
    #        myfile.write('\n')

    # Test05:
    lines = list()
    for i in range(0, 3):
        vv = list()
        for j in range(0, 5):
            vv.append(random.randint(999999994, 1000000000))
        lines.append(' '.join(list(map(lambda x: str(x), vv))))
    #    with open('test1.05.txt', mode='w') as myfile:
    #        myfile.write('\n'.join(lines))
    #        myfile.write('\n')

    # Test06:
    lines = list()
    for i in range(0, 3):
        vv = list()
        for j in range(0, 5):
            vv.append(random.randint(-1000000000, 1000000000))
        lines.append(' '.join(list(map(lambda x: str(x), vv))))
    #    with open('test1.06.txt', mode='w') as myfile:
    #        myfile.write('\n'.join(lines))
    #        myfile.write('\n')



    # Test07: All
    lines = list()
    for i in range(0,3):
        vv = list()
        for j in range(0,5):
            vv.append(random.randint(-50,0))
        lines.append(' '.join(list(map(lambda x: str(x), vv))))
#    with open('test1.07.txt', mode='w') as myfile:
#        myfile.write('\n'.join(lines))
#        myfile.write('\n')


    # Test08: All negative
    lines = list()
    for i in range(0,3):
        vv = list()
        for j in range(0,5):
            vv.append(random.randint(-2,-1))
        lines.append(' '.join(list(map(lambda x: str(x), vv))))
#    with open('test1.08.txt', mode='w') as myfile:
#        myfile.write('\n'.join(lines))
#        myfile.write('\n')


    # Test09: All negative - and very different
    lines = list()
    for i in range(0,3):
        vv = list()
        for j in range(0,5):
            vv.append(random.randint(-1000000000, -1))
        lines.append(' '.join(list(map(lambda x: str(x), vv))))
#    with open('test1.09.txt', mode='w') as myfile:
#        myfile.write('\n'.join(lines))
#        myfile.write('\n')

    # Test10: All very negative
    lines = list()
    for i in range(0,3):
        vv = list()
        for j in range(0,5):
            vv.append(random.randint(-1000000000, -999999994))
        lines.append(' '.join(list(map(lambda x: str(x), vv))))
    #with open('test1.10.txt', mode='w') as myfile:
    #    myfile.write('\n'.join(lines))


if __name__ == '__main__':
    main()