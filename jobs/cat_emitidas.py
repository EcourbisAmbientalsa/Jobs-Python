from core.template import TemplateJob

class CatEmitidasJob(TemplateJob):

    def __init__(self, engine):
        super().__init__(
            engine,
            "Cat-Emitidas",
            base_path=r"C:\Users\llima\Desktop\Relatorios"
        )
    def get_query(self):
        return f"""
WITH CTE_CM0 AS (
    SELECT
        CM0_ID,
        CM0_DURTRA,
        CM0_TRABAL,
        CM0_FILIAL,
        CM0_DTRANS,
        CM0_HTRANS,
        CM0_PROTUL,
        CM0_DTACID,
        CM0_HRACID,
        CM0_CODSIT,
        CM0_DESLES,
        CM0_TIPACI,
        CM0_DIAPRO,
        CM0_CODCID,
        CM0_DINSIS,
        ROW_NUMBER() OVER (
            PARTITION BY CM0_TRABAL, CM0_FILIAL
            ORDER BY CM0_PROTUL DESC
        ) AS rn
    FROM CM0010
),

CTE_C9V AS (
    SELECT
        C9V_CPF,
        C9V_ID,
        C9V_FILIAL,
        C9V_NOME,
        ROW_NUMBER() OVER (
            PARTITION BY C9V_ID, C9V_FILIAL
            ORDER BY C9V_NOME
        ) AS rn
    FROM C9V010
),

CTE_CMM AS (
    SELECT
        CMM_ID,
        CMM_CODIGO,
        CMM_DESCRI,
        ROW_NUMBER() OVER (
            PARTITION BY CMM_ID
            ORDER BY CMM_CODIGO
        ) AS rn
    FROM CMM010
)

SELECT DISTINCT

    'ECOURBIS' AS Unidade,

    CM0.CM0_PROTUL AS [REGISTROINSS],

    CM0.CM0_DTACID AS [Data da Ocorrência],

    STUFF(CM0.CM0_HRACID, 3, 0, ':') AS [Hora da Ocorrência],

    C8I.C8I_CODIGO AS [CHAPA],

    C9V.C9V_NOME AS [Nome Funcionário],

    RJ.RJ_DESC AS [Função],

    CTT.CTT_DESC01 AS [Setor],

    CASE
        WHEN CM0.CM0_TIPACI = 1 THEN 'Acidente Tipico com Lesão'
        WHEN CM0.CM0_TIPACI = 2 THEN 'Doença'
        WHEN CM0.CM0_TIPACI = 3 THEN 'Acidente de Trajeto com Lesão'
    END AS [Tipo de Acidente],

    C8I.C8I_DESCRI AS [Partes Lesionadas],

    CM0.CM0_DIAPRO AS [Lesão],

    CMM.CMM_CODIGO AS [CID],

    CMM.CMM_DESCRI AS [Descrição CID],

    CM0.CM0_DURTRA AS [Duração Tratamento],

    CM0.CM0_DTRANS AS [Data Registro CAT],

    CM0.CM0_HTRANS AS [Hora Transmissão CAT],

    C8L.C8L_DESCRI AS [Nome da Ocorrência],

    CM0.CM0_DESLES AS [Desc Complementar da Lesão],

    SUBSTRING(CM0.CM0_DTACID, 1, 4) AS [Ano],

    SUBSTRING(CM0.CM0_DTACID, 5, 2) AS [Mês],

    CASE
        WHEN R6.R6_TURNO IN (
            '001','002','004','005','006','007','012','014','015',
            '022','033','036','039','040','041','042','047','089',
            '093','098','132','133','135','136','144','145','156',
            '185','187','195','200','204','210','215','238','243',
            '252','263','264','265','276','277','278','279','280',
            '281','282','283','284','285','286','316','319','320',
            '321','323','325','327','329','330','332','333','338',
            '342','343','348','352','356','357','358','359','360',
            '361','364','366','376','377','379','380','384','385',
            '387','388','389','390','391','392','394','397','398',
            '399','400','406','409','410','413','414','415','416',
            '417','422','424','425','426','427','428','432','433',
            '434','435','437','438','439'
        ) THEN 'MANHÃ'

        WHEN R6.R6_TURNO IN (
            '003','008','009','010','011','020','021','024','038',
            '043','077','078','087','102','189','190','191','192',
            '193','198','203','222','248','275','288','289','290',
            '291','292','293','294','295','296','297','298','299',
            '300','301','302','304','305','318','331','334','336',
            '340','349','351','355','367','368','369','370','371',
            '372','373','374','375','383','386','403','411','412',
            '420','421'
        ) THEN 'NOITE'

        WHEN R6.R6_TURNO IN (
            '023','027','028','029','030','076','083','085','090',
            '097','110','174','223','271','272','287','317','339',
            '341','382','393','396','401','402','404','405','407',
            '408','418','419','423','429','430','431','436'
        ) THEN 'TARDE'

        ELSE 'Inativo'
    END AS [Turno]

FROM CTE_CM0 CM0

INNER JOIN CM1010 CM1
    ON CM0.CM0_ID = CM1.CM1_ID
    AND CM0.CM0_FILIAL = CM1.CM1_FILIAL

INNER JOIN C8I010 C8I
    ON C8I.C8I_ID = CM1.CM1_CODPAR

INNER JOIN CTE_C9V C9V
    ON C9V.C9V_ID = CM0.CM0_TRABAL
    AND C9V.C9V_FILIAL = CM0.CM0_FILIAL
    AND C9V.rn = 1

INNER JOIN SRA010 RA
    ON C9V.C9V_CPF = RA.RA_CIC
    AND C9V.C9V_FILIAL = RA.RA_FILIAL
    AND RA.RA_DEMISSA = ''

INNER JOIN SR6010 R6
    ON R6.R6_TURNO = RA.RA_TNOTRAB

INNER JOIN SRJ010 RJ
    ON RJ.RJ_FUNCAO = RA.RA_CODFUNC
    AND C9V.C9V_FILIAL = CM0.CM0_FILIAL

INNER JOIN CTT010 CTT
    ON CTT.CTT_CUSTO = RA.RA_CC

INNER JOIN C8L010 C8L
    ON C8L.C8L_ID = CM0.CM0_CODSIT

INNER JOIN CTE_CMM CMM
    ON CMM.CMM_ID = CM0.CM0_CODCID
    AND CMM.rn = 1

WHERE
    CM0.rn = 1
    AND CM0.CM0_DINSIS >= CONVERT(VARCHAR, DATEADD(DAY, -1, GETDATE()), 112)
    AND CM0.CM0_DTRANS <> ' '

ORDER BY 
    [Data da Ocorrência], 
    Unidade, 
    [Data Registro CAT], 
    [Hora Transmissão CAT], 
    [REGISTROINSS], 
    [Hora da Ocorrência], 
    [CHAPA], 
    [Nome Funcionário], 
    [Função], 
    [Setor], 
    [Nome da Ocorrência], 
    [Desc Complementar da Lesão], 
    [Ano], 
    [Mês], 
    [Turno], 
    [Tipo de Acidente], 
    [Partes Lesionadas], 
    [Lesão], 
    [CID], 
    [Descrição CID], 
    [Duração Tratamento]
"""