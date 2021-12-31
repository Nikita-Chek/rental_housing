import ibm_db_dbi as db
import pandas as pd
import numpy as np
from datetime import datetime

class DBApartments:
    __conn: db.Connection
    __conn_string: str
    
    def __init__(self, conn_string) -> None:
        self.__conn_string = conn_string
    
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
    
    def latest_id(self) -> int:
        self.__conn = db.connect(self.__conn_string)
        id = pd.read_sql("select max(ID) from apartments;", con=self.__conn)
        self.__conn.close()
        return id.loc[0][0]
    
    def latest_date(self) -> datetime:
        self.__conn = db.connect(self.__conn_string)
        date = pd.read_sql("select max(CREATION_DATE) from apartments;", con=self.__conn)
        self.__conn.close()
        return date.loc[0][0]
    
    def all_id(self) -> np.ndarray:
        self.__conn = db.connect(self.__conn_string)
        id = pd.read_sql("select ID from apartments;", con=self.__conn)
        self.__conn.close()
        return id #.to_numpy().flatten()
    
    def update(self, df: pd.DataFrame) -> bool:
        """
        Update given values in the table apartments
        Returns:
            bool: True if executed otherwise False
        """    
        self.__conn = db.connect(self.__conn_string)
        cursor = self.__conn.cursor()
        
        df_update = self.all_id().set_index('ID').join(df.set_index('ID'))
        names = df_update.columns.values
        
        update_command = lambda x, y: f"{y}="+ (('\''+x+'\'') if type(x)==str else str(x))
        
        for i, row in df_update.iterrows():
            update_string = "update apartments set "
            update_string += ','.join(map(update_command, row.values, names))
            update_string += f" where ID = {i};"
            try:
                cursor.execute(update_string)
            except Exception as e:
                print(e)
                return False

        cursor.execute('COMMIT')
        cursor.close()
        self.__conn.close()
        return True
    