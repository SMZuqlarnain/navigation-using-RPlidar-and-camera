import cv2
from yolo_rt import YOLO_TRT
from lidar_reader import get_lidar_points
from camera_gst import get_csi_camera
from fusion import fuse_detections

yolo = YOLO_TRT("export/model.engine")
cam = get_csi_camera()

while True:
    ret, frame = cam.read()
    if not ret:
        continue

    preds = yolo.infer(frame)       # YOLO detection
    lidar = get_lidar_points()      # LIDAR scan

    fused = fuse_detections(preds, lidar)

    for cls, dist in fused:
        cv2.putText(frame, f"{cls} {dist/1000:.1f}m", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Blind Guide", frame)
    if cv2.waitKey(1) == ord('q'):
        break
