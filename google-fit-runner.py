import requests
import time


# GET AUTH TOKEN or access_token & refresh_token
# https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=32727419809-23ou4hs3js29oml2d99v2utug8khb0rj.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&access_type=offline&prompt=select_account&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.activity.read+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.activity.write+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.blood_glucose.read+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.blood_glucose.write+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.blood_pressure.read+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.blood_pressure.write+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.body.read+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.body.write+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.body_temperature.read+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.body_temperature.write+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.location.read+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.location.write+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.nutrition.read+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.nutrition.write+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.oxygen_saturation.read+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.oxygen_saturation.write+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.reproductive_health.read+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Ffitness.reproductive_health.write&state=2LebwJ6qB6PEeo4yIB3O0uNq26QWMH

#-------------------------settings


AUTH_TOKEN = '4/1AX4XfWhvhum_zzzzzzzzzzzj4dbs8xomux70O7M3--ZcXH7QJf9c9skWv7do'
APP_NAME = 'com.google.step_count.delta:runner'
RUNNER_SPEED_steps_s = 2 #max 10
DELAY_s = 1000

client_secret = 'P_56GvaOnxlRZoIkZiKPNcau'
client_id = '32727419809-23ou4hs3js29oml2d99v2utug8khb0rj.apps.googleusercontent.com'
access_token = 'ya29.zzzzzzzzzzzuEZKkYtHYds3fwkujG1NX3l70Mzdfx03adV661X8spJjByDNTZr0GHyhUBus8ZDgEjjgIUUJrNwkqKcDlFycA5VpCMvRcoslVcte3hTugyYbPkfc7nmKoXn1LTOp7UgXy4WmQNlxMrVo7j-rOYZ'
refresh_token = '1//0zzzzzzzzzzzfGCgYIARAAGAwSNwF-L9Iro5_V1j_zzzzzzzzzzzjSkZZ87cWQmIEIKxc4r2Xhighv6ImX4dVrFdc780THR9R6IfEU'
dataSourceId = ''

#-------------------------settings


intVal = RUNNER_SPEED_steps_s*DELAY_s;
steps_count = 0

def refresh_token_func():
    global access_token
    print('Token refreshing..')
    body = {
        'client_secret':client_secret,
        'grant_type':'refresh_token',
        'refresh_token':refresh_token,
        'client_id':client_id
    }
    try:
        r = requests.post('https://oauth2.googleapis.com/token', headers = { 'content-type': 'application/x-www-form-urlencoded' }, params=body)
        if(r.status_code==200):
            access_token = r.json()['access_token']
            print('Token refreshed..')
        else:
            print(r.text)
    except Exception as e:
        print(e)
        time.sleep(1)
        refresh_token_func()
    

def work_with_auth_token():
    global access_token
    global refresh_token
    print('Recieving access_token and refresh_token from AUTH_TOKEN')
    body = {
        'code':AUTH_TOKEN,
        'client_id':client_id,
        'client_secret':client_secret,
        'redirect_uri':'urn:ietf:wg:oauth:2.0:oob',
        'grant_type':'authorization_code'
    }
    try:
        r = requests.post('https://oauth2.googleapis.com/token', headers = { 'content-type': 'application/x-www-form-urlencoded' }, params=body)
        if(r.status_code==200):
            access_token = r.json()['access_token']
            refresh_token = r.json()['refresh_token']
            print('access_token and refresh_token Recieved')
            print('access_token = '+access_token)
            print('refresh_token = '+refresh_token)
        else:
            print(r.text)
    except Exception as e:
        print(e)
        time.sleep(1)
        work_with_auth_token()

def create_data_source():
    global dataSourceId
    print('DataSource creating..')
    body = {
      'application': {
        'name': "python_runner',
      },
      'dataType': {
        'field': [
          {
            'format': "integer',
            'name': 'steps'
          }
        ],
        'name': 'com.google.step_count.delta'
      },
      'type': 'raw'
    }
    try:
        r = requests.post('https://www.googleapis.com//fitness/v1/users/me/dataSources', headers={ 'content-type': 'application/json','Authorization': 'Bearer %s' % access_token }, json=body)
        if(r.status_code==200):
            dataSourceId = r.json()['dataStreamId']
            print('DataSource created - '+dataSourceId)
        elif(r.status_code==409):
            dataSourceId = r.json()['error']['message'].split()[2]
            print('DataSource created - '+dataSourceId)
        elif(r.status_code==401):
            refresh_token_func()
            create_data_source()
        else:
            print(r.text)
    except Exception as e:
        print(e)
        time.sleep(1)
        create_data_source()


work_with_auth_token()
create_data_source()

while(True):
    end = int(round(time.time() * 1000))
    start = end-(DELAY_s*1000)
    end_nano_str = str(end).ljust(19, '0')
    start_nano_str = str(start).ljust(19, '0')
    body = {
      'dataSourceId': dataSourceId,
      'point': [
        {
          'dataTypeName': 'com.google.step_count.delta',
          'value': [
            {
              'intVal': intVal,
              'mapVal': []
            }
          ],
          'startTimeNanos': start_nano_str,
          'endTimeNanos': end_nano_str
        }
      ],
      'minStartTimeNs': start_nano_str,
      'maxEndTimeNs': end_nano_str
    }
    try:
        r = requests.patch('https://fitness.googleapis.com/fitness/v1/users/me/dataSources/'+dataSourceId+'/datasets/runner', headers={ 'content-type': 'application/json','Authorization': 'Bearer %s' % access_token }, json=body)
        if(r.status_code==200):
            steps_count += intVal
            print('Steps count ' + str(steps_count) + ' | Running', end='')
        elif(r.status_code==401):
            refresh_token_func()
        else:
            print (r.json())
    except Exception as e:
        print(e)
    for number in range(20):
        print('.', end='')
        time.sleep(DELAY_s/20)
    print()

