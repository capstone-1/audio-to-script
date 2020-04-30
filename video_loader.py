#TODO: 
# 1. get Audio from Videos - done
# 2. cut Audio (interval : 1m) -done
# 3. make script - done
# 4. merge script (10m)

from google.cloud import storage
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io
import wave
import contextlib
from pydub import AudioSegment
import glob

def download_audio(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )

def getStorageUri(bucket_name, file_name):
    return "gs://" + bucket_name + "/" + file_name


def sample_recognize_short():
        """
        Transcribe a short audio file using synchronous speech recognition
        Args:
          local_file_path Path to local audio file, e.g. /path/audio.wav
        """    
        client = speech_v1.SpeechClient()

        # The language of the supplied audio
        language_code = "ko-KR"

        # Sample rate in Hertz of the audio data sent
        sample_rate_hertz = 16000

        # Encoding of audio data sent. This sample sets this explicitly.
        # This field is optional for FLAC and WAV audio formats.
        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
        config = {
            "language_code": language_code,
            "sample_rate_hertz": sample_rate_hertz,
            "encoding": encoding,
        }

        local_files = glob.glob("./sliced*")
        for local_file_path in local_files :
            with io.open(local_file_path, "rb") as f:
                content = f.read()
            audio = {"content": content}
            script_file_name = "scrpt_" + local_file_path.split("_")[1].split(".")[0]
            fd = open(script_file_name, 'w')
            response = client.recognize(config, audio)
            print(u"Current File : " + local_file_path)
            for result in response.results:
                # First alternative is the most probable result
                alternative = result.alternatives[0]
                fd.write(alternative.transcript)
            fd.close()
                

def divide_aduio(destination_file_name):
    duration = get_audio_duration(destination_file_name)
    for start in range(0,duration,59) :
        if (duration - start < 59) :
            end = duration
        else :
            end = start + 59
        save_sliced_audio(start, end, destination_file_name)

def save_sliced_audio(start,end, destination_file_name) :
    audio = AudioSegment.from_wav(destination_file_name)
    file_name = "sliced_" + str(start) + "-" + str(end) + ".wav"
    start_time = start * 1000
    end_time = end * 1000
    audio[start_time:end_time].export(file_name ,format = "wav")
    
def get_audio_duration(destination_file_name):
    with contextlib.closing(wave.open(destination_file_name, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames/float(rate)
        return int(duration)

if __name__ == "__main__":
    bucket_name = "capstone-sptt-storage"
    file_name = "test123.wav"
    destination_file_name = "audio.wav"
    # storage_uri = getStorageUri(bucket_name,file_name)
    storage_uri = "./audio.wav"

    download_audio(bucket_name, file_name, destination_file_name)
    divide_aduio(storage_uri)
    sample_recognize_short()



##### Long Running Job
# def sample_recognize_long(storage_uri):
#     """
#     Performs synchronous speech recognition on an audio file

#     Args:
#       storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
#     """
#     client = speech_v1.SpeechClient()

#     # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.mp3'

#     # The language of the supplied audio
#     language_code = "ko-KR"

#     # Sample rate in Hertz of the audio data sent
#     sample_rate_hertz = 16000

#     # Encoding of audio data sent. This sample sets this explicitly.
#     # This field is optional for FLAC and WAV audio formats.
#     encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
#     config = {
#         "language_code": language_code,
#         "sample_rate_hertz": sample_rate_hertz,
#         "encoding": encoding,
#     }
#     audio = {"uri": storage_uri}
#     operation = client.long_running_recognize(config, audio)
#     print(u"Waiting for operations to complete...")
#     response = operation.result()
#     script = "";
#     for result in response.results:
#         # First alternative is the most probable result
#         alternative = result.alternatives[0]
#         script += (alternative.transcript + "\n")

#     print("result : " + script)