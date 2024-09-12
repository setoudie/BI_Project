# Creation d'un csv vendeur.csv --> (Name, Phone, Gender)

import csv
from faker import Faker
from numpy.ma.extras import unique

locales = [
    'en_US',  # États-Unis
    'fr_FR',  # France
    'es_ES',  # Espagne
]

nbre_vendeur = 10
fake = Faker(locale=locales)

with open('data/fake_seller.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Seller_id', 'FirstName', 'LastName', 'Phone', 'Gender'])

    for _ in range(nbre_vendeur):
        writer.writerow([
            f'S_{fake.random_int(min=1, max=1000)}',
            fake.first_name(),
            fake.last_name(),
            fake.phone_number(),
            fake.passport_gender()
        ])