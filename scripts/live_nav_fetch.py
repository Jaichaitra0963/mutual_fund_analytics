import requests
import pandas as pd

schemes = {
    "HDFC_Top100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_LargeCap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841,
}

for name, code in schemes.items():
    url = f"https://api.mfapi.in/mf/{code}"
    res = requests.get(url)
    data = res.json()
    df = pd.DataFrame(data["data"])
    df.to_csv(f"data/raw/{name}_nav.csv", index=False)
    print(f"Saved {name}: {len(df)} rows")
    print(df.head(2))
