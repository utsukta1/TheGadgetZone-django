from django.test import TestCase
from django.db import models
# Create your tests here.
import csv
from .models import Product
from django.utils.text import slugify
import random
from category.models import Category
def generate_random_price(min_price, max_price):
    price = random.uniform(min_price, max_price)
    return round(price, 2)  # Round to 2 decimal places

def import_csv_data(file_path):
    string_list = ['Television', 'Mobile Phones', 'Vacuum Cleaner', 'Camera','Computer and Laptops','Refrigirator']
    categories = Category.objects.all()
    with open(file_path, 'r') as file:
        i=0
        csv_data = csv.DictReader(file)
        for row in csv_data:
            if i < 30:
                person = Product(
                    product_name = row['name'],
                    slug = convert_to_slug(row['name']),
                    description = row['reviews.text'],
                    price = generate_random_price(200, 100000),
                    images = row['imageURLs'],
                    stock = generate_random_price(1, 100),
                    is_available = True,
                    category = random.choice(categories),
                    created_date = row['dateAdded'],
                    modified_date = row['dateUpdated'],
                )
                print("Data Added")
                i=i+1
                print(i)
                
                person.save()

def convert_to_slug(name):
    slug = slugify(name)
    print("SLUG")
    print(slug)
    return slug