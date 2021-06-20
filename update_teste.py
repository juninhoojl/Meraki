import requests
idRede = 'L_566327653141843049'
url = "https://api.meraki.com/api/v1/networks/{idRede}"

payload = '''{
    "name": "Long Island Office",
    "timeZone": "America/Los_Angeles",
    "tags": [ "tag1", "tag2" ],
    "notes": "Combined network for Long Island Office"
}'''

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"
}

response = requests.request('PUT', url, headers=headers, data = payload)

print(response.text.encode('utf8'))
