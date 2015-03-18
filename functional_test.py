from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

  def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    self.browser.quit()

  def test_can_start_a_list_and_retrieve_it_later(self):
    # Samson checks out a new to-do manager he has heard of.
    # He checks application homepage.
    self.browser.get('http://localhost:8000')

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

    # When he hits enter, the page updates, and now the page lists "1: Buy skate 
    # boots" as an item in a todo list.
    inputbox.send_keys(Keys.ENTER)

    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn('1: Buy skate boots', [row.text for row in rows])

    # There is still a text box inviting him to add another item. He enters
    # "Attach plates to skates".
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Attach plates to skates')
    inputbox.send_keys(Keys.ENTER)

    # The page updates again, and now shows both items on his list.
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn('1: Buy skate boots', [row.text for row in rows])    
    self.assertIn('2: Attach plates to skates', [row.text for row in rows])

    # Samson wonders whether the site will remember his list. Then he sees that 
    # it has generated a unique URL for him -- there is some explanatory text to
    # that effect.
    self.fail('Finish the test!')
    
    # He visits the URL - his to-do list is still there.

    # Satisfied, he goes back to sleep.

if __name__ == '__main__':
  unittest.main(warnings='ignore')