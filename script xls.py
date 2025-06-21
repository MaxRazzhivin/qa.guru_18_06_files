from xlrd import open_workbook

workbook = open_workbook("путь к файлу xls")

print(workbook.nsheets)
print(workbook.sheet_names())

sheet = workbook.sheet_by_index(0)

print(sheet.nrows)
print(sheet.ncols)
print(sheet.cell_value(colx=3, rowx=9))

for rx in range(sheet.nrows):
    print(sheet.row(rx))