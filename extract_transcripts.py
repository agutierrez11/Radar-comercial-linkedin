from youtube_transcript_api import YouTubeTranscriptApi

def fetch_and_save(video_id, filename):
    print(f"Fetching transcript for {video_id}...")
    try:
        ytt = YouTubeTranscriptApi()
        transcript = ytt.fetch(video_id, languages=['es', 'es-419', 'en'])
        full_text = []
        for item in transcript:
            full_text.append(item['text'])
        content = " ".join(full_text)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully saved {filename} ({len(content)} chars)")
        return content
    except Exception as e:
        print(f"Error fetching {video_id}: {e}")
        # Try list transcripts
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            for t in transcript_list:
                print("Available transcript:", t.language, t.language_code)
                fetched = t.fetch()
                full_text = [item['text'] for item in fetched]
                content = " ".join(full_text)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Successfully saved {filename} via list_transcripts ({len(content)} chars)")
                return content
        except Exception as ex:
            print(f"List transcripts failed: {ex}")
        return ""

t1 = fetch_and_save('f750ORi1-ws', 'transcript_video1.txt')
t2 = fetch_and_save('hS8hSusH5ck', 'transcript_video2.txt')
