import random

def main():
    # Test01 - Manual

    # Test02:
    lines = list()
    vv = list()
    for i in range(0, 20):
        vv.append(random.randint(1, 99))
    tre = max(vv) + 10
    ww = list()
    for i in range(0,20):
        ww.append(tre - vv[i] + random.randint(0,1))
    ww = random.sample(ww, len(ww))
    lines.append(str(tre))
    lines.append(' '.join(list(map(lambda x: str(x), vv))))
    lines.append(' '.join(list(map(lambda x: str(x), ww))))
    lines.append('0')
    lines.append(' '.join(list(map(lambda x: str(x), sorted(vv)))))
    lines.append(' '.join(list(map(lambda x: str(x), sorted(ww)))))
    vv = random.sample(vv, len(vv))
    ww = random.sample(ww, len(ww))
    lines.append(' '.join(list(map(lambda x: str(x), vv))))
    lines.append(' '.join(list(map(lambda x: str(x), ww))))
#    with open('test5.02.txt', mode='w') as myfile:
#        myfile.write('\n'.join(lines))
#        myfile.write('\n')


    # Test03:
    lines = list()
    vv = list()
    for i in range(0, 40):
        vv.append(random.randint(1, 399))
    tre = max(vv) + 10
    ww = list()
    for i in range(0, 40):
        ww.append(tre - vv[i] + random.randint(0,1))
    ww = random.sample(ww, len(ww))
    lines.append(str(tre))
    lines.append(' '.join(list(map(lambda x: str(x), vv))))
    lines.append(' '.join(list(map(lambda x: str(x), ww))))
    lines.append('0')
    lines.append(' '.join(list(map(lambda x: str(x), sorted(vv)))))
    lines.append(' '.join(list(map(lambda x: str(x), sorted(ww)))))
    vv = random.sample(vv, len(vv))
    ww = random.sample(ww, len(ww))
    lines.append(' '.join(list(map(lambda x: str(x), vv))))
    lines.append(' '.join(list(map(lambda x: str(x), ww))))
#    with open('test5.03.txt', mode='w') as myfile:
#        myfile.write('\n'.join(lines))
#        myfile.write('\n')

    # Test03:
    lines = list()
    vv = list()
    for i in range(0, 100):
        vv.append(random.randint(1, 399))
    tre = max(vv) + 10
    ww = list()
    for i in range(0, 100):
        ww.append(tre - vv[i] + random.randint(0,1))
    ww = random.sample(ww, len(ww))
    lines.append(str(tre))
    lines.append(' '.join(list(map(lambda x: str(x), vv))))
    lines.append(' '.join(list(map(lambda x: str(x), ww))))
    lines.append('0')
    lines.append(' '.join(list(map(lambda x: str(x), sorted(vv)))))
    lines.append(' '.join(list(map(lambda x: str(x), sorted(ww)))))
    vv = random.sample(vv, len(vv))
    ww = random.sample(ww, len(ww))
    lines.append(' '.join(list(map(lambda x: str(x), vv))))
    lines.append(' '.join(list(map(lambda x: str(x), ww))))
    with open('test5.04.txt', mode='w') as myfile:
        myfile.write('\n'.join(lines))
        myfile.write('\n')


if __name__ == '__main__':
    main()