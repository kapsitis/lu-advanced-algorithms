import random

def main():
    aa = [random.randrange(1, 1000001) for n in range(1, 500)]
    aa.append(0)
    bb = [str(a) for a in aa]
    ss = ' '.join(bb)
    with open("input8.txt", "w") as text_file:
        text_file.write(ss)
        text_file.write('\n')




if __name__ == '__main__':
    main()