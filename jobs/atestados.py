from core.template import TemplateJob
from core.database import get_engine


class AtestadosJob(TemplateJob):

    def __init__(self, engine):
        super().__init__(
            engine,
            "Atestados",
            base_path=r"C:\Users\llima\Desktop\Relatorios"
        )

    def get_query(self):
        return """
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
        )
        
        SELECT
            TNY.TNY_FILIAL AS [Filial],
            TNY.TNY_NUMFIC AS [Ficha Med],
            TM0.TM0_NOMFIC AS [Nome],
        
            SRJ.RJ_DESC AS [Descricao Func],
            CTT.CTT_DESC01 AS [Descr C/Custo],
            SRA.RA_CC AS [Centro Custo],
        
            SRA.RA_CIC AS [CPF],
            TM0.TM0_MAT AS [Matricula],
            SRA.RA_NOME AS [Funcionario],
        
            SRA.RA_TNOTRAB AS [Cod.Turno],
        
            CASE
                WHEN LTRIM(RTRIM(SRA.RA_SITFOLH)) = '' THEN 'ATIVO'
                WHEN LTRIM(RTRIM(SRA.RA_SITFOLH)) = 'F' THEN 'FÉRIAS'
                WHEN LTRIM(RTRIM(SRA.RA_SITFOLH)) IN ('30', '31') THEN 'TRANSFERIDO'
                WHEN LTRIM(RTRIM(SRA.RA_SITFOLH)) = 'D' THEN 'DESLIGADO'
                WHEN LTRIM(RTRIM(SRA.RA_SITFOLH)) = 'A' THEN 'AFASTADO'
                ELSE LTRIM(RTRIM(SRA.RA_SITFOLH))
            END AS [Situação],
        
            CONVERT(VARCHAR(10), CONVERT(DATE, TNY.TNY_DTINIC, 112), 103) AS [Inic. Afast.],
            TNY.TNY_QTDIAS AS [Qt.Dias Af],
            CONVERT(VARCHAR(10), CONVERT(DATE, TNY.TNY_DTFIM, 112), 103) AS [Data Fim],
        
            TNY.TNY_CID AS [CID Princip.],
            TNY.TNY_EMITEN AS [Emit. Atest.],
            TNP.TNP_NOME AS [Nome Médico],
        
            NULLIF(LTRIM(RTRIM(TNY.TNY_ENDERE)), '') AS [Loc.Emit.At.],
        
            TNY.TNY_QTDIAS AS [Dias Afast.],
        
            CASE
                WHEN LTRIM(RTRIM(SRA.RA_FILIAL)) = '1' THEN 'Op.Sul'
                WHEN LTRIM(RTRIM(SRA.RA_FILIAL)) = '2' THEN 'Leste'CNTA121
                ELSE LTRIM(RTRIM(SRA.RA_FILIAL))
            END AS [Unidade],
        
            CASE 
                WHEN LTRIM(RTRIM(TNY.TNY_TPEFD)) IN ('1', '01') THEN 'Atestado'
                WHEN LTRIM(RTRIM(TNY.TNY_TPEFD)) IN ('2', '02') THEN 'Ponto Eletrônico'
                WHEN LTRIM(RTRIM(TNY.TNY_TPEFD)) IN ('3', '03') THEN 'Afastamento'
                ELSE LTRIM(RTRIM(TNY.TNY_TPEFD))
            END AS [Mot. Afast]
        
        FROM TNY_BASE TNY
        
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
            AND TNY.TNY_DTINIC IS NOT NULL
            AND TNY.TNY_DTFIM IS NOT NULL
        
            AND TNY.TNY_DTINIC >= '20210101'
            AND TNY.TNY_DTINIC <= CONVERT(VARCHAR, GETDATE(), 112)
        
        ORDER BY
            TNY.TNY_FILIAL,
            TM0.TM0_MAT,
            TNY.TNY_DTINIC
        """


if __name__ == "__main__":
    print("-> Iniciando relatório de Atestados...")

    engine = get_engine()

    job = AtestadosJob(engine)
    job.run()

    print("✔ Relatório finalizado!")