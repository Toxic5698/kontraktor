import time

from tests.views.base import BaseViewsTest
from tests.factories import ClientFactory

class WelcomePageTest(BaseViewsTest):

    def test_welcome_page_local(self):
        self.webdriver.get(self.live_server_url)
        self.assertIn("Spravujte své dokumenty jednoduše!", self.webdriver.find_element(by="id", value="welcome-header").text)

    def test_welcome_page_devel(self):
        self.webdriver.get("http://kontraktor.cechpetr.cz")
        self.assertIn("Spravujte své dokumenty jednoduše!", self.webdriver.find_element(by="id", value="welcome-header").text)



class ClientViewsTest(BaseViewsTest):

    def test_get_document_list_with_sign_code(self):
        self.client = ClientFactory.create()
        self.webdriver.get(self.live_server_url)
        self.webdriver.find_element(by="name", value="sign_code").send_keys(str(self.client.sign_code))
        form = self.webdriver.find_element(by="id", value="client-signcode-form")
        form.submit()
        time.sleep(2)
        self.assertIn(self.client.name, self.webdriver.find_element(by="id", value="client-tag").text())

    # def test_get_document_list_with_email(self):
    # def test_get_document_list_not_success(self):
