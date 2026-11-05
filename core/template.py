import pandas as pd
from datetime import datetime, timedelta
import os

from core.database import _load_env_values


class TemplateJob:
    """
    As pastas de saída são configuradas SOMENTE no .env (ou variável de ambiente):
      - RELATORIOS_PATH      -> jobs principais (pasta_do_dia=True)
            <RELATORIOS_PATH>\\aaaammdd(D-1)\\<nome>_aaaammdd.xlsx
      - D2206_PATH, ATESTADOS_UTIL_PATH, ... -> jobs com pasta própria (pasta_do_dia=False)
            <PASTA>\\<nome>_aaaammdd.xlsx
    """

    def __init__(self, engine, nome_arquivo,
                 pasta_do_dia=True, env_path_key="RELATORIOS_PATH"):

        self.engine = engine
        self.nome_arquivo = nome_arquivo
        self.pasta_do_dia = pasta_do_dia
        self.env_path_key = env_path_key

        self.data_execucao = datetime.now()

    def get_query(self):
        raise NotImplementedError("Implemente o método get_query()")

    def _resolver_base_path(self):
        caminho = os.getenv(self.env_path_key) or _load_env_values().get(self.env_path_key)
        if not caminho:
            raise RuntimeError(
                f"Pasta de saída não configurada: defina {self.env_path_key} no arquivo .env"
            )
        return caminho

    def run(self):
        consulta_sql = self.get_query()

        df = pd.read_sql_query(consulta_sql, self.engine)

        data_str = self.data_execucao.strftime("%Y%m%d")

        caminho = self._resolver_base_path()
        if self.pasta_do_dia:
            # A pasta dos jobs principais leva a data do dia anterior (D-1).
            data_pasta = (self.data_execucao - timedelta(days=1)).strftime("%Y%m%d")
            caminho = os.path.join(caminho, data_pasta)

        os.makedirs(caminho, exist_ok=True)

        arquivo = os.path.join(caminho, f"{self.nome_arquivo}_{data_str}.xlsx")

        df.to_excel(arquivo, index=False)

        print(f"Relatorio gerado: {arquivo}")
