import os

d = 'src'
e = '.java'

d = 'pair_lists'
e = '.txt'

for filename in os.listdir(d):
    if filename.endswith(e):
        path_file = os.path.join(d, filename)
        with open(path_file, "r", encoding="windows-1252") as f:
            content = f.read()
        with open(path_file, "w", encoding="utf-8") as f:
            f.write(content)
