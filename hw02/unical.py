def unical(st):
    result = {}
    for i in st:
        result[i] = result.get(i, 0) + 1
    return result

print(unical('asdasdasd'))