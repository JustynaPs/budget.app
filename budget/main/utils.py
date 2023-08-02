from django.contrib.auth.models import User
from .models import Categories


# def create_default_categories():
#     default_categories = [
#         {'name': 'Przychody'},
#         {'name': 'Żywność'},
#         {'name': 'Transport'},
#         {'name': 'Podatki i opłaty'}
#     ]
#
#     for category_data in default_categories:
#         category, created = Categories.objects.get_or_create(**category_data, user_id=None)
#         if created:
#             print(f'Created default category: {category.name}')


def create_default_categories(user):
    default_categories = [
        {'name': 'Przychody', 'is_default': True},
        {'name': 'Żywność', 'is_default': True},
        {'name': 'Transport', 'is_default': True},
        {'name': 'Podatki i opłaty', 'is_default': True}
    ]

    for category_data in default_categories:
        category, created = Categories.objects.get_or_create(name=category_data['name'],  user_id=user.id, defaults={'user_id': user})
        # category, created = Categories.objects.get_or_create(name=category_data['name'],  user_id=user.id)
        # category, created = Categories.objects.get_or_create(name=category_data['name'],  user_id=user.id, defaults={'user_id': None})
        if created:
            if 'is_default' in category_data and category_data['is_default']:
                category.is_default = True
                category.save()
            print(f'Created default category: {category.name}')