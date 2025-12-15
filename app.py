import streamlit as st
import cv2
import tempfile
from ultralytics import YOLO
from collections import defaultdict
import numpy as np

from src.config import CLASS_NAMES_DICT, COLOR_RED, COLOR_GREEN, COLOR_ORANGE, DEFAULT_MODEL_PATH
from src.utils import is_crossing_line

st.set_page_config(page_title="AI Line Counter", layout="wide")
st.title("🚦 AI Traffic Counter - Chuyên Đề 2")

with st.sidebar:
    st.header("⚙️ Settings")
    model_path = st.text_input("Model Path", DEFAULT_MODEL_PATH)
    conf_thresh = st.slider("Confidence Threshold", 0.1, 1.0, 0.3)
    
    st.divider()
    st.subheader("📍 Line Coordinates")
    line_x1 = st.number_input("X1 (Start)", value=0)
    line_y1 = st.number_input("Y1 (Start)", value=400)
    line_x2 = st.number_input("X2 (End)", value=1280)
    line_y2 = st.number_input("Y2 (End)", value=400)
    
    st.divider()
    target_classes_names = st.multiselect(
        "Classes to Count", 
        list(CLASS_NAMES_DICT.values()), 
        default=["person", "car", "motorcycle", "bus", "truck"]
    )
    target_ids = [k for k, v in CLASS_NAMES_DICT.items() if v in target_classes_names]

uploaded_file = st.file_uploader("Upload Video", type=['mp4', 'avi', 'mov'])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    col1, col2 = st.columns([3, 1])
    with col2:
        st.subheader("📊 Statistics")
        stats_placeholder = st.empty()
        
    with col1:
        st.subheader("🎥 Live Feed")
        st_frame = st.empty()

    if st.button("▶️ START COUNTING"):
        model = YOLO(model_path)
        cap = cv2.VideoCapture(video_path)
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        line_start = (line_x1, line_y1)
        line_end = (line_x2 if line_x2 <= width else width, line_y2)

        track_history = defaultdict(lambda: [])
        counts = defaultdict(int)
        counted_ids = set()

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            results = model.track(frame, classes=target_ids, persist=True, 
                                  conf=conf_thresh, tracker="botsort.yaml", verbose=False)
            
            cv2.line(frame, line_start, line_end, COLOR_RED, 3)

            if results[0].boxes.id is not None:
                boxes = results[0].boxes.xywh.cpu()
                track_ids = results[0].boxes.id.int().cpu().tolist()
                class_ids = results[0].boxes.cls.int().cpu().tolist()

                for box, track_id, cls_id in zip(boxes, track_ids, class_ids):
                    x, y, w, h = box
                    center = (float(x), float(y))
                    class_name = CLASS_NAMES_DICT[cls_id]

                    track = track_history[track_id]
                    track.append(center)
                    if len(track) > 2: track.pop(0)

                    if len(track) == 2 and track_id not in counted_ids:
                        if is_crossing_line(line_start, line_end, track[0], track[1]):
                            counts[class_name] += 1
                            counted_ids.add(track_id)
                            cv2.line(frame, line_start, line_end, COLOR_GREEN, 5)

                    x1, y1 = int(x - w/2), int(y - h/2)
                    x2, y2 = int(x + w/2), int(y + h/2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), COLOR_ORANGE, 2)
                    cv2.putText(frame, f"ID:{track_id} {class_name}", (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_ORANGE, 2)

            with stats_placeholder.container():
                for name, count in counts.items():
                    st.metric(label=name.capitalize(), value=count)
                st.write(f"**Total: {sum(counts.values())}**")

            st_frame.image(frame, channels="BGR", use_container_width=True)

        cap.release()
