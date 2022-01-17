import es

searcher = es.Searcher("C:\\Users\\egor\\Desktop\\test_bot\\animes_base.xls")

print(searcher.get_res(["Драма", "Комедия", "Фантастика"]))
