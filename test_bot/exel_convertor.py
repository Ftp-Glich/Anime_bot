import xlsxwriter
from dict import Dictionary

animes = Dictionary()

workbook = xlsxwriter.Workbook('animes_base.xlsx')

worksheet = workbook.add_worksheet()

num = 0

dicts = animes.get_animes()


def write_mass(array):
    res = ""
    for j in array:
        res += j + ", "
    return res


for dictionary in dicts:
    for i in dictionary.keys():
        if i[0] == "n":
            worksheet.write_row(num, 0, dictionary[i])
        elif i[0] == "h":
            worksheet.write_url(num, 1, dictionary[i])
        else:
            worksheet.write_string(num, 2, write_mass(dictionary[i]))
    num += 1

workbook.close()
