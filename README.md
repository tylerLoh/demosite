# demosite
Workout for basic Django web framework

### Dependencies
python > 3.6
Django 3.0.1

### PREREQUISITE
* Create superusers for admin panel
1) pip install -r requirements.txt
2) python manage.py makemigrations items
3) python manage.py makemigrations vouchers
4) python manage.py migrate
5) python manage.py create_vouchers
6) python manage.py create_items 10
7) python manage.py runserver
8) sample voucher code = TREATM00001, PRODU00001

### TODO
1) add Admin.FormView validation for
   * timestamp validation for all Model
   * Voucher type discount for % >=1 AND <=100
2) add respond 404, 400, ... page
3) add test case for vouchers redemption
   * with all verify_ method
