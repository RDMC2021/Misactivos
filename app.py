from flask import Flask, request, make_response
import requests
import os
import json
import urllib.parse

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    auth_header = os.getenv('NETILION_AUTH')
    api_key = os.getenv('NETILION_API_KEY')
    request_headers = {'accept': 'application/json', 'Authorization': auth_header, 'Api-Key': api_key}
    req = request.get_json(silent=True, force=True)
    intent = req["queryResult"]["intent"]["displayName"]
    if intent == 'ResumendeEstado':
        get_total_assets_result = requests.get('https://api.netilion.endress.com/v1/assets', headers=request_headers)
        get_total_assets_json = get_total_assets_result.json()
        count_total_assets = get_total_assets_json['pagination']['total_count']

        get_failure_assets_result = requests.get('https://api.netilion.endress.com/v1/assets?status_code=failure*', headers=request_headers)
        get_failure_assets_json = get_failure_assets_result.json()
        count_failure_assets = get_failure_assets_json['pagination']['total_count']

        get_ok_assets_result = requests.get('https://api.netilion.endress.com/v1/assets?status_code=ok*', headers=request_headers)
        get_ok_assets_json = get_ok_assets_result.json()
        count_ok_assets = get_ok_assets_json['pagination']['total_count']

        get_maintenance_assets_result = requests.get('https://api.netilion.endress.com/v1/assets?status_code=maintenance*', headers=request_headers)
        get_maintenance_assets_json = get_maintenance_assets_result.json()
        count_maintenance_assets = get_maintenance_assets_json['pagination']['total_count']

        get_check_assets_result = requests.get('https://api.netilion.endress.com/v1/assets?status_code=check*', headers=request_headers)
        get_check_assets_json = get_check_assets_result.json()
        count_check_assets = get_check_assets_json['pagination']['total_count']

        get_out_assets_result = requests.get('https://api.netilion.endress.com/v1/assets?status_code=out*', headers=request_headers)
        get_out_assets_json = get_out_assets_result.json()
        count_out_assets = get_out_assets_json['pagination']['total_count']


        answer = 'Actualmente hay ' + str(count_total_assets) + ' activos conectados. De los cuales se encuentran ' + str(count_ok_assets) + ' en estado de ok ' + str(count_failure_assets) + ' en estado de Fallo '+ str(count_out_assets) + ' en estado de Fuera de Especificación ' + str(count_maintenance_assets) + ' en estado de Mantenimiento Requerido y ' + str(count_check_assets) + ' en estado de Verificar Función '

        return make_response({
            "fulfillmentText": answer,
            "fulfillmentMessages": [
                {
                    "platform": "ACTIONS_ON_GOOGLE",
                    "simpleResponses":{
                        "simpleResponses": [
                            {
                                "textToSpeech": answer
                            }
                        ]
                    }
                }
            ],
            "source": "webhook"
        })
    
    elif intent == 'ValoresMedidosFWR30':
        get_nivel_FWR30_result = requests.get('https://api.netilion.endress.com/v1/assets/88098/values?key=level', headers=request_headers)
        get_nivel_FWR30_json = get_nivel_FWR30_result.json()
        nivel_FWR30 = get_nivel_FWR30_json['values'][0]['value']

        #get_tiempo_FWR30_result = requests.get('https://api.netilion.endress.com/v1/assets/88098/values?key=level', headers=request_headers)
        #get_tiempo_FWR30_json = get_tiempo_FWR30_result.json()
        #tiempo_FWR30 = get_tiempo_FWR30_json['values'][0]['timestamp']

        get_vacio_FWR30_result = requests.get('https://api.netilion.endress.com/v1/assets/88098/values?key=distance', headers=request_headers)
        get_vacio_FWR30_json = get_vacio_FWR30_result.json()
        vacio_FWR30 = get_vacio_FWR30_json['values'][0]['value']

        get_lleno_FWR30_result = requests.get('https://api.netilion.endress.com/v1/assets/88098/values?key=level_distance', headers=request_headers)
        get_lleno_FWR30_json = get_lleno_FWR30_result.json()
        lleno_FWR30 = get_lleno_FWR30_json['values'][0]['value']

        get_bateria_FWR30_result = requests.get('https://api.netilion.endress.com/v1/assets/88098/values?key=battery', headers=request_headers)
        get_bateria_FWR30_json = get_bateria_FWR30_result.json()
        bateria_FWR30 = get_bateria_FWR30_json['values'][0]['value']

        get_temperatura_FWR30_result = requests.get('https://api.netilion.endress.com/v1/assets/88098/values?key=temperature', headers=request_headers)
        get_temperatura_FWR30_json = get_temperatura_FWR30_result.json()
        temperatura_FWR30 = get_temperatura_FWR30_json['values'][0]['value']

        answer = 'Los valores del FWR30 son nivel de ' + str(nivel_FWR30) + ' porciento distancia de vacio ' + str(vacio_FWR30) + 'milimetros distancia de lleno '+ str(lleno_FWR30) + 'milimetros vida util de la bateria ' + str(bateria_FWR30) + 'dias temperautura ' + str(temperatura_FWR30) + ' grados celcius '
        #answer = 'El nivel del Micropilot FWR30 es ' + str(nivel_FWR30) + ' porciento'

        return make_response({
            "fulfillmentText": answer,
            "fulfillmentMessages": [
                {
                    "platform": "ACTIONS_ON_GOOGLE",
                    "simpleResponses":{
                        "simpleResponses": [
                            {
                                "textToSpeech": answer
                            }
                        ]
                    }
                }
            ],
            "source": "webhook"
        })
    

    elif intent == 'ForwardFirstFailureStatusCauseAndRemedy':
        get_failure_assets_result = requests.get('https://api.netilion.endress.com/v1/assets?status_code=failure*', headers=request_headers)
        get_failure_assets_json = get_failure_assets_result.json()
        asset_id = get_failure_assets_json['assets'][0]['id']

        get_cause_remedy_url = 'https://api.netilion.endress.com/v1/assets/' + str(asset_id) + '/health_conditions?include=causes%2C%20causes.remedies'
        get_cause_remedy_result = requests.get(get_cause_remedy_url, headers=request_headers)
        get_cause_remedy_json = get_cause_remedy_result.json()
        diagnosis_code = get_cause_remedy_json['health_conditions'][0]['diagnosis_code']
        cause = get_cause_remedy_json['health_conditions'][0]['causes'][0]['description']
        remedy = get_cause_remedy_json['health_conditions'][0]['causes'][0]['remedies'][0]['description']

        get_asset_location_url = 'https://api.netilion.endress.com/v1/assets/' + str(asset_id) + '/nodes'
        get_asset_location_result = requests.get(get_asset_location_url, headers=request_headers)
        get_asset_location_json = get_asset_location_result.json()
        location = get_asset_location_json['nodes'][0]['name']

        answer = 'An asset in location ' + location + ' reads diagnostic code ' + diagnosis_code + '. The cause is: ' + cause + '. The recommendation is: ' +remedy
        
        telegram_auth = os.getenv('TELEGRAM_AUTH')
        telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        telegram_request_url = 'https://api.telegram.org/bot' + telegram_auth + '/sendMessage?chat_id=-' + telegram_chat_id + '&text=' + urllib.parse.quote(answer)
        telegram_response = requests.get(telegram_request_url)

        if telegram_response.status_code == 200:
            return make_response({
                "fulfillmentText": "message was sent out",
                "fulfillmentMessages": [
                    {
                        "platform": "ACTIONS_ON_GOOGLE",
                        "simpleResponses":{
                            "simpleResponses": [
                                {
                                    "textToSpeech": "message was sent out"
                                }
                            ]
                        }
                    }
                ],
                "source": "webhook"
            })
        else:
            return make_response({
                "fulfillmentText": "message could not be sent",
                "fulfillmentMessages": [
                    {
                        "platform": "ACTIONS_ON_GOOGLE",
                        "simpleResponses":{
                            "simpleResponses": [
                                {
                                    "textToSpeech": "message could not be sent"
                                }
                            ]
                        }
                    }
                ],
                "source": "webhook"
            })




if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')