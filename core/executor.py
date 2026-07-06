from tqdm import tqdm
''
class JobRunner:
    def __init__(self, jobs):
        self.jobs = jobs

    def run_all(self):
        with tqdm(self.jobs, desc="Executando jobs", ncols=100) as bar:
            for job in bar:
                try:
                    job.run()
                except Exception as e:
                    print(f"ERROR: Erro em {job.__class__.__name__}: {e}")