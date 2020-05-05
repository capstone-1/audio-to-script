from flask import Flask, request
from video_loader import *
from eng_sentence_extractor import *

app = Flask(__name__)
@app.route('/lda-api')
def video_to_topic():
    bucket_name = "capstone-test"
    video_name = request.args.get("fileName")
    destination_file_name = "audio.wav"
    blob_name = video_name + "/" + video_name + ".wav"
    download_audio(bucket_name, blob_name, destination_file_name)
    divide_audio(destination_file_name)
    count_script = sample_recognize_short(destination_file_name)
    make_topic(count_script, video_name)
    return video_name

@app.route('/sentence-api')
def video_to_sentence():
    script_to_summary()
    video_name = request.args.get("fileName")
    upload_total_script_file(video_name)
    return video_name

if __name__ == "__main__":
    app.run()