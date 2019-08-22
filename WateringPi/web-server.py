from flask import Flask, render_template, jsonify, request, Response, send_file, make_response, redirect
import sys
import random
import string
import time
import threading
import json
import gevent
import gevent.monkey
import telepot
from gevent.pywsgi import WSGIServer
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import dynamodb
import boto3
from boto3.dynamodb.conditions import Key, Attr
light = 0
humidity = 0
soil = 0
temperature = 0
watering = True
bucket_name = <Replace with your S3 bucket name>
host = <Replace with your own MQTT endpoint>
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"
client = AWSIoTMQTTClient("PubSub-ec2")
client.configureEndpoint(host, 8883)
client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(15)
client.configureMQTTOperationTimeout(8) 
client.connect()
#client.subscribe("device_admin/updatePrefs", 1, customCallback)
app = Flask(__name__)
my_bot_token = <Replace with your own telegram bot token>
telegram_chat_id = <Replace with your own telegram chat id>
@app.route("/api/get_environment_data/",methods=['POST','GET'])
def apidata_get_environment_data():
    if request.method == 'GET':
        try:
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            table = dynamodb.Table('light_temperature_humidity')
            startdate = '2019-08'
            response = table.query(
                KeyConditionExpression=Key('device_id').eq('raspberrypi-1') 
                                      & Key('datetime_id').begins_with(startdate),
                ScanIndexForward=False
            )

            items = response['Items']

            n=75 # limit to last 10 items
            data = items[:n]
            data_reversed = data[::-1]
	    results = data_reversed
            return jsonify(results)
	    
        except:
            import sys
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])


@app.route("/api/get_soil_data",methods=['POST','GET'])
def apidata_get_soil_data():
    if request.method == 'POST' or request.method == 'GET':
        try:
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            table = dynamodb.Table('soilmoisture')
            startdate = '2019-08'
            response = table.query(
                KeyConditionExpression=Key('device_id').eq('raspberrypi-1') 
                                      & Key('datetime_id').begins_with(startdate),
                ScanIndexForward=False
            )
            items = response['Items']

            n=75 # limit to last 10 items
            data = items[:n]
            data_reversed = data[::-1]
	    response = data_reversed[0]
            return jsonify(data_reversed)

        except:
            import sys
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])


def customCallback(client, userdata, message):
	payload = message.payload
	global light
	global humidity
	global soil
	global temperature

	payloadJson = json.loads(payload)
	light = payloadJson["light"]
	soil = payloadJson["soil"]
	temperature = payloadJson["temperature"]
	humidity = payloadJson["humidity"]
client.subscribe('sensors/realtimeData', 1, customCallback)
@app.route("/api/get_realtime_data/",methods=['POST','GET'])
def apidata_get_realtime_data():
    if request.method == 'GET':
		global light
		global humidity
		global soil
		global temperature
		message = {}
		message["action"] = 'getData'
		client.publish('sensors/getRealtimeData', json.dumps(message), 0)
		response = {}
		response["light"] = light
		response["soil"] = soil
		response["temperature"] = temperature
		response["humidity"] = humidity
		return jsonify(response)

def customCallback2(client, userdata, message):
	payload = message.payload
	global watering
	payloadJson = json.loads(payload)
	watering = payloadJson["status"]
	
client.subscribe('controller/status', 1, customCallback2)
@app.route("/api/get_realtime_status/",methods=['POST','GET'])
def apidata_get_realtime_status():
    if request.method == 'GET':
		global watering
		message = {}
		message["action"] = 'getWateringStatus'
		client.publish('controller/command', json.dumps(message), 0)
		response = {}
		response["status"] = watering
		return jsonify(response)

@app.route("/update_userprefs/",methods=['POST','GET'])
def update_user_prefs():
    if request.method == 'POST':
        try:
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            table = dynamodb.Table('user_preferences')
	    soil_interval = request.form['soilInterval']
	    environment_interval = request.form['environmentInterval']
	    photo_interval = request.form['photoInterval']
	    dry_soil_threshold = request.form['minimumMoisture']
	    watering_duration = request.form['wateringDuration']
            response = table.update_item(
		Key = {
		    'name': 'default'
		},
		UpdateExpression = "set soil_refresh_interval = :s, environment_refresh_interval = :e, photo_interval = :p, dry_soil_threshold = :t, watering_duration = :w",
		ExpressionAttributeValues = {
		    ':s': soil_interval,
		    ':e': environment_interval, 
		    ':p': photo_interval,
		    ':t': dry_soil_threshold,
		    ':w': watering_duration  
		},
		ReturnValues = "UPDATED_NEW"
	    )
            response = make_response(redirect("/"))
            return response
    	except:
        	print(sys.exc_info()[0])
        	print(sys.exc_info()[1])

