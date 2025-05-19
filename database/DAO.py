from database.DB_connect import DBConnect
from model.teams import Team


class DAO():
    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct t.`year` as year
from teams t
where t.`year` >= 1980
order by year desc"""
        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsOfYearAnno(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
from teams t
where t.`year` = %s"""
        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(Team(**row))
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllTeams():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
from teams t"""
        cursor.execute(query)

        for row in cursor:
            result.append(Team(**row))
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def salaryOfTeams(year,team,idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.ID as teamID,sum(s.salary) as totSalary
from salaries s,teams t, appearances a 
where s.`year` = t.`year`and t.`year` =a.`year` 
and a.`year` = "%s"
and t.ID = %s
and t.ID = a.teamID
and s.playerID = a.playerID
group by t.teamCode
"""
        cursor.execute(query, (year,team))

        for row in cursor:
            result.append((idMap[row["teamID"]], row["totSalary"])) #tupla con squadra e salario
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result


