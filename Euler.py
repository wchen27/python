

def isPrime(x):
    if x % 2 == 0 and x != 2:
        return False
    for i in range(int(x**(1/2) - 1)):
        if x % (i + 2) == 0: return False
    return True

# 1

# s = 0
# for i in range(1, 1000):
#     if i % 3 == 0 or i % 5 == 0:
#         s += i

# print(s)

# One line solution

print(sum([x for x in range(1, 1000) if x % 3 == 0 or x % 5 == 0]))

# 2

s = 0
curr = 1
next = 2
while curr <= 4000000:
    if curr % 2 == 0:
        s += curr
    curr, next = next, curr+next

print(s)

# 3

n = 600851475143

last = n
primes = []
for i in range(2, n):
    if isPrime(i) and n % i == 0:
        n //= i
        primes.append(i)
    if n == 1:
        break

print(primes[-1])
    
# 4

nums = []
for i in range(100, 1000):
    for j in range(100, 1000):
        if str(i * j) == str(i * j)[::-1]:
            nums.append(i * j)

print(max(x for x in nums))

# 5

def gcd(x, y):
    while  y != 0:
        x, y = y, x % y
    return x

n = 20
result = 1
for i in range(1, n+1):
    result *= i // gcd(i, result)

print(result)

# 6

# sumOfSquares = sum(x**2 for x in range(101))
# s = sum(x for x in range(101))
# print(s**2 - sumOfSquares)

# One Line Solution:

print((sum(x for x in range(101)))**2 - sum(x**2 for x in range(101)))

# 7

start = 2
primes = []
while True:
    if isPrime(start):
        primes.append(start)
    start += 1
    if len(primes) > 10001:
        break

print(primes[10000])

# 8

# helper function to find product of the digits of a number
def product(x):
    res = 1
    for i in x:
        res *= int(i)
    return res

# store n as string
n = "7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450"
print(max(product(n[i : i + 13]) for i in range(len(n) - 12)))

# 9

for i in range(1, 1001):
    for j in range(i, 1001):
        k = 1000 - j - i
        if i ** 2 + j ** 2 == k ** 2:
            print(i*j*k) # since we are told there is exactly 1 solution

# 29

# sets contain no duplicate items

print(len({x**y for x in range(2, 101) for y in range(2, 101)}))