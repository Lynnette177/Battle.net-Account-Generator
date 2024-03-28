from playwright.sync_api import sync_playwright
import re
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
import base64

config = configparser.ConfigParser()  # 类实例化
playwright = sync_playwright().start()
# 定义文件路径
path = r'.\\config.ini'


def new_auth(SSO):
    url = 'https://oauth.battle.net/oauth/sso'
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8'
    }
    data = {
        'client_id': 'baedda12fe054e4abdfc3ad7bdea970a',
        'grant_type': 'client_sso',
        'scope': 'auth.authenticator',
        'token': SSO
    }
    response = requests.post(url, headers=headers, data=data)
    print(response.text)
    jsondata = response.json()
    beartoken = jsondata["access_token"]
    print(beartoken)
    url = 'https://authenticator-rest-api.bnet-identity.blizzard.net/v1/authenticator'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + beartoken
    }

    response = requests.post(url, headers=headers)
    jsondata = response.json()
    original_bytes = bytes.fromhex(jsondata["deviceSecret"])
    # 使用 base32 进行编码
    encoded_bytes = base64.b32encode(original_bytes)
    encoded_string = encoded_bytes.decode('utf-8')
    return f'序列号:{jsondata["serial"]},还原码:{jsondata["restoreCode"]},40位设备密钥:{jsondata["deviceSecret"]},用作TOTP8位设备密钥base32编码种子:{encoded_string}'


def create_account():
    config.read(path)
    token = config['select']['simtoken']
    # token = ''
    country = config['select']['country']
    operator = config['select']['operator']
    blizzard_country = config['select']['blizzard_country']
    battle_tag = config['select']['battle_tag']

    email_doamin = config['select']['email_doamin']
    proxy = config['select']['proxy']
    isemail = config['select']['isemail']
    # country = 'england'
    # operator = 'ee'
    # blizzard_country = 'GBR'
    # battle_tag = 'SugarPlum'
    # secret_answer1 = 'none'
    # email_doamin = '@outlook.com'
    # proxy = 'Yes'

    # checking if proxy is selected
    if proxy == "Yes":
        # res = requests.get(url='')
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
        email1 = delete_file(".\\email.txt")
    else:
        email = first_name1 + last_name1 + random_num(1) + random_char(7)
        email1 = email + email_doamin
    password = random_char(7) + random_num(6)

    # start of playwright
    # browser = playwright.firefox.launch(headless=True)
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
    context = browser.new_context(viewport={"width": 500, "height": 400}, device_scale_factor=2, )
    #        viewport={"width": 500, "height": 400},
    # device_scale_factor=2,
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
    page.type('//input[@name="first-name"]', first_name1, delay=10)
    time.sleep(1)
    page.type('//input[@name="last-name"]', last_name1, delay=10)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(1)
    time.sleep(1)
    page.type('//input[@name="email"]', email1, delay=10)

    # request for 5sim number
    product = "blizzard"

    headers = {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
    }
    while True:
        try:
            response = requests.get(
                'https://5sim.net/v1/user/buy/activation/' + country + '/' + operator + '/' + product, headers=headers)
            response.close()
            print(response.text)
            break
        except:
            time.sleep(1)
    time.sleep(1)
    data = json.loads(response.text)
    id = data["id"]
    phone_number = data["phone"]
    time.sleep(5)
    page.locator("//input[@id='capture-phone-number']").fill(phone_number)
    time.sleep(1)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(2)

    # checking if "phone number in use" pops up
    error = page.content()
    check_message = "Phone number is already in use"
    if check_message in error:
        time.sleep(10)
        requests.get("https://5sim.net/v1/user/cancel/" + str(id), headers=headers)
        time.sleep(2)
        browser.close()
        t1 = threading.Thread(target=create_account)
        t1.start()

    # start of 5sim sms code request
    sms_code = ""
    time.sleep(5)
    sms_code = ""
    while True:
        try:
            print("Try request.")
            response1 = requests.get('https://5sim.net/v1/user/check/' + str(id), headers=headers)
            response.close()
            time.sleep(10)
            print("requested.")
            data1 = json.loads(response1.text)
            tryforecancel = 0
            if data1["status"] == "RECEIVED":
                # page.click("//a[@id='resend-sms-verification']")
                time.sleep(5)
                print("Recieved,but not get sms")
                if data1["sms"]:
                    sms_code = data1["sms"][0]["code"]
                    time.sleep(5)
                    print("Recieved and break.")
                    break
                tryforecancel += 1
                if tryforecancel == 20:
                    requests.post("https://5sim.net/v1/user/cancel/" + str(id), headers=headers)
                    response.close()
                    browser.close()
                    return 0
            elif data1["status"] == "PENDING":
                # page.click("//a[@id='resend-sms-verification']")
                time.sleep(5)
                print("SMS Code not received yet")
            else:
                requests.post("https://5sim.net/v1/user/cancel/" + str(id), headers=headers)
                response.close()
                time.sleep(10)
                print("wanna cancel")
        except:
            time.sleep(1)
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
    page.type('//*[@id="capture-password"]', password, delay=10)
    time.sleep(2)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(5)
    page.locator("//input[@id='capture-battletag']").fill(battle_tag)
    time.sleep(2)
    page.click('//*[@id="flow-form-submit-btn"]')
    time.sleep(1)
    page.click('//*[@id="flow-cta-btn"]')
    time.sleep(3)
    page.goto('https://account.battle.net/login/en/?ref=localhost')
    time.sleep(2)
    getssourl = page.url
    print(getssourl)
    pattern = r"ST=([^&]+)"
    match = re.search(pattern, getssourl)
    extracted_content = match.group(1)
    print("SSO:", extracted_content)
    authenticator_info = new_auth(extracted_content)
    accstr = f'账号:{email1},密码:{password},手机号：{phone_number},{authenticator_info}'
    with open("battlenet_accounts.txt", "a") as f:
        f.write(accstr + "\n")
        f.close()
    browser.close()


def main():
    acc = input("Accounts to make: ")
    acc1 = int(acc)
    for i in range(0, acc1):
        create_account()
        time.sleep(1)


main()
