from Postgres.GetQuery import getQuery

def removeOldOptions():
    useQuery = """
        DELETE FROM options WHERE expiration < now() - interval '1 day';
    """
    return getQuery(useQuery);