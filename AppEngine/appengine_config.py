# appengine_config.py
from google.appengine.ext import vendor

# Add any libraries install in the "lib" folder.
# To update lib directory:
#   pip install -t lib/ -r requirements.txt
vendor.add('lib')
