import pickle

# Đọc file .txt
with open('TuDien_AnhViet108856.txt', 'r') as f:
    data = f.read()

with open('dictionary.pkl', 'wb') as file:
    pickle.dump(data, file)