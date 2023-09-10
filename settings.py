WINDOW_SIZE = (1920, 1080)
TILE_SIZE = 128
FPS = 60
MAP_SIZE = (30, 30)

shop_items = {
    "Peel_Machine": 350
}

contracts = {
    "Easy": [
        {
            "dialogue": "집에 가구를 좀 만들고 싶네요",
            "kind": {
                "Oak_2": [3, 5]
            },
            "reward": [500, 510] #수량 X 500 ~ 510 사이의 난수
        }
    ],

    "Normal": [
        {
            "dialogue": "목공 학원 수업에 필요합니다",
            "kind": {
                "Oak_2": [10, 20]
            },
            "reward": [550, 600] #수량 X 500 ~ 510 사이의 난수
        }
    ],

    "Hard": [
        {
            "dialogue": "집이 없어요 도와주세요...",
            "kind": {
                "Oak_2": [120, 120],
                "Oak_3": [40, 40]
            },
            "reward": [1000, 2000] #수량 X 500 ~ 510 사이의 난수
        }
    ],
}

ingredient_price = {
    "Oak_0": 30,
    "Oak_1": 60,
    "Oak_2": 120,
    "Oak_3": 300
}

ingredient_real_name = {
    "Oak_0": "통나무",
    "Oak_1": "껍질 깐 통나무",
    "Oak_2": "나무 판자",
    "Oak_3": "나무 막대"
}