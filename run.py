from random import randint
from config import url, pasaporte, apellido, ano_de_nacimiento, pais, key_anticapcha
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from sound_play import sound_play
import json
import time
import datetime


def acp_api_send_request(driver, message_type, data={}):
    """ Метод отправки API запроса прямо в плагин
        Например для инициализации API ключа сервиса anti-captcha.com, необходимый для работы плагина
        Работает только на действующей HTML страничке,
        в нашем случае на https://antcpt.com/blank.html
        на страницах вроде about:blank запрос не пройдет
    """
    message = {
        # всегда указывается именно этот получатель API сообщения
        'receiver': 'antiCaptchaPlugin',
        # тип запроса, например setOptions
        'type': message_type,
        # мерджим с дополнительными данными
        **data
    }
    # выполняем JS код на странице
    # а именно отправляем сообщение стандартным методом window.postMessage
    return driver.execute_script("""
    return window.postMessage({});
    """.format(json.dumps(message)))


def t1(maxt=3000):
    time.sleep(randint(100, maxt) / 1000)


def now_date_txt():
    return str(datetime.datetime.now())


if __name__ == '__main__':
    flag = 0
    while True:
        try:
            print(f"Start {now_date_txt()}")
            # Инциируем объект опций для Хрома, чтобы иметь возможность подключить расширение
            options = webdriver.ChromeOptions()
            # Ссылка на CRX или ZIP или ZPI файл плагина, который мы скачали ранее
            options.add_extension('anticaptcha-plugin_v0.3300.crx')

            # Запускаем Браузер (Веб Драйвер Хрома) с указанием места скачивания самого файла драйвера
            driver = webdriver.Chrome('chromedriver.exe', options=options)

            # Переходим на пустую страницу для выполнения API запроса к плагину
            driver.get('https://antcpt.com/blank.html')

            # Устанавливаем API ключ anti-captcha.com
            # замените YOUR-ANTI-CAPTCHA-API-KEY на Ваш шестнадцатиричный ключ, который можно взять тут:
            # https://anti-captcha.com/clients/settings/apisetup
            acp_api_send_request(
                driver,
                'setOptions',
                {'options': {'antiCaptchaApiKey': key_anticapcha,
                             'autoSubmitForm': True,
                             'playSounds': False}}
            )

            # Три секунды паузы чтобы плагин проверил ключ на стороне anti-captcha.com
            time.sleep(3)

            driver.get(url)

            assert "cita" in driver.title
            try:
                driver.find_element_by_id("cookie_action_close_header").click()
            except:
                print("cookie_action_close_header - not found")

            t1()
            select = Select(driver.find_element_by_id("tramite"))
            select.select_by_value("10")
            t1()
            driver.find_element_by_id("btnAceptar").click()
            t1()

            assert "EX-10" in driver.find_element_by_xpath("//b[text()='EX-10']").text
            t1()
            driver.find_element_by_id("btnEntrar").click()
            t1()

            assert "PASAPORTE" in driver.find_element_by_xpath("//label[@for='rdbTipoDocPas']").text
            t1(1000)
            driver.find_element_by_id("txtIdCitado").send_keys(pasaporte)
            t1(1000)
            driver.find_element_by_id("txtDesCitado").send_keys(apellido)
            t1(1000)
            driver.find_element_by_id("txtAnnoCitado").send_keys(ano_de_nacimiento)
            t1(1000)
            select = Select(driver.find_element_by_id("txtPaisNac"))
            select.select_by_visible_text(pais)

            for i in range(120):
                time.sleep(1)
                try:
                    if pasaporte in driver.find_element_by_xpath("//legend[@class='mf-paragraph-header']/following-sibling::span[1]").text:
                        break
                except:
                    pass
            t1()
            assert pasaporte in driver.find_element_by_xpath("//legend[@class='mf-paragraph-header']/following-sibling::span[1]").text
            assert apellido in driver.find_element_by_xpath("//legend[@class='mf-paragraph-header']/following-sibling::span[1]").text
            driver.find_element_by_id("btnEnviar").click()
            t1()

            try:
                txt = driver.find_element_by_xpath("//p[contains(.,'En este momento no hay citas disponibles.En breve, la Oficina pondrá a su disposición nuevas citas.')]").text
                print(f"{now_date_txt()} - Отказ. Сит нет!")
                flag = 4
            except:
                txt = ''
                flag += 1

            if len(txt) == 0:
                print('sound')
                sound_play()
                break
        except:
            flag += 1
            pass
        try:
            driver.close()
        except:
            pass
        if flag>2:
            flag = 0
            tm = randint(300, 900)
            print(f"Пауза {tm // 60} минут {tm % 60} секунд")
            time.sleep(tm)
