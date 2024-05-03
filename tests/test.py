import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions

# The webdriver management will be handled by the browserstack-sdk
# so this will be overridden and tests will run browserstack -
# without any changes to the test files!
options = ChromeOptions()
options.set_capability('sessionName', 'BStack Sample Test')
driver = webdriver.Chrome(options=options)

try:
    # Open flipkart.com
    driver.get("https://www.flipkart.com/")
    print("Opened flipkart.com")
    
    # Wait for the search box to appear
    search_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "q")))
    print("Found search box")
    
    # Search for "Samsung Galaxy S10"
    search_box.send_keys("Samsung Galaxy S10")
    search_box.submit()
    print("Submitted search")
    
    # Wait for the "Mobiles" category link to appear and click on it
    mobiles_category = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="esFpML"]')))
    mobiles_category.click()
    print("Clicked Mobiles category")
    
    # Wait for filters to load and apply Samsung brand filter
    samsung_brand_filter = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
    (By.XPATH, '//div[@class="XqNaEv"]')))
    samsung_brand_filter.click()
    print("Applied Samsung brand filter")

    # Wait for overlay to disappear
    WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.aGZXck')))

    # Scroll to Flipkart Assured filter
    flipkart_assured_filter = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="XqNaEv eJE9fb"]')))
    actions = ActionChains(driver)
    actions.move_to_element(flipkart_assured_filter).perform()

    # Click on Flipkart Assured filter
    flipkart_assured_filter.click()
    print("Applied Flipkart Assured filter")
    
    # Sort entries by Price -> High to Low
    high_to_low_option = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Price -- High to Low"]')))
    high_to_low_option.click()
    print("Sorted by Price -> High to Low")
    
    # Read the results on page 1
    results = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="cPHDOP col-12-12"]')))
    print("Results loaded")
    
    # Create a list with required parameters
    product_details = []
    for result in results:
        try:
            product_name = WebDriverWait(result, 5).until(EC.presence_of_element_located((By.XPATH, './/div[@class="KzDlHZ"]'))).text
            display_price = WebDriverWait(result, 5).until(EC.presence_of_element_located((By.XPATH, './/div[@class="hl05eU"]'))).text
            product_link = WebDriverWait(result, 5).until(EC.presence_of_element_located((By.XPATH, './/a[@class="CGtC98"]'))).get_attribute('href')
            product_details.append({"Product Name": product_name, "Display Price": display_price, "Link to Product Details Page": product_link})
        except Exception as e:
            print(f"Error occurred while extracting product details: {e}")
    
    # Print the list on console
    for product in product_details:
        print(product)
        
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Test executed"}}')
   
except NoSuchElementException as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
except Exception as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
finally:
    # Stop the driver
    driver.quit()
