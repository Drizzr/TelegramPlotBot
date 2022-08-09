import telegram
import requests
import time
import os
import autoplot

class telegram_bot:
    token = "" # enter your bot-token here
    re_url = f"http://api.telegram.org/bot{token}/getUpdates"
    chat_id = # enter your chat_id here
    path = os.path.abspath(os.getcwd()) + "/data"

    def __init__(self):
        self.OFFSET = self.get_OFFSET()
        self.sender = None
        self.plotParams = []

    def get_OFFSET(self):
        while True:
            try:
                ID = requests.get(self.re_url).json()
                i = len(ID["result"]) - 1
                if i >= 0:
                    self.OFFSET = ID["result"][i]["update_id"] + 1
                    return self.OFFSET
                time.sleep(0.2)
            except requests.exceptions.ConnectionError:
                pass

    def get_Updates(self):
        while True:
            try:
                data = requests.get(self.re_url + "?offset=" + str(self.OFFSET)).json()
                result = data["result"][0]
                self.sender = "@" + result["message"]["from"]["first_name"] + " "
                self.OFFSET += 1
                return result
            except (requests.exceptions.ConnectionError, IndexError, KeyError):
                pass
            time.sleep(0.2)

    def get_information(self, type):
        if type == "msg":
            return self.get_Updates()["message"]["text"]
        elif type == "doc":
            return self.get_Updates()["message"]["document"]["file_id"]


def main():
    tbot = telegram_bot()
    bot = telegram.Bot(token = tbot.token)
    plot_params = []
    while True:
        try:
            if tbot.get_information("msg").lower() == "start":
                tbot.plotParams = []
                bot.sendMessage(chat_id = tbot.chat_id, text = f"{tbot.sender} \n 1.Startzeit (z.B. 2021-01-01 00:00:00): ")
                tbot.plotParams.append(tbot.get_information("msg"))
                bot.sendMessage(chat_id = tbot.chat_id, text = f"{tbot.sender} \n Schrittweite in Minuten: ")
                tbot.plotParams.append(tbot.get_information("msg"))
                bot.sendMessage(chat_id = tbot.chat_id, text = f"{tbot.sender} \n Bitte Daten in Form einer .txt-Datei hchladen!")
                tbot.plotParams.append(bot.get_file(tbot.get_information("doc")))
                tbot.plotParams[2].download(custom_path=tbot.path+"/data.txt")
                bot.sendMessage(chat_id = tbot.chat_id, text = f"{tbot.sender} \n Bereich festlegen (ja/nein)?")
                tbot.plotParams.append(tbot.get_information("msg"))

                if tbot.plotParams[3].lower() == "nein":
                    plt = autoplot.plot(tbot.plotParams[0], tbot.plotParams[1])
                    plt.make_plot()
                    with open(tbot.path+'/plot.png', 'rb') as datei: 
                        bot.send_photo(chat_id = tbot.chat_id, photo=datei)
                elif tbot.plotParams[3].lower() == "ja":
                    bot.sendMessage(chat_id = tbot.chat_id, text = f"{tbot.sender} \n 1.Startzeit (z.B. 2021-01-01 00:00:00): ")
                    tbot.plotParams.append(tbot.get_information("msg"))
                    bot.sendMessage(chat_id = tbot.chat_id, text = f"{tbot.sender} \n 1.Endzeitzeit (z.B. 2021-01-01 00:00:00): ")
                    tbot.plotParams.append(tbot.get_information("msg"))
                    plt = autoplot.plot(tbot.plotParams[0], tbot.plotParams[1], tbot.plotParams[3], tbot.plotParams[4], tbot.plotParams[5])
                    plt.make_plot()
                    with open(tbot.path+'/plot.png', 'rb') as datei: 
                        bot.send_photo(chat_id = tbot.chat_id, photo=datei)
                plt.del_files()
        except (requests.exceptions.ConnectionError, KeyError, ValueError):
            bot.sendMessage(chat_id = tbot.chat_id, text = "Ein Fehler ist aufgetreten. Versuche es erneut!")
        time.sleep(0.2)

if __name__ == "__main__":
    main()
