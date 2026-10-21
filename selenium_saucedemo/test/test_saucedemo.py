"""Kiểm thử tự động website https://www.saucedemo.com bằng Selenium + Pytest."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

VALID_USER = "standard_user"
LOCKED_USER = "locked_out_user"
PASSWORD = "secret_sauce"


# ---------- Helper ----------
def wait(driver, timeout=10):
    return WebDriverWait(driver, timeout)


def login(driver, username, password):
    driver.find_element(By.ID, "user-name").clear()
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


def get_error(driver):
    return wait(driver).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    ).text


# ---------- Test cases ----------
def test_tc01_login_success(driver):
    """TC01: Đăng nhập thành công với tài khoản hợp lệ."""
    login(driver, VALID_USER, PASSWORD)
    wait(driver).until(EC.url_contains("inventory.html"))
    assert driver.find_element(By.CLASS_NAME, "title").text == "Products"


def test_tc02_login_wrong_password(driver):
    """TC02: Đăng nhập thất bại khi sai mật khẩu."""
    login(driver, VALID_USER, "wrong_password")
    assert "Username and password do not match" in get_error(driver)
    assert "inventory.html" not in driver.current_url


def test_tc03_login_locked_user(driver):
    """TC03: Tài khoản bị khóa không thể đăng nhập."""
    login(driver, LOCKED_USER, PASSWORD)
    assert "locked out" in get_error(driver)


def test_tc04_login_empty_username(driver):
    """TC04: Bỏ trống Username hiển thị thông báo lỗi."""
    login(driver, "", PASSWORD)
    assert "Username is required" in get_error(driver)


def test_tc05_add_to_cart(driver):
    """TC05: Thêm sản phẩm vào giỏ hàng, badge = 1 và sản phẩm có trong giỏ."""
    login(driver, VALID_USER, PASSWORD)
    wait(driver).until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert badge.text == "1"
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    names = [e.text for e in wait(driver).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_name")))]
    assert "Sauce Labs Backpack" in names


def test_tc06_remove_from_cart(driver):
    """TC06: Xóa sản phẩm khỏi giỏ hàng, badge biến mất."""
    login(driver, VALID_USER, PASSWORD)
    wait(driver).until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
    driver.find_element(By.ID, "remove-sauce-labs-backpack").click()
    wait(driver).until(EC.invisibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    assert len(driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")) == 0


def test_tc07_sort_price_low_to_high(driver):
    """TC07: Sắp xếp sản phẩm theo giá tăng dần."""
    login(driver, VALID_USER, PASSWORD)
    select = Select(wait(driver).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product_sort_container"))))
    select.select_by_value("lohi")
    prices = [float(e.text.replace("$", ""))
              for e in driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
    assert prices == sorted(prices)


def test_tc08_checkout_flow(driver):
    """TC08: Thanh toán thành công (end-to-end)."""
    login(driver, VALID_USER, PASSWORD)
    wait(driver).until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-bike-light"))).click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    wait(driver).until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
    wait(driver).until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("An")
    driver.find_element(By.ID, "last-name").send_keys("Nguyen")
    driver.find_element(By.ID, "postal-code").send_keys("100000")
    driver.find_element(By.ID, "continue").click()
    wait(driver).until(EC.element_to_be_clickable((By.ID, "finish"))).click()
    header = wait(driver).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))).text
    assert header == "Thank you for your order!"


def test_tc09_logout(driver):
    """TC09: Đăng xuất về lại trang đăng nhập."""
    login(driver, VALID_USER, PASSWORD)
    wait(driver).until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))).click()
    wait(driver).until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))).click()
    wait(driver).until(EC.visibility_of_element_located((By.ID, "login-button")))
    assert driver.current_url.rstrip("/") == "https://www.saucedemo.com"
