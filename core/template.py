import pandas as pd
from datetime import datetime, timedelta
import os
import sys


class TemplateJob:
    def __init__(self, engine, nome_arquivo, base_path=None):

        self.engine = engine
        self.nome_arquivo = nome_arquivo
        self.base_path = base_path

        self.data_execucao = datetime.now()

    def get_query(self):
        raise NotImplementedError("Implemente o método get_query()")

    def run(self):
        consulta_sql = self.get_query()

        df = pd.read_sql_query(consulta_sql, self.engine)

        data_str = self.data_execucao.strftime("%d-%m-%Y")

        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.getcwd()

        if self.base_path:
            base_path = self.base_path
        else:
            base_path = os.path.join(base_dir, "Relatorios")

        caminho = os.path.join(base_path, self.nome_arquivo)

        os.makedirs(caminho, exist_ok=True)

        arquivo = os.path.join(
            caminho,
            f"{self.nome_arquivo}_{data_str}.xlsx"
        )

        df.to_excel(arquivo, index=False)

        print(f"✔ Relatório gerado: {arquivo}")