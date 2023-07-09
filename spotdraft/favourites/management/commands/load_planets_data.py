import requests
from django.core.management.base import BaseCommand
from favourites.models import Movie, Planet
from django.core.management import execute_from_command_line

class Command(BaseCommand):
    def handle(self, *args, **options):
        base_url = "https://sw-api-rwjfuiltyq-el.a.run.app/api/planets/"
        next_page = base_url + "?page=1"

        while next_page:
            response = requests.get(next_page)
            data = response.json()
            results = data.get("results", [])

            for result in results:
                planet = Planet(
                    name=result["name"],
                    rotation_period=result["rotation_period"],
                    orbital_period=result["orbital_period"],
                    diameter=result["diameter"],
                    climate=result["climate"],
                    gravity=result["gravity"],
                    terrain=result["terrain"],
                    surface_water=result["surface_water"],
                    population=result["population"],
                    residents=", ".join(result["residents"]),
                    films=", ".join(result["films"]),
                    created=result["created"],
                    edited=result["edited"],
                    url=result["url"]
                )
                planet.save()

            next_page = data.get("next")

        self.stdout.write(self.style.SUCCESS("Planets data loaded successfully."))

if __name__ == "__main__":
    execute_from_command_line()