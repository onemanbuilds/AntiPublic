from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from threading import Thread,Lock
from random import choice
from colorama import init,Fore,Style
from os import name,system
from sys import stdout
from concurrent.futures import ThreadPoolExecutor
from time import sleep

class Main:
    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title_name:str):
        system("title {0}".format(title_name))

    def GetRandomUserAgent(self):
        useragents = self.ReadFile('useragents.txt','r')
        return choice(useragents)

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('proxies.txt','r')
        return choice(proxies_file)

    def ReadFile(self,filename,method):
        with open(filename,method,encoding='utf8') as f:
            content = [line.strip('\n') for line in f]
            return content

    def TitleUpdate(self):
        while True:
            self.SetTitle(f'One Man Builds AntiPublic Tool Selenium ^| HITS: {self.hits} ^| BADS: {self.bads} ^| RETRIES: {self.retries}')
            sleep(0.1)
          
    def __init__(self):
        init(convert=True)
        self.hits = 0
        self.bads = 0
        self.retries = 0
        self.lock = Lock()
        self.clear()
        self.SetTitle('One Man Builds AntiPublic Tool Selenium')
        self.title = Style.BRIGHT+Fore.RED+"""
                                  ╔══════════════════════════════════════════════════╗          
                                               ╔═╗╔╗╔╔╦╗╦  ╔═╗╦ ╦╔╗ ╦  ╦╔═╗
                                               ╠═╣║║║ ║ ║  ╠═╝║ ║╠╩╗║  ║║  
                                               ╩ ╩╝╚╝ ╩ ╩  ╩  ╚═╝╚═╝╩═╝╩╚═╝
                                  ╚══════════════════════════════════════════════════╝
        """
        print(self.title)
        self.use_proxy = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Proxy ['+Fore.RED+'0'+Fore.CYAN+']Proxyless: '))
        self.browser_amount = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Browser amount: '))
        self.max_wait = float(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Max Wait For Elements To Load: '))
        self.max_wait_for_good = float(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Max Wait For Good Results (seconds): '))
        print('')

    def CheckLeak(self,combo):
        try:
            options = Options()

            options.add_argument(f'--user-agent={self.GetRandomUserAgent()}')
            options.add_argument('no-sadbox')
            options.add_argument('--log-level=3')
            options.add_argument('--lang=en')
            options.add_argument('--headless')

            if self.use_proxy == 1:
                options.add_argument('--proxy-server=http://{0}'.format(self.GetRandomProxy()))

            #Removes navigator.webdriver flag
            options.add_experimental_option('excludeSwitches', ['enable-logging','enable-automation'])
            
            # For older ChromeDriver under version 79.0.3945.16
            options.add_experimental_option('useAutomationExtension', False)

            options.add_argument("window-size=1280,800")

            #For ChromeDriver version 79.0.3945.16 or over
            options.add_argument('--disable-blink-features=AutomationControlled')
            driver = webdriver.Chrome(options=options)

            email = combo

            if len(email.split(':')) > 1:
                email = email.split(':')[0]

            driver.get('https://haveibeenpwned.com/')

            element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="Account"]'))
            WebDriverWait(driver, self.max_wait).until(element_present).send_keys(email)
            pwned_button_elem_present = EC.element_to_be_clickable((By.XPATH, '//*[@id="searchPwnage"]'))
            WebDriverWait(driver, self.max_wait).until(pwned_button_elem_present).click()

            try:
                bad_elem_present = EC.visibility_of_element_located((By.XPATH,'/html/body/div[4]/div/div/div[1]'))
                result_bad_elem_present = WebDriverWait(driver, self.max_wait_for_good).until(bad_elem_present)

                if result_bad_elem_present != None:
                    self.PrintText(Fore.RED,Fore.CYAN,'LEAKED',combo)
                    with open('bads.txt','a',encoding='utf8') as f:
                        f.write(combo+'\n')
                    self.bads += 1
            except TimeoutException:
                self.PrintText(Fore.CYAN,Fore.RED,'GOOD',combo)
                with open('hits.txt','a',encoding='utf8') as f:
                    f.write(combo+'\n')
                self.hits += 1
        except:
            self.retries += 1
            driver.quit()
            self.CheckLeak(email)
        finally:
            driver.quit()

    def Start(self):
        Thread(target=self.TitleUpdate).start()
        combos = self.ReadFile('combos.txt','r')
        with ThreadPoolExecutor(max_workers=self.browser_amount) as ex:
            for combo in combos:
                ex.submit(self.CheckLeak,combo)

if __name__ == "__main__":
    main = Main()
    main.Start()