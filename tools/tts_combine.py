# 한글 가사로부터 MP3 파일들을 순서대로 연결하고 딜레이를 추가하는 프로그램
# pip install pydub 필요

import os
import re
from pydub import AudioSegment

def process_lyrics_to_audio(lyrics, input_dir, output_file):
    """
    한글 가사를 받아서 각 글자에 해당하는 MP3 파일을 연결하여 WAV로 저장
    
    Args:
        lyrics (str): 노래 가사 텍스트
        input_dir (str): MP3 파일들이 있는 디렉토리 경로
        output_file (str): 출력할 WAV 파일 경로
    """
    
    # 공백과 줄바꿈 제거, 한글만 추출
    korean_chars = re.findall(r'[가-힣]', lyrics)
    
    if not korean_chars:
        print("한글 문자가 없습니다.")
        return
    
    print(f"처리할 한글 문자들: {korean_chars}")
    
    # 0.5초 딜레이 생성
    delay = AudioSegment.silent(duration=300)  # 500ms = 0.5초
    
    # 최종 오디오 시작 (0.5초 딜레이로 시작)
    final_audio = delay
    
    missing_files = []
    
    for i, char in enumerate(korean_chars):
        mp3_file = os.path.join(input_dir, f"{char}.mp3")
        
        if os.path.exists(mp3_file):
            try:
                # MP3 파일 로드
                char_audio = AudioSegment.from_mp3(mp3_file)
                
                # 문자 음성 추가
                final_audio += char_audio
                
                # 딜레이 추가
                final_audio += delay
                
                print(f"추가됨: {char}")
                
            except Exception as e:
                print(f"{char}.mp3 파일 로드 중 오류: {e}")
                missing_files.append(char)
        else:
            print(f"파일이 없습니다: {char}.mp3")
            missing_files.append(char)
    
    # 마지막에 0.5초 딜레이 추가
    final_audio += delay
    
    if missing_files:
        print(f"누락된 파일들: {missing_files}")
    
    # WAV 파일로 저장
    try:
        final_audio.export(output_file, format="wav")
        print(f"완료! 출력 파일: {output_file}")
        print(f"총 길이: {len(final_audio) / 1000:.2f}초")
        print(f"총 {len(korean_chars)}개 문자 처리됨")
        
    except Exception as e:
        print(f"파일 저장 중 오류: {e}")

def main():
    """메인 함수"""
    # 설정
    input_directory = "./tts_nogada"
    
    # 디렉토리 존재 확인
    if not os.path.exists(input_directory):
        print(f"디렉토리가 존재하지 않습니다: {input_directory}")
        return
    
    lyrics_list = [
        "이재명 뽑아줘요 일번 대한민국 대통령 일번 일잘하는 이 재명 너무 너무 좋아요",
        "윤석열 국민의힘 이번 민생경제 일으킬 이번 국민위해 일 하는 기호 이번 윤석열",
        "이준석 개혁신당 사번 청년세대 위하는 사번 연금개혁 꼭 해낼 개혁 신당 좋아요"
    ]
    
    print("-" * 50)
    
    i = 1
    # 처리 실행
    for lyrics in lyrics_list:
        output_file = "./results/"+ str(i) + "_" + lyrics + ".wav"
        process_lyrics_to_audio(lyrics, input_directory, output_file)
        i += 1

if __name__ == "__main__":
    print("=== 한글 가사를 음성으로 변환하는 프로그램 ===")
    print("사용법: 한글 가사를 입력하면 각 글자별 MP3 파일을 연결하여 WAV로 저장합니다.")
    print("필요 패키지: pip install pydub")
    print()
    
    main()