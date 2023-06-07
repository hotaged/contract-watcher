
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="CW",
    settings_files=['settings.json', '.secrets.json'],
)

TORTOISE_ORM = {
    "connections": {"default": settings.database_url},
    "apps": {
        "models": {
            "models": ["contract_watcher.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
