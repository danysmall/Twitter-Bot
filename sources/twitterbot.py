"""Main file."""
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType

from subprocess import CREATE_NO_WINDOW
from time import sleep
import pickle


class TwitterBot:
    PROXY_FILE = '.\\assets\\proxy.pkl'
    PATH = '.\\accounts\\'
    WAIT_FOR_ELEMENT_S = 10
    SITE_MAIN_URL = 'https://twitter.com/'
    MAIN_URL_LEN = len(SITE_MAIN_URL)

    def __init__(self, username, proxy, headless):
        # Setup main page
        self._main_page = 'https://twitter.com'
        self._home_url = 'https://twitter.com/home'
        self._proxy_list = dict()
        self._username = username
        self._sleep_timer = 1
        self._driver = None
        self._enable_proxy = False

        self.load_proxy_list()
        if proxy.find('127.0.0.1:80') == -1:
            self._enable_proxy = True
        if self.is_saved_proxy(username):
            # Setup proxylist
            self._proxy = Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': self._proxy_list[username],
                'ftpProxy': self._proxy_list[username],
                'sslProxy': self._proxy_list[username],
                'noProxy': ''})
        else:
            self._proxy = Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': proxy,
                'ftpProxy': proxy,
                'sslProxy': proxy,
                'noProxy': ''})
            self._proxy_list[username] = proxy
        #
        # self._capabilities = webdriver.DesiredCapabilities.CHROME
        # self._proxy.add_to_capabilities(self._capabilities)

        # Setup services
        self._service = Service('chromedriver.exe')
        self._service.creationflags = CREATE_NO_WINDOW

        # Setup options
        self._options = Options()
        self._options.add_argument('window-size=1440,900')
        self._options.add_argument("--log-level=3")
        if headless:
            self._options.add_argument('--headless')

        self._action_buttons = None

    def start_browser(self):
        # Setup browser
        if self._enable_proxy:
            self._driver = webdriver.Chrome(
                service=self._service,
                options=self._options,
                desired_capabilities=self._capabilities)
        else:
            self._driver = webdriver.Chrome(
                service=self._service,
                options=self._options)

        self._driver.implicitly_wait(TwitterBot.WAIT_FOR_ELEMENT_S)

    def load_proxy_list(self):
        try:
            self._proxy_list = pickle.load(open(TwitterBot.PROXY_FILE, 'rb'))
        except FileNotFoundError:
            pass

    def is_saved_proxy(self, username) -> bool:
        if username in self._proxy_list:
            return True
        return False

    @staticmethod
    def send_logs(log_message: str):
        print(log_message)

    def _get_main_page(self):
        self._driver.get(self._main_page)

    def is_user_logged(self: 'TwitterBot') -> bool:
        try:
            self._driver.find_element(By.CLASS_NAME, 'r-usiww2')
            if self._driver.current_url == self._home_url:
                return True
            return False
        except selenium.common.exceptions.NoSuchElementException:
            return False

    def login_new_user(self: 'TwitterBot') -> None:
        self.start_browser()
        self._driver.get(self._main_page)
        while not self.is_user_logged():
            sleep(self._sleep_timer)
        self._save_cookies(self._username)

    def login_user(self: 'TwitterBot', cookies_file: str) -> bool:
        self._driver.get(self._main_page)
        try:
            self._load_cookies(cookies_file)
            self._driver.get(self._home_url)
            self._driver.quit()
            return True
        except FileNotFoundError:
            self._driver.quit()
            return False

    def _save_cookies(self: 'TwitterBot', filename: str) -> None:
        pickle.dump(self._driver.get_cookies(), open(f'{TwitterBot.PATH}{filename}', 'wb'))

    def _load_cookies(self: 'TwitterBot', filename: str) -> None:
        cookies = pickle.load(open(filename, 'rb'))
        for cookie in cookies:
            self._driver.add_cookie(cookie)

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
                TwitterBot.send_logs('No such element')
                sleep(self._sleep_timer)
            except IndexError:
                TwitterBot.send_logs('Index Error')
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
                TwitterBot.send_logs('Cant find action pannel')
                sleep(self._sleep_timer)

    def _like_tweet(self, link):
        if self._action_buttons is None:
            self._wait_for_action_pannel(link)
        elif not self._driver.current_url == link:
            self._wait_for_action_pannel(link)

        self._action_buttons[2].click()
        TwitterBot.send_logs('Like was clicked')
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
        TwitterBot.send_logs('Retweet was clicked')
        sleep(self._sleep_timer)

    def _reply(self, link, text):
        if not self._driver.current_url == link:
            self._driver.get(link)

        while True:
            try:
                editor = self._driver.find_element(
                    By.CLASS_NAME, 'DraftEditor-editorContainer')
                TwitterBot.send_logs('Editor area found')
                break
            except selenium.common.exceptions.NoSuchElementException:
                TwitterBot.send_logs('Cant find editor area')
                sleep(self._sleep_timer)

        editor.click()
        sleep(self._sleep_timer)

        field = editor.find_element(By.TAG_NAME, 'span')
        field.send_keys(text)
        sleep(self._sleep_timer)

        self._driver.find_element(
            By.XPATH, '//*[@data-testid="tweetButtonInline"]').click()
        sleep(self._sleep_timer)

        TwitterBot.send_logs('Reply sended')

    def login_forever(self):
        self.start_browser()
        if self._driver is not None:
            self._driver.get(self._main_page)
            self._load_cookies(self._username)
            self._driver.get(self._home_url)
            while TwitterBot.is_driver_alive(self._driver):
                sleep(1)

    @staticmethod
    def is_driver_alive(driver: 'webdriver.Chrome') -> bool:
        try:
            driver.title
            return True
        except Exception:
            return False

    @staticmethod
    def get_profile_link(full_link: str) -> str:
        return full_link[:full_link.find('/', TwitterBot.MAIN_URL_LEN + 1)]

    def start(
        self,
        url_of_tweet: str,
        reply_message: str,
        like: bool,
        subscribe: bool,
        retweet: bool,
        comment: bool
    ) -> None:

        self.start_browser()
        self._get_main_page()
        self.login_user(self._username)

        if like:
            self._like_tweet(url_of_tweet)
        if subscribe:
            pass
        if retweet:
            self._retweet_tweet(url_of_tweet)
        if comment:
            self._reply(url_of_tweet, reply_message)

        print('Work Done')

    def stop(self: 'TwitterBot') -> None:
        pickle.dump(self._proxy_list, open(TwitterBot.PROXY_FILE, 'wb'))
        if self._driver is not None:
            self._driver.quit()


if __name__ == '__main__':
    tweet_link = 'https://twitter.com/_jessicasachs/status/1515855226598797321'
    message = 'Oh, nice work man'
    userbot = TwitterBot('danysmall', '128.0.0.1:80')
    try:
        userbot.start_browser()
        print(TwitterBot.get_profile_link(tweet_link))
    # userbot.start(tweet_link, message)
    finally:
        userbot.stop()

    # userbot.login_new_user('danysmall3.pkl')
    # userbot.stop()
