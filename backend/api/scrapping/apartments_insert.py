from .Apartments import Apartments
from .DBApartments import DBApartments
from django.http import JsonResponse


def apartments_insert(request):
    url = r"https://r.onliner.by/sdapi/ak.api/search/apartments?order=created_at%3Adesc&page="
    connection = "DATABASE=IBA_EDU;HOSTNAME=3d-edu-db.icdc.io;PORT=8163;PROTOCOL=TCPIP;UID=stud08;PWD=12345;"
    
    A = Apartments(url)
    DB = DBApartments(connection)
    # to write all data from site
    df = A.get_all_apartments()
    DB.insert(df)
    return JsonResponse(df.to_dict('records'), safe=False)