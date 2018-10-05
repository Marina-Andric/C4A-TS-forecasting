
label_mapping = {'a' : 1, 'b' : 2, 'c' : 3}

inv_label_mappin = {v:k for k,v in label_mapping.items()}

print (inv_label_mappin)
print (inv_label_mappin.get(1))