from json import loads

from behave import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from features.fixtures import find_by_link, invisibility_of_preloader


@given('go to login page: {link}')
def step_impl(context, link):
    context.login_page = link
    context.browser.get(link)


@when('type credentials {input_id_1} and {input_id_2}')
def step_impl(context, input_id_1, input_id_2):
    step_text = loads(context.text)
    list_size = len(step_text[input_id_1]) - 1
    i = 0
    for index in range(list_size):
        invisibility_of_preloader(context)
        context.browser.find_element_by_id(input_id_1).send_keys(step_text[input_id_1][index])
        context.browser.find_element_by_id(input_id_2).send_keys(step_text[input_id_2][index])
        previous_url = context.browser.current_url
        if i < list_size:
            click_on_btn(context, 'login_submit')
            stay_on_page(context, previous_url)
            show_message(context, 'CPF/CNPJ inválido', 'Email inválido', 'invalid-feedback')
            i += 1
            context.browser.find_element_by_id(input_id_1).clear()
            # context.browser.find_element_by_id(input_id_2).clear()


@when('click on {btn_input} button')
def click_on_btn(context, btn_input):
    try:
        context.browser.find_element_by_xpath(btn_input).click()
    except NoSuchElementException:
        try:
            context.browser.find_element_by_id(btn_input).click()
        except NoSuchElementException:
            try:
                context.browser.find_element_by_class_name(btn_input).click()
            except NoSuchElementException:
                try:
                    link_button = find_by_link(context, btn_input)
                    if link_button is not None:
                        link_button.click()
                except NoSuchElementException as e:
                    raise e


@then('stay on page: {link}')
def stay_on_page(context, link):
    assert context.browser.current_url == link


@then('show {msg_1} or {msg_2} on {div}')
def show_message(context, msg_1, msg_2, div):
    feedback_list = context.browser.find_elements_by_class_name(div)
    for feedback in feedback_list:
        assert msg_1 or msg_2 in feedback.text


@when('type {input_id}: <{value}>')
def type_by_id(context, input_id, value):
    context.browser.find_element_by_id(input_id).send_keys(value)


@then('redirect to {name} page: {link}')
def redirect_to_page(context, name, link):
    page_title = context.browser.find_element_by_class_name('breadcrumb-item')
    assert context.browser.current_url == link
    assert name in page_title.text