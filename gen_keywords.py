
import sqlite3

from yargy import rule, Parser
from yargy.predicates import gram, normalized
from yargy.pipelines import morph_pipeline
from yargy.predicates.bank import activate
from openpyxl import load_workbook

conn = sqlite3.connect('course_base.db')
cursor = conn.cursor()
# cursor.execute('DROP TABLE competences')
cursor.execute('''CREATE TABLE IF NOT EXISTS competences(
    compid INT PRIMARY KEY,
    name TEXT,
    list TEXT);
''')

R1 = rule(gram('ADJF').optional(), gram('NOUN'))  # rule searching all key pairs ADJECTIVE NOUN
parser = Parser(R1)

comps = load_workbook('competences.xlsx')  # opening xlsx table as data source


for c in range(2, 19):  # walking across comp indicators
    first = comps['Лист1']
    text = first[f'C{c}'].value

    res = set()
    for item in parser.findall(text):  # getting simple 'keywords' from table cell
        res.add(' '.join([activate(normalized(_.value)).value.pop() for _ in item.tokens]))
    print(res)
    R2 = morph_pipeline(list(res))  # rule searching matches by keywords in desc
    parser1 = Parser(R2)


    def find_all_courses() -> dict:
        names = dict()  # resulting list
        for i in range(2, 200):  # processing first 200 courses from table
            list_of_matched = []  # cleaning list
            tmp = cursor.execute(f'SELECT * FROM courses WHERE courseid = {i}')  # setting value of considered page
            desc = tmp.fetchone()


            #print(type(desc), desc[0], desc[1], desc[2], sep='\n')
            for match in parser1.findall(desc[2]):  # parsing
                list_of_matched.append(' '.join([activate(normalized(_.value)).value.pop()
                                                 if len(_.value) > 1 else '' for _ in match.tokens]))
            val = len(res.intersection(set(list_of_matched)))
            if val > len(list_of_matched)*0.1 and val > 1:  # checking if more than 10% of keywords are equal
                # print(desc[1], '\n')  # name of course
                names[desc[1]] = val
                del list_of_matched
            del tmp

        return names  # returning set of names

    a = find_all_courses()
    print(list(a.keys()))
    b = sorted(list(a.keys()), key=lambda x: -a[x])
    b = '/'.join(b)
    query = f'INSERT INTO competences VALUES({c}, "{text}", "{b}")'
    print(query)
    cursor.execute(query)
    del first, text
    conn.commit()
conn.close()

