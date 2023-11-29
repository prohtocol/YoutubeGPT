"""
FILE NAME   : strings.py
PURPOSE     : Collection of strings used in the program
PROGRAMMER  : Aleksei Seliverstov.
NOTE        : None.

Copyright (c) 2023 Aleksei Seliverstov
"""

intro_prompt = """The total length of the content that I want to send you is too large to send in only one piece.

For sending you that content, I will follow this rule:

[START PART 1/10]
this is the content of the part 1 out of 10 in total
[END PART 1/10]

Then you just answer: "Received part 1/10"

And when I tell you "ALL PARTS SENT", then you can continue processing the data and answering my requests."""

unique_char = 'ß'


def transcript_part_begin(i):
    return f"""Do not answer yet. This is just another part of the text I want to send you. Just receive and
    acknowledge as "Part {i}/{unique_char} received" and wait for the next part.
[START PART {i}/{unique_char}]"""


def transcript_part_end(i):
    return f"[END PART {i}/{unique_char}]"


def transcript_last_part(i):
    return (f'Do not answer yet. This is just another part of the text I want to send you. Just receive and '
            f'acknowledge as "Part {i - 1}/{i - 1} received" and wait for the next part.')


final_prompt = ("ALL PARTS SENT. Now you can continue processing the request. Summarize the transcript with no less "
                "than 10 timecodes.")
