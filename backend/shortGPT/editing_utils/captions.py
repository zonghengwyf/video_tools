import re
from shortGPT.subtitles.subtitles_utls import PUNCTUATION_pattern

def getSpeechBlocks(whispered, silence_time=2):
    text_blocks, (st, et, txt) = [], (0,0,"")
    for i, seg in enumerate(whispered['segments']):
        if seg['start'] - et > silence_time:
            if txt: text_blocks.append([[st, et], txt])
            (st, et, txt) = (seg['start'], seg['end'], seg['text'])
        else: 
            et, txt = seg['end'], txt + seg['text']

    if txt: text_blocks.append([[st, et], txt]) # For last text block

    return text_blocks

def cleanWord(word):
    return re.sub(r'[^\w\s\-_"\'\']', '', word)

def interpolateTimeFromDict(word_position, d):
    for key, value in d.items():
        if key[0] <= word_position <= key[1]:
            return value
    return None

def getTimestampMapping(whisper_analysis):
    index = 0
    locationToTimestamp = {}
    for segment in whisper_analysis['segments']:
        for word in segment['words']:
            newIndex = index + len(word['text'])+1
            locationToTimestamp[(index, newIndex)] = word['end']
            index = newIndex
    return locationToTimestamp

def splitWordsBySize(words, maxCaptionSize):
    halfCaptionSize = maxCaptionSize / 2.0
    captions = []
    while words:
        caption = words[0]
        words = words[1:]
        while words and len(caption.encode('gbk') + ' '.encode('gbk') + words[0].encode('gbk')) <= maxCaptionSize:
            caption += ' ' + words[0]
            words = words[1:]
            if len(caption.encode('gbk')) >= halfCaptionSize and words:
                break
        captions.append(caption)
    return captions

def getCaptionsWithTime(whisper_analysis, maxCaptionSize=15, considerPunctuation=True):
    wordLocationToTime = getTimestampMapping(whisper_analysis)
    position = 0
    start_time = 0
    CaptionsPairs = []
    text = whisper_analysis['text']
    
    if considerPunctuation:
        sentences = re.split(PUNCTUATION_pattern, text)
        words = [word for sentence in sentences for word in splitWordsBySize(sentence.split(), maxCaptionSize)]
    else:
        words = text.split()
        words = [cleanWord(word) for word in splitWordsBySize(words, maxCaptionSize)]
    for word in words:
        position += len(word) + 1
        end_time = interpolateTimeFromDict(position, wordLocationToTime)
        if end_time and word:
            CaptionsPairs.append(((start_time, end_time), word))
            start_time = end_time

    return CaptionsPairs


def getCaptionsWithTimeChinese(whisper_analysis, maxCaptionSize=15, considerPunctuation=False):
    CaptionsPairs = []
    word_index = 0

    words = re.split(PUNCTUATION_pattern, whisper_analysis['text'])
    for segment in whisper_analysis['segments']:
        start_time = segment['start']
        end_time = segment['end']
        find_word = ""
        for word in segment['words']:
            word_text = cleanWord(word["text"])
            if find_word == "":
                #start_time = word['start']
                start_time = CaptionsPairs[-1][0][1] if CaptionsPairs else end_time
            find_word += word_text
            if find_word == "" or words[word_index].find(word_text) < 0:
                word_index += 1
                continue
            if find_word == words[word_index]:
                end_time = word["end"]
                word_index += 1
                CaptionsPairs.append(((start_time, end_time), find_word))
                find_word = ""
    if CaptionsPairs and len(CaptionsPairs[0]) == 2:
        CaptionsPairs[0] = ((0, CaptionsPairs[0][0][1]), CaptionsPairs[0][1])
        CaptionsPairs[-1] = ((CaptionsPairs[-1][0][0], whisper_analysis['segments'][-1]["end"]), CaptionsPairs[-1][1])
    return CaptionsPairs
