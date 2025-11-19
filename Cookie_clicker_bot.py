"""
EXTREME COOKIE CLICKER BOT (EDGE EDITION)
-----------------------------------------

• Auto-clicks the cookie at very high speed
• Auto-buys upgrades and buildings
• Auto-collects golden cookies
• Auto-pops wrinklers
• Logs:
    - Building purchases
    - Upgrade purchases
    - Golden cookie clicks
    - Wrinkler pops

Great for automation beginners using Selenium + Edge.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# ============================================================
# CONFIGURATION
# ============================================================

CLICK_INTERVAL = 0.0001      # Speed of clicking the cookie
UPGRADE_INTERVAL = 0.5       # Interval to buy upgrades
BUILD_INTERVAL = 1.5         # Interval to buy the best building
GOLDEN_INTERVAL = 0.1        # Interval to click golden cookies
WRINKLER_INTERVAL = 2        # Interval to pop wrinklers
RUN_MINUTES = 5              # Total run time


# ============================================================
# BROWSER SETUP (EDGE VERSION)
# ============================================================

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Edge(options=options)

driver.get("https://ozh.github.io/cookieclicker/")
time.sleep(3)

# Click English language if available
try:
    driver.find_element(By.ID, "langSelect-EN").click()
    time.sleep(2)
except:
    pass


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def js(code):
    """Execute JS safely."""
    return driver.execute_script(code)


def safe_click(element):
    """Click an element without crashing on errors."""
    try:
        element.click()
    except:
        try:
            driver.execute_script("arguments[0].click();", element)
        except:
            pass


def remove_popups():
    """Remove annoying banners or consent popups."""
    try:
        popups = driver.find_elements(By.CSS_SELECTOR, ".cc_banner, .fc-consent-root")
        for p in popups:
            driver.execute_script("arguments[0].remove()", p)
    except:
        pass


# ============================================================
# LOGGING HELPERS
# ============================================================

def log_building_purchase(product):
    pid = product.get_attribute("id")
    name = product.find_element(By.CLASS_NAME, "title").text
    cost = product.find_element(By.CLASS_NAME, "price").text
    print(f"[BUILDING] Bought {name} ({pid}) — {cost}")


def log_upgrade_purchase(upg):
    name = upg.get_attribute("onmouseover")
    print(f"[UPGRADE] Purchased → {name}")


def log_golden():
    print("[GOLDEN] Golden cookie clicked!")


def log_wrinkler():
    print("[WRINKLER] Wrinkler popped!")


# ============================================================
# BOT FEATURES
# ============================================================

def click_golden_cookies():
    shimmers = driver.find_elements(By.CSS_SELECTOR, ".shimmer")
    for s in shimmers:
        safe_click(s)
        log_golden()


def buy_upgrades():
    upgrades = driver.find_elements(By.CSS_SELECTOR, ".upgrade.enabled")
    for u in upgrades:
        log_upgrade_purchase(u)
        safe_click(u)


def buy_best_building():
    products = driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")
    if products:
        best = products[-1]
        log_building_purchase(best)
        safe_click(best)


def pop_wrinklers():
    wrinklers = driver.find_elements(By.CSS_SELECTOR, "#wrinklers > div")
    for w in wrinklers:
        safe_click(w)
        log_wrinkler()


# ============================================================
# MAIN LOOP — EXTREME MODE
# ============================================================

cookie = driver.find_element(By.ID, "bigCookie")
end_time = time.time() + RUN_MINUTES * 60

next_upgrade = time.time()
next_build = time.time()
next_golden = time.time()
next_wrinkler = time.time()

print("🚀 EXTREME MODE STARTED (EDGE VERSION)\n")

while time.time() < end_time:

    cookie.click()

    if time.time() > next_golden:
        click_golden_cookies()
        next_golden = time.time() + GOLDEN_INTERVAL

    remove_popups()

    if time.time() > next_upgrade:
        buy_upgrades()
        next_upgrade = time.time() + UPGRADE_INTERVAL

    if time.time() > next_build:
        buy_best_building()
        next_build = time.time() + BUILD_INTERVAL

    if time.time() > next_wrinkler:
        pop_wrinklers()
        next_wrinkler = time.time() + WRINKLER_INTERVAL


# ============================================================
# END SUMMARY
# ============================================================

stats = driver.find_element(By.ID, "cookies").text.split()
total = stats[0]
cps = stats[4]

print("\n==== GAME SUMMARY ====")
print(f"Total Cookies: {total}")
print(f"Cookies Per Second: {cps}")
print("======================\n")

print("🎉 Extreme mode finished! 🎉")
