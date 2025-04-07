import shutil
import os

base_dir = os.getcwd()

img_dir = 'C:/Users/Erica/Desktop/Personal Data Projects/Yrden DB/Riot API/DataDragonFiles/dragontail-15.1.1/img/champion/tiles'
target_dir = 'C:/Users/Erica/Desktop/Personal Data Projects/Yrden DB/Riot API/DataDragonFiles/dragontail-15.1.1/img/champion/base_champ'

os.makedirs(target_dir, exist_ok=True)


for name in os.listdir(img_dir):
    if name.endswith("_0.jpg"):
        source_path = os.path.join(img_dir, name)
        target_path = os.path.join(target_dir, name)

        shutil.copy2(source_path, target_path)
        print(f'Copied: {name}')

print('File copying completed.')