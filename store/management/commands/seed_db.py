from django.core.management.base import BaseCommand
from django.db import connection
from pathlib import Path
import os

class Command(BaseCommand):
    help = "Populates database with collection and products from seed.sql"

    def handle(self, *args, **options): 
        print('Populates the database...')
        current_dir = os.path.dirname(__file__)
        file =  os.path.join(current_dir, 'seed.sql')
        sql = Path(file).read_text()
        
        with connection.cursor() as cursor:
            cursor.execute(sql)