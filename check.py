s = []
for i in 66000:
    a = input()
    s.append(a)
z = {}
for i in s:
    if i in z:
        z[i] += 1
    else:
        z[i] = 1
print(z)

