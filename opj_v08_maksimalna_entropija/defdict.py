from collections import defaultdict

s = defaultdict(lambda: 0.0)

s[3]=4
print(s['a'])

def dotprod(a, b):
    return sum(x*y for x,y in zip(a,b))
    



a = [1,3,-5]

b = [4,-2,-1]

print(dotprod(a,b))