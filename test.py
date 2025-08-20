import os

paths = [
            os.path.join(root, file).replace('\\', '/')
            for root, _, files in os.walk('./results/Checkpoint')
            for file in files
            if os.path.splitext(file)[1] == '.pt'
            ]
if len(paths) > 0:
    path = max(paths, key = os.path.getctime)


print(path)