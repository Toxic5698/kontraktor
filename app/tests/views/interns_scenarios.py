import time

from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By

from tests.views.base import BaseViewsTest

class AuthenticationTest(BaseViewsTest):

    def test_user_login_success(self):
        self.webdriver.get(self.live_server_url)
        self.webdriver.find_element(by="id", value="login").click()
        self.webdriver.find_element(by="id", value="username").send_keys(self.user.username)
        self.webdriver.find_element(by="id", value="password").send_keys(self.user.password)
        self.webdriver.find_element(by="id", value="login-submit").click()
        time.sleep(1)
        self.assertEqual(self.user.username, self.webdriver.find_element(by="id", value="user-button").text)

    def test_user_login_not_success(self):
        self.webdriver.get(self.live_server_url)
        self.webdriver.find_element(by="id", value="login").click()
        self.webdriver.find_element(by="id", value="username").send_keys(self.user.username)
        self.webdriver.find_element(by="id", value="password").send_keys(self.user.password)
        self.webdriver.find_element(by="id", value="login-submit").click()
        time.sleep(1)
        self.assertEqual(self.user.username, self.webdriver.find_element(by="id", value="user-button").text)

    # def test_user_logout(self):

    # def test_user_change_password(self):



class TestProposalViews(BaseViewsTest):

    def test_create_proposal(self):
        # get to start page
        self.get_login_required_page(url='/proposals')
        self.assertNotIn("login", self.webdriver.current_url, "Proposals page is not loaded")


        # get to form
        self.webdriver.find_element(by="id", value="create-client-and-proposal").click()
        self.assertIn("/proposals/create", self.webdriver.current_url, "Proposal form is not successfully loaded")


        # fill & submit form
        self.fill_client_form()
        self.fill_proposal_form()

        form = self.webdriver.find_element(by="id", value="proposal-form")
        form.submit()
        time.sleep(1)

        # evaluate result of proposal form
        self.assertIn("/proposals/edit/", self.webdriver.current_url, "Proposal form is not successfully submitted")

        # create items
        self.webdriver.find_element(by="id", value="items-button").click()
        self.assertIn("/proposals/items/", self.webdriver.current_url, "Items page is not loaded")
        self.fill_new_item_form()


        # create contract
        # self.webdriver.find_element(by="id", value="create-contract-button").click()
        # self.assertIn("/contracts/edit/", self.webdriver.current_url, "Contract is not successfully created")



    # def test_proposal_list(self):
    #     self.get_login_required_page(url='/proposals')
    #     self.get_login_required_page(url='/proposals')
