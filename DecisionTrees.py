with open('mushroom.csv', 'r') as f:
    lines = [line.strip().split(',') for line in f.readlines()]
    lines = lines[1:]

