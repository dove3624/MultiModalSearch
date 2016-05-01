from pydub import AudioSegment
from os import listdir
from subprocess import call

filenames = listdir("../dataset/audio_text/")

for filename in filenames:

    if 'wav' in filename:
        sound = AudioSegment.from_mp3("../dataset/audio_text/"+filename)

        #sound.export("../dataset/audio_text/"+filename[:-4] + '.wav', format="wav")

        call(['avconv', '-i', "../dataset/audio_text/"+filename, '-c:a',  'copy',  '-c:v', 'copy', '-ss', '00:00:10', '-t', '00:00:10', "../dataset/audios/"+filename])