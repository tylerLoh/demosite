# demosite
Workout for basic Django web framework using PyCharm

### Dependencies
- python > 3.6
- Django 2.2.8

### Docstring format
NumPy/SciPy

### PREREQUISITE
- Create superusers for admin panel
1) pip install -r requirements.txt
2) python manage.py makemigrations items
3) python manage.py makemigrations vouchers
4) python manage.py migrate
5) python manage.py create_vouchers
6) python manage.py create_items 10
7) python manage.py runserver
8) sample voucher code = TREATM00001, PRODU00001

### TEST
python manage.py test vouchers

### TODO
- [x] Restructure follow PEP8 standard
- [x] Add docstring
- [x] Add respond 404, 400 page
- [x] Add unittest for vouchers redemption
- [] 
- [] Add advance testing
- [] Custom ModelAdmin view with timestamp validation