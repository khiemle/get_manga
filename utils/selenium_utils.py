from selenium.common.exceptions import NoSuchElementException

def get_text_by_xpath(driver, xpath):
    try:
        element = driver.find_element(by="xpath", value=xpath)
        return element.text
    except NoSuchElementException:
        return None

def get_attribute_by_xpath(driver, xpath, attribute):
    try:
        attributeValue = driver.find_element(by="xpath", value=xpath).get_attribute(attribute)
        return attributeValue
    except NoSuchElementException:
        return None