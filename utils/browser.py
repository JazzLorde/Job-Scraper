"""
Browser Utilities
Chrome driver setup and browser-related functions
"""

import random
import time
import undetected_chromedriver as uc
from selenium_stealth import stealth

def get_chrome_driver(load_cookies_from=None):
    """Create and configure Chrome driver with stealth settings"""
    options = uc.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options)

    # Random configurations for stealth
    languages = [["en-US", "en"], ["en-GB", "en"], ["en"], ["en-US"]]
    vendors = ["Google Inc.", "Apple Inc.", "Mozilla Foundation"]
    platforms = ["Win32", "Linux x86_64", "MacIntel"]
    renderers = ["Intel Iris OpenGL Engine", "AMD Radeon Pro", "NVIDIA GeForce", "Apple M1"]

    stealth(driver,
        languages=random.choice(languages),
        vendor=random.choice(vendors),
        platform=random.choice(platforms),
        webgl_vendor="Intel Inc.",
        renderer=random.choice(renderers),
        fix_hairline=True,
    )

    return driver

def human_like_scroll(driver):
    """Perform human-like scrolling"""
    total_height = driver.execute_script("return document.body.scrollHeight")
    scroll_points = random.randint(5, 10)
    for _ in range(scroll_points):
        scroll_distance = total_height // scroll_points
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(random.uniform(0.5, 1.5))