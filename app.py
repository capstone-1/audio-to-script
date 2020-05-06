from flask import Flask, request
from video_loader import *
from eng_sentence_extractor import *

app = Flask(__name__)
@app.route('/script-api')
def extractor():
    # audio download -> sliced audio
    bucket_name = "capstone-test"
    video_name = request.args.get("fileName")
    destination_file_name = "audio.wav"
    blob_name = video_name + "/source/" + video_name + ".wav"
    download_audio(bucket_name, blob_name, destination_file_name)
    divide_audio(destination_file_name)

    # sliced audio -> sliced script, total script
    count_script = sample_recognize_short(destination_file_name)

    # sliced-script -> topic words
    make_topic(count_script, video_name)

    # total-script -> summary
    script_to_summary(video_name)

    return video_name

if __name__ == "__main__":
    app.run()