"""
FILE NAME   : main.py
PURPOSE     : Main logic to summarize a youtube video using chatGPT
PROGRAMMER  : Aleksei Seliverstov.
NOTE        : None.

Copyright (c) 2023 Aleksei Seliverstov
"""
import config
import strings
import utils


def main(yt_link):
    """
    Generate a summary of the transcript of a YouTube video.

    Args:
        yt_link (str): The link to the YouTube video.

    Returns:
        None
    """
    video_id = utils.get_video_id(yt_link)

    # Get transcript in parts:
    #
    # Send several messages to ChatGPT:
    # First is:
    # strings.intro_prompt
    # Every following is:
    # strings.transcript_part_begin + [timestamp: line] * x times
    # + strings.transcript_part_end
    # Each of these messages has to fit in token limits, so no more
    # than config.token_limit characters in any language
    # For the very last part:
    # strings.transcript_part_begin + [timestamp: line] * x times
    # + strings.final_prompt
    #
    split_transcript = [strings.intro_prompt]
    i = 1
    transcript_text = strings.transcript_part_begin(i)
    for t in utils.get_video_transcript(video_id):
        timestamp = utils.convert_seconds_to_time(t['start'])
        transcript_text += f"{timestamp} {t['text']}\n"
        if len(transcript_text) > config.token_limit:
            # Avoid token limit -- split too long transcripts into parts
            transcript_text += strings.transcript_part_end(i)
            split_transcript.append(transcript_text)
            i += 1
            transcript_text = strings.transcript_part_begin(i)
    split_transcript = [t.replace(strings.unique_char, str(i - 1))
                        for t in split_transcript]
    split_transcript[-1] = split_transcript[-1].replace(
        strings.transcript_last_part(i), '') + strings.final_prompt

    # Make a request to chatGPT for every part of transcript
    for tr in split_transcript[:-1]:
        response = utils.use_chatgpt(tr)
        # Every response here is disposable of (is garbage)
        print(response)
    # The last response is requested summary
    summary = utils.use_chatgpt(split_transcript[-1])

    with open("summary.txt", "w", encoding='utf-8') as f:
        f.write(summary)
    print(summary)


if __name__ == "__main__":
    main("https://youtu.be/MqyJZsGFZ3M")
