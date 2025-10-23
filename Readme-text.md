# 🚗 Brain AI Car

DFRobot 확장 보드와 Micro:bit를 사용한 자율주행 RC카 프로젝트

## 📋 목차

- [프로젝트 소개](#프로젝트-소개)
- [시스템 구성](#시스템-구성)
- [설치 방법](#설치-방법)
- [사용 방법](#사용-방법)
- [프로젝트 구조](#프로젝트-구조)
- [하드웨어 설정](#하드웨어-설정)

---

## 🎯 프로젝트 소개

Brain AI Car는 딥러닝 기반 차선 인식을 통한 자율주행 RC카 프로젝트입니다.

### 주요 기능
- 🎮 PS4 컨트롤러를 이용한 수동 조작
- 📹 실시간 영상 스트리밍 (IP Webcam)
- 💾 주행 데이터 자동 수집 및 라벨링
- 🧠 CNN 기반 차선 인식 모델 학습
- 🚘 자율주행 모드
- 🔍 물체 감지 및 안전 정지

---

## 🔧 시스템 구성

### 하드웨어
- **제어 보드**: BBC Micro:bit (2개)
  - 차량 본체용 1개
  - 시리얼-라디오 브릿지용 1개
- **확장 보드**: DFRobot Driver Expansion Board (DFR0548)
- **모터**: DC 모터 (M1 포트 연결)
- **서보**: 서보 모터 (S8 포트 연결)
- **컨트롤러**: PS4 DualShock 4
- **카메라**: IP Webcam (Android 앱)

### 소프트웨어
- Python 3.8+
- TensorFlow 2.13+
- OpenVINO 2023+
- OpenCV 4.8+
- Pygame 2.5+

---

## 📦 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/yourusername/brain-ai-car.git
cd brain-ai-car
```

### 2. 가상환경 생성 (권장)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. Micro:bit 펌웨어 업로드
1. `microbit/car_body.py`를 차량 본체 Micro:bit에 업로드
2. `microbit/controller_bridge.py`를 PC 연결용 Micro:bit에 업로드

---

## 🚀 사용 방법

### Step 1: PS4 컨트롤러 테스트
```bash
python -m main.test_controller
```
컨트롤러가 정상적으로 연결되었는지 확인합니다.

### Step 2: 데이터 수집
```bash
python -m main.collect_data
```
**조작 방법:**
- `R2`: 전진
- `L2`: 후진
- `왼쪽 스틱`: 조향
- `R1`: 녹화 토글
- `Q`: 종료
- `D`: 마지막 2초 삭제

### Step 3: 이미지 라벨링
```bash
python -m tools.annotator
```
수집한 이미지에 조향 값을 라벨링합니다.

### Step 4: 데이터셋 생성
```bash
python -m training.dataset_creator
```
라벨링된 데이터를 학습/검증 세트로 분할합니다.

### Step 5: 모델 학습
```bash
python -m training.model_trainer
```
CNN 모델을 학습합니다.

### Step 6: 자율주행
```bash
python -m main.autonomous_drive
```
학습된 모델로 자율주행을 실행합니다.

---

## 📂 프로젝트 구조

```
brain_ai_car/
│
├── main/                      # 메인 실행 파일
│   ├── test_controller.py    # PS4 컨트롤러 테스트
│   ├── collect_data.py       # 데이터 수집
│   └── autonomous_drive.py   # 자율주행
│
├── core/                      # 핵심 모듈
│   ├── car_controller.py     # 차량 제어
│   ├── ps4_controller.py     # PS4 컨트롤러
│   ├── video_stream.py       # 비디오 스트림
│   ├── data_collector.py     # 데이터 수집
│   ├── lane_detector.py      # 차선 감지
│   └── object_detector.py    # 물체 감지
│
├── training/                  # 학습 관련
│   ├── model_trainer.py      # 모델 학습
│   ├── model_updater.py      # 모델 업데이트
│   └── dataset_creator.py    # 데이터셋 생성
│
├── tools/                     # 유틸리티 도구
│   ├── annotator.py          # 이미지 라벨링
│   ├── data_viewer.py        # 데이터 확인
│   └── video_extractor.py    # 비디오 프레임 추출
│
├── microbit/                  # Micro:bit 펌웨어
│   ├── car_body.py           # 차량 본체
│   └── controller_bridge.py  # 시리얼-라디오 브릿지
│
├── models/                    # 학습된 모델
├── data/                      # 수집 데이터
├── requirements.txt           # 의존성
└── README.md                  # 이 파일
```

---

## 🔌 하드웨어 설정

### DFRobot 확장 보드 핀 연결

#### 모터 M1 (주행 모터)
- `P13`: 방향 제어 (1=전진, 0=후진)
- `P14`: 속도 제어 (PWM, 0-1023)

#### 서보 S8 (조향 서보)
- `P8`: PWM 신호 (각도 45-135도)

### Micro:bit 간 통신
- **라디오 그룹**: 123
- **통신 방식**: 2.4GHz 라디오

### PC 연결
- **시리얼 통신**: USB (115200 baud)
- **프로토콜**: 텍스트 기반 명령

---

## 🎮 제어 명령

### 시리얼 명령 형식
- `0`: 정지
- `-1`: 후진
- `45-135`: 서보 각도
- `180-1023`: 전진 속도
- `2000`: 연결 확인

---

## 📊 모델 정보

### 아키텍처
- **백본**: MobileNetV3-Large (α=0.75)
- **입력 크기**: 224×224×3
- **출력**: 단일 값 (조향 각도)
- **손실 함수**: MSE
- **옵티마이저**: Adam

### 성능
- **추론 속도**: ~30 FPS (OpenVINO)
- **정확도**: MAE < 5도

---

## 🛠️ 문제 해결

### Micro:bit 연결 안 됨
```bash
# 포트 확인
python -c "import serial.tools.list_ports; print([p.device for p in serial.tools.list_ports.comports()])"
```

### PS4 컨트롤러 연결 안 됨
- Bluetooth 페어링 확인
- Steam이 실행 중인지 확인 (종료 필요)

### IP Webcam 연결 실패
- 같은 Wi-Fi 네트워크에 연결되어 있는지 확인
- 방화벽 설정 확인
- URL 형식: `http://[IP주소]:8080/video`

---

## 📝 라이선스

MIT License

---

## 👥 기여자

- Your Name - Initial work

---

## 🙏 감사의 말

- DFRobot for the expansion board
- BBC Micro:bit Foundation
- TensorFlow and OpenVINO teams
