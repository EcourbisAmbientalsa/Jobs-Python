from datetime import date
import calendar


def quinto_dia_util(ano, mes):
    _, ultimo_dia = calendar.monthrange(ano, mes)

    contador = 0

    for dia in range(1, ultimo_dia + 1):
        data = date(ano, mes, dia)

        # ignora somente domingo
        if data.weekday() != 6:
            contador += 1

            if contador == 5:
                return data.strftime('%Y%m%d')


def primeiro_dia_mes_anterior(ano, mes):
    if mes == 1:
        return date(ano - 1, 12, 1).strftime('%Y%m%d')

    return date(ano, mes - 1, 1).strftime('%Y%m%d')


hoje = date.today()

data_inicio = primeiro_dia_mes_anterior(hoje.year, hoje.month)
data_fim = quinto_dia_util(hoje.year, hoje.month)

print(data_inicio)
print(data_fim)