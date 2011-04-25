import array
import wave

chunk_len = 440
chunk_secs = .01
threshhold = 10

fd = wave.open('audiodump.wav')

chunk_sz = fd.getnchannels() * fd.getsampwidth() * chunk_len

chunk = fd.readframes(chunk_len)

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

lead_time = 0.0
tail_time = 0.0
for i in range(len(chunk_avgs)):
	if chunk_avgs[i] > threshhold:
		break
	lead_time += chunk_secs

for i in range(len(chunk_avgs)-1, -1, -1):
	if chunk_avgs[i] > threshhold:
		break
	tail_time += chunk_secs

print 'Lead time: %s seconds' % lead_time
print 'Tail time: %s seconds' % tail_time

