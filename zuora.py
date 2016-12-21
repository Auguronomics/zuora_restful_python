import requests
import json


class Zuora(object):
    def __init__(self, config):
        self.config = config
        self.auth = (config['user'], config['password'])
        self.accountingPeriods = None
        
    def _get(self, path):
        response = requests.get(self.config['endpoint'] + path, 
                        auth=self.auth)
        return self._unpackResponse('GET', path, response)
        
    def _delete(self, path):
        response = requests.delete(self.config['endpoint'] + path, 
                        auth=self.auth)
        return self._unpackResponse('GET', path, response)

    def _post(self, path, payload):
        response = requests.post(self.config['endpoint'] + path, 
                        json=payload,
                        auth=self.auth)
        return self._unpackResponse('POST', path, response)
        
    def _unpackResponse(self, operation, path, response):
        assert response.status_code == 200, '{} to {} failed: {}'.format(operation, path, response.json())
        return json.loads(response.text)

    def query(self, queryString):    
        response = self._post("/action/query", {"queryString" : queryString})
        return response
        
    def queryAll(self, queryString):
        records = []
        response = self.query(queryString)
        records += response['records']
        
        while response['done'] == False:
            response = self.queryMore(response['queryLocator'])
            records += response['records']
        
        return records
        
    # Use queryMore to request additional results from a previous query call. If your initial query call returns more than 2000 results, you can use queryMore to query for the additional results.

    def queryMore(self, queryLocator):
        return self._post("/action/queryMore", {"queryLocator" : queryLocator})
        
    def revenueRecognitionRule(self, chargeKey):
        if isinstance(chargeKey, dict):
            if 'ChargeId' in chargeKey:
                chargeKey = chargeKey['ChargeId']
        response = self._get("/revenue-recognition-rules/subscription-charges/" + chargeKey)
        assert response['success'], response
        return response['revenueRecognitionRuleName']
                
    def getRevenueSchedulesForInvoiceItem(self, invoiceItemId):
        # assert len(self.query("select id from invoiceitem where id ='{}'".format(invoiceItemId))['records'])
        response = self._get("/revenue-schedules/invoice-items/" + invoiceItemId)
        return response

    def deleteRevenueSchedule(self, rsNumber):
        response = self._delete("/revenue-schedules/" + rsNumber)
        assert response['success'], response
        
    def getAccountPeriods(self):
        if not self.accountingPeriods:
            self.accountingPeriods = {}
            response = self._get("/accounting-periods/")
            assert response['success'], response
            for p in response['accountingPeriods']:
                self.accountingPeriods[p['name']] = p
            
        return self.accountingPeriods
    
    # samplePayload = {
    #     "revenueDistributions": [
    #         {
    #             "accountingPeriodName": "Jan '16",
    #             "newAmount": "20"
    #         },
    #         {
    #             "accountingPeriodName": "Open-Ended",
    #             "newAmount": "30"
    #         }
    #     ],
    #     "revenueEvent": {
    #         "eventType": "Revenue Distributed",
    #         "eventTypeSystemId": "RevenueDistributed__z",
    #         "notes": "My notes"
    #     }
    # }
    
    def revenueSchedule(self, invoiceItemId, payload):
        response = self._post('/revenue-schedules/invoice-items/' + invoiceItemId, payload)
        assert response['success'], response
        return response
        
        
