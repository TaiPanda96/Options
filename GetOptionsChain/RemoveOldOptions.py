from Postgres.GetQuery import getQuery
from datetime import datetime, timedelta

def removeOldOptions():
    queryDate = datetime.today() - timedelta(days=1) - timedelta(hours=5);
    useQuery  = """SELECT * FROM options WHERE expiration < '{}'""".format(queryDate);
    oldData   = getQuery(useQuery, []);
    if (len(oldData) == 0): return;
    deleteQuery = """DELETE FROM options WHERE expiration < '{}'""".format(queryDate);
    getQuery(deleteQuery, []);