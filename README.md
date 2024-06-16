# Automated Testing for Automation Exercise Website

This project aims to provide automated tests for the website https://www.automationexercise.com using the Allure framework. The tests cover various scenarios such as registration, cart, order, search, etc.

## Tools

- Python 3.10+
- Libraries:
  - pytest
  - requests
  - playwright
  - allure

## Functionality

This is a program with automated tests: 5 tests for the API and 5 tests for the UI for different scenarios.

## Test List

- API Tests:
  - `test_api_register_new_user` - A test that checks the functionality of the new user registration function via the API
  - `test_api_search_product` - A test that checks the functionality of the product search function via the API
  - `test_api_get_user_account_detail_by_email` - A test that checks the functionality of the function for obtaining information about the user by specifying an email via the API
  - `test_api_update_user_account` - A test that checks the functionality of updating user information via the API
  - `test_api_delete_user_account` - A test that checks the functionality of the user account deletion function via the API
- UI Tests:
  - `test_ui_register_new_user` - A test that checks the functionality of the new user registration function via the UI
  - `test_ui_add_products_in_cart` - A test that checks the functionality of the function of adding products to the cart via the UI
  - `test_ui_search_product` - A test that checks the functionality of the product search function via the UI
  - `test_ui_contact_us_form` - A test that checks the functionality of the function of sending a feedback form via the UI
  - `test_ui_add_review_on_product` - A test that checks the functionality of the function of sending a review for a product through the UI
 
## Installation

### First Option:
1. Clone the project from the repository using `git clone https://github.com/K4vabanga/PT_START_INT-12.git`
2. Install Allure
3. Install all required libraries using `pip install requirements.txt`
4. Run the test using `pytest --alluredir=/path/to/allure_reports_dir main.py`
5. Run the Allure report using `allure serve /path/to/allure_reports_dir`

### Second Option:
1. Clone the project from the repository using `git clone https://github.com/K4vabanga/PT_START_INT-12.git`
2. Install Docker
3. Create a Docker image using `docker build /path/to/repository`
4. Run the Docker container using `docker run -p 5555:5555 <image_name>`
5. The report can be viewed at `http://localhost:5555`

## Additional Information

Feel free to contribute to this project by submitting pull requests or opening issues.

Happy testing!
