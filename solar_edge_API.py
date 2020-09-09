import requests
import json
import datetime
import os
import subprocess

def elektrarna_API_to_JSON(url):
    page = requests.get(url)
    try:
        page.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))     
    # print(page.text)
    json_txt = json.loads(page.text)
    return json_txt
    # print(json_txt)


current_date = datetime.datetime.now()
current_month = current_date.month
year = current_date.year
today_day = current_date.day
hour = current_date.hour

# num_of_days_in_month = ((datetime.date(year, current_month + 1 , 1) - datetime.date(year, current_month, 1)).days)

startTime = str(year) + '-' + str(current_month - 1) + '-' + str(today_day) + ' '+ str(hour) + ':00:00'
endTime = str(year) + '-' + str(current_month) + '-' +str(today_day) + ' '+ str(hour) + ':00:00'

# startTime = '2020-09-09 09:30:00'
# endTime = '2020-09-09 17:15:00'

url = 'https://monitoringapi.solaredge.com/site/1419088/power?startTime=' + startTime + '&endTime=' + endTime + '&api_key=KU6Z3LNCNW5TV3I52GUDK9TFYRH704M2'

json_page = elektrarna_API_to_JSON(url)


post_dict = {} # send multiple requests
post_dict['measurements'] = [] # send multiple requests

# ppost_dict = {} # send 1 request

for i,measurement in enumerate(json_page['power']['values']):

    date_object = datetime.datetime.strptime(measurement['date'], '%Y-%m-%d %H:%M:%S')
    two_hours = datetime.timedelta(hours=2)
    new_date = date_object - two_hours

    date = str(new_date).replace(' ', 'T') + '.0000000Z'

    if measurement['value'] == None:
        power = 0.0

    else:
        power = measurement['value']/1000

    post_dict['measurements'].append({"period_end": date, "period": "PT15M", "total_power": power}) # send multiple requests
    # ppost_dict['measurements']={"period_end": date, "period": "PT15M", "total_power": power} # send 1 request
    # answer = requests.post('https://api.solcast.com.au/rooftop_sites/5acd-c6e4-a6a2-178b/measurements?api_key=1B1PXJGIPaMnir_Z-wxj5CFk8D8Bj-vz', ppost_dict) # send 1 request
    # print(answer) # send 1 request

# file = open('post_data.txt','w')
# file.write(json.dumps(post_dict))
print(str(json.dumps(post_dict)))


headers = {
  'Content-Type': 'application/json',
  'Cookie': 'ss-opt=temp; X-UAId=7936; ss-id=bS5Hg1HNyObQvebjVQnk; ss-pid=5EfILP7m8vmY4zEDDufg'
}

post_url = 'https://api.solcast.com.au/rooftop_sites/5acd-c6e4-a6a2-178b/measurements?api_key=1B1PXJGIPaMnir_Z-wxj5CFk8D8Bj-vz'
answer = requests.post('https://api.solcast.com.au/rooftop_sites/5acd-c6e4-a6a2-178b/measurements?api_key=1B1PXJGIPaMnir_Z-wxj5CFk8D8Bj-vz', headers=headers, data=str(json.dumps(post_dict)))
# answer = requests.request("POST", post_url, headers=headers, post_dict)
print('')
print('')
print(answer.text.encode('utf8'))
print('')
print(answer)


# 'curl -X POST https://api.solcast.com.au/utility_scale_sites/5acd-c6e4-a6a2-178b/measurements -H "Authorization: Bearer 1B1PXJGIPaMnir_Z-wxj5CFk8D8Bj-vz" -H "Content-Type: application/json" -d ' + str(json.dumps(post_dict))




# sub_output = subprocess.check_output(['curl','--insecure' , '-X', 'POST', 'https://api.solcast.com.au/utility_scale_sites/5acd-c6e4-a6a2-178b/measurements' ,'-H' ,"Authorization: Bearer 1B1PXJGIPaMnir_Z-wxj5CFk8D8Bj-vz", '-H' ,"Content-Type: application/json", '-d', str(json.dumps(post_dict))])
# print(sub_output)
