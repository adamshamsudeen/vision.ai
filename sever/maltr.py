import requests
import re
from mtranslate import translate

def mallu(line):


	a=translate(line,"ml")
	b=a.encode('utf-8').decode('utf-8')
	print b
	r = requests.post("http://210.212.237.167/tts/festival_cs.php", data={'op':b, 'Languages':'malayalam', 'Voice':'voice1', 'ex':'execute', 'ip':'', 'rate':'normal'})
	print r.status_code
	m = re.search('(\d_\d+).wav', r.text)

	url = "http://210.212.237.167/tts/wav_output/fest_out"+m.group(1)+".wav"
	return url
