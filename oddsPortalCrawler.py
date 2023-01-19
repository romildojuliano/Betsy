from constants import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
from arb import Arbitrage
import time
from typing import List
import pandas as pd
from telebot import TeleBot
from telebot.async_telebot import AsyncTeleBot

API_KEY = "5539887723:AAEKKIZipyepZjP7d_-LpOqpel36rQxU8dE"

# async_bot = AsyncTeleBot(API_KEY)
bot = TeleBot(API_KEY)
df = pd.DataFrame()

class WebCrawlerOddsPortal:
    driver: webdriver
    available_games: list
    current_game: str

    def __init__(self) -> None:
        try:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
            self.driver.get("https://www.oddsportal.com/")
            assert self.login_oddsPortal() == True
        except AssertionError:
            print("Ocorreu um erro ao realizar o login no OddsPortal")

    def retrieve_bet_houses_info_from_spec_game(self, parsed_text: List[str]) -> pd.DataFrame:
        sites = dict()
        inc = 0
        try:
            while True:
                casa_aposta, odd_a, empate, odd_b, payout = parsed_text[5+inc:10+inc]
                casa_aposta = casa_aposta.lower()

                if casa_aposta in CASAS_DE_APOSTA_BR and payout != '-':
                    sites[casa_aposta] = {
                        "Odd_a":    float(odd_a),
                        "Empate":   float(empate),
                        "Odd_b":    float(odd_b),
                        "Payout":   payout
                    }
                inc += 5 
        except:
            pass
        
        # print("Sites obtidos: ", sites)
        return pd.DataFrame(sites).T

    def retrieve_game_parsed_text(self, url):
        webElement = None
        
        # print("URL atual: {}".format(url))
        try:
            self.driver.get(url)
        except:
            pass

        webElement = None
        while webElement is None:
            try:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "odds-data-table")))
                webElement = self.driver.execute_script('return document.getElementById("odds-data-table").outerHTML')
            except TimeoutException:
                pass
            except WebDriverException:
                return pd.DataFrame()
        

        self.current_game = self.driver.execute_script('return document.title')
        print(self.current_game)
        
        assert isinstance(webElement, str)
        
        SoupElement = BeautifulSoup(webElement, 'html.parser')
        raw_text = [text for text in SoupElement.stripped_strings]
        # print(raw_text)

        return self.retrieve_bet_houses_info_from_spec_game(raw_text)

    def login_oddsPortal(self) -> bool:

        try:
            # Continua tentando executar o programa até o fim
            
            while True:
                try:
                    self.driver.execute_script('document.getElementsByClassName("inline-btn-2 r button-dark")[0].click()')
                    time.sleep(2)
                    break
                except:
                    pass
            
            # Continua tentando fazer o login até conseguir
            
            while self.driver.current_url == "https://www.oddsportal.com/login/":
                try:
                    time.sleep(5)
                    self.driver.find_element(By.ID, "login-username1").send_keys("picaxota2")
                    self.driver.find_element(By.ID, "login-password1").send_keys("123456")
                    self.driver.execute_script("document.getElementsByClassName('inline-btn-2')[2].click()")
                except:
                    pass

            print("O login foi realizado com sucesso")
            return True
        except:
            print("Ocorreu um erro ao executar o login")
            return False

    def operate():

        pass
    
    def crawl(self, list_of_websites: List[str], verbose: bool):
        for link in list_of_websites:
            suburl = link[26:]
            available_games = list()
            print("Site atual: {}\tSite desejado: {}".format(self.driver.current_url, link))
            try:
                while self.driver.current_url != link:
                    try:
                        self.driver.get(link)
                    except:
                        pass
            except WebDriverException:
                pass
            
            webElement = None
            while webElement == None:
                try:
                    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "tournamentTable")))
                    webElement = self.driver.execute_script('return document.getElementById("tournamentTable").outerHTML')
                except TimeoutException:
                    pass

            try:
                assert isinstance(webElement, str)
            except AssertionError:
                print("A tabela dos jogos não foi baixada corretamente.")
                return False

            SoupElement = BeautifulSoup(webElement, 'html.parser')
            for href in SoupElement.find_all('a', href=True):
                sublink = href["href"].replace("https://www.oddsportal.com", "")
            
                assert isinstance(sublink, str)
                # Esse len(sublink) > 31 serve para remover lixos que estão em alguns hrefs
                # o do sublink != SUBURL indica que o sublink não pode ser igual ao site + SUBURL,
                # que é o site atual
                if len(sublink) > 31 and sublink != suburl:
                    print(sublink)
                    available_games.append(sublink)

            for link_to_game in available_games:
                global df
                df = self.retrieve_game_parsed_text("https://www.oddsportal.com" + link_to_game) 
                print(df)
                if (df.empty == False):
                    temp = Arbitrage(
                            odd_a = df["Odd_a"].max(),
                            odd_b = df["Odd_b"].max(),
                            odd_draw = df["Empate"].max(),
                            total_bet=100,
                            platform= str(),
                        ).calculate_bets(verbose=True)
                    
                    a, b, liga = self.current_game.replace("Betting Odds, Soccer ", "").split('-')
                    # df.info()
                    # print(df["Odd_a"])

                    if temp["Profit Rate"].iloc[0] > 0:
                        home = df["Odd_a"].astype(float).idxmax()
                        away = df["Odd_b"].astype(float).idxmax()
                        draw = df["Empate"].astype(float).idxmax()

                        title = u'🚨' +  " Oportunidade de apostas " + u'🚨\n'
                        game = f"{a}x{b} - {liga}\n"
                        casas = f'Casa: {home} ({temp["Bet a"].iloc[0]}) \nEmpate: {draw} ({temp["Draw"].iloc[0]}) \nFora: {away} ({temp["Bet b"].iloc[0]})\n'
                        bot.send_message(chat_id=-742911060, text=f"{title}{game}{casas}")
                    else:
                        print("A aposta não gera lucro.")

                print('\n')
                print("******************************************************************************")
                print("******************************************************************************")
                print('\n')
    
        return True
            
def main():
    pass

if __name__ == "__main__":
    x = WebCrawlerOddsPortal()
    x.crawl(SITES_DISPONIVEIS, verbose=True)
    time.sleep(5)
    exit(0)    