import time
import pytest
from playwright.sync_api import sync_playwright
import requests
from allure import feature, story, title, description, step

@feature('API-тесты')
class TestClassAPI:
    email = "testuser" + str(int(time.time())) + "@abc.com"
    myjson = {
        "name": "Test1",
        "email": email,
        "password": "Test1234!",
        "title": "Mr",
        "birth_date": "1",
        "birth_month": "1",
        "birth_year": "2001",
        "firstname": "Test",
        "lastname": "Test",
        "company": "",
        "address1": "Test",
        "address2": "",
        "country": "United States",
        "zipcode": "Test",
        "state": "Test",
        "city": "Test",
        "mobile_number": "88000000000"
    }


    @story('Создание пользователя')
    def test_api_register_new_user(self):
        with step('Отправка POST-запроса'):
            response = requests.post("https://automationexercise.com/api/createAccount", data = self.myjson)
            assert response.json()['responseCode'] == 201, f"Failed to register new user via API! {response.json()['message']}"
            print(response.json()['message'])

    @story('Поиск продукта')
    def test_api_search_product(self):
        with step('Отправка POST-запроса'):
            response = requests.post("https://automationexercise.com/api/searchProduct", data = {'search_product': "top"})
            assert response.json()['responseCode'] == 200, f"Failed to search product via API! {response.json()['message']}"
            print('Product found!')
            #print('Data: ',response.json()['products'])

    @story('Получение информации о пользователе')
    def test_api_get_user_account_detail_by_email(self):
        with step('Отправка GET-запроса'):
            response = requests.get("https://automationexercise.com/api/getUserDetailByEmail", params = {'email': self.email})
            assert response.json()['responseCode'] == 200, f"Failed to get user account detail by email via API! {response.json()['message']}"
            print('Data received!')
            #print('Data: ', response.json()['user'])

    @story('Обновление информации о пользователе')
    def test_api_update_user_account(self):
        with step('Отправка PUT-запроса'):
            self.myjson['birth_date'] = '29'
            self.myjson['birth_month'] = '4'
            self.myjson['birth_year'] = '2002'
            response = requests.put("https://automationexercise.com/api/updateAccount", data = self.myjson)
            assert response.json()['responseCode'] == 200, f"Failed to update user account via API! {response.json()['message']}"
            print(response.json()['message'])

    @story('Удаление акаунта')
    def test_api_delete_user_account(self):
        with step('Отправка DELETE-запроса'):
            response = requests.delete("https://automationexercise.com/api/deleteAccount", data = {'email': self.email, 'password': "Test1234!"})
            assert response.json()['responseCode'] == 200, f"Failed to delete user account via API! {response.json()['message']}"
            print(response.json()['message'])

