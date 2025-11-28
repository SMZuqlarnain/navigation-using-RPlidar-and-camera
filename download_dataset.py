# download_multiple_datasets.py
import os
import urllib.request
import zipfile
import shutil
import yaml

def download_multiple_datasets():
    """Download and combine multiple datasets"""
    
    coco_classes = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
    
    # Create directories
    directories = [
        "training/images/train",
        "training/images/val", 
        "training/labels/train",
        "training/labels/val"
    ]
    
    for dir_path in directories:
        os.makedirs(dir_path, exist_ok=True)
    
    datasets = [
        {
            "name": "COCO8",
            "url": "https://github.com/ultralytics/assets/releases/download/v0.0.0/coco8.zip",
            "files": 8
        },
        {
            "name": "VOC", 
            "url": "http://data.brainchip.com/dataset-mirror/voc/VOCtrainval_11-May-2012.tar",
            "files": 12
        }
    ]
    
    total_downloaded = 0
    
    for dataset in datasets:
        print(f"Downloading {dataset['name']}...")
        
        try:
            zip_path = f"{dataset['name'].lower()}.zip"
            urllib.request.urlretrieve(dataset["url"], zip_path)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall("temp_extract")
            
            # Copy images and labels
            for split in ['train', 'val']:
                images_dir = f"temp_extract/{dataset['name'].lower()}/images/{split}"
                labels_dir = f"temp_extract/{dataset['name'].lower()}/labels/{split}"
                
                if os.path.exists(images_dir):
                    for file in os.listdir(images_dir):
                        shutil.copy2(os.path.join(images_dir, file), f"training/images/{split}/")
                        total_downloaded += 1
                
                if os.path.exists(labels_dir):
                    for file in os.listdir(labels_dir):
                        shutil.copy2(os.path.join(labels_dir, file), f"training/labels/{split}/")
            
            # Clean up
            shutil.rmtree("temp_extract")
            os.remove(zip_path)
            
            print(f"✅ {dataset['name']}: {dataset['files']} images downloaded")
            
        except Exception as e:
            print(f"❌ {dataset['name']} failed: {e}")
    
    # Update data.yaml
    with open("training/data.yaml", 'w') as f:
        f.write(f"""train: training/images/train
val: training/images/val
nc: {len(coco_classes)}
names: {coco_classes}
""")
    
    print(f"\n📊 Total downloaded: {total_downloaded} images")
    print("⚠️  Note: For 100+ images per class, consider:")
    print("   - Using the synthetic dataset generator above")
    print("   - Downloading full COCO dataset (80,000+ images)")
    print("   - Using web scraping for specific classes")

if __name__ == "__main__":
    download_multiple_datasets()