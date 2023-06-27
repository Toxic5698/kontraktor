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
        self.webdriver.add_cookie({'name': settings.SESSION_COOKIE_NAME, 'value': session_key, 'path': '/'})
        self.webdriver.get(self.live_server_url + url)

    def fill_client_form(self):
        self.webdriver.find_element(by="id", value="id_name").send_keys("Test")
        self.webdriver.find_element(by="id", value="id_email").send_keys("test@test.cz")
        self.webdriver.find_element(by="id", value="id_id_number").send_keys("59389329")
        self.webdriver.find_element(by="id", value="id_phone_number").send_keys("745687909")
        self.webdriver.find_element(by="id", value="id_address").send_keys("u testova, 4")
        self.webdriver.find_element(by="id", value="id_note").send_keys("jen test")

    def fill_proposal_form(self):
        self.webdriver.find_element(by="id", value="id_proposal_number").send_keys("D45test")
        self.webdriver.find_element(by="id", value="id_subject").send_keys("DVERE")
        self.webdriver.find_element(by="id", value="id_contract_type").send_keys("Smlouva o dílo")
        self.webdriver.find_element(by="id", value="id_fulfillment_at").send_keys("2023-09-09")
        self.webdriver.find_element(by="id", value="id_fulfillment_place").send_keys("Brno")
        # self.webdriver.find_element(by="id", value="id_file").send_keys("test@test.cz")

    def fill_new_item_form(self):
        self.webdriver.find_element(by="id", value="title_new").send_keys(faker.color_name())
        self.webdriver.find_element(by="id", value="description_new").send_keys(faker.safe_color_name())

