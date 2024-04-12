import time

from selenium.common import NoSuchElementException

from tests.views.base import BaseViewsTest


class OnDevServerTest(BaseViewsTest):

    def test_user_login_success(self):
        self.webdriver.get("http://demo.samoset.cechpetr.cz")
        self.webdriver.find_element(by="id", value="login").click()
        self.webdriver.find_element(by="id", value="username").send_keys("petr")
        self.webdriver.find_element(by="id", value="password").send_keys("12345")
        self.webdriver.find_element(by="id", value="login-submit").click()
        time.sleep(1)
        self.assertEqual("petr", self.webdriver.find_element(by="id", value="user-button").text)

    def test_walk_on_dev_server(self):
        proposal_tests = TestProposalViews()
        # get to user interface
        self.test_user_login_success()
        # create client and proposal
        create_client_and_proposal(self)
        create_item(self)
        create_item(self)
        create_item(self)
        edit_payment_part_and_due(self)

        create_client_and_proposal(self)
        create_item(self)
        create_item(self)
        create_item(self)
        edit_payment_part_and_due(self)
        upload_attachment(self)


class TestProposalViews(BaseViewsTest):

    def test_walk(self):
        get_to_page(self, "proposals")
        create_client_and_proposal(self)
        # create_item(self)
        # create_item(self)
        # edit_item(self)
        # edit_payment_due_success(self)
        # edit_payment_due_not_success(self)
        # edit_payment_part_success(self)
        # edit_payment_part_not_success(self)
        # edit_payment_part_and_due(self)
        # delete_item(self)
        # create_or_edit_contract_from_proposal_page(self)
        create_or_edit_contract_from_proposal_page(self)
        get_to_page(self, "clients/edit/1")
        upload_attachment(self)


def get_to_page(summoner, page):
    # get to start page
    summoner.get_login_required_page(url=f"/{page}")
    summoner.assertNotIn("login", summoner.webdriver.current_url, f"{page} page is not loaded")
    summoner.assertIn(page, summoner.webdriver.current_url, f"{page} page is not loaded")


def create_client_and_proposal(summoner):
    # get to form
    summoner.webdriver.find_element(by="id", value="create-client-and-proposal").click()
    summoner.assertIn("/proposals/create", summoner.webdriver.current_url, "Proposal form is not successfully loaded")

    # fill & submit form
    summoner.fill_client_form()
    summoner.fill_proposal_form_work()
    # summoner.fill_proposal_form_buy()

    form = summoner.webdriver.find_element(by="id", value="proposal-form")
    form.submit()
    time.sleep(3)

    # evaluate result of proposal form
    summoner.assertIn("/proposals/edit/", summoner.webdriver.current_url, "Proposal form is not successfully submitted")


def create_item(summoner):
    # get page
    summoner.webdriver.find_element(by="id", value="items-button").click()
    summoner.assertIn("/proposals/items/", summoner.webdriver.current_url, "Items page is not loaded")

    # get count before creating
    count_before = len(summoner.webdriver.find_elements(by="css selector", value="tr"))

    # fill and submit form
    summoner.fill_new_item_form()
    summoner.webdriver.find_element(by="id", value="create_button").click()
    time.sleep(1)

    # evaluate result of create item form
    count_after = len(summoner.webdriver.find_elements(by="css selector", value="tr"))
    summoner.assertNotEquals(count_before, count_after, "Items form have same count of tr elements")

    # back to proposal
    summoner.webdriver.find_element(by="id", value="back_to_proposal_button").click()


def edit_item(summoner):
    # get page
    summoner.webdriver.find_element(by="id", value="edit_items_from_page").click()
    summoner.assertIn("/proposals/items/", summoner.webdriver.current_url, "Items page is not loaded")

    # fill and submit form
    old_data, new_data = summoner.fill_and_submit_edit_item_form()

    # evaluate result of create item form
    summoner.assertNotEquals(old_data, new_data, f"Item's title didn't change {old_data} x {new_data}")

    # back to proposal
    summoner.webdriver.find_element(by="id", value="back_to_proposal_button").click()


def delete_item(summoner):
    # get page
    summoner.webdriver.find_element(by="id", value="items-button").click()
    summoner.assertIn("/proposals/items/", summoner.webdriver.current_url, "Items page is not loaded")

    # get count before creating
    count_before = len(summoner.webdriver.find_elements(by="css selector", value="tr"))

    # perform deletion
    summoner.webdriver.find_element(by="id", value="delete").click()
    summoner.webdriver.find_element(by="id", value="delete-confirm").click()

    # evaluate result of create item form
    count_after = len(summoner.webdriver.find_elements(by="css selector", value="tr"))
    summoner.assertNotEquals(count_before, count_after, "Items form have same count of tr elements")

    # back to proposal
    summoner.webdriver.find_element(by="id", value="back_to_proposal_button").click()


