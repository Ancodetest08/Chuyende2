# AI Traffic Counter (YOLOv8 + Streamlit)

Dự án môn học: **Chuyên đề 2**
Tác giả: **Nhóm 18**

## 1. Giới thiệu
Ứng dụng đếm phương tiện giao thông (hoặc đối tượng bất kỳ) di chuyển qua một vạch kẻ định trước (Line Crossing). Sử dụng mô hình **YOLOv8** để nhận diện và **Streamlit** để hiển thị giao diện.

## 2. Tính năng
- Đếm đối tượng qua vạch kẻ (Line Crossing Detection).
- Tùy chỉnh vị trí vạch kẻ trực tiếp trên giao diện.
- Lọc đối tượng cần đếm (Xe máy, Ô tô, Người đi bộ...).
- Thống kê thời gian thực.

## 3. Cài đặt
1. **Clone dự án:**
    ```bash
    git clone https://github.com/Ancodetest08/Chuyende2.git
    cd Chuyende2
    ```
2. **Tạo môi trường ảo**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```
3. **Cài đặt thư viện**
    ```bash
    pip install -r requirements.txt
    ```
4. **Chạy ứng dụng**
    ```bash
    streamlit run app.py
    ```

## 4. Cấu trúc dự án
`src/`: Mã nguồn xử lý (Config, Utils).

`app.py`: Giao diện chính.

`models/`: Chứa file weights (yolov8s.pt).

`videos/`: Chứa videos test
