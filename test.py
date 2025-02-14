ARRYA = []
for i in range(0,5):
    ARRYA.append({i,"Text"})    

print(ARRYA)
print(type(ARRYA))

for i in range(len(ARRYA)):
    print(ARRYA[i])

response = {
    "category" : "table",
    "message" : "hi",
    "data": [ARRYA],
    "select": 0
    }

print(response)
