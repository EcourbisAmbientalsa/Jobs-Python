import os
from pathlib import Path
from urllib.parse import quote_plus

from sqlalchemy import create_engine


def _load_env_values(env_path=None):
    env_path = Path(env_path) if env_path else Path(__file__).resolve().parents[1] / '.env'
    values = {}

    if env_path.exists():
        for raw_line in env_path.read_text(encoding='utf-8').splitlines():
            line = raw_line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue

            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            if key and value:
                values[key] = value

    for key in ('DB_SERVER', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_DRIVER'):
        if not values.get(key):
            env_value = os.getenv(key)
            if env_value:
                values[key] = env_value

    return values


def _get_db_config(env_path=None):
    values = _load_env_values(env_path)
    missing = [
        key for key in ('DB_SERVER', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_DRIVER')
        if not values.get(key)
    ]

    if missing:
        raise RuntimeError(
            'Configuração do banco ausente. Defina as variáveis DB_SERVER, DB_NAME, '
            'DB_USER, DB_PASSWORD e DB_DRIVER no arquivo .env ou no ambiente.'
        )

    return values


def build_connection_string(env_path=None):
    config = _get_db_config(env_path)
    return (
        f"DRIVER={{{config['DB_DRIVER']}}};"
        f"SERVER={config['DB_SERVER']};"
        f"DATABASE={config['DB_NAME']};"
        f"UID={config['DB_USER']};"
        f"PWD={config['DB_PASSWORD']};"
    )


def get_engine(env_path=None):
    conn_str = quote_plus(build_connection_string(env_path))
    return create_engine(f'mssql+pyodbc:///?odbc_connect={conn_str}')