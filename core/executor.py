import traceback

from tqdm import tqdm


class JobRunner:
    def __init__(self, jobs):
        self.jobs = jobs

    def run_all(self):
        """Executa todos os jobs e retorna a lista com os nomes dos que falharam."""
        falhas = []
        with tqdm(self.jobs, desc="Executando jobs", ncols=100) as bar:
            for job in bar:
                try:
                    job.run()
                except Exception as e:
                    nome = job.__class__.__name__
                    falhas.append(nome)
                    print(f"ERROR: Erro em {nome}: {e}")
                    traceback.print_exc()
        return falhas
