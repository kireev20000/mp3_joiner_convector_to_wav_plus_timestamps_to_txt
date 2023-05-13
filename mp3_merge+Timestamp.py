import os
import glob
from pydub import AudioSegment
from pydub.utils import mediainfo
import datetime
from PIL import Image


start = datetime.timedelta(0)
list_lenght = []

def parse_ts(ts: str) -> datetime.timedelta:
    h, m, s = ts.split(':')
    return datetime.timedelta(hours=int(h), minutes=int(m), seconds=float(s))



extension_list = ('*.mp3', '*.flac')
combined = AudioSegment.empty()
text_length = []
os.chdir('.')  # Path where the files are located

for extension in extension_list:
    for file_to_merge in glob.glob(extension):
        mp3_filename = os.path.splitext(os.path.basename(file_to_merge))[0] + '.mp3'
        mp3_to_list = AudioSegment.from_mp3(mp3_filename)
        end = str(datetime.timedelta(seconds=len(mp3_to_list) / 1000))
        mp3_tags = mediainfo(mp3_filename)
        print(mp3_tags['TAG']['track'], mp3_tags['TAG']['title'])

        if mp3_tags.get('TAG', {}).get('grouping') is None:
            mp3_tag_grouping = ''
        else:
            mp3_tag_grouping = mp3_tags['TAG']['grouping']

        list_lenght.append(
                            str(start).split('.')[0] + ' Track ' +
                            (mp3_tags['TAG']['track']).split('/')[0] + ' ' +
                            mp3_tags['TAG']['title'] + '' +
                            mp3_tag_grouping
        )
        start += parse_ts(end)
        combined += mp3_to_list

    output_file_name = mp3_tags['TAG']['album_artist'] + ' ' + mp3_tags['TAG']['album'] + '.wav'
    combined.export(output_file_name, format="wav")
    print(*list_lenght, sep='\n')

    with open("info.txt", 'w') as output:
        for row in list_lenght:
            output.write(str(row) + '\n')
    break

image = Image.open('folder.jpg')
new_image = image.resize((720, 720))
new_image.save('00.jpg')

cmd_to_run = str(f'ffmpeg -loop 1 -r 1 -i "00.jpg" -vcodec vp8 -i "{output_file_name}" -acodec copy -shortest "{output_file_name[:len(output_file_name)-4]}.mkv"')
os.popen(cmd_to_run)

print('done')
