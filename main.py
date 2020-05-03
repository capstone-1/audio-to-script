from flask import Flask, request
from video_loader import *

app = Flask(__name__)
@app.route('/lda-api')
def create_script():
    bucket_name = "capstone-test"
    file_name = request.args.get("fileName")+".wav"
    destination_file_name = "audio.wav"
    # storage_uri = getStorageUri(bucket_name,file_name)
    download_audio(bucket_name, file_name, destination_file_name)
    divide_audio(destination_file_name)
    sample_recognize_short(destination_file_name)
    make_topic()
    return file_name

if __name__ == "__main__":
    app.run()