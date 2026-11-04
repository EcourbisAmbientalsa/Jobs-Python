import sys

from core.database import get_engine
from core.executor import JobRunner
from core.checkDay import checkDay

from jobs.base_salarios import BaseSalariosJob
from jobs.absenteismo import ControleAbsenteismoJob
from jobs.atestados import AtestadosJob
from jobs.cat_emitidas import CatEmitidasJob
from jobs.horas_trabalhadas import HorasTrabalhadasJob
from jobs.exames_ocupacionais import ExamesOcupacionaisJob
from jobs.d2206 import D2206Job
from jobs.atestados_dia_util import AtestadosUtilJob

# def gerar_datas(inicio, fim):
#    data_atual = inicio
#
#   while data_atual <= fim:
#       yield data_atual
#       data_atual += timedelta(days=1)

def main():
    print("-> Iniciando jobs...\n")

    engine = get_engine()

    # ✅ CORRETO: converter string para datetime
    #
    #  data_inicio = datetime.strptime("2026-04-13", "%Y-%m-%d")

    # data_fim = datetime.now()

    jobs = [
        ControleAbsenteismoJob(engine),
        AtestadosJob(engine),
        BaseSalariosJob(engine),
        CatEmitidasJob(engine),
        ExamesOcupacionaisJob(engine),
        HorasTrabalhadasJob(engine),
    ]

    if checkDay():
        jobs.append(D2206Job(engine))

    if AtestadosUtilJob.should_run():
        jobs.append(AtestadosUtilJob(engine))

    runner = JobRunner(jobs)
    falhas = runner.run_all()

    if falhas:
        print(f"ERROR: {len(falhas)} job(s) falharam: {', '.join(falhas)}")
        return 1

    print("✔ Jobs finalizados!")
    return 0

if __name__ == "__main__":
    sys.exit(main())