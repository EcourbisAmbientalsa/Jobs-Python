from datetime import datetime
import holidays

def checkDay():
    hoje = datetime.now()

    if hoje.weekday() == 4:
        return True
    else:
        return False


feriados_sp = holidays.Brazil(state="SP", years=range(2026,2030))

print(feriados_sp)

# só as datas (pra usar em comparações)
lista_datas = sorted(feriados_sp.keys())

feriados_formatados = [
    f"{data.strftime('%d/%m/%Y')} - {nome}"
    for data, nome in sorted(feriados_sp.items())
]