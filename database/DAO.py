from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllColors():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT gp.Product_color as color
                    FROM go_products gp"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["color"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllProducts(color):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT gp.*
        FROM go_products gp 
        WHERE gp.Product_color=%s """

        cursor.execute(query, (color,))

        for row in cursor:
            result.append(Product(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSales(p1, p2, year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT COUNT(DISTINCT s1.Date) as N 
                   FROM go_daily_sales s1, go_daily_sales s2
                   WHERE s1.Date = s2.Date
                   AND s1.Retailer_code = s2.Retailer_code
                   AND s1.Product_Number = %s 
                   AND s2.Product_Number = %s
                   AND YEAR(s1.Date) = %s"""

        cursor.execute(query, (p1.Product_number, p2.Product_number, year))

        for row in cursor:
                result.append(row["N"])

        cursor.close()
        conn.close()
        return result

    # @staticmethod
    # def getAllProductsV2():
    #     conn = DBConnect.get_connection()
    #
    #     result = []
    #
    #     cursor = conn.cursor(dictionary=True)
    #     query = """SELECT gp.*
    #         FROM go_products gp """
    #
    #     cursor.execute(query)
    #
    #     for row in cursor:
    #         result.append(Product(**row))
    #
    #     cursor.close()
    #     conn.close()
    #     return result


