import pygame, os, random
from pygame._sdl2 import *
from settings import *
from gui import *

class ContractInfo:
    def __init__(self, dialogue, kind: dict, reward) -> None:
        self.dialogue = dialogue
        self.kind = kind.copy()
        self.reward = reward

        count_sum = 0

        for k, v in self.kind.items():
            self.kind.update({f"{k}": random.randint(int(v[0]), int(v[1]))})

            count_sum += self.kind[k]

        self.reward = count_sum * random.randint(self.reward[0], self.reward[1])

        


class Contract:
    def __init__(self, app) -> None:
        self.app = app

        easy_contract = contracts["Easy"][random.randint(0, len(contracts["Easy"]) - 1)]
        normal_contract = contracts["Normal"][random.randint(0, len(contracts["Normal"]) - 1)]
        hard_contract = contracts["Hard"][random.randint(0, len(contracts["Hard"]) - 1)]

        self.easy_contract = ContractInfo(easy_contract["dialogue"], easy_contract["kind"], easy_contract["reward"])
        self.normal_contract = ContractInfo(normal_contract["dialogue"], normal_contract["kind"], normal_contract["reward"])
        self.hard_contract = ContractInfo(hard_contract["dialogue"], hard_contract["kind"], hard_contract["reward"])
        
    def click(self, button):
        if button.name == "B_Accept0": #Easy Contract
            isAcceptable = True
            for k, v in self.easy_contract.kind.items():
                if self.app[2]["Inventory"][k] < v:
                    isAcceptable = False
                    break
            if isAcceptable:
                for k, v in self.easy_contract.kind.items():
                    self.app[2]["Inventory"][k] -= v
                self.app[2]["Money"] += self.easy_contract.reward

        elif button.name == "B_Accept1": #Normal Contract
            isAcceptable = True
            for k, v in self.normal_contract.kind.items():
                if self.app[2]["Inventory"][k] < v:
                    isAcceptable = False
                    break
            if isAcceptable:
                for k, v in self.normal_contract.kind.items():
                    self.app[2]["Inventory"][k] -= v
                self.app[2]["Money"] += self.normal_contract.reward

        elif button.name == "B_Accept2": #Hard Contract
            isAcceptable = True
            for k, v in self.hard_contract.kind.items():
                if self.app[2]["Inventory"][k] < v:
                    isAcceptable = False
                    break
            if isAcceptable:
                for k, v in self.hard_contract.kind.items():
                    self.app[2]["Inventory"][k] -= v
                self.app[2]["Money"] += self.hard_contract.reward

        elif button.name == "B_Cancel0": #Easy Contract Cancel
            easy_contract = contracts["Easy"][random.randint(0, len(contracts["Easy"]) - 1)]
            self.easy_contract = ContractInfo(easy_contract["dialogue"], easy_contract["kind"], easy_contract["reward"])
        elif button.name == "B_Cancel1": #Normal Contract Cancel
            normal_contract = contracts["Normal"][random.randint(0, len(contracts["Normal"]) - 1)]
            self.normal_contract = ContractInfo(normal_contract["dialogue"], normal_contract["kind"], normal_contract["reward"])
        elif button.name == "B_Cancel2": #Hard Contract Cancel
            hard_contract = contracts["Hard"][random.randint(0, len(contracts["Hard"]) - 1)]
            self.hard_contract = ContractInfo(hard_contract["dialogue"], hard_contract["kind"], hard_contract["reward"])


    def run(self):
        pass

