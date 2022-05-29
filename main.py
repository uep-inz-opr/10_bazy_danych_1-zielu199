if __name__ == '__main__':
    import csv, sqlite3
    sqlite_con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) # change to 'sqlite:///your_filename.db'
    # This little bugger above https://stackoverflow.com/questions/1829872/how-to-read-datetime-back-from-sqlite-as-a-datetime-instead-of-string-in-python
    cur = sqlite_con.cursor()

    #Tworzymy pusta tabele polaczenia
    cur.execute('''CREATE TABLE polaczenia (from_subscriber data_type INTEGER, 
                          to_subscriber data_type INTEGER, 
                          datetime data_type timestamp, 
                          duration data_type INTEGER , 
                          celltower data_type INTEGER);''') # use your column names here

        #Otwieramy plik.csv i przerzucamy go w najprostszy sposób do naszej nowo utworzonej bazy sqlite
    with open('D:\kacpe\Documents\Studia\Magisterka\drugi_semestr\IO\zadanie_bazy_danych\polaczenia_duze.csv','r') as fin:
            # csv.DictReader uses first line in file for column headings by default
        reader = csv.reader(fin, delimiter = ";") # comma is default delimiter
        next(reader, None)  # skip the headers
        rows = [x for x in reader]
        cur.executemany("INSERT INTO polaczenia (from_subscriber, to_subscriber, datetime, duration , celltower) VALUES (?, ?, ?, ?, ?);", rows)
        sqlite_con.commit()

    class ReportGenerator:
        def __init__(self,connection, escape_string = "(%s)"):
            self.connection = connection
            self.report_text = None
            self.escape_string = escape_string
            self.result = 0

        def generate_report(self, user_id):
            cursor = self.connection.cursor()
            sql_query = f"Select sum(duration) from polaczenia where from_subscriber ={self.escape_string}"
            args = (user_id,)
            cursor.execute(sql_query, args)
            self.result = cursor.fetchone()[0]
            self.report_text = f"Łączny czas trwania dla użytkownika {user_id} to {self.result}"

        def get_report(self):
            return self.result

    suma = 0

    for i in range(len(rows)):
        rg = ReportGenerator(sqlite_con, escape_string="?")
        rg.generate_report(i)
        skladowa = rg.get_report()
        if skladowa is not None:
            suma += skladowa
        else:
            continue

    print(int(suma))

