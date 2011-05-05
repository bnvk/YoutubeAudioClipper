import load_unprocessed
import subprocess
import os
import clip

def dump_audio(clip_path, dest_path):
	if subprocess.check_call(['mplayer', '-vc', 'dummy', '-vo', 'null', '-ao', 'pcm', clip_path]) != 0:
		print 'Error dumping audio for %s' % clip_path
	elif subprocess.check_call(['mv', 'audiodump.wav', '%s' % dest_path]) != 0:
		print 'Error moving audiodump.wav'
	print 'Audio successfully dumped'

if __name__=='__main__':
	load_unprocessed.loadUnprocessed()
	unprocessed_list = os.listdir(load_unprocessed.unprocessed_dir)
	for clip_path in unprocessed_list:
		dump_audio(load_unprocessed.unprocessed_dir + '/' + clip_path, 'Audio/' + clip_path.split('.')[0] + '.wav')	

	processed = []
	unprocessed_list = os.listdir('Audio')
	for clip_path in unprocessed_list:
		v = clip.getClipLen('Audio/' + clip_path)
		v['id'] = clip_path.split('.')[0]
		processed.append(v)

	print processed