class ContractGUI(GUIFrame):
    def __init__(self, app) -> None:
        super().__init__(app, "contract_gui")

        self.easy_contract = None
        self.normal_contract = None
        self.hard_contract = None

        self.frame_structure = {
            "UI_Contract": [{
                "position": (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2),
            }],

            "UI_QuestBox1": [{
                "position": (WINDOW_SIZE[0] / 2 - 50, WINDOW_SIZE[1] / 2 + 200 * i - 150)
            } for i in range(3)],

            

        }

        self.button_structure = {
            "B_Accept": [{
                "position": (WINDOW_SIZE[0] / 2 + 210, WINDOW_SIZE[1] / 2 + 200 * i - 170)
            } for i in range(3)],

            "B_Cancel": [{
                "position": (WINDOW_SIZE[0] / 2 + 160, WINDOW_SIZE[1] / 2 + 200 * i - 170)
            } for i in range(3)],

            "B_Close": {
                "position": (WINDOW_SIZE[0] / 2 + 260, WINDOW_SIZE[1] / 2 -385)
            },
        }

        self.text_structure = {
            "Easy_Dialogue": {
                "font": "OTF_Medium.otf",
                "font-size": 18,
                "text": "대화",
                "position": (WINDOW_SIZE[0] / 2 - 200, WINDOW_SIZE[1] / 2 - 200),
                "color": (255, 255, 255)
            },

            "Easy_Count": {
                "font": "OTF_Medium.otf",
                "font-size": 18,
                "text": "판매 수량: ",
                "position": (WINDOW_SIZE[0] / 2 - 200, WINDOW_SIZE[1] / 2 - 150),
                "color": (255, 255, 255)
            },
            "Easy_Reward": {
                "font": "OTF_Medium.otf",
                "font-size": 18,
                "text": "보상: ",
                "position": (WINDOW_SIZE[0] / 2 - 200, WINDOW_SIZE[1] / 2 - 120),
                "color": (255, 255, 255)
            },

            "Normal_Dialogue": {
                "font": "OTF_Medium.otf",
                "font-size": 18,
                "text": "대화",
                "position": (WINDOW_SIZE[0] / 2 - 200, WINDOW_SIZE[1] / 2),
                "color": (255, 255, 255)
            },

            "Normal_Count": {
                "font": "OTF_Medium.otf",
                "font-size": 18,
                "text": "판매 수량: ",
                "position": (WINDOW_SIZE[0] / 2 - 200, WINDOW_SIZE[1] / 2 + 50),
                "color": (255, 255, 255)
            },
            "Normal_Reward": {
                "font": "OTF_Medium.otf",
                "font-size": 18,
                "text": "보상: ",
                "position": (WINDOW_SIZE[0] / 2 - 200, WINDOW_SIZE[1] / 2 + 80),
                "color": (255, 255, 255)
            },

            "Hard_Dialogue": {
                "font": "OTF_Medium.otf",
                "font-size": 18,
                "text": "대화",
                "position": (WINDOW_SIZE[0] / 2 - 200, WINDOW_SIZE[1] / 2 + 200),
                "color": (255, 255, 255)
            },

            "Hard_Count": {
                "font": "OTF_Medium.otf",
                "font-size": 18,
                "text": "판매 수량: ",
                "position": (WINDOW_SIZE[0] / 2 - 200, WINDOW_SIZE[1] / 2 + 250),
                "color": (255, 255, 255)
            },
            "Hard_Reward": {
                "font": "OTF_Medium.otf",
                "font-size": 18,
                "text": "보상: ",
                "position": (WINDOW_SIZE[0] / 2 - 200, WINDOW_SIZE[1] / 2 + 280),
                "color": (255, 255, 255)
            },
        }

        self.load_guis()

    def update_contract(self, easy_contract, normal_contract, hard_contract):
        if easy_contract != self.easy_contract:
            self.easy_contract = easy_contract

            for text in self.texts:
                if text.name == "Easy_Dialogue":
                    text.text = easy_contract.dialogue
                elif text.name == "Easy_Count":
                    newText = "판매 수량: "
                    for k, v in easy_contract.kind.items():
                        newText += ingredient_real_name[k] + " x " + str(v) + ", "
                    text.text = newText.removesuffix(", ")
                elif text.name == "Easy_Reward":
                    text.text = "보상: " + str(easy_contract.reward)
        if normal_contract != self.normal_contract:
            self.normal_contract = normal_contract

            for text in self.texts:
                if text.name == "Normal_Dialogue":
                    text.text = normal_contract.dialogue
                elif text.name == "Normal_Count":
                    newText = "판매 수량: "
                    for k, v in normal_contract.kind.items():
                        newText += ingredient_real_name[k] + " x " + str(v) + ", "
                    text.text = newText.removesuffix(", ")
                elif text.name == "Normal_Reward":
                    text.text = "보상: " + str(normal_contract.reward)

        if hard_contract != self.hard_contract:
            self.hard_contract = hard_contract

            for text in self.texts:
                if text.name == "Hard_Dialogue":
                    text.text = hard_contract.dialogue
                elif text.name == "Hard_Count":
                    newText = "판매 수량: "
                    for k, v in hard_contract.kind.items():
                        newText += ingredient_real_name[k] + " x " + str(v) + ", "
                    text.text = newText.removesuffix(", ")
                elif text.name == "Hard_Reward":
                    text.text = "보상: " + str(hard_contract.reward)
        