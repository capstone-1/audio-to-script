import com.google.api.gax.longrunning.OperationFuture;
import com.google.cloud.speech.v1.*;
import com.google.cloud.storage.*;

import java.io.FileWriter;
import java.io.UnsupportedEncodingException;

import static java.nio.charset.StandardCharsets.UTF_8;


public class Main {

    public static void main(String[] args) {
        //File format have to be wav
        String storageUri = getStorageUri("capstone-sptt-storage", "test-video.mp4");
        divideVideo(storageUri);
//        sampleRecognize(storageUri);
    }

    private static String getStorageUri(String storageName, String fileName) {
        return "gs://" + storageName + "/" + fileName;
    }

    private static void divideVideo(String storageUri) {

    }
    /**
     * Performs synchronous speech recognition on an audio file
     *
     * @param storageUri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
     */
    public static void sampleRecognize(String storageUri) {
        try (SpeechClient speechClient = SpeechClient.create()) {
            RecognitionConfig config = getRecognitionConfig();
            RecognitionAudio audio = RecognitionAudio.newBuilder().setUri(storageUri).build();
            LongRunningRecognizeRequest request =
                    LongRunningRecognizeRequest.newBuilder().setConfig(config).setAudio(audio).build();
            OperationFuture<LongRunningRecognizeResponse, LongRunningRecognizeMetadata> future =
                    speechClient.longRunningRecognizeAsync(request);

            System.out.println("Waiting for operation to complete...");

            LongRunningRecognizeResponse response = future.get();

            System.out.println("Completed!");
            //FileWriter writer = new FileWriter("script.txt");
            StringBuilder resultScript = new StringBuilder();
            for (SpeechRecognitionResult result : response.getResultsList()) {
                // First alternative is the most probable result
                SpeechRecognitionAlternative alternative = result.getAlternativesList().get(0);
                resultScript.append(alternative.getTranscript()).append('\n');
            }
            uploadToGoogleStorage(resultScript.toString());
//            writer.write(resultScript.toString());
//            writer.close();
        } catch (Exception exception) {
            System.err.println("Failed to create the client due to: " + exception);
        }
    }

    private static RecognitionConfig getRecognitionConfig() {
        // The language of the supplied audio
        String languageCode = "ko-KR";
        // Sample rate in Hertz of the audio data sent
        int sampleRateHertz = 16000;
        // Encoding of audio data sent. This sample sets this explicitly.
        RecognitionConfig.AudioEncoding encoding = RecognitionConfig.AudioEncoding.LINEAR16;
        // This field is optional for FLAC and WAV audio formats.
        return RecognitionConfig.newBuilder()
                .setLanguageCode(languageCode)
                .setSampleRateHertz(sampleRateHertz)
                .setEncoding(encoding)
                .build();
    }

    public static void uploadToGoogleStorage(String data) throws UnsupportedEncodingException {
        Storage storage = StorageOptions.getDefaultInstance().getService();
        BlobId blobId = BlobId.of("capstone-sptt-storage", "script.txt");
        BlobInfo blobInfo = BlobInfo.newBuilder(blobId).setContentType("text/plain").build();
        Blob blob = storage.create(blobInfo, data.getBytes(UTF_8));
    }
}
