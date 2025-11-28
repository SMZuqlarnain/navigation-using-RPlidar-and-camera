# train_final.py
from ultralytics import YOLO
import torch
import os
import yaml

def main():
    # Check for GPU (you're using CPU now, but let's check)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Verify data.yaml one more time
    try:
        with open("training/data.yaml", 'r') as f:
            data_config = yaml.safe_load(f)
        print("Data configuration:")
        print(f"  Train: {data_config.get('train')}")
        print(f"  Val: {data_config.get('val')}")
        print(f"  Classes: {data_config.get('nc')}")
        print(f"  Names: {data_config.get('names')}")
    except Exception as e:
        print(f"Error reading data.yaml: {e}")
        return

    try:
        # Load model
        print("Loading YOLOv8n model...")
        model = YOLO("yolov8n.pt")
        
        # Train the model with optimized parameters for CPU
        print("Starting training...")
        train_results = model.train(
            data="training/data.yaml",
            epochs=50,
            imgsz=640,
            device=device,  # This will use CPU since that's what you have
            batch=4,        # Smaller batch for CPU
            workers=2,      # Fewer workers for CPU
            patience=10,    # Stop early if no improvement
            lr0=0.01,      # Learning rate
            save_period=10, # Save checkpoint every 10 epochs
            plots=True,     # Generate plots
            verbose=True    # Show training progress
        )

        print("Training completed!")
        
        # Validate the model
        print("Running validation...")
        metrics = model.val()
        print(f"Validation mAP50-95: {metrics.box.map:.4f}")
        
        # Export to ONNX for deployment
        print("Exporting to ONNX...")
        export_path = model.export(format="onnx")
        print(f"Model exported to: {export_path}")
        
        # Test prediction on a sample image
        print("Testing prediction on sample image...")
        if os.path.exists("training/images/val/image_000.jpg"):
            results = model("training/images/val/image_000.jpg")
            results[0].show()
            print("Prediction test completed!")
        
    except Exception as e:
        print(f"Error during training: {e}")

if __name__ == "__main__":
    main()