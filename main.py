import load_unprocessed
import subprocess
import os
import json
import urllib
import urllib2

import clip
import settings

post_url = settings.success_url
def dump_audio(clip_path, dest_path):
	if subprocess.check_call(['mplayer', '-vc', 'dummy', '-vo', 'null', '-ao', 'pcm', clip_path]) != 0:
		print 'Error dumping audio for %s' % clip_path
		return False
	elif subprocess.check_call(['mv', 'audiodump.wav', '%s' % dest_path]) != 0:
		print 'Error moving audiodump.wav'
		return False
	print 'Audio successfully dumped'
	return True

if __name__=='__main__':
	#load_unprocessed.loadUnprocessed()
	
	# Unprocessed Videos
	unprocessed_list = os.listdir(load_unprocessed.unprocessed_dir)
	for clip_path in unprocessed_list:
		extension = clip_path.split('.')[1]
		orig_file = clip_path.split('.')[0]
		# Check that extension is valid
		if not extension in settings.valid_video_extensions:
			print 'Invalid extension on file', clip_path
			continue
		# Dump audio and move audiodump.wav to Unprocessed Audio
		dst_path = 'UnprocessedAudio/' + orig_file + '.wav'
		if dump_audio(load_unprocessed.unprocessed_dir + '/' + clip_path, dst_path):
			subprocess.check_call(['mv', load_unprocessed.unprocessed_dir + '/' + clip_path, load_unprocessed.processed_dir + '/' + clip_path])

	processed = []
	unprocessed_list = os.listdir('UnprocessedAudio')
	for clip_path in unprocessed_list:
		if clip_path[0] == '.':
			continue
		try:
			v = clip.getClipLen('UnprocessedAudio/' + clip_path)
		except Exception, e:
			print 'Skipping bad clip'
			continue
		v['clip_id'] = clip_path.split('.')[0]
		processed.append(v)

	for clip_data in processed:
		post_data = {}
		post_data['audio_process_data'] = json.dumps(clip_data)
		post_data['the_magic_word'] = 'I luvs my #s'
		f = urllib2.urlopen(post_url + clip_data['clip_id'], urllib.urlencode(post_data))
		resp = json.loads(f.read())
		if resp['status'] == 'success':
			if subprocess.check_call(['mv', 'UnprocessedAudio/' + clip_data['clip_id'] + '.wav', 'Audio/']) == 0:
				print 'Completed %s' % clip_data['clip_id']
		else:
			print resp

