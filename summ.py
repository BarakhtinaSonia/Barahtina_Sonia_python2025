def summ(mas, res):
    a=dict()
    for i in range(len(mas)):
        if mas[i] in a:
            return i, a[mas[i]]
        a[res-mas[i]] = i

print(summ([1,2,3,4], 4))
