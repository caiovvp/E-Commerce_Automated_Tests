from datetime import date
import datetime
import random
from json import loads

from ipython_genutils.py3compat import xrange

from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import DesiredCapabilities, Remote


# FUNCTION THAT INSTANCES THAT THE BROWSER IS CHROME AND THAT IT QUITS ONCE THE TEST IS OVER
def browser_chrome(context):
    # -- BEHAVE-FIXTURE: Similar to @contextlib.contextmanager
    # capability = DesiredCapabilities.FIREFOX
    # context.browser = Remote('http://srv01.connect.com.vc:4444/wd/hub', capability)
    context.browser = Firefox(executable_path='C:\Selenium WebDriver\geckodriver.exe')
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    context.browser.quit()


# FUNCTION TO TIMEOUT THE TEST IF NECESSARY
def timeout_for_page_load(context):
    context.browser.set_page_load_timeout(8)


# -- NOTE: Change False for True if you want ipdb debugger running when an error happens
BEHAVE_DEBUG_ON_ERROR = False


def setup_debug_on_error(userdata):
    global BEHAVE_DEBUG_ON_ERROR
    BEHAVE_DEBUG_ON_ERROR = userdata.getbool("BEHAVE_DEBUG_ON_ERROR")


def invisibility_of_preloader(context):
    WebDriverWait(context.browser, 5).until(EC.invisibility_of_element_located((By.ID, 'preloader')))


# LOAD INFORMATION ON THE STEP DEFINITION AND RUN CONFIRM_MESSAGE() WITH THE PARAMETERS LOADED
def assert_message(context):
    text_from_step = loads(context.text)
    confirm_message(context, text_from_step['web_ele'], text_from_step['message'])


# CONFIRM IF MESSAGE IS INSIDE THE TEXT OF A WEB ELEMENT
def confirm_message(context, web_ele, message):
    box = context.browser.find_element_by_xpath(web_ele)
    assert message in box.text


# RETURNS A WEB ELEMENT THAT CONTAINS THE HREF "LINK" IN ITS PROPERTIES
def find_by_link(context, link):
    anchors_list = context.browser.find_elements_by_tag_name('a')
    for element in anchors_list:
        if element.get_attribute('href') is not None and link in element.get_attribute('href'):
            return element


# CALCULATES A RANDOM CPF AND RETURNS IT (NOT FORMATTED, ONLY NUMBERS)
def cpf():
    def calculate_cpf(digs):
        s = 0
        qtd = len(digs)
        for i in xrange(qtd):
            s += n[i] * (1 + qtd - i)
        res = 11 - s % 11
        if res >= 10:
            return 0
        return res

    n = [random.randrange(10) for i in xrange(9)]
    n.append(calculate_cpf(n))
    n.append(calculate_cpf(n))
    return "%d%d%d%d%d%d%d%d%d%d%d" % tuple(n)


# CALCULATES A RANDOM INDEX FOR AN ITEM ON A LIST
def random_option(options_list):
    if len(options_list) == 1:
        random_num = 0
    else:
        random_num = random.randint(0, (len(options_list) - 1))
    return random_num


# GENERATE RANDOM DATE TIME AND RETURNS IT
def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_datetime = start_date + datetime.timedelta(days=random_number_of_days)
    return random_datetime.strftime('%d\%m\%Y')


# SAVE THE INPUT VALUE AND CLEAR IT LATER
def save_and_clear(input):
    input_value = input.get_attribute('value')
    input.clear()
    return input_value


# FIND AN INPUT ON THE PAGE AND CLEAR IT
def find_and_clear_input(context, id):
    input = context.browser.find_element_by_id(id)
    input.clear()
    return input


# GENERATES RANDOM INTEGERS ACCORDING TO THE RANGE GIVEN
def random_numbers(web_ele, num_quantity):
    for num in range(num_quantity):
        web_ele.send_keys(f'{random.randint(0, 9)}')
