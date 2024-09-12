import csv
from faker import Faker
from seller import locales

nbre_clients = 2000
fake = Faker(locale=locales)

with open('data/fake_customer.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Cust_id', 'FirstName', 'LastName', 'Phone', 'Gender', 'Type'])

    for _ in range(nbre_clients):
        writer.writerow([
            f'C_{fake.random_int(min=1, max=1000)}',
            fake.first_name(),
            fake.last_name(),
            fake.phone_number(),
            fake.passport_gender(),
            fake.random_element(elements=('XXL', 'XL', 'L'))
        ])