@app.route("/api/get_userprefs/")
def get_user_prefs():
	dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
	table = dynamodb.Table('user_preferences')
	deviceid = 'deviceid_dorachua'
	response = table.query(KeyConditionExpression = Key('name').eq('default'),
				ScanIndexForward = False
				)
	results = response["Items"]
	return jsonify(results)

@app.route("/api/get_image/")
def get_image():
    global bucket_name
    try:
	s3 = boto3.resource('s3', region_name='us-east-1')
	s3.Bucket(bucket_name).download_file('image', '/home/ubuntu/flaskproject/image.jpg')
	return send_file('/home/ubuntu/flaskproject/image.jpg', mimetype='image/jpeg')
    except:
	print(sys.exc_info()[0])
	print(sys.exc_info()[1])

@app.route("/api/update_image/",methods=['POST','GET'])
def update_image():
	if request.method == 'GET':
	    try:
		message = {}
		message["action"] = 'takephoto'
		client.publish('sensors/takePhoto', json.dumps(message), 0)
		response = {}
		response["message"] = ' '
		return jsonify(response)
	    except:
		print(sys.exc_info()[0])
		print(sys.exc_info()[1])

@app.route("/api/beginwatering/",methods=['POST','GET'])
def apicontrol_start_watering():
	if request.method == 'POST':
	    try:
		message = {}
		message["action"] = "start"
		client.publish('controller/command', json.dumps(message), 1)
		return "On"
	    except:
		print(sys.exc_info()[0])
		print(sys.exc_info()[1])

@app.route("/api/stopwatering/",methods=['POST','GET'])
def apicontrol_stop_watering():
	if request.method == 'POST':
	    try:
		message = {}
		message["action"] = "stop"
		client.publish('controller/command', json.dumps(message), 1)
		return "On"
	    except:
		print(sys.exc_info()[0])
		print(sys.exc_info()[1])

@app.route("/logout/")
def logout():
	response= make_response(redirect("/login_page"))
	response.set_cookie('logged_in', '')
	return response

@app.route("/login/",methods=['POST','GET'])
def login_check_credentials():
	if request.method == 'POST':
		try:
			dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
			password = request.form["password"]
			table = dynamodb.Table('credentials')
			response = table.query(KeyConditionExpression = Key('username').eq('WateringPi'),
						ScanIndexForward = False
						)
			results = response["Items"]
			stored_password = results[0]["password"]
			if password == stored_password:
				response = make_response(redirect('/'))
				response.set_cookie('logged_in', 'True')
				return response
			else:
				global telegram_chat_id
				bot.sendMessage(telegram_chat_id, 'Someone unsuccessfully tried to log in to your WateringPi. If you see this message a few more times and it wasn\'t you trying to login, it might be someone trying to gain unauthorised access to your WateringPi. Consider changing the password to make your WateringPi more secure.')
				response = make_response(redirect('/login_page'))
				return response
		except:
			print(sys.exc_info()[0])
			print(sys.exc_info()[1])

@app.route("/change_password/",methods=['POST','GET'])
def change_password_check():
	if request.method == 'POST':
		try:
			dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
			cur_password = request.form["currentPassword"]
			new_password = request.form["newPassword"]
			new_password_confirm = request.form["newPasswordConfirm"]
			table = dynamodb.Table('credentials')
			response = table.query(KeyConditionExpression = Key('username').eq('WateringPi'),
						ScanIndexForward = False
						)
			results = response["Items"]
			stored_password = results[0]["password"]
			if cur_password == stored_password and new_password == new_password_confirm:
				response = table.update_item(
						Key = {
						    'username': 'WateringPi'
						},
						UpdateExpression = "set password = :p, is_temp = :t",
						ExpressionAttributeValues = {
						    ':p': new_password,
						    ':t': 'false'
						},
						ReturnValues = "UPDATED_NEW"
					    )
				global telegram_chat_id
				bot.sendMessage(telegram_chat_id, 'Your WateringPi password was changed. If it wasn\'t you who changed the password, reset it immediately.')
				response = make_response(redirect('/password_changed/'))
				return response
			else:
				response = make_response(redirect('/change_password/'))
				return response
		except:
			print(sys.exc_info()[0])
			print(sys.exc_info()[1])

