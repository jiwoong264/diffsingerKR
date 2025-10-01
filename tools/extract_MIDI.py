from mido import MidiFile

def extract_midi_data(midi_file_path):
    mid = MidiFile(midi_file_path)
    
    ticks_per_beat = mid.ticks_per_beat
    tempo = 500000
    
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = msg.tempo
                break

    def ticks_to_seconds(ticks):
        return (ticks * tempo) / (ticks_per_beat * 1000000)

    notes = []
    durations = []
    lyrics = []

    # 모든 트랙을 병합해서 처리
    all_messages = []
    for track_idx, track in enumerate(mid.tracks):
        time_accum = 0
        for msg in track:
            time_accum += msg.time
            all_messages.append((time_accum, msg, track_idx))
    
    # 시간순 정렬
    all_messages.sort(key=lambda x: x[0])
    
    current_note = None
    note_start_time = None
    last_end_time = 0
    
    # 묵음 임계값 (초 단위) - 이 값 이상의 간격만 묵음으로 처리
    REST_THRESHOLD = 0.1  # 0.1초 이상 간격만 묵음으로 간주
    
    for time_accum, msg, track_idx in all_messages:
        
        if msg.type == 'note_on' and msg.velocity > 0:
            
            # 묵음 기간 체크 (임계값 이상의 간격만)
            if last_end_time > 0 and time_accum > last_end_time:
                rest_duration_ticks = time_accum - last_end_time
                rest_duration_seconds = ticks_to_seconds(rest_duration_ticks)
                
                # 임계값 이상일 때만 묵음 추가
                if rest_duration_seconds >= REST_THRESHOLD:
                    notes.append(0)
                    durations.append(rest_duration_seconds)
                    lyrics.append('<X>')
            
            # 이전 노트 종료 처리
            if current_note is not None and note_start_time is not None:
                duration_ticks = time_accum - note_start_time
                duration_seconds = ticks_to_seconds(duration_ticks)
                durations.append(duration_seconds)
                last_end_time = time_accum
            
            # 새 노트 시작
            current_note = msg.note
            note_start_time = time_accum
            notes.append(current_note)
            lyrics.append('')

        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            
            if current_note == msg.note and note_start_time is not None:
                duration_ticks = time_accum - note_start_time
                duration_seconds = ticks_to_seconds(duration_ticks)
                durations.append(duration_seconds)
                last_end_time = time_accum
                current_note = None
                note_start_time = None

        elif msg.type == 'lyrics':
            
            try:
                lyric_bytes = msg.text.encode('latin1')
                lyric_decoded = lyric_bytes.decode('euc-kr')
            except UnicodeDecodeError:
                lyric_decoded = msg.text

            # 가장 최근 빈 lyrics에 입력
            for i in range(len(lyrics) - 1, -1, -1):
                if lyrics[i] == '':
                    lyrics[i] = lyric_decoded
                    break
            else:
                lyrics.append(lyric_decoded)
    
    # 길이 맞추기
    min_len = min(len(notes), len(durations), len(lyrics)) if notes and durations and lyrics else 0

    # lyrics 원소 한 글자씩만 남기기
    for i in range(min_len):
        if lyrics[i] != '<X>':
            lyrics[i] = lyrics[i][0] if lyrics[i] else ''

    
    return notes[:min_len], durations[:min_len], lyrics[:min_len]



notes, durations, lyrics = extract_midi_data('/home/woong/song/diffsingerKR/Datasets_s02ro/data/eval/ro_00973_+0_a_s02_m_02.mid')

print(f"\n=== 최종 결과 ===")
print(f"notes: {notes}")
print(f"durations: {durations}")
print(f"lyrics: {lyrics}")

# for n, d, l in zip(notes, durations, lyrics):
#     print(f"n: {n}, d: {d}, l: '{l}'")