@feature('UI-тесты')
class TestClassUI:
    email = "testuser" + str(int(time.time())) + "@gmail.com"
    myjson = {
          "name": "Test1",
          "email": email,
          "password": "Test1234!",
          "firstname": "Test",
          "lastname": "Test",
          "company": "Test",
          "address1": "Test",
          "address2": "Test",
          "zipcode": "Test",
          "state": "Test",
          "city": "Test",
          "mobile_number": "88000000000",
          "search_product": "Top",
          "subject": "Test",
          "text": "Test"
    }

    @pytest.fixture(scope="class")
    def resource_setup(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            yield page
            return

    @story('Создание и удаление пользователя')
    def test_ui_register_new_user(self, resource_setup):
        page = resource_setup
        with step('Переход на главную страницу'):
            page.goto("http://automationexercise.com", timeout=60000)
            assert page.title() == "Automation Exercise", "Invalid page!"

        with step('Переход к разделу регистрации'):
            page.click('#header > div > div > div > div.col-sm-8 > div > ul > li:nth-child(4) > a')
            assert page.text_content(".signup-form h2") == "New User Signup!", "Registration is not available!"

        with step('Переход к форме регистрации'):
            page.fill("#form > div > div > div:nth-child(3) > div > form > input[type=text]:nth-child(2)", self.myjson['name'])
            page.fill("#form > div > div > div:nth-child(3) > div > form > input[type=email]:nth-child(3)", self.myjson['email'])
            page.click("#form > div > div > div:nth-child(3) > div > form > button")
            assert page.text_content("#form > div > div > div > div > h2 > b") == "Enter Account Information", "Failed to proceed with registration!"

        with step('Заполнение формы регистрации'):
            page.click("#id_gender1")
            page.fill("#password", self.myjson['password'])
            page.select_option("#days", '1')
            page.select_option("#months", '1')
            page.select_option("#years", '2001')
            page.click("#newsletter")
            page.click("#optin")
            page.fill("#first_name", self.myjson['firstname'])
            page.fill("#last_name", self.myjson['lastname'])
            page.fill("#company", self.myjson['company'])
            page.fill("#address1", self.myjson['address1'])
            page.fill("#address2", self.myjson['address2'])
            page.select_option("#country", "Canada")
            page.fill("#state", self.myjson['state'])
            page.fill("#city", self.myjson['city'])
            page.fill("#zipcode", self.myjson['zipcode'])
            page.fill("#mobile_number", self.myjson['mobile_number'])
            page.click("#form > div > div > div > div > form > button")
            assert page.text_content("#form > div > div > div > h2 > b") == "Account Created!", "Failed to register!"

        with step('Проверка входа в аккаунт'):
            page.click("#form > div > div > div > div > a")
            assert page.text_content("#header > div > div > div > div.col-sm-8 > div > ul > li:nth-child(10) > a > b") == "Test1", "Invalid user!"

        with step('Удаление аккаунта'):
            page.click("#header > div > div > div > div.col-sm-8 > div > ul > li:nth-child(5) > a")
            assert page.text_content("#form > div > div > div > h2 > b") == "Account Deleted!", "Account could not be deleted!"

        page.click("#form > div > div > div > div > a")
        print("User created and deleted!")

    @story('Добавление продуктов в корзину')
    def test_ui_add_products_in_cart(self, resource_setup):
        page = resource_setup
        with step('Переход на главную страницу'):
            page.goto("http://automationexercise.com", timeout=60000)
            assert page.title() == "Automation Exercise", "Invalid page!"

        with step('Переход на страницу покупок'):
            page.click('#header > div > div > div > div.col-sm-8 > div > ul > li:nth-child(2) > a')
            assert page.text_content("body > section:nth-child(3) > div > div > div.col-sm-9.padding-right > div > h2") == "All Products", "It was not possible to switch to all products!"

        with step('Добавление товаров в корзину'):
            lable1 = page.text_content("body > section:nth-child(3) > div > div > div.col-sm-9.padding-right > div > div:nth-child(3) > div > div.single-products > div.productinfo.text-center > p")
            cost1 = page.text_content("body > section:nth-child(3) > div > div > div.col-sm-9.padding-right > div > div:nth-child(3) > div > div.single-products > div.productinfo.text-center > h2")
            lable2 = page.text_content("body > section:nth-child(3) > div > div > div.col-sm-9.padding-right > div > div:nth-child(4) > div > div.single-products > div.productinfo.text-center > p")
            cost2 = page.text_content("body > section:nth-child(3) > div > div > div.col-sm-9.padding-right > div > div:nth-child(4) > div > div.single-products > div.productinfo.text-center > h2")
            page.click('body > section:nth-child(3) > div > div > div.col-sm-9.padding-right > div > div:nth-child(3) > div > div.single-products > div.productinfo.text-center > a')
            page.click('#cartModal > div > div > div.modal-footer > button')
            page.click('body > section:nth-child(3) > div > div > div.col-sm-9.padding-right > div > div:nth-child(4) > div > div.single-products > div.productinfo.text-center > a')
            page.click('#cartModal > div > div > div.modal-body > p:nth-child(2) > a > u')
            assert page.text_content("#cart_items > div > div.breadcrumbs > ol > li.active") == "Shopping Cart", "The shopping cart is not available!"

        with step('Проверка корзины'):
            assert page.text_content("#product-1 > td.cart_description > h4 > a") == lable1 and page.text_content("#product-2 > td.cart_description > h4 > a") == lable2, "Incorrect products!"
            assert page.text_content("#product-1 > td.cart_price > p") == cost1 and page.text_content("#product-2 > td.cart_price > p") == cost2, "Incorrect price!"
            assert page.text_content("#product-1 > td.cart_quantity > button") == '1' and page.text_content("#product-2 > td.cart_quantity > button") == '1', "Incorrect quantity!"
            assert page.text_content("#product-1 > td.cart_total > p") == cost1 and page.text_content("#product-2 > td.cart_total > p") == cost2, "Incorrect cost!"

        print("Products added to cart!")

    @story('Поиск продуктов')
    def test_ui_search_product(self, resource_setup):
        page = resource_setup
        with step('Переход на главную страницу'):
            page.goto("http://automationexercise.com", timeout=60000)
            assert page.title() == "Automation Exercise", "Invalid page!"

        with step('Переход на страницу покупок'):
            page.click('#header > div > div > div > div.col-sm-8 > div > ul > li:nth-child(2) > a')
            assert page.text_content("body > section:nth-child(3) > div > div > div.col-sm-9.padding-right > div > h2") == "All Products", "It was not possible to switch to all products!"

        with step('Поиск продуктов'):
            page.fill("#search_product", self.myjson['search_product'])
            page.click('#submit_search')
            assert page.text_content("body > section:nth-child(3) > div > div > div.col-sm-9.padding-right > div > h2") == "Searched Products", "The search failed!"

        with step('Проверка поиска'):
            assert "Top" in page.text_content("body > section:nth-child(3) > div > div > div.col-sm-9.padding-right > div > div:nth-child(3) > div > div.single-products > div.productinfo.text-center > p"), "Invalid search result!"

        print("Products added to cart!")

    @story('Отправка обратной связи')
    def test_ui_contact_us_form(self, resource_setup):
        page = resource_setup
        with step('Переход на главную страницу'):
            page.goto("http://automationexercise.com", timeout=60000)
            assert page.title() == "Automation Exercise", "Invalid page!"

        with step('Переход на главную обратной связи'):
            page.click('#header > div > div > div > div.col-sm-8 > div > ul > li:nth-child(8) > a')
            assert page.text_content("#contact-page > div.row > div.col-sm-8 > div > h2") == "Get In Touch", "The feedback form is not available!"

        with step('Заполнение формы обратной связи'):
            page.fill("#contact-us-form > div:nth-child(2) > input", self.myjson['name'])
            page.fill("#contact-us-form > div:nth-child(3) > input", self.myjson['email'])
            page.fill("#contact-us-form > div:nth-child(4) > input", self.myjson['subject'])
            page.fill("#message", self.myjson['text'])
            page.set_input_files("#contact-us-form > div:nth-child(6) > input","README.MD")
            page.on("dialog", lambda dialog: dialog.accept())
            time.sleep(1)
            page.click('#contact-us-form > div:nth-child(7) > input')
            assert page.text_content("#contact-page > div.row > div.col-sm-8 > div > div.status.alert.alert-success") == "Success! Your details have been submitted successfully.", "The feedback form could not be sent!"

        with step('Переход на главную страницу'):
            page.click('#form-section > a > span')
            assert page.title() == "Automation Exercise", "Invalid page!"

        print("Products added to cart!")

    @story('Отправление отзыва на товар')
    def test_ui_add_review_on_product(self, resource_setup):
        page = resource_setup
        with step('Переход на главную страницу'):
            page.goto("http://automationexercise.com", timeout=60000)
            assert page.title() == "Automation Exercise", "Invalid page!"

        with step('Переход на страницу покупок'):
            page.click('#header > div > div > div > div.col-sm-8 > div > ul > li:nth-child(2) > a')
            assert page.text_content("body > section:nth-child(3) > div > div > div.col-sm-9.padding-right > div > h2") == "All Products", "It was not possible to switch to all products!"

        with step('Переход на страницу отзыва о товаре'):
            page.click('body > section:nth-child(3) > div > div > div.col-sm-9.padding-right > div > div:nth-child(3) > div > div.choose > ul > li > a')
            assert page.text_content("body > section > div > div > div.col-sm-9.padding-right > div.category-tab.shop-details-tab > div.col-sm-12 > ul > li > a") == "Write Your Review", "The feedback form is not available!"

        with step('Заполнение отзыва'):
            page.fill("#name", self.myjson['name'])
            page.fill("#email", self.myjson['email'])
            page.fill("#review", self.myjson['text'])
            page.click('#button-review')
            assert page.text_content("#review-section > div > div > span") == "Thank you for your review.", "The review could not be uploaded!"

        print("Products added to cart!")

if __name__ == "__main__":

    print("+ Info: These are automated tests for the site https://www.automationexercise.com\n"
          "+ List of tests:\n"
          "\t|\_ TestClassAP\n"
          "\t|\t\t\_ test_api_register_new_user\n"
          "\t|\t\t\_ test_api_search_product\n"
          "\t|\t\t\_ test_api_get_user_account_detail_by_email\n"
          "\t|\t\t\_ test_api_update_user_account\n"
          "\t|\t\t\_ test_api_delete_user_account\n"
          "\t\_ TestClassUI\n"
          "\t\t\t\_ test_ui_register_new_user\n"
          "\t\t\t\_ test_ui_add_products_in_cart\n"
          "\t\t\t\_ test_ui_search_product\n"
          "\t\t\t\_ test_ui_contact_us_form\n"
          "\t\t\t\_ test_ui_add_review_on_product\n\n"
          "Use pytest to run tests")
