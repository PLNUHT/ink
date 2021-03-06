import ink

# 分词
print("====== 分词 =======")
sents = [  "我爱北京天安门" ]

model = ink.cws.get_cws("bert")
print("bert:", model(sents))
model = ink.cws.get_cws("thulac")
print("thulac:", model(sents))
print("\n\n")

print("====== NER =======")
sents = [  "我爱北京天安门" ]
model = ink.ner.get_ner("bert")
print("bert:", model(sents))

print("====== POS Tagging =======")
sents = [  "我爱北京天安门" ]
model = ink.postagging.get_pos_tagging("bert")
print("bert:", model(sents))

print("====== POS Tagging =======")
sents = [("3月15日,北方多地正遭遇近10年来强度最大、影响范围最广的沙尘暴。", (30, 33)),
    ("张淑芳老人记得照片是在工人文化宫照的，而且还是在一次跳完集体舞后拍摄的。但摄影师是谁，照片背后的字是谁写的，已经找寻不到答案了。", (22, 24))]
model = ink.typing.get_typing("bert")
print("bert:", model(sents))
