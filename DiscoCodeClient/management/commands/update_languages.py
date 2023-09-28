import requests
from django.core.management.base import BaseCommand
from DiscoCodeClient.models import Language, Configuration

class Command(BaseCommand):
    help = 'Update Language models with Piston API runtimes'

    def handle(self, *args, **kwargs):
        
        config = Configuration.objects.first()
        Language.objects.update(is_enabled=False)

        response = requests.get(config.runtime_endpoint)
        if response.status_code == 200:
            language_list = response.json()

            if not isinstance(language_list, list):
                self.stdout.write(self.style.ERROR('Unexpected API response format'))
                return

            running_aliases = set()
            for lang_data in language_list:
                if not isinstance(lang_data, dict) or 'language' not in lang_data:
                    self.stdout.write(self.style.ERROR('Unexpected language data format'))
                    continue

                language_name = lang_data.get('language')
                language, created = Language.objects.get_or_create(language=language_name)
                
                aliases = lang_data.get('aliases', [])
                aliases.append(language_name)
                for alias in aliases:
                    if alias not in language.aliases and alias not in running_aliases and ' ' not in alias:
                        language.aliases.append(alias)
                        running_aliases.add(alias)

                language.version = lang_data.get('version')
                language.is_enabled = True
                
                language.save()

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Added new language: {language_name}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated language: {language_name}'))
            
            self.stdout.write(self.style.SUCCESS('Successfully updated languages'))