import json
from datetime import date
from pathlib import Path
import holidays

# arquivo de estado na raiz do projeto
STATE_FILE = Path(__file__).resolve().parents[1] / "envio_state.json"


def eh_dia_util(dia=None):
    dia = dia or date.today()
    feriados = holidays.Brazil(state="SP", years=dia.year)
    return dia.weekday() < 5 and dia not in feriados


def competencia_atual(hoje=None):
    hoje = hoje or date.today()
    return f"{hoje.year}-{hoje.month:02d}"  


def _ler_estado():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _salvar_estado(estado):
    STATE_FILE.write_text(
        json.dumps(estado, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def deve_enviar(job_key, hoje=None):
    """True se hoje é dia útil E a competência atual ainda não foi enviada."""
    hoje = hoje or date.today()
    if not eh_dia_util(hoje):
        return False
    return _ler_estado().get(job_key) != competencia_atual(hoje)


def marcar_enviado(job_key, hoje=None):
    estado = _ler_estado()
    estado[job_key] = competencia_atual(hoje)
    _salvar_estado(estado)