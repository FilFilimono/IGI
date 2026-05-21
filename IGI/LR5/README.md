pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data     
python manage.py runserver


admin / admin123
manager1 / manager123
buyer1 / buyer123


python manage.py test tests --verbosity=2      
python -m coverage run manage.py test tests    
python -m coverage report                      


