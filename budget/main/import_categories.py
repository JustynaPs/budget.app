# import json
# from django.contrib.auth.models import User
# from main.models import Categories
#
# def import_categories_from_json():
#     with open(r'C:\Users\juzus\PycharmProjects\budget_app\budget\main\fixtures\categories.json', 'r') as json_file:
#         categories_data = json.load(json_file)
#
#         for category_data in categories_data:
#             category_name = category_data['fields']['name']
#             user_id = category_data['fields']['user_id']
#
#             if user_id is None:
#                 # Jeśli user_id jest None, przypisz kategorię do wszystkich użytkowników
#                 users = User.objects.all()
#                 for user in users:
#                     Categories.objects.create(name=category_name, user_id=user.id)
#             else:
#                 # Jeśli user_id jest określone, przypisz kategorię tylko do tego użytkownika
#                 user = User.objects.get(id=user_id)
#                 Categories.objects.create(name=category_name, user_id=user.id)
#
#         print('Import completed successfully.')
#
# import_categories_from_json()