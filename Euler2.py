
# 11


def product(x0, y0, x, y):
    s = 1
    for i in range(4):
        s *= numbers[y0 + i * y][x0 + i * x]
    
    return s

def calc_max_product():
    s = 0
    height, width = 20, 20
    for i in range(height):
        for j in range(width):
            # attempt 4 steps in each direction
            if i + 4 <= width:
                s = max(product(i, j, 1, 0), s)
            if i + 4 <= width and j + 4 <= height:
                s = max(product(i, j, 1, 1), s)
            if j + 4 <= height:
                s = max(product(i, j, 0, 1), s)
            if i - 4 >= -1 and j  + 4 <= height:
                s = max(product(i, j, -1, 1), s)
    
    return s

# store grid as 2d array

numbers = [[8, 2, 22, 97, 38, 15, 0, 40, 0, 75, 4, 5, 7, 78, 52, 12, 50, 77, 91, 8],
	[49, 49, 99, 40, 17, 81, 18, 57, 60, 87, 17, 40, 98, 43, 69, 48, 4, 56, 62, 0],
	[81, 49, 31, 73, 55, 79, 14, 29, 93, 71, 40, 67, 53, 88, 30, 3, 49, 13, 36, 65],
	[52, 70, 95, 23, 4, 60, 11, 42, 69, 24, 68, 56, 1, 32, 56, 71, 37, 2, 36, 91],
	[22, 31, 16, 71, 51, 67, 63, 89, 41, 92, 36, 54, 22, 40, 40, 28, 66, 33, 13, 80],
	[24, 47, 32, 60, 99, 3, 45, 2, 44, 75, 33, 53, 78, 36, 84, 20, 35, 17, 12, 50],
	[32, 98, 81, 28, 64, 23, 67, 10, 26, 38, 40, 67, 59, 54, 70, 66, 18, 38, 64, 70],
	[67, 26, 20, 68, 2, 62, 12, 20, 95, 63, 94, 39, 63,  8, 40, 91, 66, 49, 94, 21],
	[24, 55, 58, 5, 66, 73, 99, 26, 97, 17, 78, 78, 96, 83, 14, 88, 34, 89, 63, 72],
	[21, 36, 23, 9, 75, 0, 76, 44, 20, 45, 35, 14, 0, 61, 33, 97, 34, 31, 33, 95],
	[78, 17, 53, 28, 22, 75, 31, 67, 15, 94, 3, 80, 4, 62, 16, 14, 9, 53, 56, 92],
	[16, 39, 5, 42, 96, 35, 31, 47, 55, 58, 88, 24, 0, 17, 54, 24, 36, 29, 85, 57],
	[86, 56, 0, 48, 35, 71, 89, 7, 5, 44, 44, 37, 44, 60, 21, 58, 51, 54, 17, 58],
	[19, 80, 81, 68, 5, 94, 47, 69, 28, 73, 92, 13, 86, 52, 17, 77, 4, 89, 55, 40],
	[4, 52, 8, 83, 97, 35, 99, 16, 7, 97, 57, 32, 16, 26, 26, 79, 33, 27, 98, 66],
	[88, 36, 68, 87, 57, 62, 20, 72, 3, 46, 33, 67, 46, 55, 12, 32, 63, 93, 53, 69],
	[4, 42, 16, 73, 38, 25, 39, 11, 24, 94, 72, 18,  8, 46, 29, 32, 40, 62, 76, 36],
	[20, 69, 36, 41, 72, 30, 23, 88, 34, 62, 99, 69, 82, 67, 59, 85, 74, 4, 36, 16],
	[20, 73, 35, 29, 78, 31, 90, 1, 74, 31, 49, 71, 48, 86, 81, 16, 23, 57, 5, 54],
	[1, 70, 54, 71, 83, 51, 54, 69, 16, 92, 33, 48, 61, 43, 52, 1, 89, 19, 67, 48],]

print(calc_max_product())

# 12

def num_divisors(n):
    s = 0
    for i in range(1, int(n ** (1/2)) + 1):
        if n % i == 0:
            s += 2
    if int(n ** (1/2)) ** 2 == n:
        s -= 1
    return s

def triangle(n):
    return n*(n + 1)//2

s = 0
while num_divisors(triangle(s)) <= 500:
    s += 1

print(triangle(s))

# 17

def number_to_Letter(n):
    if 0 <= n < 20:
        return o[n]
    elif 20 <= n < 100:
        return t[n // 10] + (o[n % 10] if (n % 10 != 0) else "")
    elif 100 <= n < 1000:
        return o[n // 100] + "hundred" + (("and" + number_to_Letter(n % 100)) if (n % 100 != 0) else "") # adding 'hundred' 
    elif 1000 <= n < 1000000:
        return number_to_Letter(n // 1000) + "thousand" + (number_to_Letter(n % 1000) if (n % 1000 != 0) else "") # adding 'thousand' 

# one through twenty are unique words
o = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen")
# we can create all numbers from 1 to 1000000 with these other multiples of 10 and adding 'hundred' and 'thousand' as necessary
t = ("one", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety")

s = 0
for i in range(1, 1001):
    s += len(number_to_Letter(i))

print(s)

# 21 (slightly faster than brute force)

sums = [0] * 10000
def calc_amicable_sum():
    for i in range(1, 10000):
        for j in range(2 * i, 10000, i):
            sums[j] += i
    
    # find amicable numbers by only checking inside list
    s = 0
    for i in range(1, 10000):
        temp = sums[i]
        if temp < 10000:
            if i != temp and sums[temp] == i:
                s += i
    return s

print(calc_amicable_sum())

# 28 

print(1 + sum(4 * i * i - 6 * (i - 1) for i in range(3, 1002, 2))) # utilizing the nice pattern that the numbers on the diagonals make
  

# 30

s=0

for i in range(2, 5 * 9 ** 5):
    if sum(int(x)**5 for x in str(i)) == i:
        s += int(i)

print(s)
