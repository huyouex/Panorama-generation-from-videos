import cv2
import os


def video_to_frames(video_path, output_dir, num_frames=50):
    """
    Extract frames from a video and save them as images.
    :param video_path: Path to the video file.
    :param output_dir: Directory to save the extracted images.
    :param num_frames: Number of frames to extract.
    :return: List of file paths to the extracted frames.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, frame_count // num_frames)  # Step for frame extraction

    frames = []
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % step == 0:
            frame_filename = os.path.join(output_dir, f"frame_{count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            frames.append(frame_filename)
        count += 1

    cap.release()
    return frames


def detect_video_orientation(frames):
    w_total, h_total = 0, 0
    for img in frames[:min(5, len(frames))]:  # Use the first 5 frames
        h, w = img.shape[:2]
        w_total += w
        h_total += h
    return "landscape" if w_total > h_total else "portrait"
