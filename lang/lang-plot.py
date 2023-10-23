import matplotlib.pyplot as plt
import pandas as pd
import json

with open('freq.json','r',encoding='utf-8') as f:
    freq = json.load(f)

#언어마다 계산하기
lang_dict = {}
for i, label in enumerate(freq[0]['labels']):
    fq = freq[0]["freqs"][i]
    if not label in lang_dict:
        lang_dict[label] = fq # 인도네시아어가 없으면 fq 를 추가해주고 label에  넣어주기
        continue
    for idx, v in enumerate(fq):
        lang_dict[label][idx] = (lang_dict[label][idx] + v )/ 2

asc_list = [[chr(n) for n in range(97, 97 + 26)]]   # 97부터 122까지
df = pd.DataFrame(lang_dict, index=asc_list)

plt.style.use('ggplot')
df.plot(kind="bar", subplots=True, ylim=(0,0.15))
plt.show()
plt.savefig("lang-plot.png")


