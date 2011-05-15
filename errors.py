import urllib2
import urllib
import json

import settings

def send_badclip_error(content_id):
	url = settings.error_url
	post_data = {'the_magic_word': 'I luvs my #s'}
	f = urllib2.urlopen(url + content_id, urllib.urlencode(post_data))
	resp = json.loads(f.read())
	if resp['status'] == 'success':
		print 'Updated clip as error'
	else:
		print 'Error notifying server of bad clip!'

