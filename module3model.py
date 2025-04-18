import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# 读取资产相关信息
class Module3Model:
    def __init__(self, parameter1=100, parameter2=0.5):
        """
        Initialize the model with parameters.
        
        Parameters:
            parameter1 (float): A model-specific constant used in processing.
            parameter2 (float): A scaling factor for the computed result.
        """
        self.parameter1 = parameter1
        self.parameter2 = parameter2
    
    def load_data(self):
        """
        Loads data directly from in-memory dictionaries and returns three DataFrames:
          - asset_df: contains asset statistics,
          - asset_price: contains asset price information,
          - df_gas: contains gas price prediction data.
        
        Returns:
            tuple: (asset_df, asset_price, df_gas)
        """
        # Load asset data (资产数据)
        data1 = {
            "asset_name": [
                "AAL", "BNO", "CAD", "Chevron", "ConocoPhillips", "DAL", "ExxonMobil",
                "INR", "JPY", "NIO", "OILK", "QCLN", "RUB", "TSLA", "UPS", "USO", "VIX", "XLE"
            ],
            "expected_return": [
                0.09615933796, -0.0350557703, 0.008469792256, 0.001373749184, -0.03447023149,
                -0.03329547321, -0.002181379976, 0.0005344578895, 0.006989143263, 0.3430941193,
                -0.05837208194, -0.001927182439, -0.01745702487, -0.073723641, -0.02870185356,
                -0.05588783588, 0.07396351304, -0.131861816
            ],
            "score": [
                0.027554, 0.049244, 0.139437, 0.205812, 0.023349, 0.027867, 0.189337,
                0.238236, 0.238164, 0.029693, 0.048956, 0.145005, 0.195016, 0.028758,
                0.223193, 0.050604, 0.146487, 0.235782
            ],
            "normalized_score": [
                0.0123, 0.022, 0.0622, 0.0918, 0.0104, 0.0124, 0.0844, 0.1062, 0.1062,
                0.0132, 0.0218, 0.0647, 0.087, 0.0128, 0.0995, 0.0226, 0.0653, 0.1051
            ],
            "correlation_with_oil": [
                0.044038, 0.337322, -0.083387, 0.807201, 0.76908, 0.128151, 0.671652,
                0.44107, 0.567697, -0.242988, 0.332469, -0.051891, 0.169778, 0.446324,
                0.412251, 0.326205, -0.236089, 0.187466
            ],
            "direction": [
                "positive", "positive", "negative", "positive", "positive", "positive",
                "positive", "positive", "positive", "negative", "positive", "negative",
                "positive", "positive", "positive", "positive", "negative", "positive"
            ]
        }
        asset_df = pd.DataFrame(data1)

        # Load asset price data (价格相关信息)
        data2 = {
            "Date": [
                "2025-04-10", "2025-04-17", "2025-04-24", "2025-05-01", "2025-05-08", "2025-05-15",
                "2025-05-22", "2025-05-29", "2025-06-05", "2025-06-12", "2025-06-19", "2025-06-26"
            ],
            "USO": [80.365377, 79.971279, 77.506376, 75.646674, 75.148323, 75.022803, 77.673704, 75.486745, 75.694515, 75.8732, 75.87393, 75.87393],
            "OILK": [46.804481, 46.800007, 45.227739, 43.863403, 43.429655, 43.366491, 45.938341, 43.722036, 43.948372, 44.062829, 44.072406, 44.072406],
            "BNO": [31.344369, 31.200026, 30.652943, 30.210722, 30.108301, 30.099204, 30.451006, 30.255041, 30.262763, 30.320562, 30.245568, 30.245568],
            "Chevron": [153.077434, 153.47143, 153.686281, 153.59292, 153.681963, 153.496163, 153.355956, 153.376608, 153.310658, 153.280347, 153.287724, 153.287724],
            "ExxonMobil": [117.472427, 118.309682, 118.322396, 117.835519, 117.541827, 117.262163, 117.206714, 117.298161, 117.165607, 117.106382, 117.216175, 117.216175],
            "ConocoPhillips": [97.333579, 94.366768, 94.188719, 93.572866, 93.598907, 93.533024, 92.853089, 93.77517, 93.854864, 93.797187, 93.978468, 93.978468],
            "QCLN": [94.002517, 94.104127, 94.08516, 94.009398, 93.832923, 93.672225, 93.519044, 93.335665, 93.298057, 93.293036, 93.482673, 93.821357],
            "XLE": [29.195715, 28.91077, 28.680776, 28.297201, 27.89335, 27.279647, 26.916788, 26.053626, 25.491251, 25.225315, 25.252067, 25.345915],
            "UPS": [111.358592, 111.464094, 111.363425, 110.76097, 109.971361, 109.537275, 109.132003, 108.813553, 108.308679, 108.234142, 108.162394, 108.162394],
            "DAL": [37.705456, 37.294033, 36.689144, 35.944103, 36.450035, 36.199459, 35.944103, 37.705456, 36.689144, 35.944103, 36.450035, 36.450035],
            "AAL": [10.011425, 10.628444, 10.90798, 11.081293, 10.974117, 11.031317, 11.081293, 10.011425, 10.90798, 11.081293, 10.974117, 10.974117],
            "TSLA": [235.755692, 226.663483, 220.339493, 214.717392, 218.374924, 216.550507, 214.717392, 235.755692, 220.339493, 214.717392, 218.374924, 218.374924],
            "NIO": [3.816052, 4.336818, 4.927811, 5.518668, 5.125317, 5.322287, 5.518668, 3.816052, 4.927811, 5.518668, 5.125317, 5.125317],
            "RUB": [84.285095, 84.354866, 84.224731, 84.047554, 83.643852, 83.259972, 83.072327, 82.813728, 82.984367, 82.813728, 82.984367, 82.813728],
            "CAD": [1.438406, 1.442245, 1.443482, 1.445156, 1.448147, 1.449994, 1.451806, 1.452247, 1.45241, 1.452086, 1.452091, 1.450589],
            "JPY": [148.29686, 147.54454, 147.484604, 147.589111, 148.018066, 148.425751, 148.868118, 149.333328, 149.176682, 149.333328, 149.176682, 149.333328],
            "INR": [86.893656, 87.031159, 87.151712, 87.192656, 87.259863, 87.240946, 87.165445, 87.106393, 87.010059, 86.930597, 86.902981, 86.940097],
            "VIX": [31.456064, 30.468369, 31.722168, 32.921757, 33.173145, 33.351933, 33.521645, 33.782665, 33.69978, 33.782665, 33.69978, 33.782665]
        }
        asset_price = pd.DataFrame(data2)

        # Load gas price prediction data (读取油价预测数据)
        data3 = {
            "Date": [
                "2025-04-10", "2025-04-17", "2025-04-24", "2025-05-01",
                "2025-05-08", "2025-05-15", "2025-05-22", "2025-05-29",
                "2025-06-05", "2025-06-12", "2025-06-19", "2025-06-26"
            ],
            "Gas_Price": [
                3.041306, 2.985237, 2.964385, 2.952460, 2.978964, 2.989690,
                3.013564, 3.018698, 3.060508, 3.118732, 3.148079, 3.171664
            ]
        }
        df_gas = pd.DataFrame(data3)
        df_gas["Date"] = pd.to_datetime(df_gas["Date"])
        df_gas.set_index("Date", inplace=True)

        return asset_df, asset_price, df_gas

if __name__ == "__main__":
    # When run as a standalone script, load and print the data preview.
    model = Module3Model()
    asset_df, asset_price, df_gas = model.load_data()
    
    print("Asset DataFrame:")
    print(asset_df.head())
    
    print("\nAsset Price DataFrame:")
    print(asset_price.head())
    
    print("\nGas Price DataFrame:")
    print(df_gas.head())
