import sys

arg = sys.argv[1]


if arg == 'A':
    s = 0
    for i in sys.argv[2:5]:
        s+=int(i)
        
    print(s)

if arg == 'B':
    s = 0
    for i in sys.argv[2:]:
        s += int(i)
        
    print(s)

if arg == 'C':
    l = []
    for i in sys.argv[2:]:
        if int(i) % 3 == 0:
            l.append(int(i))

    print(l)

if arg == 'D':
    l = [1, 1]
    i = int(sys.argv[2])
    if i <= 0:
        print("i <= 0")
    elif i == 1:
        print("1")
    else:
        for x in range(i - 1):
            l.append(l[len(l)-1]+l[len(l)-2])
            print(l[x], end=", ")

        print(l[i-1])

if arg == 'E':
    for x in range(int(sys.argv[2]), int(sys.argv[3])):
        print(x**2 - 3*x + 2, end=", ")

    print(int(sys.argv[3])**2 - 3*int(sys.argv[3]) + 2)

if arg == 'F':
    lengths = []
    for i in sys.argv[2:5]:
        lengths.append(float(i))
    lengths.sort()
    if lengths[0] + lengths[1] < lengths[2]:
        print("Not a triangle")

    else:
        a = lengths[0]
        b = lengths[1]
        c = lengths[2]
        s = (a + b + c)/2

        print((s*(s-a)*(s-b)*(s-c))**(1/2))

if arg == 'G':
    count = [0, 0, 0, 0, 0]
    wordlist = [x for x in sys.argv[2]]
    for ch in wordlist:
        if ch == 'a':
            count[0] += 1
        if ch == 'e':
            count[1] += 1
        if ch == 'i':
            count[2] += 1
        if ch == 'o':
            count[3] += 1
        if ch == 'u':
            count[4] += 1
    print("a: ", count[0], "e: ", count[1], "i: ", count[2], "o: ", count[3], "u: ", count[4])


        