def edit_payment_due_success(summoner):
    element = summoner.webdriver.find_element(by="id", value="payment_due_1")
    old_data = element.get_attribute("value")
    element.send_keys("po dokončení")
    summoner.webdriver.find_element(by="id", value="save_payments").click()
    new_data = summoner.webdriver.find_element(by="id", value="payment_due_1").get_attribute("value")
    summoner.assertNotEquals(old_data, new_data, f"Payment due didn't change {old_data} x {new_data}")


def edit_payment_due_not_success(summoner):
    element = summoner.webdriver.find_element(by="id", value="payment_due_1")
    element.send_keys("-")
    summoner.webdriver.find_element(by="id", value="save_payments").click()
    alert = summoner.webdriver.find_element(by="class name", value="toast-body").text
    summoner.assertIn(alert, "U plateb musí být nastavena splatnost.", f"Payment due alert didn't appear")


def edit_payment_part_success(summoner):
    element = summoner.webdriver.find_element(by="id", value="payment_part_1")
    old_data = element.get_attribute("value")
    element.clear()
    element.send_keys("80")
    summoner.webdriver.find_element(by="id", value="payment_part_2").send_keys("20")
    summoner.webdriver.find_element(by="id", value="save_payments").click()
    new_data = summoner.webdriver.find_element(by="id", value="payment_part_1").get_attribute("value")
    summoner.assertNotEquals(old_data, new_data, f"Payment part didn't change {old_data} x {new_data}")


def edit_payment_part_not_success(summoner):
    element = summoner.webdriver.find_element(by="id", value="payment_part_1")
    element.clear()
    element.send_keys("80")
    summoner.webdriver.find_element(by="id", value="payment_part_2").send_keys("60")
    summoner.webdriver.find_element(by="id", value="save_payments").click()
    alert = summoner.webdriver.find_element(by="class name", value="toast-body").text
    summoner.assertIn(alert, "Souhrn částí plateb se nerovná celku.", f"Payment part alert didn't appear")


def edit_payment_part_and_due(summoner):
    part_1 = summoner.webdriver.find_element(by="id", value="payment_part_1")
    old_data = part_1.get_attribute("value")
    part_1.clear()
    part_1.send_keys("80")
    summoner.webdriver.find_element(by="id", value="payment_part_2").send_keys("20")
    summoner.webdriver.find_element(by="id", value="payment_due_2").send_keys("po dokončení")
    summoner.webdriver.find_element(by="id", value="save_payments").click()
    new_data = summoner.webdriver.find_element(by="id", value="payment_part_1").get_attribute("value")
    summoner.assertNotEquals(old_data, new_data, f"Payment part didn't change {old_data} x {new_data}")


# def show_proposal(summoner):
#     summoner.webdriver.find_element(by="id", value="show-proposal-button").click()
#     time.sleep(5)


def create_or_edit_contract_from_proposal_page(summoner):
    try:
        element = summoner.webdriver.find_element(by="id", value="create-contract-button")
    except NoSuchElementException:
        element = summoner.webdriver.find_element(by="id", value="edit-contract-button")
    element.click()
    summoner.assertIn("/contracts/edit/", summoner.webdriver.current_url, "Contract is not successfully created")
    summoner.webdriver.back()
    summoner.webdriver.refresh()


def upload_attachment(summoner):
    summoner.webdriver.find_element(by="id", value="manage-attachments-button").click()
    summoner.assertIn(
        "/attachments/manage", summoner.webdriver.current_url, "Attachments page is not successfully loaded"
    )

    count_before = len(summoner.webdriver.find_elements(by="css selector", value="tr"))

    summoner.webdriver.find_element(by="id", value="upload-button").click()
    summoner.fill_upload_form()
    summoner.webdriver.find_element(by="id", value="submit-upload-button").click()

    # evaluate result of create item form
    count_after = len(summoner.webdriver.find_elements(by="css selector", value="tr"))
    summoner.assertNotEquals(count_before, count_after, "Attachments have same count of tr elements")


def create_protocol(summoner):
    summoner.webdriver.find_element(by="id", value="manage-attachments-button").click()
    summoner.assertIn(
        "/attachments/manage", summoner.webdriver.current_url, "Attachments page is not successfully loaded"
    )

    count_before = len(summoner.webdriver.find_elements(by="css selector", value="tr"))

    summoner.webdriver.find_element(by="id", value="create-protocol-button").click()
    summoner.assertIn(
        "/contracts/create-protocol", summoner.webdriver.current_url, "Protocol page is not successfully loaded"
    )
