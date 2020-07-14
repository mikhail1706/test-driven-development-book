from django.core import mail
from selenium.webdriver.common.keys import Keys
import os
import poplib
import re
import time

from .base import FunctionalTest

SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    def wait_for_email(self, test_email, subject):
        '''ожидать электронное сообщение'''
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body
        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.mail.gmail.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['YAHOO_PASSWORD'])
            while time.time() - start < 60:
                # получить 10 самых новых сообщений
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        '''тест: можно получить ссылку по почте для регистрации'''
        # Эдит заходит на офигительный сайт суперсписков и впервые
        # замечает раздел "войти" в навигационной панели
        # Он говорит ей ввести свой адрес электронной почты, что она и делает
        if self.staging_server:
            test_email = 'mihailgumen@gmail.com'
        else:
            test_email = 'edith@example.com'

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)
        # Появляется сообщение, которое говорит, что ей на почту
        # было выслано электронное письмо
        # Появляется сообщение, которое говорит Эдит, что ей на почту
        # было выслано электронное письмо

        # self.wait_for(lambda: self.assertIn(
        #     'Check your email',
        #     self.browser.find_element_by_tag_name('body').text
        # ))
        # Эдит проверяет свою почту и находит сообщение

        body = self.wait_for_email(test_email, SUBJECT)

        # Оно содержит ссылку на url-адрес
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)

        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        # Эдит нажимает на ссылку
        self.browser.get(url)
        # Она зарегистрирована в системе!
        self.wait_to_be_logged_in(email=test_email)

        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(test_email, navbar.text)

        # Теперь она выходит из системы
        self.browser.find_element_by_link_text('Log out').click()
        # Она вышла из системы
        self.wait_to_be_logged_out(email=test_email)
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(test_email, navbar.text)
