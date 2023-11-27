import sys
import youtube_api as yt
import openai_api as op
import datetime





def main():
    # youtube_link = sys.argv[1]
    # output_language = sys.argv[2]
    youtube_link = "https://youtu.be/MqyJZsGFZ3M"
    video_id = yt.getVideoId(youtube_link)

    #### Get transcript in parts

    def convert_seconds_to_time(seconds):
        time = str(datetime.timedelta(seconds=seconds))
        time_parts = time.split(":")
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        seconds = int(float(time_parts[2]))
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


    tr = yt.getTranscript(video_id)
    transcripts = ["""The total length of the content that I want to send you is too large to send in only one piece.

For sending you that content, I will follow this rule:

[START PART 1/10]
this is the content of the part 1 out of 10 in total
[END PART 1/10]

Then you just answer: "Received part 1/10"

And when I tell you "ALL PARTS SENT", then you can continue processing the data and answering my requests."""]
    i = 1
    transcript_text = f"""Do not answer yet. This is just another part of the text I want to send you. Just receive and acknowledge as "Part {i}/ß received" and wait for the next part.
[START PART {i}/ß]"""
    for t in tr:
        start_time = convert_seconds_to_time(t['start'])
        transcript_text += f"{start_time} {t['text']}\n"
        if len(transcript_text) > 10000:
            transcript_text += f"[END PART {i}/ß]"
            i += 1
            transcripts.append(transcript_text)
            transcript_text = f"""Do not answer yet. This is just another part of the text I want to send you. Just receive and acknowledge as "Part {i}/ß received" and wait for the next part.
[START PART {i}/ß]"""


    transcripts = [t.replace("ß", str(i - 1)) for t in transcripts]
    # transcript = yt.getTranscriptText(video_id)


    for text in transcripts[:-1]:
        a = op.use_chatGPT(text)
        print(a)

    summary = op.use_chatGPT(transcripts[-1])
    print(summary)



if __name__ == "__main__":
    main()
