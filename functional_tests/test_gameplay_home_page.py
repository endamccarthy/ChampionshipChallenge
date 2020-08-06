# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.urls import reverse
# from selenium import webdriver


# class TestUserIsLoggedOut(StaticLiveServerTestCase):

#   def setUp(self):
#     self.browser = webdriver.Chrome('functional_tests/chromedriver')

#   def tearDown(self):
#     self.browser.close()

#   def test_login_and_register_buttons_are_displayed_correctly(self):
#     self.browser.get(self.live_server_url)
#     buttons_displayed = True
#     login_buttons = self.browser.find_elements_by_link_text('Login')
#     register_buttons = self.browser.find_elements_by_link_text('Register')
#     if (len(login_buttons) != 2 or len(register_buttons) != 2):
#       buttons_displayed = False
#     self.assertTrue(buttons_displayed)

#   def test_register_button_redirects_to_register_page(self):
#     self.browser.get(self.live_server_url)
#     register_url = self.live_server_url + reverse('account_signup')
#     register_buttons = self.browser.find_elements_by_link_text('Register')

#     if len(register_buttons) > 0:
#       register_buttons[0].click()
#       self.assertEqual(
#           self.browser.current_url,
#           register_url
#       )
#     else:
#       self.fail("Register button not found.")
