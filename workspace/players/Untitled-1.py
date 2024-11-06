
def add_or_replace(queue,key, value):
    for i, (k, v) in enumerate(queue):
        if k == key:
            if value < v:
                queue[i] = (key, value)
            return
    queue.append((key, value))

print(add_or_replace([(1, 2), (2, 3)], 1, 1))
print(add_or_replace([(1, 2), (2, 3)], 3, 4))   

