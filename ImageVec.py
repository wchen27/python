import urllib.request
import io
from PIL import Image
import random
import time

s = time.perf_counter()
# URL = 'https://images-ext-1.discordapp.net/external/HVXoHD-3CWjJ5XI6AbTMkV-462gbOFE4GA0AZbN3RZI/https/i.pinimg.com/originals/95/2a/04/952a04ea85a8d1b0134516c52198745e.jpg?width=453&height=675'
# f = io.BytesIO(urllib.request.urlopen(URL).read()) 
# img = Image.open(f)
img = Image.open(r'C:\Users\Wilson\Downloads\swigglehat.jpg')
img.show() 
width, height = img.size
pixels = img.load()


def naive_quant_27(rgb):
    quant = []
    for color in rgb:
        if color < 255 // 3:
            quant.append(0)
        elif color > 255 * 2 // 3:
            quant.append(255)
        else:
            quant.append(127)
    
    return tuple(quant)

def naive_quant_8(rgb):
    quant = []
    for color in rgb:
        if color < 128:
            quant.append(0)
        else:
            quant.append(255)
    return tuple(quant)

def naive_quant(k):
    newImg = Image.new("RGB", (width, height + (width // k)), 0)
    newPixels = newImg.load()
    for r in range(width):
        for c in range(height):
            if k == 8:
                newPixels[r, c] = naive_quant_8(pixels[r, c])
            elif k == 27:
                newPixels[r, c] = naive_quant_27(pixels[r, c])
    if k == 8:
        colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255)]
    elif k == 27:
        # let colors be all combinations of 0, 127, 255
        colors = [(0, 0, 0), (0, 127, 0), (0, 255, 0), (127, 0, 0), (127, 127, 0), (127, 255, 0), (255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 0, 127), (0, 127, 127), (0, 255, 127), (127, 0, 127), (127, 127, 127), (127, 255, 127), (255, 0, 127), (255, 127, 127), (255, 255, 127), (0, 0, 255), (0, 127, 255), (0, 255, 255), (127, 0, 255), (127, 127, 255), (127, 255, 255), (255, 0, 255), (255, 127, 255), (255, 255, 255)]
    for i in range(len(colors)):
        curr = (int(colors[i][0]), int(colors[i][1]), int(colors[i][2]))
        for r in range(height, height + (width // k)):
            for c in range(i * (width // k), (i + 1) * (width // k)):
                newPixels[c, r] = curr
    newImg.show()

def get_error(mean, color):
    m1, m2, m3 = mean
    s1, s2, s3 = color
    return (m1 - s1) ** 2 + (m2 - s2) ** 2 + (m3 - s3) ** 2

def get_avg(group):
    s1, s2, s3 = 0, 0, 0
    for color in group:
        r, g, b = color
        s1 += r
        s2 += g
        s3 += b
    return ((s1 / len(group)), (s2 / len(group)), (s3 / len(group)))

def kmeanspp_quant(k):
    newImg = Image.new("RGB", (width, height + (width // k)), 0)
    newPixels = newImg.load()
    rgbs = dict()
    for r in range(width):
        for c in range(height):
            if pixels[r, c] not in rgbs.keys():
                rgbs[pixels[r, c]] = [(r, c)]
            else:
                rgbs[pixels[r, c]].append((r, c))
    i = 0

    means = set()
    colors = list(rgbs.keys())
    means.add((r := random.choice(colors)))
    s = 0
    for color in colors:
        s += get_error(r, color)
    while True:
        for color in colors:
            if get_error(r, color) / s * 10 ** 3 > random.random():
                means.add(color)
            if len(means) == k:
                break
        if len(means) == k:
            break
    

        

        
        
    means = list(means)
    # while len(means) < k:
    #     means.add(pixels[random.randint(0, width - 1), random.randint(0, height - 1)])
    # means = list(means)

    # k-means++ means selection
    

    meanGroups = dict()
    for point in means:
        meanGroups[point] = []

    while True:
        print('generation', i, end=' --> ')
        for color in rgbs.keys():
            errors = []
            for mean in means:
                errors.append(get_error(mean, color))
                
            meanGroups[means[errors.index(min(errors))]].append(color)
                

        newMeans = []
        for key in meanGroups:
            newMeans.append(get_avg(meanGroups[key]))
        
        diff = [x for x in newMeans if x not in means]
        
        print(len(diff), 'differences in means')
        print(means)
        print(newMeans)
        if means == newMeans:
            break
            
        means = newMeans
        meanGroups = dict()
        for mean in means:
            meanGroups[mean] = []
        i += 1

    for key in meanGroups.keys():
        points = meanGroups[key]
        for point in points:
            for pix in rgbs[point]:
                a, b, c = int(key[0]), int(key[1]), int(key[2])
                newPixels[pix] = a, b, c
    colors = list(meanGroups.keys())
    for i in range(len(colors)):
        curr = (int(colors[i][0]), int(colors[i][1]), int(colors[i][2]))
        for r in range(height, height + (width // k)):
            for c in range(i * (width // k), (i + 1) * (width // k)):
                newPixels[c, r] = curr
    newImg.show()


def kmeans_quant(k):
    newImg = Image.new("RGB", (width, height + (width // k)), 0)
    newPixels = newImg.load()
    rgbs = dict()
    for r in range(width):
        for c in range(height):
            if pixels[r, c] not in rgbs.keys():
                rgbs[pixels[r, c]] = [(r, c)]
            else:
                rgbs[pixels[r, c]].append((r, c))
    i = 0
    means = set()
    while len(means) < k:
        means.add(pixels[random.randint(0, width - 1), random.randint(0, height - 1)])
    means = list(means)


    print(means)
    meanGroups = dict()
    for point in means:
        meanGroups[point] = []
    
    while True:
        print('generation', i, end=' --> ')
        for color in rgbs.keys():
            errors = []
            for mean in means:
                errors.append(get_error(mean, color))
                
            meanGroups[means[errors.index(min(errors))]].append(color)
                

        newMeans = []
        for key in meanGroups:
            newMeans.append(get_avg(meanGroups[key]))
        
        diff = [x for x in newMeans if x not in means]
        
        print(len(diff), 'differences in means')
        print(means)
        print(newMeans)
        if means == newMeans:
            break
            
        means = newMeans
        meanGroups = dict()
        for mean in means:
            meanGroups[mean] = []
        i += 1

    for key in meanGroups.keys():
        points = meanGroups[key]
        for point in points:
            for pix in rgbs[point]:
                a, b, c = int(key[0]), int(key[1]), int(key[2])
                newPixels[pix] = a, b, c
    colors = list(meanGroups.keys())
    for i in range(len(colors)):
        curr = (int(colors[i][0]), int(colors[i][1]), int(colors[i][2]))
        for r in range(height, height + (width // k)):
            for c in range(i * (width // k), (i + 1) * (width // k)):
                newPixels[c, r] = curr
    newImg.show()


    # for r in range(height, height + (width // k) - 1):
    #     for c in range(width):
    #         currColor = colors[r // (width // k)]
    #         newPixels[c, r] = int(currColor[0]), int(currColor[1]), int(currColor[2])
    
def find_closest_color(rgb, colors):
    errors = []
    for color in colors:
        errors.append(get_error(color, rgb))
    return colors[errors.index(min(errors))]


def kmeans_quant_dither(k):
    newImg = Image.new("RGB", (width, height + (width // k)), 0)
    newPixels = newImg.load()
    rgbs = dict()
    for r in range(width):
        for c in range(height):
            if pixels[r, c] not in rgbs.keys():
                rgbs[pixels[r, c]] = [(r, c)]
            else:
                rgbs[pixels[r, c]].append((r, c))
    i = 0
    means = set()
    while len(means) < k:
        means.add(pixels[random.randint(0, width - 1), random.randint(0, height - 1)])
    means = list(means)


    print(means)
    meanGroups = dict()
    for point in means:
        meanGroups[point] = []
    
    while True:
        print('generation', i, end=' --> ')
        for color in rgbs.keys():
            errors = []
            for mean in means:
                errors.append(get_error(mean, color))
                
            meanGroups[means[errors.index(min(errors))]].append(color)
                

        newMeans = []
        for key in meanGroups:
            newMeans.append(get_avg(meanGroups[key]))
        
        diff = [x for x in newMeans if x not in means]
        
        print(len(diff), 'differences in means')
        print(means)
        print(newMeans)
        if means == newMeans:
            break
            
        means = newMeans
        meanGroups = dict()
        for mean in means:
            meanGroups[mean] = []
        i += 1

    for key in meanGroups.keys():
        points = meanGroups[key]
        for point in points:
            for pix in rgbs[point]:
                a, b, c = int(key[0]), int(key[1]), int(key[2])
                newPixels[pix] = a, b, c
    colors = list(meanGroups.keys())
    newColors = []
    for curr in colors:
        newColors.append((int(curr[0]), int(curr[1]), int(curr[2])))
    colors = newColors


    for x in range(height):
        for y in range(width):
            curr = pixels[y, x]
            newpix = find_closest_color(curr, colors)
            newPixels[y, x] = newpix
            error = (curr[0] - newpix[0], curr[1] - newpix[1], curr[2] - newpix[2])
            try:
                newPixels[y, x + 1] = (newpix[0] + error[0] * 7 // 16, newpix[1] + error[1] * 7 // 16, newpix[2] + error[2] * 7 // 16)
                newPixels[y + 1, x - 1] = (newpix[0] + error[0] * 3 // 16, newpix[1] + error[1] * 3 // 16, newpix[2] + error[2] * 3 // 16)
                newPixels[y + 1, x] = (newpix[0] + error[0] * 5 // 16, newpix[1] + error[1] * 5 // 16, newpix[2] + error[2] * 5 // 16)
                newPixels[y + 1, x + 1] = (newpix[0] + error[0] * 1 // 16, newpix[1] + error[1] * 1 // 16, newpix[2] + error[2] * 1 // 16)
            except IndexError:
                continue



    for i in range(len(colors)):
        curr = (int(colors[i][0]), int(colors[i][1]), int(colors[i][2]))
        for r in range(height, height + (width // k)):
            for c in range(i * (width // k), (i + 1) * (width // k)):
                newPixels[c, r] = curr
    newImg.show()

# s = time.perf_counter()
# kmeans_quant(8)
# e = time.perf_counter()
# s2 = time.perf_counter()
# kmeans_quant(8)
# e2 = time.perf_counter()
# print('normal:', e - s)
# print('k++:', e2 - s2)
# # 158 normal
# # 
kmeans_quant_dither(8)