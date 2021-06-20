import os
from dotenv import load_dotenv
from requests import Session
load_dotenv()

class NoRebuildAuthSession(Session):
 def rebuild_auth(self, prepared_request, response):
   '''
   No code here means requests will always preserve the Authorization header when redirected.
   Be careful not to leak your credentials to untrusted hosts!
   '''
session = NoRebuildAuthSession()
API_KEY = '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'

response = session.get('https://api.meraki.com/api/v1/organizations/', headers={'Authorization': f'Bearer {API_KEY}'}, timeout=5)
print(response.json())

