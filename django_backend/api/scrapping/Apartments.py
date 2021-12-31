from fake_useragent import UserAgent
import requests
import json
import pandas as pd
import re
from datetime import datetime


timestamp_format = lambda date: str(
    datetime.strptime(
        date,
        '%Y-%m-%dT%H:%M:%S%z'
        ).replace(tzinfo=None))


class Apartments:
    __url: str
    
    def __init__(self, url: str) -> None:
        self.__url = url
    
    def get_response_page(self, page: int) -> dict:
        headers = {"User-Agent": UserAgent().random}
    
        responce = requests.get(url=self.__url + str(page), headers=headers)
        if responce.status_code == 200:
            return json.loads(responce.text)
        return responce.status_code

    def get_df_from_responce(self, responce: dict, latest: datetime) -> pd.DataFrame:
        df_apartments_list = []
        if responce["apartments"]:
            for i in responce["apartments"]:
                try:
                    rooms = int(re.findall(
                        r"\d+", 
                        i["rent_type"]
                        )[0])
                except:
                    rooms = 1
                
                apartment = {"ID": int(i["id"]),
                    "PRICE": float(i["price"]["amount"]),
                    "ROOMS": rooms,
                    "OWNER": bool(i["contact"]["owner"]),
                    "LOCATION_LATITUDE": float(i["location"]["latitude"]),
                    "LOCATION_LONGTITUDE": float(i["location"]["longitude"]),
                    "LOCATION_ADDRESS": i["location"]["address"],
                    "CREATION_DATE": timestamp_format(i["created_at"]),
                    "URL": i["url"]
                    }
                if latest and pd.Timestamp(apartment["CREATION_DATE"]) <= latest:
                    break
                df_apartments_list.append(apartment)
                
        return pd.DataFrame(df_apartments_list)


    def get_apartments_by_page(self, page: int, latest: datetime) -> pd.DataFrame:
        df = pd.DataFrame()
        responce = self.get_response_page(page)
        if responce:
            df = self.get_df_from_responce(responce, latest)
        return df


    def get_all_apartments(self, latest: datetime) -> pd.DataFrame:
        df_total = pd.DataFrame()
        i = 1
        while True:
            df = self.get_apartments_by_page(i, latest)
            if df.empty:
                return df_total
            df_total = df_total.append(df)
            i += 1
    
    def get_latest_apartments(self, latest: datetime) -> pd.DataFrame:
        return self.get_all_apartments(latest)