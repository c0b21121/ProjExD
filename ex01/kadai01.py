import random

tai=["a","b","c","d","f"]
print("対象文字:",tai)

hiy=random.sample(tai,3)
print("表示文字:",random.sample(hiy,3))

keso=list(set(tai)-set(hiy))
print("欠損文字:",keso)
print(len(keso))
inputword=(input(("欠損文字はいくつあるでしょうか?:")))
if (int(inputword))==(len(keso)):
    print("正解")
else:
    print("残念！")



    




