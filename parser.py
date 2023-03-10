import time
import sqlalchemy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy.orm import sessionmaker
from settings import DB_URL
from db.models import Task

engine = sqlalchemy.create_engine(DB_URL)
connection = engine.connect()
Session = sessionmaker(bind=engine)

def parser():
    """The function parses the codeforces.com pages"""
    options = webdriver.ChromeOptions()
    options.add_argument('headless') #Turn on the mode without launching Chrome
    options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(options=options)
    browser.get(f"https://codeforces.com/problemset/page/1?order=BY_SOLVED_DESC&locale=ru")
    last_page = browser.find_element(By.XPATH, '//*[@id="pageContent"]/div[3]/ul/li[6]/span/a')
    last_page = int(last_page.text)

    for page_number in range(1, last_page + 1):
        browser.get(f"https://codeforces.com/problemset/page/{page_number}?order=BY_SOLVED_DESC&locale=ru")
        try:
            try:
                for i in range(2, 102):
                    title = browser.find_element(By.XPATH, \
                                                 f'//*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[{i}]/td[2]/div[1]/a')
                    number = browser.find_element(By.XPATH, \
                                                 f'//*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[{i}]/td[1]/a')
                    theme = browser.find_element(By.XPATH, \
                                                  f'//*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[{i}]/td[2]/div[2]')
                    diff = browser.find_element(By.XPATH, \
                                                 f'//*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[{i}]/td[4]/span')
                    solved = browser.find_element(By.XPATH, \
                                                f'//*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[{i}]/td[5]/a')
                    link = browser.find_element(By.XPATH, \
                                                f'//*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[{i}]/td[2]/div[1]/a')

                    session = Session()
                    exists = session.query(Task).filter(Task.number==number.text).scalar() is not None

                    if not exists:
                        data = Task(
                            number=number.text,
                            title=title.text,
                            theme=theme.text,
                            diff=diff.text,
                            solved=solved.text,
                            link=link.get_attribute('href')
                            )
                        session.add(data)
                    session.commit()
                    session.close()
            except ValueError:
                pass
        except NoSuchElementException:
            pass


while True:
    print('Начинаю обновление данных')
    parser()
    print('Данные обновлены')
    time.sleep(3600)