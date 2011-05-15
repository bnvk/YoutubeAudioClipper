import urllib2
import json
import subprocess

import settings
import errors

unprocessed_dir = 'UnprocessedVideos'
processed_dir = 'Videos'

def loadUnprocessed():
	unprocesed_url = settings.video_grab_url

	try:
		f = urllib2.urlopen(unprocesed_url)
	except urllib2.URLError,e:
		print 'Could not load videos', e.reason()
		raise e
	resp = json.loads(f.read())

	dl_queue = resp['data']
	for clip in dl_queue:
		print 'Processing', clip['title_url']
		try:
			yt_dl_out = subprocess.check_output(["python", "youtube-dl.py", "%s" % clip['title_url']])
		except subprocess.CalledProcessError, e:
			print 'Could not download video \'' + clip['title_url'] + '\' using youtube-dl'
			errors.send_badclip_error(clip['content_id'])
			continue
		out_path = yt_dl_out.split('\n')[4]
		out_path = out_path.split(' ')[2]
		if subprocess.check_call(['mv', out_path, 'UnprocessedVideos']) != 0:
			print 'Error moving video into unprocessed dir'
			return
		print 'Saved to %s/%s' % (unprocessed_dir, out_path)

if __name__=='__main__':
	loadUnprocessed()

