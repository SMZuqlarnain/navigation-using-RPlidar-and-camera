# verify_dataset.py
import os
import yaml

def verify_dataset():
    print("Verifying dataset structure...")
    
    # Check data.yaml
    try:
        with open("training/data.yaml", 'r') as f:
            data_config = yaml.safe_load(f)
        print("✓ data.yaml loaded successfully")
        print(f"  Train path: {data_config.get('train')}")
        print(f"  Val path: {data_config.get('val')}")
        print(f"  Number of classes: {data_config.get('nc')}")
        print(f"  Class names: {data_config.get('names')}")
    except Exception as e:
        print(f"✗ Error loading data.yaml: {e}")
        return
    
    # Check if paths exist and have images
    train_path = data_config.get('train')
    val_path = data_config.get('val')
    
    def check_folder(folder_path, folder_name):
        if not os.path.exists(folder_path):
            print(f"✗ {folder_name} path doesn't exist: {folder_path}")
            return False
        
        images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f"✓ {folder_name}: {len(images)} images found")
        
        if len(images) == 0:
            print(f"  Warning: No images in {folder_path}")
            return False
        return True
    
    train_ok = check_folder(train_path, "Training folder")
    val_ok = check_folder(val_path, "Validation folder")
    
    # Check corresponding labels
    def check_labels(image_folder, label_folder_name):
        image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        label_files = [f.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt') 
                      for f in image_files]
        
        labels_exist = 0
        for label_file in label_files:
            label_path = os.path.join("training/labels", label_folder_name, label_file)
            if os.path.exists(label_path):
                labels_exist += 1
        
        print(f"  Labels: {labels_exist}/{len(image_files)} images have label files")
        return labels_exist > 0
    
    if train_ok:
        check_labels(train_path, "train")
    if val_ok:
        check_labels(val_path, "val")
    
    if train_ok and val_ok:
        print("\n🎉 Dataset is ready for training!")
    else:
        print("\n❌ Please fix the dataset issues above")

if __name__ == "__main__":
    verify_dataset()