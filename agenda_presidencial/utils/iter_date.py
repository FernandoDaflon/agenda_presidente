from datetime import date, timedelta

# hj = date.today()
# dia = hj.day + 1
# mes = hj.month
# ano = hj.year


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)



# start_date = date(2019, 1, 1)
# end_date = date(ano, mes, dia)
# for single_date in daterange(start_date, end_date):
#     print(single_date.strftime("%Y-%m-%d"))