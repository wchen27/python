from math import log
import random

with open('star_data.csv', 'r') as f:
    lines = []
    star_vectors = []
    for line in f.readlines():
        if line[0].isalpha():
            continue
        lines.append(line.strip().split(',')[:-2])
    for line in lines:
        temp, luminosity, radius, avm, stype = line
        star_vectors.append((log(float(temp)), log(float(luminosity)), log(float(radius)), float(avm), stype))


'''
STAR TYPES:
Brown Dwarf -> Star Type = 0
Red Dwarf -> Star Type = 1
White Dwarf-> Star Type = 2
Main Sequence -> Star Type = 3
Supergiant -> Star Type = 4
Hypergiant -> Star Type = 5
'''
star_types = {
    0 : 'Brown Dwarf',
    1 : 'Red Dwarf',
    2 : 'White Dwarf',
    3 : 'Main Sequence',
    4 : 'Supergiant',
    5 : 'Hypergiant'
}

def get_error(mean, star):
    m1, m2, m3, m4, mtype = mean
    s1, s2, s3, s4, stype = star
    return (m1 - s1) ** 2 + (m2 - s2) ** 2 + (m3 - s3) ** 2 + (m4 - s4) ** 2

def get_avg(group):
    s1, s2, s3, s4 = 0, 0, 0, 0
    for star in group:
        c1, c2, c3, c4, stype = star
        s1 += c1
        s2 += c2
        s3 += c3
        s4 += c4
    l = len(group)
    return (s1/l, s2/l, s3/l, s4/l, -1)

def k_means(k, stars):
    i = 0
    means = random.sample(stars, k)
    meanGroups = dict()
    for star in means:
        meanGroups[star] = []

    while True:
        for star in stars:
            errors = []
            for mean in means:
                errors.append(get_error(mean, star))
            
            meanGroups[means[errors.index(min(errors))]].append(star)
        
        newMeans = []
        for key in meanGroups:
            newMeans.append(get_avg(meanGroups[key]))
        
        if means == newMeans:
            break

        means = newMeans
        meanGroups = dict()
        for mean in means:
            meanGroups[mean] = []
        i += 1
        
    return meanGroups, i

meanGroups, runs = (k_means(7, star_vectors))

for key, val in meanGroups.items():
    print('Group:', key[:-1])
    types = []
    for star in val:
        print(star)
        types.append(star[-1])
    print('Star types:', types)
    print()
print('Total runs:', runs)