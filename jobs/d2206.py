from core.template import TemplateJob
from datetime import datetime


class D2206Job(TemplateJob):
    def __init__(self, engine):
        super().__init__(
            engine,
            "Relatorio_2206",
            pasta_do_dia=False,
            env_path_key="D2206_PATH",
        )

    def get_query(self):
        return """
        SELECT
            T1V_FILIAL,
            T1V_MATRIC,
            T1V_CPF,
            T1V_NOME,
            T1V_NMCARG AS FUNCAO,
            T1V_VLSLFX,
            T1V_DTALT,
            T1V_DESALT
        FROM T1V010
        WHERE
            D_E_L_E_T_ = ' '
            AND T1V_STATUS = ' '
            AND T1V_DTALT >= CONCAT(YEAR(GETDATE()),'0101')
        ORDER BY
            T1V_FILIAL,
            T1V_NOME
        """