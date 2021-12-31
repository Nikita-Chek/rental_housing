from django.http import HttpResponse

def api_help(request):
    """
    Yes, i know, this hardcode line is horible, 
    but when i try to return html file, i recive an error.
    And i don't have any time
    """
    
    html = """
<!DOCTYPE html>
<html>
   <body>
      <h1 style=\"font-family:sans-serif\">This is api for apartments analytics app</h1>
      <table style=\"font-family:sans-serif; font-size:30px\">
         <tr>
            <td>apartments/</td>
            <td>is for getting all apartments</td>
         </tr>
         <tr>
            <td>apartments/page/(int:pk)/ </td>
            <td>is for getting 20 * pageNumber apartments</td>
         </tr>
         <tr>
            <td>apartments/(int:pk)/</td>
            <td>is for getting apartment with ID == (int:pk)</td>
         </tr>
         <tr>
            <td>apartments/update/</td>
            <td>is for updating apartments to the newest condition</td>
         </tr>
         <tr>
            <td>apartments/insert/</td>
            <td>is for writing all existing apartments to db</td>
         </tr>
         <tr>
            <td>mean_by/(period)</td>
            <td>is for getting mean price of period (month, year)</td>
         </tr>
         <tr>
            <td>count_rooms/</td>
            <td>is for getting number of apartments with specified number of rooms</td>
         </tr>
         <tr>
            <td>median_by_year/</td>
            <td>is for getting median price by year</td>
         </tr>
      </table>
   </body>
</html>
"""
    return HttpResponse(html.replace('\n', ''))