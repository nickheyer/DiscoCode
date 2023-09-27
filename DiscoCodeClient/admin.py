from django.contrib import admin
from DiscoCodeClient.models import (
    Configuration,
    State,
    ErrLog,
    EventLog,
    User,
    DiscordServer,
    Language
)

models_to_register = [
    Configuration,
    State,
    ErrLog,
    EventLog,
    User,
    DiscordServer,
    Language
]

for model in models_to_register:
    admin.site.register(model)