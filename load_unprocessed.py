import urllib2
import json
import subprocess

unprocessed_dir = 'UnprocessedVideos'

def loadUnprocessed():
	unprocesed_url = 'http://rafachant.reverseproductions.com/api/content/view/module/rafachant'

	f = urllib2.urlopen(unprocesed_url)
	resp = json.loads(f.read())

	dl_queue = resp['data']
	for clip in dl_queue:
		print 'Processing', clip['title_url']
		yt_dl_out = subprocess.check_output(["python", "youtube-dl.py", "%s" % clip['title_url']])
		out_path = yt_dl_out.split('\n')[4]
		out_path = out_path.split(' ')[2]
		if subprocess.check_call(['mv', out_path, 'UnprocessedVideos']) != 0:
			print 'Error moving video into unprocessed dir'
			return
		print 'Saved to %s/%s' % (unprocessed_dir, out_path)

if __name__=='__main__':
	loadUnprocessed()

