from database.DB_connect import DBConnect
from model.connessioni import Connessione
from model.retailer import Retailer


class DAO():
    @staticmethod
    def getCountries():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct gr.Country as country
                        from go_retailers gr
                        order by gr.Country"""
            cursor.execute(query, )
            for row in cursor:
                result.append(row["country"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getRetailers(country):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                        from go_retailers gr  
                        where gr.Country = %s"""
            cursor.execute(query, (country,))
            for row in cursor:
                result.append(Retailer(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllConnessioni(year, country, idmap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select gr1.Retailer_code as retailer1, gr2.Retailer_code as retailer2, count(*) as peso
                        from go_retailers gr1, go_retailers gr2, go_daily_sales gds1, go_daily_sales gds2  
                        where gr1.Retailer_code = gds1.Retailer_code
                        and gr2.Retailer_code = gds2.Retailer_code
                        and gds1.Product_number = gds2.Product_number
                        and gr1.Retailer_code<gr2.Retailer_code
                        and year(gds2.`Date`) = year (gds1.`Date`)
                        and year(gds2.`Date`) = %s
                        and gr1.Country = gr2.Country
                        and gr1.Country = %s
                        group by gr1.Retailer_code, gr2.Retailer_code """
            cursor.execute(query, (year,country))
            for row in cursor:
                result.append(Connessione(idmap[row["retailer1"]], idmap[row["retailer2"]],
                                          row["peso"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllConnessioni2(code1, code2, year, country):
        cnx = DBConnect.get_connection()
        result = 0
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select count(distinct gds1.Product_number) as peso
                        from go_retailers gr1, go_retailers gr2, go_daily_sales gds1, go_daily_sales gds2
                        where gr1.Retailer_code = %s
                        and  gr1.Retailer_code = gds1.Retailer_code
                        and gr2.Retailer_code = %s
                        and gr2.Retailer_code = gds2.Retailer_code
                        and gds1.Product_number = gds2.Product_number
                        and year(gds2.`Date`) = year (gds1.`Date`)
                        and year(gds2.`Date`) = %s 
                        and gr1.Country = gr2.Country
                        and gr1.Country = %s
                        group by gr1.Retailer_code, gr2.Retailer_code"""
            cursor.execute(query, (code1, code2, year, country))
            for row in cursor:
                result = row["peso"]
            cursor.close()
            cnx.close()
        return result
