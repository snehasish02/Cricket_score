import requests
import pynotify
import json
import time
import sys

def sendmessage(title, message):
	pynotify.init("Test")
	notice = pynotify.Notification(title, message)
	notice.show()
	return

def get_all_match_data():
	r = requests.get("http://cricscore-api.appspot.com/csa")
	if r and r.status_code == requests.codes.ok:
		return r.json()
	else:
		raise Exception("Unable to get data from cricscore-api")

def get_specific_match_data(match_id):
	timestamp = str(time.strftime("%a, %d %b %Y %H:%M:%S IST"))
	url = "http://cricscore-api.appspot.com/csa?id="+str(match_id)
	headers = {"If-Modified-Since":str(timestamp)}
	r = requests.get(url, headers = headers)
	if r and r.status_code == requests.codes.ok:
		return r.json()
	elif r and r.status_code ==	requests.codes.NOT_MODIFIED:
		print "No change in respone."
	else:
		pass
		#raise Exception("Unable to get data from cricscore-api")

if __name__== "__main__":
	match_list = get_all_match_data()

	keyword_list = sys.argv
	del keyword_list[0]
	match_id_list = list()
	for keyword in keyword_list:
		for match in match_list:
			if match["t1"].find(keyword)>=0 or match["t2"].find(keyword)>=0:
				match_id_list.append(str(match["id"]))
	match_id =  "+".join(match_id_list)
	
	while True:
		score = get_specific_match_data(match_id)
		if score:
			sendmessage("Score", str(score))
		time.sleep(60)



