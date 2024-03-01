import pandas as pd

all_data = {}
brain = []
id = []
cach = ''
count  = 0

df = pd.read_csv('PyDash/data/best.csv', sep=";")
for i in df['brain']:
    print(i)
    if i == cach:
        pass
    else:
        brain.append(i)
        id.append(count)
        cach = i
    count += 1

all_data['id'] = id
all_data['brain'] = brain

df = pd.DataFrame(all_data)
df.to_csv('PyDash/data/best.csv', index=False, sep=";")