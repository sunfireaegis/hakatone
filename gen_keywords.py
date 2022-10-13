
import sqlite3
import time

from yargy import rule, Parser
from yargy.predicates import gram, normalized
from yargy.pipelines import morph_pipeline
from yargy.predicates.bank import activate
from openpyxl import load_workbook


'''class GenCoursesToIndicator:
    def __init__(self, item) -> None:
        self.item = item
        comps = load_workbook('competences.xlsx')  # indicators table attr
        self.indicators = comps['Лист1']
        page = load_workbook('courses.xlsx')  # attr page with courses' descriptions
        self.courses = page['Описание курсов']


    def gen_ind_keywords(self) -> set:
        R1 = rule(gram('ADJF').optional(), gram('NOUN'))  # rule searching all key pairs ADJECTIVE NOUN
        parser = Parser(R1)

        text = self.indicators[f'C{self.item}'].value
        res = set()
        for item in parser.findall(text):  # getting simple 'keywords' from table cell
            res.add(' '.join([activate(normalized(_.value)).value.pop() for _ in item.tokens]))
        return res


    def get_matching_courses(self) -> dict:
        data = self.gen_ind_keywords()
        R2 = morph_pipeline(list(data))  # rule searching matches by keywords in desc
        parser1 = Parser(R2)

        list_of_matched, names = [], dict()  # resulting list
        for i in range(2, 500):
            list_of_matched.clear()  # cleaning list
            desc = self.courses[f'B{i}'].value  # setting value of considered page

            for match in parser1.findall(desc):  # parsing
                list_of_matched.append(' '.join([activate(normalized(_.value)).value.pop()
                                                 if len(_.value) > 1 else '' for _ in match.tokens]))

            val = len(data.intersection(set(list_of_matched)))
            if val > len(list_of_matched) * 0.1 and val > 1:  # checking if more than 10% of keywords are equal
                # print(val)
                # print(page[f'A{i}'].value, '\n')  # name of course
                names[self.courses[f'A{i}'].value] = val
        return names



getter = GenCoursesToIndicator(2)
print(getter.get_matching_courses())
'''



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


for c in range(2, 19):
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
        for i in range(2, 200):
            list_of_matched = []  # cleaning list
            tmp = cursor.execute(f'SELECT * FROM courses WHERE courseid = {i}')  # setting value of considered page
            desc = tmp.fetchone()

            #print(type(desc), desc[0], desc[1], desc[2], sep='\n')
            for match in parser1.findall(desc[2]):  # parsing
                list_of_matched.append(' '.join([activate(normalized(_.value)).value.pop()
                                                 if len(_.value) > 1 else '' for _ in match.tokens]))
            val = len(res.intersection(set(list_of_matched)))
            if val > len(list_of_matched)*0.1 and val > 1:  # checking if more than 10% of keywords are equal
                print(desc[1], '\n')  # name of course
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
    time.sleep(5)
conn.close()

