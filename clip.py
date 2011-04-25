import sys
import array
import wave

def getClipLen(file_path):
	chunk_len = 44
	chunk_secs = .001
	threshhold = .015

	fd = wave.open(file_path)

	chunk_sz = fd.getnchannels() * fd.getsampwidth() * chunk_len

	chunk = fd.readframes(chunk_len)

	# load average chunk vals
	chunk_avgs = []
	while len(chunk) == chunk_sz:
		decoded = array.array('H', chunk)
		chunk_accum = 0
		# Sump up the frames
		for frame_ndx in range(chunk_len):
			# Sum up the channels
			channel_accum = 0
			for channel_i in range(fd.getnchannels()):
				channel_accum = channel_accum + decoded[frame_ndx+channel_i]
			chunk_accum = chunk_accum + channel_accum
		chunk_avgs.append(chunk_accum / (chunk_len * fd.getnchannels()))
		chunk = fd.readframes(chunk_len)

	# determine threshold
	chunk_accum = 0
	for chunk in chunk_avgs:
		chunk_accum += chunk

	thresh_sum = chunk_accum * threshhold

	# Find endpoints
	lead_time = 0.0
	tail_time = 0.0

	accum = 0
	for i in range(len(chunk_avgs)):
		accum += chunk_avgs[i]
		if accum >= thresh_sum:
			break
		lead_time += chunk_secs

	accum = 0
	for i in range(len(chunk_avgs)-1, -1, -1):
		accum += chunk_avgs[i]
		if accum >= thresh_sum:
			break
		tail_time += chunk_secs

	return lead_time, tail_time

if __name__ == '__main__':
	print getClipLen(sys.argv[1])

