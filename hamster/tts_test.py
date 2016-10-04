import androidhelper

a = androidhelper.Android()

a.ttsSpeak('Hello World! Now we are talking.')

if a.ttsIsSpeaking():
    print('Either TTS has been speaking or ttsSpeak() is async.')
else:
    print('TTS is not speaking as of now.')
