import os
import shutil
import random
from pathlib import Path
import yaml

# Set random seed for reproducibility
random.seed(42)

# Define paths
base_path = Path('.')
images_path = base_path / 'images' / 'Train'
labels_path = base_path / 'labels' / 'Train'
train_text = base_path / 'Train.txt'

# Create new directories
for folder in ['train', 'val']:
    for subdir in ['images', 'labels']:
        (base_path / folder / subdir).mkdir(parents=True, exist_ok=True)


# Get list of labeled images
labeled_images = set(f"{os.path.splitext(label)[0]}.png" for label in os.listdir(labels_path) if label.endswith('.txt'))

# Remove unlabled images
for img in os.listdir(images_path):
    if img not in labeled_images:
        os.remove(images_path / img)
        print(f"Removed unlabeled images: {img}")

# Read image paths from Train.txt
with open(train_text, 'r') as f:
    image_paths = [f"./images/Train/{os.path.basename(path)}" for path in f.read().splitlines()]
    image_paths = [path for path in image_paths if os.path.basename(path) in labeled_images]

# Shuffle and split data (80% train, 20% val)
random.shuffle(image_paths)
split = int(0.8 * len(image_paths))
train_images = image_paths[:split]
val_images = image_paths[split:]

print("TRAIN IMAGES BEFORE: ", train_images)

# Function to copy files
def copy_files(image_list, destination):
    for img_path in image_list:
        img_name = os.path.basename(img_path)
        label_name = os.path.splitext(img_name)[0] + '.txt'
        print("IMAGE PATH: ", img_path)
        print("IMAGE NAME: ", img_name)

        shutil.copy(img_path, destination / 'images' / img_name)
        shutil.copy(labels_path / label_name, destination / 'labels' / label_name)

# Copy files to new directories
print("TRAIN IMAGES: ", train_images)
copy_files(train_images, base_path / 'train')
copy_files(val_images, base_path / 'val')
# Update data.yaml
with open('data.yaml', 'r') as f:
    data = yaml.safe_load(f)

data['train'] = 'train/images'
data['val'] = 'val/images'

with open('data.yaml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False)

print("Dataset split and data.yaml updated successfully")
