from flask import Flask, request
from video_loader import *

app = Flask(__name__)
@app.route('/lda-api')
def video_to_text():
    bucket_name = "capstone-test"
    file_name = request.args.get("fileName")
    destination_file_name = "audio.wav"
    blob_name = file_name + "/" + file_name + ".wav"
    download_audio(bucket_name, blob_name, destination_file_name)
    divide_audio(destination_file_name)
    count_script = sample_recognize_short(destination_file_name)
    make_topic(count_script, file_name)
    return file_name

if __name__ == "__main__":
    app.run()