from core.template import TemplateJob
from datetime import datetime


class D2206Job(TemplateJob):
    def __init__(self, engine):

        data_atual = datetime.now().strftime("%d-%m-%Y")

        super().__init__(
            engine,
            "Relatorio_2206",
            base_path=r"C:\Users\llima\Desktop\Relatorios",
            subpastas=[
                "Relatorios Semanais",
                "Relatorio_2206"
            ]
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