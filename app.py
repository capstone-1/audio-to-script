from flask import Flask, request, jsonify
from video_loader import download_audio, divide_audio, sample_recognize_short
from kor_sentence_extractor import script_to_summary 
from topic_maker import make_topic
from collections import OrderedDict
from flask_cors import CORS, cross_origin
import json
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/script-api')
@cross_origin()
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
    topics = make_topic(count_script)

    # total-script -> summary
    summary = script_to_summary(video_name)

    script_url = "https://storage.cloud.google.com/" + bucket_name + "/" + video_name + "/result/total_script.txt"

    return make_response(script_url, topics, summary)

def make_response(script_url, topics, summary):
    scriptItem = OrderedDict()
    scriptItem["fullScript"] = script_url
    scriptItem["summary"] = summary
    scriptItem["topicEditList"] = topics
    
    return jsonify(scriptItem)

if __name__ == "__main__":
    app.run(port = 5000)