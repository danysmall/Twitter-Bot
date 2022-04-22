"""Main file."""
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from time import sleep
import pickle


class TwitterBot():

    def __init__(self):
        # Setup main page
        self._main_page = 'https://twitter.com'
        self._home_url = 'https://twitter.com/home'
        self._sleep_timer = 1

        # Setup services
        self._service = Service('chromedriver.exe')

        # Setup options
        self._options = Options()
        self._options.add_argument('window-size=1440,900')
        # self._options.add_argument('--headless')

        # Setup browser
        self._driver = webdriver.Chrome(
            service=self._service,
            options=self._options)

        self._action_buttons = None

    def _send_logs(self, message: str):
        print(message)

    def _get_main_page(self):
        self._driver.get(self._main_page)

    def _wait_for_login(self):
        try:
            cookies = pickle.load(open('cookies.pkl', 'rb'))
            for cookie in cookies:
                self._driver.add_cookie(cookie)
            self._driver.get(self._home_url)
            self._send_logs('Login was successful')
            return
        except FileNotFoundError:
            pass

        while True:
            try:
                self._driver.find_element(By.CLASS_NAME, 'r-usiww2')
                if self._driver.current_url == self._home_url:
                    self._send_logs('Login was successful')
                    break
                else:
                    self._send_logs('Waiting for login...')
                    sleep(self._sleep_timer)
            except selenium.common.exceptions.NoSuchElementException:
                self._send_logs('Waiting for login...')
                sleep(self._sleep_timer)

    def _save_cookies(self):
        pickle.dump(self._driver.get_cookies(), open('cookies.pkl', 'wb'))

    def _wait_for_action_pannel(self, link):
        # Goto link of the tweet
        self._driver.get(link)

        while True:
            try:
                tweet_panel = self._driver.find_elements(
                    By.CLASS_NAME, 'r-1oszu61')
                action_pannel = tweet_panel[1]
                break
            except selenium.common.exceptions.NoSuchElementException:
                self._send_logs('No such element')
                sleep(self._sleep_timer)
            except IndexError:
                self._send_logs('Index Error')
                sleep(self._sleep_timer)

        while True:
            try:
                buttons = action_pannel.find_elements(
                    By.CLASS_NAME, 'r-bztko3')
                if len(buttons) == 4:
                    self._action_buttons = buttons
                    return
                print(len(buttons))
                sleep(self._sleep_timer)
            except selenium.common.exceptions.NoSuchElementException:
                self._send_logs('Cant find action pannel')
                sleep(self._sleep_timer)

    def _like_tweet(self, link):
        if self._action_buttons is None:
            self._wait_for_action_pannel(link)
        elif not self._driver.current_url == link:
            self._wait_for_action_pannel(link)

        self._action_buttons[2].click()
        self._send_logs('Like was clicked')
        sleep(self._sleep_timer)

    def _retweet_tweet(self, link):
        if self._action_buttons is None:
            self._wait_for_action_pannel(link)
        elif not self._driver.current_url == link:
            self._wait_for_action_pannel(link)

        self._action_buttons[1].click()
        sleep(self._sleep_timer)

        retweet_btn = self._driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div/div[1]/div[2]/'
            + 'div/div/div/div[2]/div[3]/div/div/div/div')
        retweet_btn.click()
        self._send_logs('Retweet was clicked')
        sleep(self._sleep_timer)

    def _reply(self, link, text):
        if not self._driver.current_url == link:
            self._driver.get(link)

        while True:
            try:
                editor = self._driver.find_element(
                    By.CLASS_NAME, 'DraftEditor-editorContainer')
                self._send_logs('Editor area found')
                break
            except selenium.common.exceptions.NoSuchElementException:
                self._send_logs('Cant find editor area')
                sleep(self._sleep_timer)

        editor.click()
        sleep(self._sleep_timer)

        field = editor.find_element(By.TAG_NAME, 'span')
        field.send_keys(text)
        sleep(self._sleep_timer)

        self._driver.find_element(
            By.XPATH, '//*[@data-testid="tweetButtonInline"]').click()
        sleep(self._sleep_timer)

        self._send_logs('Reply sended')

    def start(self, tweet_link):
        self._get_main_page()
        self._wait_for_login()
        self._save_cookies()
        self._like_tweet(tweet_link)
        self._retweet_tweet(tweet_link)
        self._reply(tweet_link, 'Oh, nice work man')
        sleep(5)
        self._driver.quit()


if __name__ == '__main__':
    tweet_link = 'https://twitter.com/_jessicasachs/status/1515855226598797321'
    userbot = TwitterBot()
    userbot.start(tweet_link)
