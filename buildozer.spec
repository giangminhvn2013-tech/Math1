[app]

# Tên ứng dụng hiển thị trên Android
title = Toán Lớp 1 Vui Nhộn

# Tên gói nội bộ (chữ thường, không khoảng trắng)
package.name = toanlop1

# Domain ngược (dùng tạm org.example)
package.domain = org.example

# Thư mục chứa source code
source.dir = .

# Bao gồm các file cần thiết khi đóng gói
source.include_exts = py,wav,png,jpg,ogg,mp3

# Thư viện Python cần dùng
requirements = python3,pygame

# Hướng màn hình
orientation = portrait

# Toàn màn hình
fullscreen = 1

# Phiên bản ứng dụng
version = 1.0.0

# Icon (nếu có file icon.png trong thư mục gốc)
# icon.filename = %(source.dir)s/icon.png


[buildozer]

# Cấp độ log (0 = ít, 2 = nhiều chi tiết)
log_level = 2

# Cảnh báo khi chạy dưới quyền root
warn_on_root = 1

