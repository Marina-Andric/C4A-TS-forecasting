import matplotlib.pyplot as plt

labelsValues = [
                ('First-order autoregressive', 525),
                ('Random walk', 249),
                ('Simple exponential smoothing with drift', 100),
                ('Second order autoregressive with a constant', 85),
                ('Simple exponential smoothing', 64),
                ('Differenced first order autoregressive model', 49),
                ('Damped-trend linear exponential smoothing\nLinear exponential smoothing\nRandom walk with drift', 25)
                ]
labels=[x[0] for x in labelsValues]
values=[x[1] for x in labelsValues]

patches, _, texts = plt.pie(values, startangle=90, autopct='%1.0f%%', pctdistance=1.1)
plt.legend(patches, labels, loc="best")
plt.axis('equal')
plt.tight_layout()
plt.show()

# labels = ['Cookies', 'Jellybean', 'Milkshake', 'Cheesecake']
# sizes = [38.4, 40.6, 20.7, 10.3]
# colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
# patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
# plt.legend(patches, labels, loc="best")
# plt.axis('equal')
# plt.tight_layout()
# plt.show()

# plt.figure(figsize=(10,8 ))
# plt.pie(values, labels=labels, startangle=50, autopct='%.1f%%')
# plt.title(' ')
# plt.show()
