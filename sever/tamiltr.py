import requests
import re
from mtranslate import translate

def tamil(line):

	#line="what happened to you jiss? Are you sleeping?"
	a=translate(line,"ta")
	b=a.encode('utf-8').decode('utf-8')
	print b

	r = requests.post("http://www.iitm.ac.in/donlab/hts/festival_cs.php", data={'op':b, 'Languages':'tamil1',  'ex':'execute', 'ip':''})
	print r.status_code

	m = re.search('(\d+).wav', r.text)
	print m.group(1)

	url = "http://www.iitm.ac.in/donlab/hts/wav_output/hts_out"+m.group(1)+".wav"


	return url