@app.route("/")
def home():
	logged_in = request.cookies.get('logged_in')
	if logged_in == 'True':
		return render_template("index.html")
	else:
		response = make_response(redirect('/login_page/'))
		return response

@app.route("/login_page/")
def login():
	return render_template("login.html")

@app.route("/forgot-password/")
def forgot_password():
	global telegram_chat_id
	new_password = ''
	letters = string.ascii_letters
	for i in range(12):
		character = random.choice(letters)
		new_password = new_password + character
	dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
	table = dynamodb.Table('credentials')
	response = table.update_item(
				Key = {
					'username': 'WateringPi'
				},
				UpdateExpression = "set password = :p, is_temp = :t",
				ExpressionAttributeValues = {
					':p': new_password,
					':t': 'true'
				},
				ReturnValues = "UPDATED_NEW"
			)
	message = {}
	message["default"] = 'Your new password is ' + new_password + '.'
	client.publish('password/reset', json.dumps(message), 1)
	bot.sendMessage(telegram_chat_id, 'We\'ve just received a password reset request! Go check your email for the temporary password. Once logged in, it is best you change it immediately.')
	return render_template("forgot-password.html")

@app.route("/credentials/")
def credentials():
	logged_in = request.cookies.get('logged_in')
	if logged_in == 'True':
		return render_template("credentials.html")
	else:
		response = make_response(redirect('/login_page/'))
		return response

@app.route("/password_changed/")
def password_changed():
	logged_in = request.cookies.get('logged_in')
	if logged_in == 'True':
		return render_template("password_change_success.html")
	else:
		response = make_response(redirect('/login_page/'))
		return response

@app.route("/settings/")
def preferences():
	logged_in = request.cookies.get('logged_in')
	if logged_in == 'True':
		return render_template("settings.html")
	else:
		response = make_response(redirect('/login_page/'))
		return response

@app.route("/latest_image/")
def latest_image():
	logged_in = request.cookies.get('logged_in')
	if logged_in == 'True':
		return render_template("image.html")
	else:
		response = make_response(redirect('/login_page/'))
		return response

def respondToMsg(msg):
    global light
    global humidity
    global soil
    global temperature
    chat_id = msg['chat']['id']
    command = msg['text']
    valid_commands = ('List of valid commands:\n\n'
       + '\'test\': Test if your are able to connect to the bot\n'
       + '\'current-status\': View the latest values of the sensors\n'
       + '\'start-watering\': Start watering your plants\n'
       + '\'stop-watering\': Stop watering your plants\n'
       + '\'chat-id\': Obtain the chat ID of this conversation. Necessary when setting up the bot in order to be able to receive notifications.')

    if command == 'test':
       bot.sendMessage(chat_id, 'Received your message successfully!')
    elif command =='/start':
       bot.sendMessage(chat_id, valid_commands)
    elif command == 'start-watering':
       message = {}
       message["action"] = "start"
       client.publish('controller/command', json.dumps(message), 1)
       bot.sendMessage(chat_id, 'Watering started.')
    elif command == 'stop-watering':
       message = {}
       message["action"] = "stop"
       client.publish('controller/command', json.dumps(message), 1)
       bot.sendMessage(chat_id, 'Watering stopped.')
    elif command == 'current-status':
       message = {}
       message["action"] = 'getData'
       client.publish('sensors/getRealtimeData', json.dumps(message), 0)	
       response = ('Light: ' + str(light) + '\nSoil moisture: ' + str(soil) + '\nTemperature: ' + str(temperature) + u'\u00b0 C' + '\nHumidity: ' + str(humidity) + '%')
       bot.sendMessage(chat_id, response)
    elif command == 'chat-id':
       bot.sendMessage(chat_id, 'The chat ID of this conversation is ' + str(chat_id))
    else:
       bot.sendMessage(chat_id, 'The command \'' + command + '\' is invalid!\n' + valid_commands)

bot = telepot.Bot(my_bot_token)
bot.message_loop(respondToMsg)
WSGIServer(('0.0.0.0', 80), app).serve_forever()

