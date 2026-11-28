# quick stills for given line indices: bash qs.sh 0 4 5
cd "$(dirname "$0")"; python3 -c "
import json,sys;tl=json.load(open('../../karl01/build/timeline.json'));print(','.join(str(round((tl['lines'][int(i)]['start']+tl['lines'][int(i)]['end'])/2,2)) for i in sys.argv[1:]))" "$@" > /tmp/claude-0/ts.txt
rm -rf /tmp/claude-0/qs; node rep.js "episode.html?tl=finance_series/karl01/build/timeline.json" stills /tmp/claude-0/qs $(cat /tmp/claude-0/ts.txt) | tail -2
cd /tmp/claude-0/qs && ls f_*.jpg | sort -t_ -k2 -g | head -12 > /tmp/claude-0/l.txt; n=$(wc -l < /tmp/claude-0/l.txt); ffmpeg -loglevel error -y $(sed "s/^/-i /" /tmp/claude-0/l.txt) -filter_complex "$(python3 -c "
n=$n;print(''.join(f'[{i}:v]scale=640:360[v{i}];' for i in range(n))+''.join(f'[v{i}]' for i in range(n))+f'xstack=inputs={n}:layout='+'|'.join(f'{(i%4)*640}_{(i//4)*360}' for i in range(n))+':fill=black')")" /tmp/claude-0/qs.jpg
