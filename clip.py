import sys
import array
import wave

#import matplotlib.pyplot as plt

def getClipLen(file_path):
	chunk_len = 4410
	chunk_secs = .1
	hist_n_intervals = 100
	threshhold = .4

	try:
		fd = wave.open(file_path)
	except EOFError e:
		print 'Could not open %s for analysis' % file_path
		raise e
	total_time = fd.getnframes()*fd.getsampwidth() / float(fd.getnchannels() * fd.getframerate())

	chunk_sz = fd.getnchannels() * fd.getsampwidth() * chunk_len
	chunk = fd.readframes(chunk_len)

	# load average chunk vals
	chunk_max = -1
	chunk_min = 0xFF
	chunk_avgs = []
	times = []
	cur_time = 0
	while len(chunk) == chunk_sz:
		decoded = array.array('h', chunk)
		chunk_accum = 0
		# Sump up the frames
		for frame_ndx in range(chunk_len):
			# Sum up the channels
			channel_accum = 0
			for channel_i in range(fd.getnchannels()):
				channel_accum = channel_accum + decoded[frame_ndx+channel_i]
			chunk_accum = chunk_accum + channel_accum
		avg = abs(chunk_accum / (chunk_len * fd.getnchannels()))
		chunk_avgs.append(avg)
		times.append(cur_time)
		cur_time += chunk_secs

		# set max
		if avg >= chunk_max or chunk_max < 0:
			chunk_max = avg

		# set min
		if avg <= chunk_min or chunk_min < 0:
			chunk_min = avg

		chunk = fd.readframes(chunk_len)

	print "Max Min: ", chunk_max, chunk_min

	# Create histogram
	hist_interval_size = float(chunk_max - chunk_min) / hist_n_intervals
	hist = {}
	for chunk in chunk_avgs:
		chunk_hist_val = int(chunk / hist_interval_size)
		try:
			hist[chunk_hist_val] += 1
		except KeyError:
			hist[chunk_hist_val] = 1

	# Find threshold volume
	chunk_n_thresh = len(chunk_avgs) * threshhold
	n = 0
	for i in range(int(chunk_max / hist_interval_size)):
		try:
			n += hist[i]
		except KeyError:
			pass
		if n > chunk_n_thresh:
			break
	chunk_thresh = n * hist_interval_size

	# Find endpoints
	lead_time = 0.0
	tail_time = 0.0
	for chunk in chunk_avgs:
		if chunk >= chunk_thresh:
			break
		lead_time += chunk_secs

	for chunk in reversed(chunk_avgs):
		if chunk >= chunk_thresh:
			break
		tail_time += chunk_secs

#	plt.plot(times, chunk_avgs)
#	plt.show()

	return {'lead_time': lead_time,
		'tail_time': tail_time,
		'total_time': total_time }

if __name__ == '__main__':
	print getClipLen(sys.argv[1])

