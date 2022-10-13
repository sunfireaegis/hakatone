from yargy import rule, Parser
from yargy.predicates import gram, dictionary, normalized
from yargy.pipelines import morph_pipeline
from yargy.predicates.bank import activate
from openpyxl import load_workbook


R1 = rule(gram('ADJF').optional(), gram('NOUN'))  # rule searching all key pairs ADJECTIVE NOUN
parser = Parser(R1)

comps = load_workbook('competences.xlsx')  # opening xlsx table as data source
first = comps['Лист1']
c = int(input())
print(first[f'B{c}'].value)
text = first[f'C{c}'].value

res = set()
for item in parser.findall(text):  # getting simple 'keywords' from table cell
    res.add(' '.join([activate(normalized(_.value)).value.pop() for _ in item.tokens]))
print(res)

R2 = morph_pipeline(list(res))  # rule searching matches by keywords in desc
parser1 = Parser(R2)

courses = load_workbook('courses.xlsx')  # loading page with courses' descriptions
page = courses['Описание курсов']

# we need to normalise the keywords in list_of_matched for better matching and reformat the whole script to single class
def find_all_courses() -> set:
    list_of_matched, names = [], []  # resulting list
    for i in range(2, 500):
        list_of_matched.clear()  # cleaning list
        desc = page[f'B{i}'].value  # setting value of considered page

        for match in parser1.findall(desc):  # parsing
            list_of_matched.append(' '.join([_.value if len(_.value) > 1 else '' for _ in match.tokens]))

        val = len(res.intersection(list_of_matched)) > len(list_of_matched)//10
        if len(res.intersection(list_of_matched)) > len(list_of_matched)//10:  # checking if more than 20% of keywords are equal
            # print(list_of_matched)
            print(page[f'A{i}'].value)  # name of course
            names.append(page[f'A{i}'].value)


        # print(len(res.intersection(list_of_matched)) > len(res)//10)
        # print(page[f'A{i}'].value)  # name of course

    return set(names)  # returning set of names

print(find_all_courses())