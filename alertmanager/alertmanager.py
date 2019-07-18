import urllib.request, urllib.parse, json


class Alertmanager:
    def __init__(self, host):
        self.host = host


    def alerts(self):
        with urllib.request.urlopen(self.host + "/api/v2/alerts") as url:
            data = json.loads(url.read().decode())

            return data

    def fire(self):
        url = self.host + "/api/v2/alerts"
        data_fields = [{
            "startsAt": "2019-07-15T22:07:01.535Z",
            #"endsAt": "2019-07-15T22:07:01.535Z",
            "annotations": {
                "summary": "string",
                },
            "labels": {
                'alertname': 'string',
                'instance': 'string',
                'job': 'string',
                'severity': 'string'
                },
            "generatorURL": "http://string"
            }]

        request = urllib.request.Request(url, data=json.dumps(data_fields).encode('utf8'), method='POST', headers={"Content-Type": "application/json", "accept": "application/json"})
        data = urllib.request.urlopen(request).getcode()

        return data
