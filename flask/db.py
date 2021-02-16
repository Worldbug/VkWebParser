import psycopg2

db = psycopg2.connect(dbname='vk_parser_ex', user='app',
                        password='simplepass', host='localhost')
cursor = db.cursor()

cursor.execute("""INSERT INTO people
               (vkid, fname, sname, sex, bday, city, phone, platform, source)
               VALUES
               (666, 'Кира', 'Тихий', 'М', '2000-12-02', 'Москва', '89775993717', '3', 'devnull')
               """)
db.commit()
