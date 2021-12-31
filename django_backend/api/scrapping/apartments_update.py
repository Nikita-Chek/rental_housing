from .Apartments import Apartments
from .DBApartments import DBApartments
from django.http import JsonResponse


def apartments_update(request):
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
    return JsonResponse(df.to_dict('records'), safe=False)