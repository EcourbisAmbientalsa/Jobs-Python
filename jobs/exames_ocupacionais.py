from core.template import TemplateJob

class ExamesOcupacionaisJob(TemplateJob):

    def __init__(self, engine):
        super().__init__(
            engine,
            "Exames-Ocupacionais",
            base_path=r"C:\Users\llima\Desktop\Relatorios"
        )

    def get_query(self):
        return f"""SELECT (SELECT CASE
                   WHEN TMY_NATEXA = '1' THEN 'Admissional'
                   when TMY_NATEXA = '2' then 'Periodico'
                   when TMY_NATEXA = '3' then 'Mudança de Riscos Ocupacionais'
                   WHEN TMY_NATEXA = '4' THEN 'Retorno ao trabalho'
                   WHEN TMY_NATEXA = '5' THEN 'Demissional'
                   WHEN TMY_NATEXA = '6'
                       THEN 'Monitoração Pontual' end) as 'TIPO', (SELECT CASE WHEN TMY_INDPAR = '1' THEN 'Normal' Else 'Anormal' end) as 'RESULTADO',
    (CASE
         WHEN TMY_NATEXA = '1' THEN 'Admissional'
         WHEN TMY_NATEXA = '2' THEN 'Periodico'
         WHEN TMY_NATEXA = '3' THEN 'Mudança de Riscos Ocupacionais'
         WHEN TMY_NATEXA = '4' THEN 'Retorno ao trabalho'
         WHEN TMY_NATEXA = '5' THEN 'Demissional'
         WHEN TMY_NATEXA = '6' THEN 'Monitoração Pontual' END) + '-' +
    (CASE WHEN TMY_INDPAR = '1' THEN 'Normal' ELSE 'Anormal' END) AS 'TIPO_RESULTADO', 'EXAME CLÍNICO' AS 'NOMEEXAME', RA_MAT 'CODPESSOA', TMY_FILIAL 'CODFILIAL', '999999' 'CHAPA',
       FORMAT(CONVERT(DATE, TMY_DTGERA), 'dddd, d \de MMMM \de yyyy', 'pt-BR') 'DT_COMPETENCIA'
FROM TMY010
         INNER JOIN TM0010 ON TM0_NUMFIC = TMY_NUMFIC AND TM0_FILIAL = TMY_FILIAL
         INNER JOIN SRA010 ON RA_MAT = TM0_MAT AND RA_FILIAL = TM0_FILIAL
WHERE TMY_DTGERA >= CONVERT(VARCHAR, DATEADD(DAY, -1, GETDATE()), 112)
  and TMY010.D_E_L_E_T_ = ''
  and TM0010.D_E_L_E_T_ = ''
        """