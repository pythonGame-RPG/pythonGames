import http.client

conn = http.client.HTTPSConnection("api.zoom.us")

# Bearer Tokenを取得したい
headers = {
    'authorization': "Bearer " + api_token,
    'content-type': "application/json"
    }

conn.request("GET", "/v2/users?status=active&page_size=30&page_number=1", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))