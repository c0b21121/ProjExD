import random

tai=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
print("対象文字:",tai)

hiy=random.sample(tai,23)
print("表示文字:",random.sample(hiy,23))

keso=list(set(tai)-set(hiy))
print("欠損文字:",keso)
print(len(keso))
inputword=(input(("欠損文字はいくつあるでしょうか?:")))

if (int(inputword))==(len(keso)):
    print("正解")
else:
    print("残念！")