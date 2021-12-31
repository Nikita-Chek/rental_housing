from django.http import JsonResponse, HttpResponse
import ibm_db_dbi as db
import pandas as pd

CONNECTION_STRING = "DATABASE=IBA_EDU;HOSTNAME=3d-edu-db.icdc.io;PORT=8163;PROTOCOL=TCPIP;UID=stud08;PWD=12345;"


def apartments_all(request):
    if request.method == 'GET':
        global CONNECTION_STRING
        connection = db.connect(CONNECTION_STRING)
        queryset =  pd.read_sql(
            "select * from apartments",
            con=connection)
        connection.close()
        response = queryset.to_dict('records')
        return JsonResponse(response, safe=False)


def apartments_page(request, pk):
    if request.method == 'GET':
        global CONNECTION_STRING
        connection = db.connect(CONNECTION_STRING)
        queryset =  pd.read_sql(
            f"select * from apartments limit {pk * 20}",
            con=connection)
        connection.close()
        response = queryset.to_dict('records')
        return JsonResponse(response, safe=False)

    
def apartment(request, pk):
    if request.method == 'GET':
        global CONNECTION_STRING
        connection = db.connect(CONNECTION_STRING)
        queryset =  pd.read_sql(
            f"select * from apartments where ID = {pk}",
            con=connection)
        connection.close()
        if queryset.empty:
            return HttpResponse(status=204)
        response = queryset.to_dict('records')
        return JsonResponse(response, safe=False)
    

def count_rooms(request):
    if request.method == 'GET':
        global CONNECTION_STRING
        connection = db.connect(CONNECTION_STRING)
        queryset =  pd.read_sql(
            "select count(*) as TOTAL, ROOMS from APARTMENTS group by ROOMS;",
            con=connection)
        connection.close()
        if queryset.empty:
            return HttpResponse(status=204)
        response = queryset.to_dict('records')
        return JsonResponse(response, safe=False)
    

def mean_by(request, period):
    if request.method == 'GET':
        global CONNECTION_STRING
        connection = db.connect(CONNECTION_STRING)
        try:
            queryset =  pd.read_sql(
                f"select SUM(PRICE)/COUNT(PRICE) AS MEAN, {period}(CREATION_DATE) AS {period} FROM APARTMENTS GROUP BY {period}(CREATION_DATE);",
                con=connection)
        except Exception:
            connection.close()
            return HttpResponse(status=404)
        if queryset.empty:
            return HttpResponse(status=204)
        response = queryset.to_dict('records')
        connection.close()
        return JsonResponse(response, safe=False)
    
def median_by_year(request):
    if request.method == 'GET':
        global CONNECTION_STRING
        connection = db.connect(CONNECTION_STRING)
        try:
            queryset =  pd.read_sql(
                """
                with T AS (select PRICE,
                    YEAR(CREATION_DATE) AS YEAR,
                    ROW_NUMBER() over
                    (
                        partition by YEAR(CREATION_DATE)
                        order by PRICE
                    ) AS ROW,
                    COUNT(*) over (partition by YEAR(CREATION_DATE)) AS TOTAL
                from APARTMENTS)
                select PRICE AS MEDIAN, YEAR
                from T where ROW = TOTAL/2;""".replace('\n', ''),
                con=connection)
            connection.close()
        except Exception:
            connection.close()
            return HttpResponse(status=404)
        if queryset.empty:
            return HttpResponse(status=204)
        response = queryset.to_dict('records')
        return JsonResponse(response, safe=False)
    