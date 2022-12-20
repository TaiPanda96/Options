from  datetime import datetime
import traceback
import pytz
from Postgres.InsertQuery import toColumns
from Postgres.Connect import connect

debug = True;

def getQuery(useQuery = """ """, useValues = []):
    connection = connect(); 
    if (connection is None): return;
    if (len(useQuery)  == 0): return;
    if (len(useValues) == 0): return;
    try: 
        cursor = connection.cursor();
        for idx, elem in enumerate(useValues):
            if (idx < len(useValues) - 1):
                useQuery = useQuery.replace("${}".format(idx), elem, 1);
            else: 
                useQuery = useQuery.replace("${}".format(idx), elem, 1);

        cursor.execute(useQuery);
        results = cursor.fetchall();
        if len(results) == 0: return [];
        connection.commit();
        cursor.close();
        return results if results else [];
    except Exception as error: 
        print(error)
        traceback.print_exc()