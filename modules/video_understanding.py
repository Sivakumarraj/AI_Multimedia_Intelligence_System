import cv2
from transformers import pipeline

captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = frame_count // 5
    captions = []

    for i in range(0, frame_count, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret: break
        frame_path = f"temp_frame_{i}.jpg"
        cv2.imwrite(frame_path, frame)
        caption = captioner(frame_path)[0]['generated_text']
        captions.append(caption)

    cap.release()
    return captions
