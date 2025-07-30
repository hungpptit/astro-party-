
# 🚀 ASTRO PARTY – GAME ĐỒ ÁN PYTHON

**Học viện Công nghệ Bưu chính Viễn thông – Cơ sở TP.HCM**  
**Ngành học**: Công nghệ thông tin  
**Lớp**: D22CQCN01-N  
**Thực hiện bởi**: Nguyễn Thanh Khai, Phạm Đăng Khôi, Phạm Tuấn Hưng  
📅 **Thời gian thực hiện**: 11/2024  

---

## 🎯 MỤC TIÊU DỰ ÁN

Phát triển trò chơi 2–4 người chơi dạng đối kháng không gian. Người chơi điều khiển máy bay để:
- Bắn hạ đối thủ bằng nhiều loại vũ khí (đạn thường, laser, kiếm, bom)
- Né tránh chướng ngại vật (chuồn chuồn, thiên thạch)
- Tận dụng kỹ năng tốc biến và các vật phẩm tăng sức mạnh
- Mang lại trải nghiệm kịch tính nhưng dễ tiếp cận

---

## 🛠️ CÔNG NGHỆ & CẤU TRÚC

- **Ngôn ngữ**: Python 3.8+
- **Thư viện chính**: `pygame` – xử lý hình ảnh, âm thanh, sự kiện
- **Lập trình hướng đối tượng (OOP)**: chia module cho từng đối tượng như máy bay, vũ khí, quái vật
- **Quản lý va chạm**: `pygame.sprite.Group` cho hiệu suất cao
- **Tạo hiệu ứng vật lý**: mô phỏng quán tính chuyển động, phản lực khi bắn
- **Tích hợp âm thanh & rung màn hình**: tăng tính trực quan

---

## 👨‍👨‍👦 PHÂN CÔNG CÔNG VIỆC

| Thành viên          | Nhiệm vụ                                                                 |
|---------------------|--------------------------------------------------------------------------|
| Nguyễn Thanh Khai   | Hành vi máy bay, xử lý chuyển động, chướng ngại vật (chuồn chuồn, đá)    |
| Phạm Tuấn Hưng      | Giao diện người dùng (UI), âm thanh, hiệu ứng rung, vật cản, hiệu ứng    |
| Phạm Đăng Khôi      | Xây dựng các lớp vũ khí, logic va chạm, xử lý kỹ năng đặc biệt           |

🎥 **Video demo**: [Xem tại đây](https://youtu.be/G8xf9Aszqgg?si=oWytsqU3B2Zcm88L)

---

## ⚙️ HƯỚNG DẪN CÀI ĐẶT

### 1. Yêu cầu:
- Python 3.8 trở lên
- pip (Python package installer)

### 2. Cài đặt thư viện:
```bash
pip install pygame
```

### 3. Chạy game:
```bash
python main.py
```

### 4. Cấu trúc đề xuất:
```
D:/
├── README.md
└── astro_party_git/
    ├── main.py
    ├── image/
    ├── sound/
    └── [các file nguồn khác]
```

---

## 🎮 HƯỚNG DẪN CHƠI GAME

- **Số lượng người chơi**: 2 đến 4
- **Điều khiển mỗi máy bay bằng 2 phím**:
  - 1 phím để xoay
  - 1 phím để tấn công
  - Nhấn xoay 2 lần nhanh để **tốc biến**
- **Mỗi 20 giây** sẽ đổi bản đồ ngẫu nhiên
- **Vũ khí**: 
  - `Đạn thường`: tấn công cơ bản
  - `Laser`: mạnh, ngắn hạn
  - `Lôi cầu (Kiếm)`: quay quanh máy bay
  - `Bom`: phát nổ khi đến gần mục tiêu
  - `Đảo hướng`: đảo điều khiển đối thủ
- **Chướng ngại vật**:
  - `Dragonfly`: di chuyển thông minh, tấn công người gần nhất
  - `Thiên thạch`: bay ngang làm khó né tránh
- **Tính năng nâng cao**:
  - Hồi đạn tự động
  - Recoil khi bắn
  - Rung màn hình khi nổ
  - Va chạm tạo hiệu ứng

---

## 🖼️ HÌNH ẢNH MINH HỌA
![image2](AstroParty/img/image2.png)
![image3](AstroParty/img/image3.png)

![image5](AstroParty/img/image5.png)

![image7](AstroParty/img/image7.png)

![image13](AstroParty/img/image13.png)
![image17](AstroParty/img/image17.png)

![image19](AstroParty/img/image19.jpeg)
![image20](AstroParty/img/image20.png)
![image21](AstroParty/img/image21.png)

![image24](AstroParty/img/image24.png)

![image26](AstroParty/img/image26.png)

![image29](AstroParty/img/image29.png)

![image34](AstroParty/img/image34.png)
![image35](AstroParty/img/image35.png)
![image36](AstroParty/img/image36.png)
![image37](AstroParty/img/image37.png)
