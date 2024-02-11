from playwright.sync_api import sync_playwright
from threading import Thread
import time
from webbrowser import get
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, expect
import time
import string
import json
import requests
import threading
import sys
import os
import random
import hashlib
import configparser

config = configparser.ConfigParser() # 类实例化
api_key = "81A9bf13407f7A92cA3b0f9c25b778c8"
service = "bz"  # 选择您想要的服务，例如：tg 代表 Telegram

# 通过 SMS-Activate API 获取手机号码
# 定义文件路径
path = r'.\\config.ini'

def create_account():
    config.read(path)
    token = config['select']['simtoken']
    #token = ''
    country = config['select']['country']
    operator = config['select']['operator']
    blizzard_country = config['select']['blizzard_country']
    battle_tag = config['select']['battle_tag']

    email_doamin = config['select']['email_doamin']
    proxy = config['select']['proxy']
    isemail = config['select']['isemail']
    #country = 'england'
    #operator = 'ee'
    #blizzard_country = 'GBR'
    #battle_tag = 'SugarPlum'
    #secret_answer1 = 'none'
    #email_doamin = '@outlook.com'
    #proxy = 'Yes'

    # checking if proxy is selected
    if proxy == "Yes":
        #res = requests.get(url='')
        res = requests.get(url=config['select']['proxytoken'])
        print(res.text)

    def random_char(char_num):
        return "".join(random.choice(string.ascii_letters) for _ in range(char_num))


    def read_data(file):
        with open(file, encoding='utf-8') as f:
            data = f.readlines()
            return data

    def delete_file(file):
        file_data = read_data(file)
        # 删除列表中的最后一行，并且循环新列表中的内容，将新的内容写入文件中
        delete_data = file_data.pop()
        delete_data.strip("\n")
        # # 判断原文件是否存在，如果存在，就删除,写文件时，会自动创建文件
        if os.path.exists(file):
            os.remove(file)
            for data in file_data:
                data = data.strip("\n")
                with open(file, mode="a", encoding="utf-8") as f:
                    f.write(data)
                    f.write("\n")
                with open(".\\used.txt", mode="a", encoding="utf-8") as f:
                    f.write(delete_data)
                    f.write("\n")
        return delete_data

    def random_num(charnum1):
        return "".join(random.choice(string.digits) for _ in range(charnum1))

    first_name = [
        "Natha",
        "Narin",
        "Nan",
        "Nahon",
        "Nafeh",
        "Naira",
        "Nina",
        "Myie",
        "Myle",
        "Minh",
        "Musa",
        "Mogan",
        "Monia",
        "Monia",
        "Demris",
        "Delnn",
        "Deler",
        "Deisi",
        "Dera",
        "Decon",
        "Dayan",
        "Aziah",
        "Ayy",
        "Avia",
        "Anti",
        "Aelle",
    ]
    last_name = [
        "MEEZ",
        "BUS",
        "VGHN",
        "PKS",
        "DASON",
        "SANO",
        "NORIS",
        "LOVE",
        "SEE",
        "CURY",
        "PWERS",
        "SCTZ",
        "BAKER",
        "GUAN",
        "PAGE",
        "MUZ",
        "BAL",
        "BBS",
        "TER",
        "GSS",
        "FTZGD",
        "STES",
        "DOYLE",
        "SHERN",
        "SAURS",
        "WSE",
        "CON",
        "GIL",
        "ALO",
        "GRER",
        "PALA",
        "SON",
        "WATS",
        "NUNZ",
        "BOOE",
        "COEZ",
    ]
    random1 = ["01", "02", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    random1 = random.choice(random1)
    random2 = random.randint(10, 29)
    random3 = random.randint(1970, 2002)
    first_name1 = random.choice(first_name).lower()
    last_name1 = random.choice(last_name).lower()
    if isemail == "Yes":
        email1= delete_file(".\\email.txt")
    else:
        email = first_name1 + last_name1 + random_num(1)+random_char(7)
        email1 = email + email_doamin
    password = random_char(7) + random_num(6)

    # start of playwright
    playwright = sync_playwright().start()
    #browser = playwright.firefox.launch(headless=True)
    browser = playwright.firefox.launch(headless=False)
    # launching playwright with proxy
    if proxy == "Yes":
        browser = playwright.firefox.launch(headless=False, proxy={
        "server": res.text,
        "username": "",
        "password": ""
    })

    # launching playwright without proxy

    else:
        browser = playwright.firefox.launch(headless=False)
    context = browser.new_context( viewport={"width": 1000, "height": 800},device_scale_factor=2,)
    #        viewport={"width": 500, "height": 400},
        #device_scale_factor=2,
    page = context.new_page()
    page.set_default_timeout(9000000)
    page.goto("https://account.battle.net/creation/flow/creation-full")
    time.sleep(4)
    page.locator("//select[@id='capture-country']").select_option(blizzard_country)
    time.sleep(2)
    page.type(
        '//input[@name="dob-plain"]',
        str(random1) + str(random2) + str(random3),
        delay=100,
    )
    time.sleep(1)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(1)
    page.type('//input[@name="first-name"]', first_name1, delay=100)
    time.sleep(1)
    page.type('//input[@name="last-name"]', last_name1, delay=100)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(1)
    time.sleep(1)
    page.type('//input[@name="email"]', email1, delay=100)

    # request for 5sim number
    product = "blizzard"

    response = requests.get(
        f"https://sms-activate.ru/stubs/handler_api.php?api_key={api_key}&country=46&action=getNumber&service={service}")
    result = response.text.split(":")
    if result[0] == "ACCESS_NUMBER":
        phone_number_id = result[1]
        phone_number = result[2]
        print(f"Phone number ID: {phone_number_id}")
        print(f"Phone number: {phone_number}")
    else:
        print("Error: Unable to get phone number")
    time.sleep(5)
    page.locator("//input[@id='capture-phone-number']").fill(phone_number)
    time.sleep(1)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(2)

    # start of 5sim sms code request
    sms_code = ""
    time.sleep(5)
    status = "1"  # 设置状态为 1，表示已成功接收短信
    # 等待并获取短信验证码
    while True:
        response = requests.get(
            f"https://sms-activate.ru/stubs/handler_api.php?api_key={api_key}&action=getStatus&id={phone_number_id}")
        result = response.text.split(":")

        if result[0] == "STATUS_OK":
            sms_code = result[1]
            print(f"SMS code: {sms_code}")
            break
        elif result[0] == "STATUS_WAIT_CODE" or result[0] == "STATUS_WAIT_RETRY":
            print("Waiting for SMS code...")
            time.sleep(30)  # 等待 30 秒，然后再次检查状态
        else:
            print("Error: Unable to get SMS code")
            break
    print("end loop")
    page.locator("//input[@id='field-0']").fill(sms_code[0])
    page.locator("//input[@id='field-1']").fill(sms_code[1])
    page.locator("//input[@id='field-2']").fill(sms_code[2])
    page.locator("//input[@id='field-3']").fill(sms_code[3])
    page.locator("//input[@id='field-4']").fill(sms_code[4])
    page.locator("//input[@id='field-5']").fill(sms_code[5])

    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(2)
    # page.evaluate("document.getElementById('capture-opt-in-blizzard-news-special-offers').click();")
    page.evaluate("document.getElementsByClassName('step__checkbox')[1].click();")
    time.sleep(2)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(1)
    page.type('//*[@id="capture-password"]', password, delay=200)
    time.sleep(2)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(2)
    page.locator("//input[@id='capture-battletag']").fill(battle_tag)
    time.sleep(2)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(1)
    page.click('//*[@id="flow-cta-btn"]')
    page.goto("https://account.battle.net/security")
    time.sleep(3)
    page.goto("https://account.battle.net/security")
    #time.sleep(3)
    #page.locator("//input[@id='accountName']").type(email1, delay=100)
    time.sleep(1)
    #page.locator("//input[@id='password']").type(password, delay=100)
    time.sleep(1)
    #page.click("//button[@id='submit']")
    #time.sleep(8)
    #if page.title() == "Battle.net Login":
    #    page.click("//button[@id='submit']")
    #page.click("//a[normalize-space()='Select a Secret Question']")
    time.sleep(10)
    page.goto("https://authenticator-rest-api.bnet-identity.blizzard.net/webjars/swagger-ui/index.html")
    time.sleep(3)
    page.get_by_role("button", name="Authorize").click()
    time.sleep(3)
    page.locator("label").filter(has_text="auth.authenticatorAuthenticator").locator("span").click()
    time.sleep(3)
    page.get_by_label("client_id:").click()
    time.sleep(3)
    page.get_by_label("client_id:").fill("baedda12fe054e4abdfc3ad7bdea970a")
    time.sleep(3)
    page.get_by_role("button", name="Authorize").nth(1).click()
    time.sleep(3)
   # page.locator('//*[@id="question-select"]').select_option("21")
   # time.sleep(1)
    #page.locator('//*[@id="answer"]').type(secret_answer1)
    #time.sleep(1)
   # time.sleep(1)
   # page.click("//button[@id='sqa-submit']")
   # time.sleep(2)

    # out putting accounts to .txt
    data_list = [email1, password, phone_number]
    with open("battlenet_accounts.txt", "a") as f:
        json.dump(data_list, f, indent=5)
        f.write("\n")
        f.close
    time.sleep(50)

    browser.close()


def main():
    acc = input("Accounts to make: ")
    acc1 = int(acc)



    for i  in range(0,acc1):
        t1 = threading.Thread(target=create_account)
        time.sleep(1)


        t1.start()

main()