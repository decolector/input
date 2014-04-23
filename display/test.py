import requests

host = "https://api.mongohq.com/databases/vital/collections/messages/documents"
key = '6pnomhzb6yre2nifkc4u'
limit = 10
heads = {'content-type': 'application/json'}


params = {'_apikey': key, 'sort': '{"date":-1}', 'limit': 100}
res = requests.get(host, headers=heads, params=params)

msgs = []
actualBatch = 0

if res.status_code != 200:
    print "Error in response: " + res.text
else:
    totalMessages = res.headers['X-Mongohq-Count']

    for row in res.json():
        msgs.append(row)

    for i in range(len(msgs), int(totalMessages), 100):
        res = requests.get(host, headers=heads, params={'_apikey': key,
                                                        'sort': '{"date":-1}',
                                                        'limit': 100,
                                                        'skip': i})
        
        for row in res.json():
            msgs.append(row)

    print len(msgs)
                