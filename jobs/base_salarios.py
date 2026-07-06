from core.template import TemplateJob

class BaseSalariosJob(TemplateJob):

    def __init__(self, engine):
        def __init__(self, engine):
            super().__init__(
                engine,
                "Base-Salários",
                base_path=r"C:\Users\llima\Desktop\Relatorios"
            )
    def get_query(self):
        return f"""
            SELECT DISTINCT
        RA_FILIAL,
        (SELECT RJ_DESC FROM SRJ010 WHERE RJ_FUNCAO = RA_CODFUNC) AS 'FUNÇÃO',
        RA_CODFUNC,
        'R$ ' + CAST(RA_SALARIO AS VARCHAR) AS RA_SALARIO,
        RA_SALARIO / 30 AS 'Salario/30'
    FROM SRA010
    WHERE RA_DEMISSA = ''
    AND RA_MAT IN (SELECT TNY_MAT FROM TNY010 WHERE TNY_DTINIC >= CONVERT(VARCHAR, DATEADD(DAY, 1, GETDATE()), 112) AND TNY_DTINIC <= CONVERT(VARCHAR, GETDATE(), 112) AND D_E_L_E_T_ = '')
    ORDER BY 'FUNÇÃO'
           """