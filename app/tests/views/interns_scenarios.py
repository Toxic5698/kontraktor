import time

from selenium.common import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.by import By

from tests.views.base import BaseViewsTest

class AuthenticationOnServerTest(BaseViewsTest):

    def test_user_login_success(self):
        self.webdriver.get("http://kontraktor.cechpetr.cz")
        self.webdriver.find_element(by="id", value="login").click()
        self.webdriver.find_element(by="id", value="username").send_keys("petr")
        self.webdriver.find_element(by="id", value="password").send_keys("12345")
        self.webdriver.find_element(by="id", value="login-submit").click()
        time.sleep(1)
        self.assertEqual("petr", self.webdriver.find_element(by="id", value="user-button").text)

    def test_create_client_and_proposal(self):
        # get to user interface
        self.test_user_login_success()
        # create client and proposal
        TestProposalViews.create_client_and_proposal()

    def test_create_item(self):
        self.test_user_login_success()




    # def test_user_logout(self):

    # def test_user_change_password(self):



class TestProposalViews(BaseViewsTest):

    def test_walk(self):
        self.get_to_proposals_page()
        self.create_client_and_proposal()
        self.create_item()
        self.create_item()
        self.edit_item()
        # self.edit_payment_due_success()
        # self.edit_payment_due_not_success()
        # self.edit_payment_part_success()
        # self.edit_payment_part_not_success()
        self.edit_payment_part_and_due()
        self.delete_item()
        self.create_or_edit_contract_from_proposal_page()
        self.create_or_edit_contract_from_proposal_page()

    def get_to_proposals_page(self):
        # get to start page
        self.get_login_required_page(url='/proposals')
        self.assertNotIn("login", self.webdriver.current_url, "Proposals page is not loaded")

    def create_client_and_proposal(self):
        self.get_to_proposals_page()

        # get to form
        self.webdriver.find_element(by="id", value="create-client-and-proposal").click()
        self.assertIn("/proposals/create", self.webdriver.current_url, "Proposal form is not successfully loaded")


        # fill & submit form
        self.fill_client_form()
        self.fill_proposal_form_work()

        form = self.webdriver.find_element(by="id", value="proposal-form")
        form.submit()
        time.sleep(3)

        # evaluate result of proposal form
        self.assertIn("/proposals/edit/", self.webdriver.current_url, "Proposal form is not successfully submitted")

    def create_item(self):
        # get page
        self.webdriver.find_element(by="id", value="items-button").click()
        self.assertIn("/proposals/items/", self.webdriver.current_url, "Items page is not loaded")

        # get count before creating
        count_before = len(self.webdriver.find_elements(by="css selector", value="tr"))

        # fill and submit form
        self.fill_new_item_form()
        self.webdriver.find_element(by="id", value="create_button").click()
        time.sleep(1)

        # evaluate result of create item form
        count_after = len(self.webdriver.find_elements(by="css selector", value="tr"))
        self.assertNotEquals(count_before, count_after, "Items form have same count of tr elements")

        # back to proposal
        self.webdriver.find_element(by="id", value="back_to_proposal_button").click()

    def edit_item(self):
        # get page
        self.webdriver.find_element(by="id", value="edit_items_from_page").click()
        self.assertIn("/proposals/items/", self.webdriver.current_url, "Items page is not loaded")

        # fill and submit form
        old_data, new_data = self.fill_and_submit_edit_item_form()

        # evaluate result of create item form
        self.assertNotEquals(old_data, new_data, f"Item's title didn't change {old_data} x {new_data}")

        # back to proposal
        self.webdriver.find_element(by="id", value="back_to_proposal_button").click()

    def delete_item(self):
        # get page
        self.webdriver.find_element(by="id", value="items-button").click()
        self.assertIn("/proposals/items/", self.webdriver.current_url, "Items page is not loaded")

        # get count before creating
        count_before = len(self.webdriver.find_elements(by="css selector", value="tr"))

        # perform deletion
        self.webdriver.find_element(by="id", value="delete").click()
        self.webdriver.find_element(by="id", value="delete-confirm").click()

        # evaluate result of create item form
        count_after = len(self.webdriver.find_elements(by="css selector", value="tr"))
        self.assertNotEquals(count_before, count_after, "Items form have same count of tr elements")

        # back to proposal
        self.webdriver.find_element(by="id", value="back_to_proposal_button").click()

    def edit_payment_due_success(self):
        element = self.webdriver.find_element(by="id", value="payment_due_1")
        old_data = element.get_attribute("value")
        element.send_keys("po dokončení")
        self.webdriver.find_element(by="id", value="save_payments").click()
        new_data = self.webdriver.find_element(by="id", value="payment_due_1").get_attribute("value")
        self.assertNotEquals(old_data, new_data, f"Payment due didn't change {old_data} x {new_data}")


    def edit_payment_due_not_success(self):
        element = self.webdriver.find_element(by="id", value="payment_due_1")
        element.send_keys("-")
        self.webdriver.find_element(by="id", value="save_payments").click()
        alert = self.webdriver.find_element(by="class name", value="toast-body").text
        self.assertIn(alert, "U plateb musí být nastavena splatnost.", f"Payment due alert didn't appear")

    def edit_payment_part_success(self):
        element = self.webdriver.find_element(by="id", value="payment_part_1")
        old_data = element.get_attribute("value")
        element.clear()
        element.send_keys("80")
        self.webdriver.find_element(by="id", value="payment_part_2").send_keys("20")
        self.webdriver.find_element(by="id", value="save_payments").click()
        new_data = self.webdriver.find_element(by="id", value="payment_part_1").get_attribute("value")
        self.assertNotEquals(old_data, new_data, f"Payment part didn't change {old_data} x {new_data}")

    def edit_payment_part_not_success(self):
        element = self.webdriver.find_element(by="id", value="payment_part_1")
        element.clear()
        element.send_keys("80")
        self.webdriver.find_element(by="id", value="payment_part_2").send_keys("60")
        self.webdriver.find_element(by="id", value="save_payments").click()
        alert = self.webdriver.find_element(by="class name", value="toast-body").text
        self.assertIn(alert, "Souhrn částí plateb se nerovná celku.", f"Payment part alert didn't appear")

    def edit_payment_part_and_due(self):
        part_1 = self.webdriver.find_element(by="id", value="payment_part_1")
        old_data = part_1.get_attribute("value")
        part_1.clear()
        part_1.send_keys("80")
        self.webdriver.find_element(by="id", value="payment_part_2").send_keys("20")
        self.webdriver.find_element(by="id", value="payment_due_2").send_keys("po dokončení")
        self.webdriver.find_element(by="id", value="save_payments").click()
        new_data = self.webdriver.find_element(by="id", value="payment_part_1").get_attribute("value")
        self.assertNotEquals(old_data, new_data, f"Payment part didn't change {old_data} x {new_data}")

    # def show_proposal(self):
    #     self.webdriver.find_element(by="id", value="show-proposal-button").click()
    #     time.sleep(5)

    def create_or_edit_contract_from_proposal_page(self):
        try:
            element = self.webdriver.find_element(by="id", value="create-contract-button")
        except NoSuchElementException:
            element = self.webdriver.find_element(by="id", value="edit-contract-button")
        element.click()
        self.assertIn("/contracts/edit/", self.webdriver.current_url, "Contract is not successfully created")
        self.webdriver.back()
        self.webdriver.refresh()
