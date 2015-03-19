from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])   

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Samson checks out a new to-do manager he has heard of.
        # He checks application homepage.
        self.browser.get(self.live_server_url)

        # He sees the browser title and header mentions to-dos.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item right away.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
        inputbox.get_attribute('placeholder'),
        'Enter a to-do item'
        )

        # He types "Buy skate boots" into a text box.
        inputbox.send_keys('Buy skate boots')

        # When he hits enter, the page updates, and now the page lists "1: Buy
        # skate boots" as an item in a todo list.
        inputbox.send_keys(Keys.ENTER)
        samson_list_url = self.browser.current_url
        self.assertRegex(samson_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy skate boots')

        # There is still a text box inviting him to add another item. He enters
        # "Attach plates to skates".
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Attach plates to skates')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on his list.
        self.check_for_row_in_list_table('1: Buy skate boots')
        self.check_for_row_in_list_table('2: Attach plates to skates')

        # Now a new user, Delilah, cines along to the site.

        ## We use a new browser session to make sure that no information of 
        ## Samson's is coming through cookies.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Delilah visits the home page. There is no sign of Sampson's list.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy skate boots', page_text)
        self.assertNotIn('Attach plates', page_text)    

        # Delilah starts a new list by entering an item. She is more dangerous 
        # than Samson.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy clippers')
        inputbox.send_keys(Keys.ENTER)

        # Delilah gets her own unique URL
        delilah_list_url = self.browser.current_url
        self.assertRegex(delilah_list_url, '/lists/.+')
        self.assertNotEqual(delilah_list_url, samson_list_url)

        # Again, there is no trace of Samson's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy skate boots', page_text)
        self.assertIn('Buy clippers', page_text)  

        # Satisfied, they both go back to sleep.

    def test_layout_and_styling(self):
        # Samson goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
        inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
            )

        # He starts a new list and sees that it is centered there as well
        inputbox.send_keys('testing/n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
        inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
            )