import pickle
with open(r'record.txt','wb') as f:
    a=[0]*10
    print(a)
    pickle.dump(a,f)
