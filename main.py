from datetime import date
from core.database import get_engine
from core.mailer import OutlookMailer
from core.envio_control import deve_enviar, marcar_enviado

from jobs.atestados_dia_util import AtestadosUtilJob


DESTINATARIOS = ["rgarcia@ecourbis.com.br"]
COPIA = ["llima@ecourbis.com.br", "gcalves@ecourbis.com.br", "bhora@ecourbis.com.br", "rribeiro@ecourbis.com.br"] 

def main():
    print("-> Verificando envio de Atestados...\n")

    if not deve_enviar("atestados"):
        print("Fora da janela (dia não útil ou já enviado neste mês). Nada a fazer.")
        return

    engine = get_engine()
    job = AtestadosUtilJob(engine)
    caminho = job.run()

    if not caminho:
        print("Relatório não gerado. Envio abortado.")
        return

    try:
        OutlookMailer().enviar(
            para=DESTINATARIOS,
            cc=COPIA or None,
            assunto=f"Relatório de Atestados - {date.today():%m/%Y}",
            corpo="""
                <p>Olá,</p>
                <p>Segue em anexo o relatório de atestados do período.</p>
                <p><em>Enviado automaticamente.</em></p>
            """,
            anexos=[caminho],
        )
        marcar_enviado("atestados")   # só marca se enviou sem erro
    except Exception as e:
        print(f"ERRO no envio: {e}")
        print("Não marcado — vai tentar de novo no próximo dia útil.")

    print("\n✔ Finalizado!")


if __name__ == "__main__":
    main()