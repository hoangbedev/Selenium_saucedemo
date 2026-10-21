# Báo cáo: Kiểm thử tự động với Selenium

- **Họ và tên:** Vu Huy Hoang
- **MSSV:** 23010138
- **Lớp / Môn học:** Đánh giá và kiểm định chất lượng phần mềm
- **Website kiểm thử:** https://www.saucedemo.com (website demo dành riêng cho việc luyện kiểm thử)

## 1. Giới thiệu Selenium
Selenium là bộ công cụ mã nguồn mở dùng để tự động hóa thao tác trên trình duyệt web, phục vụ kiểm thử chức năng (functional testing) và kiểm thử hồi quy (regression testing). Selenium WebDriver điều khiển trình duyệt (Chrome, Firefox, Edge...) thông qua driver, hỗ trợ nhiều ngôn ngữ (Python, Java, C#, JavaScript...).

**Công nghệ sử dụng trong bài:** Python 3, Selenium WebDriver 4, Pytest, pytest-html, Google Chrome.

**Tài liệu / video tham khảo:** <điền link video hoặc tài liệu bạn đã học>

## 2. Cấu trúc project
```
selenium-saucedemo/
├── tests/
│   ├── conftest.py          # Fixture khởi tạo/đóng trình duyệt, chụp ảnh khi test fail
│   └── test_saucedemo.py    # 9 test case
├── requirements.txt
├── pytest.ini
└── README.md
```

## 3. Hướng dẫn cài đặt và chạy
```bash
git clone <link-repo>
cd selenium-saucedemo
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                           # chạy có mở trình duyệt
HEADLESS=1 pytest                # chạy ẩn trình duyệt (Windows PowerShell: $env:HEADLESS=1; pytest)
```
Sau khi chạy, file báo cáo HTML được tạo tại `report.html`. Ảnh chụp khi test lỗi nằm trong `screenshots/`.

## 4. Danh sách test case

| ID | Tên test case | Các bước thực hiện | Kết quả mong đợi |
|----|---------------|--------------------|------------------|
| TC01 | Đăng nhập thành công | Nhập `standard_user` / `secret_sauce` → Login | Chuyển tới trang Products |
| TC02 | Đăng nhập sai mật khẩu | Nhập `standard_user` / mật khẩu sai → Login | Hiển thị lỗi "Username and password do not match..." |
| TC03 | Tài khoản bị khóa | Nhập `locked_out_user` / `secret_sauce` → Login | Hiển thị lỗi "...user has been locked out." |
| TC04 | Bỏ trống Username | Để trống Username, nhập mật khẩu → Login | Hiển thị lỗi "Username is required" |
| TC05 | Thêm sản phẩm vào giỏ | Đăng nhập → Add to cart "Sauce Labs Backpack" → mở giỏ | Badge = 1, sản phẩm có trong giỏ |
| TC06 | Xóa sản phẩm khỏi giỏ | Đăng nhập → Add → Remove | Badge giỏ hàng biến mất |
| TC07 | Sắp xếp giá tăng dần | Đăng nhập → chọn "Price (low to high)" | Danh sách giá được sắp xếp tăng dần |
| TC08 | Thanh toán thành công | Add sản phẩm → Cart → Checkout → nhập thông tin → Finish | Hiển thị "Thank you for your order!" |
| TC09 | Đăng xuất | Đăng nhập → mở menu → Logout | Quay về trang đăng nhập |

## 5. Kết quả thực thi
<img width="1688" height="1036" alt="image" src="https://github.com/user-attachments/assets/a56b6a3c-4e21-4f57-ad16-7483b954aa9d" />

<img width="1918" height="952" alt="image" src="https://github.com/user-attachments/assets/5049861d-c436-44c3-8d8f-f62f1526b83e" />


Chạy bằng lệnh `pytest`: **9/9 test case Pass (tỉ lệ đạt 100%)**.

| ID | Tên test case | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
|----|---------------|------------------|-----------------|------------|
| TC01 | Đăng nhập thành công | Chuyển tới trang Products | Chuyển tới trang Products | ✅ Pass |
| TC02 | Đăng nhập sai mật khẩu | Hiển thị lỗi "Username and password do not match..." | Hiển thị đúng thông báo lỗi | ✅ Pass |
| TC03 | Tài khoản bị khóa | Hiển thị lỗi "...user has been locked out." | Hiển thị đúng thông báo lỗi | ✅ Pass |
| TC04 | Bỏ trống Username | Hiển thị lỗi "Username is required" | Hiển thị đúng thông báo lỗi | ✅ Pass |
| TC05 | Thêm sản phẩm vào giỏ | Badge = 1, sản phẩm có trong giỏ | Badge = 1, sản phẩm có trong giỏ | ✅ Pass |
| TC06 | Xóa sản phẩm khỏi giỏ | Badge giỏ hàng biến mất | Badge biến mất | ✅ Pass |
| TC07 | Sắp xếp giá tăng dần | Danh sách giá tăng dần | Danh sách giá tăng dần | ✅ Pass |
| TC08 | Thanh toán thành công | Hiển thị "Thank you for your order!" | Hiển thị đúng thông báo | ✅ Pass |
| TC09 | Đăng xuất | Quay về trang đăng nhập | Quay về trang đăng nhập | ✅ Pass |

**Tổng kết:**

| Tổng số | Pass | Fail | Tỉ lệ đạt |
|---------|------|------|-----------|
| 9 | 9 | 0 | 100% |
