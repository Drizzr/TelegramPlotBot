
import matplotlib.pyplot as plt
import pandas as pd
import os

class plot:
    def __init__(self, startzeit, schrittweite, bereich = "", b_startzeit = None, b_endzeit = None):
        self.startzeit = startzeit
        self.schrittweite = schrittweite
        self.bereich = bereich
        self.b_startzeit = b_startzeit
        self.b_endzeit = b_endzeit
        self.ticks = []        
        self.ts = None
        self.values = []
        self.path = os.path.abspath(os.getcwd()) + "/data"
    
    def del_files(self):
        for filename in os.listdir(self.path):
            if filename.lower().endswith((".txt", ".png")):
                os.remove(filename)

    def get_txt_file(self):
        for filename in os.listdir(self.path):
            if filename.lower().endswith((".txt")):
                return filename

    def make_x_y(self):
        with open(self.get_txt_file()) as datei:
            y = [int(value) for value in datei]
            x = pd.date_range(self.startzeit, periods=len(y), freq=f'{self.schrittweite}min')
            self.ts = pd.DataFrame(y, index=x)

            if self.bereich.lower() == "ja":
                start_index = self.ts.index.tolist().index(pd.Timestamp(self.b_startzeit, freq='T'))
                end_index = self.ts.index.tolist().index(pd.Timestamp(self.b_endzeit, freq='T'))
                x = self.ts.index.tolist()[start_index:end_index+1]
                y = y[start_index:end_index+1]
                self.ts = pd.DataFrame(y, index=x)

    def get_value_list(self):
        for value in self.ts.values.tolist():
            self.values.append(value[0])

    def make_plot(self):
        self.make_x_y()
        self.get_value_list()
        plot = self.ts.plot(color = "black", drawstyle = "steps")
        plt.fill_between(self.ts.index, self.values, 0, color = "black")
        plt.xlabel("Zeit", fontsize = 8)
        plt.ylabel("CO2", fontsize = 8)
        plt.legend(["CO2"])
        figure=plot.get_figure()
        if self.bereich.lower() == "nein":
            figure.savefig("data/plot.png", dpi=400)
        else:
            figure.savefig("data/plot.png", dpi=600)
        plt.close(fig=figure)
