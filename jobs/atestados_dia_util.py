from datetime import date, datetime
from core.calc_dia_util import quinto_dia_util
from core.template import TemplateJob
from core.database import get_engine


def primeiro_dia_mes_anterior(ano, mes):
    if mes == 1:
        return date(ano - 1, 12, 1).strftime("%Y%m%d")

    return date(ano, mes - 1, 1).strftime("%Y%m%d")


def normalizar_data_protheus(valor):
    """
    Garante que a data usada no filtro fique no formato YYYYMMDD.
    Serve caso a função quinto_dia_util retorne date/datetime ou string.
    """
    if isinstance(valor, (date, datetime)):
        return valor.strftime("%Y%m%d")

    return str(valor).strip()


class AtestadosUtilJob(TemplateJob):
    def __init__(self, engine):
        super().__init__(
            engine,
            "Atestados-Dia-útil",
            base_path=r"C:\Users\llima\Desktop\Relatorios"
        )

    @staticmethod
    def should_run():
        hoje = date.today()
        return hoje.strftime("%Y%m%d") == quinto_dia_util(hoje.year, hoje.month)

    def get_query(self):
        hoje = date.today()

        data_inicio = primeiro_dia_mes_anterior(hoje.year, hoje.month)
        data_fim = normalizar_data_protheus(
            quinto_dia_util(hoje.year, hoje.month)
        )

        return f"""
        WITH TNY_BASE AS (
            SELECT
                TNY_FILIAL,
                TNY_NUMFIC,
                TNY_DTINIC,
                TNY_QTDIAS,
                TNY_DTFIM,
                TNY_CID,
                TNY_EMITEN,
                TNY_ENDERE,
                TNY_TPEFD,
                D_E_L_E_T_
            FROM TNY010

            UNION ALL

            SELECT
                TNY_FILIAL,
                TNY_NUMFIC,
                TNY_DTINIC,
                TNY_QTDIAS,
                TNY_DTFIM,
                TNY_CID,
                TNY_EMITEN,
                TNY_ENDERE,
                TNY_TPEFD,
                D_E_L_E_T_
            FROM TNY020
        ),

        TNY_TRATADO AS (
            SELECT
                *,

                TRY_CONVERT(
                    DATE,
                    NULLIF(LTRIM(RTRIM(CAST(TNY_DTINIC AS VARCHAR(20)))), ''),
                    112
                ) AS DT_INICIO,

                TRY_CONVERT(
                    DATE,
                    NULLIF(LTRIM(RTRIM(CAST(TNY_DTFIM AS VARCHAR(20)))), ''),
                    112
                ) AS DT_FIM_RAW,

                TRY_CONVERT(
                    INT,
                    TRY_CONVERT(
                        NUMERIC(18, 2),
                        NULLIF(LTRIM(RTRIM(CAST(TNY_QTDIAS AS VARCHAR(20)))), '')
                    )
                ) AS QT_DIAS_RAW,

                RIGHT(
                    '00' + LTRIM(RTRIM(CAST(TNY_TPEFD AS VARCHAR(10)))),
                    2
                ) AS TIPO_AFAST

            FROM TNY_BASE
        ),

        TNY_CALCULADO AS (
            SELECT
                *,

                CASE
                    WHEN DT_FIM_RAW IS NOT NULL
                        THEN DT_FIM_RAW

                    WHEN ISNULL(QT_DIAS_RAW, 0) > 0
                         AND DT_INICIO IS NOT NULL
                        THEN DATEADD(DAY, QT_DIAS_RAW - 1, DT_INICIO)

                    WHEN DT_INICIO IS NOT NULL
                        THEN DT_INICIO

                    ELSE NULL
                END AS DT_FIM_CALCULADA

            FROM TNY_TRATADO
        ),

        TNY_FINAL AS (
            SELECT
                *,

                CASE
                    WHEN ISNULL(QT_DIAS_RAW, 0) > 0
                        THEN QT_DIAS_RAW

                    WHEN DT_INICIO IS NOT NULL
                         AND DT_FIM_CALCULADA IS NOT NULL
                         AND DT_FIM_CALCULADA >= DT_INICIO
                        THEN DATEDIFF(DAY, DT_INICIO, DT_FIM_CALCULADA) + 1

                    WHEN DT_INICIO IS NOT NULL
                        THEN 1

                    ELSE 0
                END AS DIAS_AFAST_CALCULADO

            FROM TNY_CALCULADO
        )

        SELECT
            TNY.TNY_FILIAL AS [Filial],
            TNY.TNY_NUMFIC AS [Ficha Med],
            TM0.TM0_NOMFIC AS [Nome],

            SRJ.RJ_DESC AS [Descricao Func],
            CTT.CTT_DESC01 AS [Descr C/Custo],
            SRA.RA_CC AS [Centro Custo],

            TM0.TM0_MAT AS [Matricula],
            SRA.RA_TNOTRAB AS [Cod.Turno],

            CONVERT(VARCHAR(10), TNY.DT_INICIO, 103) AS [Inic. Afast.],

            TNY.DIAS_AFAST_CALCULADO AS [Qt.Dias Af],

            CONVERT(VARCHAR(10), TNY.DT_FIM_CALCULADA, 103) AS [Data Fim],

            TNY.TNY_CID AS [CID Princip.],
            TNY.TNY_EMITEN AS [Emit. Atest.],
            TNP.TNP_NOME AS [Nome Médico],

            NULLIF(LTRIM(RTRIM(TNY.TNY_ENDERE)), '') AS [Loc.Emit.At.],

            TNY.DIAS_AFAST_CALCULADO AS [Dias Afast.],

            CASE
                WHEN LTRIM(RTRIM(SRA.RA_FILIAL)) = '1' THEN 'Op.Sul'
                WHEN LTRIM(RTRIM(SRA.RA_FILIAL)) = '2' THEN 'Leste'
                ELSE LTRIM(RTRIM(SRA.RA_FILIAL))
            END AS [Unidade],

            CASE 
                WHEN TNY.TIPO_AFAST = '01' THEN 'Atestado'
                WHEN TNY.TIPO_AFAST = '02' THEN 'Ponto Eletrônico'
                WHEN TNY.TIPO_AFAST = '03' THEN 'Afastamento'
                ELSE ''
            END AS [Mot. Afast]

        FROM TNY_FINAL TNY

            LEFT JOIN TM0010 TM0
                ON  TM0.TM0_NUMFIC = TNY.TNY_NUMFIC
                AND TM0.TM0_FILIAL = TNY.TNY_FILIAL
                AND TM0.D_E_L_E_T_ = ''

            LEFT JOIN SRA010 SRA
                ON  SRA.RA_FILIAL = TM0.TM0_FILIAL
                AND SRA.RA_MAT = TM0.TM0_MAT
                AND SRA.D_E_L_E_T_ = ''

            LEFT JOIN SRJ010 SRJ
                ON  SRJ.RJ_FUNCAO = SRA.RA_CODFUNC
                AND SRJ.D_E_L_E_T_ = ''

            LEFT JOIN CTT010 CTT
                ON  CTT.CTT_CUSTO = SRA.RA_CC
                AND CTT.D_E_L_E_T_ = ''

            LEFT JOIN TNP010 TNP
                ON  TNP.TNP_EMITEN = TNY.TNY_EMITEN
                AND TNP.D_E_L_E_T_ = ''

        WHERE
            TNY.D_E_L_E_T_ = ''
            AND TNY.DT_INICIO IS NOT NULL

            AND TNY.DT_INICIO >= TRY_CONVERT(DATE, '{data_inicio}', 112)
            AND TNY.DT_INICIO <= TRY_CONVERT(DATE, '{data_fim}', 112)

        ORDER BY
            TNY.TNY_FILIAL,
            TM0.TM0_MAT,
            TNY.DT_INICIO
        """


if __name__ == "__main__":
    print("-> Iniciando relatório de Atestados...")

    engine = get_engine()

    job = AtestadosUtilJob(engine)
    job.run()

    print("✔ Relatório finalizado!")