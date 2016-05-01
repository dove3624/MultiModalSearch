import pickle
from os import listdir, stat

filenames = listdir('../dataset/audios/')
files = listdir('../dataset/audio_text')


size_to_txt = {}
for filename in filenames:
    if '.wav' in filename:
        statinfo = stat('../dataset/audios/' + filename)
        size_to_txt[statinfo.st_size] = open('../dataset/audio_text/' + filename[:-4] + '.txt','r').read()

fout = open('../dataset/s_to_t.p','wb')
pickle.dump(size_to_txt, fout)

fout.close()