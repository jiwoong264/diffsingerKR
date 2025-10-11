import os
import re
import csv
from collections import Counter
from mido import MidiFile

# 1. MIDI 파일들이 있는 폴더 경로를 지정합니다.
# 경로의 시작 부분에 'r'을 붙이거나, 백슬래시를 두 번(\\) 사용해주세요.
MIDI_FOLDER_PATH = r'/home/woong/song/diffsingerKR/Datasets_s02ro/data/train'  # <--- 분석하고 싶은 미디 파일이 있는 폴더 경로를 여기에 입력하세요.

# 3. 최종 결과가 저장될 CSV 파일 경로입니다.
OUTPUT_CSV_PATH = './output.csv'

def analyze_lyrics_in_folder(folder_path):
    """
    지정된 폴더 내의 모든 MIDI 파일에서 한글 가사를 추출하고,
    어절별 빈도수를 계산합니다.
    """
    if not os.path.isdir(folder_path):
        print(f"오류: 폴더를 찾을 수 없습니다 - '{folder_path}'")
        return None

    korean_word_counter = Counter()
    
    # 폴더 내의 모든 파일을 순회합니다.
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.mid'):
            file_path = os.path.join(folder_path, filename)
            print(f"'{file_path}' 파일 분석 중...")
            
            try:
                mid = MidiFile(file_path, clip=True)
                syllables = []
                
                # MIDI 파일의 모든 트랙과 메시지를 확인합니다.
                for track in mid.tracks:
                    for msg in track:
                        if msg.type == 'lyrics':
                            try:
                                # 가사 인코딩 처리 (euc-kr 시도)
                                lyric_bytes = msg.text.encode('latin1')
                                lyric_decoded = lyric_bytes.decode('euc-kr')
                                syllables.append(lyric_decoded)
                            except (UnicodeDecodeError, AttributeError):
                                # 디코딩 실패 시 원본 텍스트(알파벳 등)는 무시
                                pass

                # 추출된 음절들을 합쳐 전체 가사 문자열 생성
                full_lyrics = "".join(syllables)
                
                # 불필요한 문자(개행 등)를 공백으로 치환
                cleaned_lyrics = full_lyrics.replace('\r', ' ').replace('\n', ' ')
                
                # 공백을 기준으로 어절(단어) 분리
                words = cleaned_lyrics.split()
                
                # 한글로만 이루어진 어절만 필터링하여 카운터에 추가
                for word in words:
                    # 정규표현식을 사용하여 한글이 아닌 모든 문자 제거
                    korean_word = re.sub(r'[^가-힣]', '', word)
                    if korean_word:  # 정제 후 남은 한글이 있을 경우에만
                        korean_word_counter[korean_word] += 1
                        
            except Exception as e:
                print(f"'{file_path}' 파일 처리 중 오류 발생: {e}")

    return korean_word_counter

def save_counts_to_csv(word_counts, output_path):
    """
    어절 빈도수 데이터를 기반으로 CSV 파일을 생성합니다.
    """
    if not word_counts:
        print("분석된 한글 어절이 없어 CSV 파일을 생성하지 않습니다.")
        return

    # 가나다 순으로 정렬
    sorted_items = sorted(word_counts.items())
    
    try:
        # CSV 파일로 저장
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            # 헤더(머리글) 작성
            writer.writerow(['어절', '빈도수'])
            # 데이터 작성
            writer.writerows(sorted_items)
            
        print(f"\n결과가 성공적으로 '{output_path}' 파일에 저장되었습니다.")
        print("엑셀이나 다른 스프레드시트 프로그램으로 파일을 열어보세요.")

    except Exception as e:
        print(f"CSV 파일 저장 중 오류 발생: {e}")


if __name__ == '__main__':
    # 폴더가 없으면 생성
    if not os.path.exists(MIDI_FOLDER_PATH):
        print(f"'{MIDI_FOLDER_PATH}' 폴더를 생성합니다. 분석할 MIDI 파일들을 해당 폴더에 넣어주세요.")
        os.makedirs(MIDI_FOLDER_PATH)

    # 메인 로직 실행
    word_counts = analyze_lyrics_in_folder(MIDI_FOLDER_PATH)
    if word_counts:
        save_counts_to_csv(word_counts, OUTPUT_CSV_PATH)

