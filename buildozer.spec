[app]

# Thông tin ứng dụng
title = Toán Lớp 1
package.name = toanlop1
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,ogg,mp3

# Thư viện cần thiết
requirements = python3,kivy

# Màn hình
orientation = portrait

# Cho phép log chi tiết để debug
log_level = 2

# Icon & ảnh splash (tùy chọn, bạn có thể thay đường dẫn file thật)
icon.filename = %(source.dir)s/data/icon.png
presplash.filename = %(source.dir)s/data/presplash.png

# Android thông tin thêm
android.api = 31
android.minapi = 21
android.sdk = 30
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.ndk_api = 21

# APK type
android.accept_sdk_license = True
fullscreen = 0


# (Tùy chọn) nếu bạn muốn xuất bản release có ký
# android.release = True
# android.sign = True
# android.keyalias = mykey

[buildozer]

log_level = 2
warn_on_root = 1
