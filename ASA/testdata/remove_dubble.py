res = []
with open('test_set.txt') as f:
    lines = f.readlines()
    for line in lines:
        res.append(line.strip())
res = list(set(res))
for l in res:
    print(l)
