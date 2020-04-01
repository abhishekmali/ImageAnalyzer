import MySQLdb

db = MySQLdb.connect("localhost", "root", "", "imageanalyzer")

cursor = db.cursor()