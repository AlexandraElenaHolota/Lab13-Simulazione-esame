from database.DB_connect import DBConnect
from model.state import State


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllShape(anno):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """SELECT s.shape 
                    FROM sighting s 
                    WHERE YEAR (s.`datetime` ) = %s """

        cursor.execute(query, (anno,))

        result = []
        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllState():
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """SELECT s.id , s.Lat, s.Lng 
                    FROM state s """

        cursor.execute(query,)

        result = []
        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllWeightEdges(anno, shape):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """SELECT n.state1 , n.state2 , COUNT(*) as peso 
                    FROM neighbor n , sighting s 
                    WHERE YEAR (s.`datetime`) = %s and s.shape = %s  and (s.state=n.state1 or s.state=n.state2) and n.state1<n.state2 
                    GROUP by n.state1 , n.state2 """

        cursor.execute(query, (anno, shape) )

        result = []
        for row in cursor:
            result.append((row["state1"], row["state2"], row["peso"]))

        cursor.close()
        conn.close()
        return result

