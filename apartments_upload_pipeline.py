import airflow
from airflow import DAG
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.sensors.http_sensor import HttpSensor
from airflow.providers.jdbc.operators.jdbc import JdbcOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta
from fake_useragent import UserAgent
import requests
import json
import re
import ibm_db_dbi as db
import pandas as pd


default_args = {
            "owner": "User08",
            "start_date": airflow.utils.dates.days_ago(1),
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
            "email": "youremail@host.com",
            "retries": 1,
            "retry_delay": timedelta(minutes=5)
        }


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

    def get_df_from_responce(self, responce: dict, latest=None) -> pd.DataFrame:
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


    def get_apartments_by_page(self, page: int, latest: int=0) -> pd.DataFrame:
        df = pd.DataFrame()
        responce = self.get_response_page(page)
        if responce:
            df = self.get_df_from_responce(responce, latest)
        return df


    def get_all_apartments(self, latest=0) -> pd.DataFrame:
        df_total = pd.DataFrame()
        i = 1
        while True:
            df = self.get_apartments_by_page(i, latest)
            if df.empty:
                return df_total
            df_total = df_total.append(df)
            i += 1
    
    def get_latest_apartments(self, latest) -> pd.DataFrame:
        return self.get_all_apartments(latest)
    


class DBApartments:
    __conn: db.Connection
    __conn_string: str
    
    def __init__(self, conn_string) -> None:
        self.__conn_string = conn_string
    
    def latest_date(self) -> datetime:
        self.__conn = db.connect(self.__conn_string)
        date = pd.read_sql("select max(CREATION_DATE) from apartments;", con=self.__conn)
        self.__conn.close()
        return date.loc[0][0]
    
    def insert(self, df: pd.DataFrame) -> bool:
        """
        Write all values into the table apartments
        Returns:
            bool: True if executed otherwise False
        """    
        self.__conn = db.connect(self.__conn_string)
        cursor = self.__conn.cursor()

        insert_string = f"insert into apartments values ";

        for i, row in df.iterrows():
            insert_string += f"{*row.values,},"

        try:
            cursor.execute(insert_string[:-1] + ";")
        except Exception as e:
            print(e)
            return False

        cursor.execute('COMMIT')
        cursor.close()
        self.__conn.close()
        return True
    
    
def apartments_update(**kwargs):
    last_run = kwargs["prev_execution_date"]
    last_run = datetime.fromtimestamp(last_run.int_timestamp)
    curr_run = kwargs["execution_date"]
    curr_run = datetime.fromtimestamp(curr_run.int_timestamp)
    
    if not last_run:
        last_run = datetime(1970, 1, 1)
        

    url = r"https://r.onliner.by/sdapi/ak.api/search/apartments?order=created_at%3Adesc&page="
    connection = ('DATABASE=IBA_EDU;'+
                  'HOSTNAME=3d-edu-db.icdc.io;'+
                  'PORT=8163;'+
                  'PROTOCOL=TCPIP;'+
                  'UID=stud08;'+
                  'PWD=12345;')

    A = Apartments(url)
    DB = DBApartments(connection)
    latest = DB.latest_date()
    df = A.get_all_apartments(latest)
    DB.insert(df)
    
    


with DAG(dag_id="apartments_upload_pipeline", schedule_interval="@hourly", default_args=default_args, catchup=False) as dag:

    is_apartments_api_available = HttpSensor(
            task_id="is_apartments_api_available",
            method="GET",
            http_conn_id="u08_appart_onliner",
            endpoint="",
            response_check=lambda response: "apartments" in response.text,
            poke_interval=5,
            timeout=20
    )


    apartments_updating = PythonOperator(
            task_id="apartments_update",
            provide_context=True,
            python_callable=apartments_update
    )

    
    is_apartments_api_available >> apartments_updating