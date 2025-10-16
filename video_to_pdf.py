import cv2
from PIL import Image
import os

def video_to_pdf(video_path, output_pdf):
    # Create a folder for temporary frame images
    temp_dir = "frames_temp"
    os.makedirs(temp_dir, exist_ok=True)

    # Open video
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps)

    frame_count = 0
    saved_count = 0

    print("Extracting frames...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Capture 1 frame per second
        if frame_count % frame_interval == 0:
            frame_path = os.path.join(temp_dir, f"frame_{saved_count}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_count += 1

        frame_count += 1

    cap.release()

    # Convert all saved frames to a PDF
    print("Converting to PDF...")

    images = []
    for i in range(saved_count):
        img = Image.open(os.path.join(temp_dir, f"frame_{i}.jpg")).convert("RGB")
        images.append(img)

    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"✅ PDF saved as: {output_pdf}")
    else:
        print("❌ No frames were extracted.")

    # Cleanup
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)

# Example usage:
video_to_pdf("video.mp4", "output.pdf")