from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from residencehall import ResidenceHall
from timeit import default_timer
import time


def find_element_with_id_wait(browser, element_id, delay=3):
    try:
        return WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, element_id)))
    except TimeoutException:
        print('Cannot find element ID: {}'.format(element_id))


def find_element_with_xpath_wait(browser, xpath, delay=3):
    try:
        return WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        print('Cannot find element ID: {}'.format(xpath))


def enter_info_in_search(element, input):
    try:
        element.send_keys(input)
    except AttributeError:
        print('\tDoesn\'t exists: Unable to type in element in search')


def submit_element(element):
    """Submit in form doesn't seem to work for my case"""
    try:
        element.submit()
    except AttributeError:
        print('\tDoesn\'t exists: Unable to find element to submit')


def click_element(element):
    try:
        element.click()
    except AttributeError:
        print('\tDoesn\'t exists: Unable to click element')
    except WebDriverException:
        print('\tElement became unable to be clicked')


def find_element_xpath(browser, xpath):
    try:
        return browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        print('Element cannot be found')


def click_all_elements(elements):
    for element in elements:
        try:
            click_element(element)
        except StaleElementReferenceException:
            print('Element moved from original place in HTML')


def get_element_attribute(element, attribute):
    try:
        return element.get_attribute(attribute)
    except AttributeError:
        print('\tDoesn\'t exists: Unable to get attribute')


def get_element_attribute_with_error_handle(browser, element, attribute, element_xpath):
    """Returns element and element attribute"""
    try:
        attr = get_element_attribute(element, attribute)
        return element, attr
    except StaleElementReferenceException:
        element = find_element_xpath(browser, element_xpath)
        attr = get_element_attribute(element, attribute)
        return element, attr


def clicking_overlap(element_one, element_two):
    return element_one == element_two


def does_not_exists(element):
    return element is None


def click_all_elements_with_wait(browser, xpath, delay=0.3):
    """
    Clicking all buttons on page with a mandatory wait.
    All the checks in this method is for bad internet.
    In an environment with good internet, all these checks do not need to happen.
    Slower the internet - Greater the delay should be for it to work properly
    """
    element = find_element_with_xpath_wait(browser, xpath)
    extra_delay = False
    consecutive_delay_count = 0
    while element is not None:
        element_element_id = get_element_attribute_with_error_handle(browser, element, 'id', xpath)
        element = element_element_id[0]
        element_id = element_element_id[1]
        if does_not_exists(element):
            print('Breaking Point 1: Breaking loop')
            break
        click_element(element)
        time.sleep(delay)
        print('Mandatory Wait: {}'.format(delay))
        if extra_delay:
            time.sleep(0.5 * (consecutive_delay_count+1))
            print('Additional Wait: {}'.format(delay * (consecutive_delay_count+1)))
            extra_delay = False
            consecutive_delay_count += 1
        element = find_element_xpath(browser, xpath)
        if does_not_exists(element):
            print('Breaking Point 2: Breaking loop')
            break
        element_element_id = get_element_attribute_with_error_handle(browser, element, 'id', xpath)
        element = element_element_id[0]
        next_element_id = element_element_id[1]
        if does_not_exists(element):
            print('Breaking Point 3: Breaking loop')
            break
        overlap = element_id == next_element_id
        print('PrevElem: {}, CurrentElem: {}, Boolean: {}'.format(element_id, next_element_id, overlap))
        if clicking_overlap(element_id, next_element_id):
            extra_delay = True
        if not clicking_overlap(element_id, next_element_id):
            consecutive_delay_count = 0
        print('\tConsective Delay: {}'.format(consecutive_delay_count))


def find_washer_dryer_elements(browser):
    all_washer_dryer_count = browser.find_elements_by_xpath("//*[contains(@id, 'ctl00_ctvUniversities_actbtn')]")[1:]
    return list(map(lambda x: int(x.text), all_washer_dryer_count))


def create_all_washer_dryer_count(browser):
    try:
        return find_washer_dryer_elements(browser)
    except StaleElementReferenceException:
        time.sleep(0.1)
        return find_washer_dryer_elements(browser)


def create_pairs_of_every_two_element(array_list):
    if len(array_list) % 2 != 0:
        raise ValueError
    new_array_list = []
    index = 0
    length = len(array_list)
    while index < length:
        new_array_list.append((array_list[index], array_list[index+1]))
        index += 2
    return new_array_list


def create_residence_hall_with_washer_dryer_pairs(browser):
    all_washer_dryer_count = create_all_washer_dryer_count(browser)
    wash_dry_count_pairs = create_pairs_of_every_two_element(all_washer_dryer_count)
    res_hall_wash_dry_dict = {}
    for enum_pair, wash_dry_pair in zip(ResidenceHall.__members__.items(), wash_dry_count_pairs):
        res_hall_wash_dry_dict[enum_pair[0]] = wash_dry_pair
    return res_hall_wash_dry_dict


def print_res_hall_wash_dry_dict(dictionary):
    print('------------------------------------')
    print('   {: <15} {: ^7} {: ^7}'.format('Res.Hall', 'Washer', 'Dryer'))
    print('------------------------------------')
    for res_hall, counts in dictionary.items():
        print('   {: <15} {: ^7} {: ^7}'.format(res_hall, counts[0], counts[1]))


def main():
    browser = webdriver.PhantomJS()
    browser.get('http://umassamherst.laundrytracker.com/Room.aspx')
    university_code_input = find_element_with_id_wait(browser, element_id='txtSchoolCode')
    enter_info_in_search(university_code_input, 'amherst')
    enter_button = find_element_with_id_wait(browser, element_id='imgEnter')
    click_element(enter_button)
    button_xpath = '//*[@src="Images/nodeexp.png"]'
    # start = default_timer()
    click_all_elements_with_wait(browser, button_xpath)
    res_hall_wash_dry_dict = create_residence_hall_with_washer_dryer_pairs(browser)
    print_res_hall_wash_dry_dict(res_hall_wash_dry_dict)
    # Next thing to do is to find how many total washers and dryers there are and not just
    # the ones that are open.
    # print('Time passed: {}'.format(default_timer() - start))
    # For python 3.6 and selenium, python requires the webdriver to quit before the
    # program finishes.
    print('Ending program')
    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    main()


