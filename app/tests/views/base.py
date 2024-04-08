import os
import time

from django.conf import settings
from django.test.selenium import LiveServerTestCase
from django.test.utils import override_settings
from selenium import webdriver

from tests.factories import *


@override_settings(DEBUG=True, ENVIRONMENT="localtest")
class BaseViewsTest(LiveServerTestCase):

    def setUp(self):
        self.operator = OperatorFactory.create()
        self.user = UserFactory.create()
        self.contract_type = ContractTypeFactory.create()
        self.contract_subject = ContractSubjectFactory.create()
        self.webdriver = webdriver.Firefox()

    def tearDown(self):
        self.webdriver.quit()

    def get_login_required_page(self, url):
        self.client.force_login(self.user)
        session_key = self.client.cookies[settings.SESSION_COOKIE_NAME].value
        self.webdriver.get(self.live_server_url + url)
        self.webdriver.add_cookie({"name": settings.SESSION_COOKIE_NAME, "value": session_key, "path": "/"})
        self.webdriver.get(self.live_server_url + url)

    def fill_client_form(self):
        self.webdriver.find_element(by="id", value="id_name").send_keys(faker.name())
        self.webdriver.find_element(by="id", value="id_email").send_keys(faker.email())
        self.webdriver.find_element(by="id", value="id_id_number").send_keys(faker.numerify(text="#########"))
        self.webdriver.find_element(by="id", value="id_phone_number").send_keys(faker.numerify(text="%%%%%%%%%"))
        self.webdriver.find_element(by="id", value="id_address").send_keys(faker.address())
        self.webdriver.find_element(by="id", value="id_note").send_keys("jen test")

    def fill_proposal_form_work(self):
        self.webdriver.find_element(by="id", value="id_document_number").send_keys(faker.numerify(text="D%%%"))
        self.webdriver.find_element(by="id", value="id_subject").send_keys("DVERE")
        self.webdriver.find_element(by="id", value="id_contract_type").send_keys("Smlouva o dílo")
        self.webdriver.find_element(by="id", value="id_fulfillment_at").send_keys(faker.date())
        self.webdriver.find_element(by="id", value="id_fulfillment_place").send_keys(faker.city())
        self.webdriver.find_element(by="id", value="id_file").send_keys(
            os.path.abspath("/Users/petr/github/kontraktor/NAB_TIC.pdf")
        )

    def fill_proposal_form_buy(self):
        self.webdriver.find_element(by="id", value="id_document_number").send_keys(faker.numerify(text="K%%%"))
        self.webdriver.find_element(by="id", value="id_subject").send_keys("DVERE")
        self.webdriver.find_element(by="id", value="id_contract_type").send_keys("Kupní smlouva")
        self.webdriver.find_element(by="id", value="id_fulfillment_at").send_keys(faker.date())
        self.webdriver.find_element(by="id", value="id_fulfillment_place").send_keys(faker.city())
        # self.webdriver.find_element(by="id", value="id_file").send_keys(os.path.abspath("path/to/profilepic.gif"))

    def fill_new_item_form(self):
        self.webdriver.find_element(by="id", value="title_new").send_keys(faker.color_name())
        self.webdriver.find_element(by="id", value="description_new").send_keys(faker.safe_color_name())
        self.webdriver.find_element(by="id", value="production_date_new").send_keys(faker.date())
        self.webdriver.find_element(by="id", value="production_price_new").send_keys(faker.random_int(min=100, max=150))
        self.webdriver.find_element(by="id", value="price_per_unit_new").send_keys(faker.random_int(min=200, max=250))
        self.webdriver.find_element(by="id", value="quantity_new").send_keys(faker.random_digit_not_null())
        self.webdriver.find_element(by="id", value="sale_discount_new").send_keys(faker.random_digit_not_null())

    def fill_and_submit_edit_item_form(self):
        item_id = (
            self.webdriver.find_element(by="class name", value="edit-form").get_attribute("id").strip("edit_item_form_")
        )
        element = self.webdriver.find_element(by="id", value="title_" + item_id)
        old_data = element.get_attribute("value")
        element.clear()
        element.send_keys(faker.color_name())
        # self.webdriver.find_element(by="id", value="description_" + item_id).clear()
        # self.webdriver.find_element(by="id", value="description_" + item_id).send_keys(faker.safe_color_name())
        # self.webdriver.find_element(by="id", value="production_date_" + item_id).clear()
        # self.webdriver.find_element(by="id", value="production_date_" + item_id).send_keys(faker.date())
        # self.webdriver.find_element(by="id", value="production_price_" + item_id).clear()
        # self.webdriver.find_element(by="id", value="production_price_" + item_id).send_keys(faker.random_int(min=100, max=150))
        # self.webdriver.find_element(by="id", value="price_per_unit_" + item_id).clear()
        # self.webdriver.find_element(by="id", value="price_per_unit_" + item_id).send_keys(faker.random_int(min=200, max=250))
        # self.webdriver.find_element(by="id", value="quantity_" + item_id).clear()
        # self.webdriver.find_element(by="id", value="quantity_" + item_id).send_keys(faker.random_digit_not_null())
        # self.webdriver.find_element(by="id", value="sale_discount_" + item_id).clear()
        # self.webdriver.find_element(by="id", value="sale_discount_" + item_id).send_keys(faker.random_digit_not_null())
        self.webdriver.find_element(by="id", value="save_" + item_id).click()
        time.sleep(1)
        new_data = self.webdriver.find_element(by="id", value="title_" + item_id).get_attribute("value")
        return old_data, new_data

    def fill_upload_form(self):
        self.webdriver.find_element(by="id", value="id_file").send_keys(
            os.path.abspath("/Users/petr/github/kontraktor/NAB_TIC.pdf")
        )
        self.webdriver.find_element(by="id", value="id_tag").send_keys(os.path.abspath("nahraný testový soubor"))
