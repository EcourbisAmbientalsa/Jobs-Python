from core.template import TemplateJob

class ControleAbsenteismoJob(TemplateJob):
    def __init__(self, engine):
        super().__init__(
            engine,
            "Controle_Absenteismo",
            base_path=r"C:\Users\llima\Desktop\Relatorios"
        )
    def get_query(self):
        return f"""SELECT RA_CODFUNC 'Código da Função'
	, (SELECT RJ_DESC FROM SRJ010 WHERE RA_CODFUNC = RJ_FUNCAO) 'Função'
	, RA_CC 'Código do centro de custo'
	, (SELECT TOP 1 CTT_DESC01
       FROM CTT010
       WHERE CTT_CUSTO = (SELECT TOP 1 RA_CC
                          FROM SRA010
                          WHERE RA_MAT = (SELECT TM0_MAT
                                          FROM TM0010
                                          WHERE TM0_NUMFIC = TNY_NUMFIC
                                            AND TM0_FILIAL = TNY_FILIAL)
                            AND (SELECT TM0_MAT
                                 FROM TM0010
                                 WHERE TM0_NUMFIC = TNY_NUMFIC
                                   AND TM0_FILIAL = TNY_FILIAL)
                              <> '')) 'Desc centro de custo'
	, CONVERT(VARCHAR, CONVERT(DATE, RA_ADMISSA, 112), 103) 'Data de Admissão'
	, DATEDIFF(YEAR, RA_NASC, GETDATE()) AS 'Idade'
	, (SELECT X5_DESCRI FROM SX5010 WHERE X5_TABELA = '30' AND X5_CHAVE = TNY_TIPAFA) 'Tipo de Afastamento'
	, TNY_CID 'CID'
	, (SELECT CASE WHEN TNY_CID = '' THEN '' ELSE (SELECT TMR_DOENCA FROM TMR010 WHERE TMR_CID = TNY_CID) END) AS 'Descrição do CID'
	, TNY_DTINIC 'Data Inicio'
	, TNY_DTFIM 'Data Fim'
	, TNY_QTDIAS 'Dias de Atestado'
	, TNY_HRINIC 'Hora Inicio'
	, TNY_HRFIM 'Hora Final'
	, 'N/A' AS 'Previsão de Termino'
	, 'N/A' AS 'Avaliação de Retorno' 
	, 'N/A' AS 'Data da pericia' 
	, 'ECOURBIS' AS Entidade
     , (SELECT TNP_NOME FROM TNP010 WHERE TNY_EMITEN = TNP_EMITEN) AS Médico
     , TRIM((SELECT TNP_NUMENT FROM TNP010 WHERE TNY_EMITEN = TNP_EMITEN)) +
       (SELECT TNP_UF FROM TNP010 WHERE TNY_EMITEN = TNP_EMITEN)
    as 'CRM/UF'
FROM TNY010
         INNER JOIN TM0010 ON TM0_NUMFIC = TNY_NUMFIC AND TM0_FILIAL = TNY_FILIAL
         INNER JOIN SRA010 ON RA_MAT = TM0_MAT AND RA_FILIAL = TM0_FILIAL
WHERE TNY_DTINIC >= CONVERT(VARCHAR, DATEADD(DAY, -1, GETDATE()), 112)
  AND TM0010.D_E_L_E_T_ = ''
  AND TNY010.D_E_L_E_T_ = ''
"""