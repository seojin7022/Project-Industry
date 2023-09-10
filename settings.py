WINDOW_SIZE = (1920, 1080)
TILE_SIZE = 128
FPS = 60
MAP_SIZE = (30, 30)

shop_items = {
    "Peel_Machine": 350,
    "Extrude_Machine": 2000,
}

contracts = {
    "Easy": [
        {
            "dialogue": "집에 원목을 전시하고 싶네요",
            "kind": {
                "Oak_0": [3, 5]
            },
            "reward": [100, 150] #수량 X 500 ~ 510 사이의 난수
        },

        {
            "dialogue": "원목 5개만 주세요",
            "kind": {
                "Oak_0": [5, 5]
            },
            "reward": [100, 100] #수량 X 500 ~ 510 사이의 난수
        },
    ],

    "Normal": [
        {
            "dialogue": "목공 학원 수업에 필요합니다",
            "kind": {
                "Oak_2": [10, 20]
            },
            "reward": [400, 450] #수량 X 500 ~ 510 사이의 난수
        },

        {
            "dialogue": "식탁을 좀 만들고 싶어요",
            "kind": {
                "Oak_1": [10, 20]
            },
            "reward": [200, 250] #수량 X 500 ~ 510 사이의 난수
        },
    ],

    "Hard": [
        {
            "dialogue": "집이 없어요 도와주세요...",
            "kind": {
                "Oak_2": [120, 120],
                "Oak_3": [40, 40]
            },
            "reward": [1000, 2000] #수량 X 500 ~ 510 사이의 난수
        },

        {
            "dialogue": "나무 막대가 필요해요. 최대한 많이요",
            "kind": {
                "Oak_3": [100, 150]
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
    "Oak_0": "원목",
    "Oak_1": "껍질 벗긴 원목",
    "Oak_2": "나무 판자",
    "Oak_3": "나무 막대"
}