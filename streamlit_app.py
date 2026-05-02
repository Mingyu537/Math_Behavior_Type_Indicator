from html import escape

import streamlit as st
import streamlit.components.v1 as components


APP_TITLE = "MBTI"
APP_SUBTITLE = "Mathematics Behavior Type Indicator"
TOTAL_QUESTIONS = 12


LIKERT_OPTIONS = [
    (-2, "매우 왼쪽", "왼쪽 성향에 아주 가까워요"),
    (-1, "약간 왼쪽", "왼쪽 성향에 조금 가까워요"),
    (0, "중간", "두 성향이 비슷해요"),
    (1, "약간 오른쪽", "오른쪽 성향에 조금 가까워요"),
    (2, "매우 오른쪽", "오른쪽 성향에 아주 가까워요"),
]


AXIS_META = {
    "S": {
        "name": "Solo",
        "label": "독립형",
        "description": "혼자 생각을 정리하고 자신만의 속도로 문제를 풀 때 몰입합니다.",
    },
    "T": {
        "name": "Team",
        "label": "협업형",
        "description": "다른 사람과 아이디어를 주고받으며 수학적 사고가 선명해집니다.",
    },
    "V": {
        "name": "Visual",
        "label": "시각 중심",
        "description": "도형, 그래프, 공간 이미지로 개념을 먼저 이해합니다.",
    },
    "N": {
        "name": "Numeric",
        "label": "수치/기호 중심",
        "description": "숫자, 식, 기호의 규칙을 통해 구조를 빠르게 파악합니다.",
    },
    "I": {
        "name": "Intuitive",
        "label": "직관적",
        "description": "전체 흐름과 번뜩이는 아이디어로 해결의 실마리를 찾습니다.",
    },
    "A": {
        "name": "Analytical",
        "label": "분석적",
        "description": "조건과 근거를 차근차근 따져 논리적으로 해결합니다.",
    },
    "R": {
        "name": "Research",
        "label": "탐구/원리",
        "description": "공식과 개념이 왜 성립하는지 깊이 파고드는 데 끌립니다.",
    },
    "P": {
        "name": "Practical",
        "label": "응용/실용",
        "description": "배운 수학을 실제 문제, 발명, 생활 속 활용으로 연결합니다.",
    },
}


QUESTIONS = [
    {
        "id": "q01",
        "axis": ("S", "T"),
        "question": "어려운 수학 문제를 처음 만났을 때 나는?",
        "left": {
            "code": "S",
            "title": "혼자 조용히 생각한다",
            "body": "잠깐 거리를 두고 내 방식대로 조건과 풀이 방향을 정리한다.",
        },
        "right": {
            "code": "T",
            "title": "함께 이야기한다",
            "body": "친구나 팀원과 생각을 나누며 가능한 풀이를 빠르게 넓힌다.",
        },
    },
    {
        "id": "q02",
        "axis": ("V", "N"),
        "question": "새로운 개념을 배울 때 더 먼저 떠오르는 것은?",
        "left": {
            "code": "V",
            "title": "그림과 모양",
            "body": "도형, 그래프, 위치 관계를 머릿속에 그리면 이해가 빨라진다.",
        },
        "right": {
            "code": "N",
            "title": "숫자와 기호",
            "body": "식, 수열, 계산 패턴을 보면 개념의 규칙이 잘 보인다.",
        },
    },
    {
        "id": "q03",
        "axis": ("I", "A"),
        "question": "풀이 아이디어가 떠올랐을 때 나는?",
        "left": {
            "code": "I",
            "title": "직감적으로 밀고 간다",
            "body": "전체 흐름이 맞아 보이면 먼저 시도하면서 감을 확인한다.",
        },
        "right": {
            "code": "A",
            "title": "근거를 확인한다",
            "body": "조건, 정의, 정리를 하나씩 점검하며 논리의 빈틈을 줄인다.",
        },
    },
    {
        "id": "q04",
        "axis": ("R", "P"),
        "question": "수학에서 더 흥미로운 질문은?",
        "left": {
            "code": "R",
            "title": "왜 그렇게 되는가",
            "body": "공식 뒤에 숨어 있는 원리와 증명 과정을 탐구하고 싶다.",
        },
        "right": {
            "code": "P",
            "title": "어디에 쓸 수 있는가",
            "body": "개념을 문제 해결, 발명, 현실 상황에 적용해 보고 싶다.",
        },
    },
    {
        "id": "q05",
        "axis": ("S", "T"),
        "question": "수학 활동에서 가장 편한 방식은?",
        "left": {
            "code": "S",
            "title": "내 속도로 파고들기",
            "body": "혼자 충분히 고민한 뒤 정리된 생각을 보여주는 편이 좋다.",
        },
        "right": {
            "code": "T",
            "title": "역할을 나누어 해결하기",
            "body": "서로 다른 아이디어를 모아 한 문제를 함께 완성하는 편이 좋다.",
        },
    },
    {
        "id": "q06",
        "axis": ("V", "N"),
        "question": "문제 풀이를 시작할 때 더 자주 쓰는 단서는?",
        "left": {
            "code": "V",
            "title": "공간과 관계",
            "body": "점, 선, 면, 그래프의 위치와 움직임을 먼저 살핀다.",
        },
        "right": {
            "code": "N",
            "title": "계산과 패턴",
            "body": "값을 대입하거나 식을 변형하며 숨어 있는 규칙을 찾는다.",
        },
    },
    {
        "id": "q07",
        "axis": ("I", "A"),
        "question": "복잡한 문제를 만났을 때 나는?",
        "left": {
            "code": "I",
            "title": "핵심 장면을 잡는다",
            "body": "문제의 분위기와 큰 아이디어를 먼저 포착하려고 한다.",
        },
        "right": {
            "code": "A",
            "title": "조건을 분해한다",
            "body": "주어진 정보와 필요한 결론을 분리해 단계별로 정리한다.",
        },
    },
    {
        "id": "q08",
        "axis": ("R", "P"),
        "question": "새로운 공식을 배웠을 때 더 끌리는 쪽은?",
        "left": {
            "code": "R",
            "title": "증명과 배경",
            "body": "그 공식이 어떤 생각에서 나왔는지 끝까지 알고 싶다.",
        },
        "right": {
            "code": "P",
            "title": "활용과 효과",
            "body": "그 공식으로 어떤 문제를 더 빠르고 강력하게 풀 수 있는지 궁금하다.",
        },
    },
    {
        "id": "q09",
        "axis": ("S", "T"),
        "question": "풀이가 막혔을 때 나는 보통?",
        "left": {
            "code": "S",
            "title": "다시 혼자 정리한다",
            "body": "내가 놓친 조건을 찾기 위해 처음부터 차분히 되짚는다.",
        },
        "right": {
            "code": "T",
            "title": "다른 생각을 듣는다",
            "body": "누군가의 다른 접근을 들으면 막힌 지점이 빨리 열린다.",
        },
    },
    {
        "id": "q10",
        "axis": ("V", "N"),
        "question": "해설을 볼 때 더 만족스러운 설명은?",
        "left": {
            "code": "V",
            "title": "눈에 보이는 설명",
            "body": "그림, 표, 좌표, 그래프로 풀이의 구조를 보여주는 설명이 좋다.",
        },
        "right": {
            "code": "N",
            "title": "식으로 정리된 설명",
            "body": "정확한 기호와 계산 흐름으로 결론까지 이어지는 설명이 좋다.",
        },
    },
    {
        "id": "q11",
        "axis": ("I", "A"),
        "question": "답이 맞는지 확신하는 순간은?",
        "left": {
            "code": "I",
            "title": "전체 흐름이 맞을 때",
            "body": "풀이의 큰 방향과 결론이 자연스럽게 연결되면 확신이 든다.",
        },
        "right": {
            "code": "A",
            "title": "검산이 끝났을 때",
            "body": "각 단계가 정의와 조건에 맞는지 확인해야 마음이 놓인다.",
        },
    },
    {
        "id": "q12",
        "axis": ("R", "P"),
        "question": "수학 프로젝트를 고른다면?",
        "left": {
            "code": "R",
            "title": "개념을 깊이 탐구하기",
            "body": "한 주제의 원리, 역사, 구조를 끝까지 파헤치는 프로젝트가 좋다.",
        },
        "right": {
            "code": "P",
            "title": "쓸모 있는 결과 만들기",
            "body": "수학을 이용해 도구, 모델, 해결책을 만들어 보는 프로젝트가 좋다.",
        },
    },
]


TYPE_DATA = {
    "SVIR": {
        "number": 1,
        "pronunciation": "스비르",
        "person": "앙리 푸앵카레",
        "quote": "우주의 모양을 주무르는 상상력 대가!",
        "tendency": "혼자서(S) 공간 형태를(V) 직관적으로 상상하며(I) 탐구(R)",
        "achievement": "위상수학의 토대 마련",
    },
    "SVIP": {
        "number": 2,
        "pronunciation": "스빕",
        "person": "아르키메데스",
        "quote": "유레카! 실용 수학의 끝판왕!",
        "tendency": "홀로 사색하다(S) 도형의 원리를(V) 번뜩이는 직관으로 깨달아(I) 발명에 응용(P)",
        "achievement": "부력의 원리 발견, 나선 양수기 발명",
    },
    "SVAR": {
        "number": 3,
        "pronunciation": "스바르",
        "person": "르네 데카르트",
        "quote": "도형의 위치를 지도로 그린 사색가!",
        "tendency": "혼자 누워(S) 기하학을(V) 논리적으로 분석해(A) 좌표평면을 탐구(R)",
        "achievement": "해석기하학 창시",
    },
    "SVAP": {
        "number": 4,
        "pronunciation": "스밥",
        "person": "브누아 망델브로",
        "quote": "끝없는 반복 무늬를 찾아낸 마법사!",
        "tendency": "홀로 개척하며(S) 자연의 복잡한 모양을(V) 컴퓨터로 분석해(A) 그래픽에 응용(P)",
        "achievement": "프랙탈 기하학 개척",
    },
    "SNIR": {
        "number": 5,
        "pronunciation": "스니르",
        "person": "스리니바사 라마누잔",
        "quote": "숫자의 비밀을 꿰뚫어 본 마술사!",
        "tendency": "고향에서 홀로(S) 숫자의 규칙을(N) 직관으로 찾아내어(I) 수많은 공식을 탐구(R)",
        "achievement": "수론 및 무한급수 분야의 막대한 기여",
    },
    "SNIP": {
        "number": 6,
        "pronunciation": "스닙",
        "person": "블레즈 파스칼",
        "quote": "주사위 게임에서 수학의 미래를 발견!",
        "tendency": "사색에 빠져(S) 통계를(N) 직관적으로 떠올려(I) 최초의 계산기와 확률에 응용(P)",
        "achievement": "확률론의 선구자, 기계식 계산기 발명",
    },
    "SNAR": {
        "number": 7,
        "pronunciation": "스나르",
        "person": "쿠르트 괴델",
        "quote": "수학의 한계를 증명해 낸 은둔자!",
        "tendency": "고독한 환경에서(S) 수학 기호를(N) 철저히 논리적으로 분석해(A) 한계를 탐구(R)",
        "achievement": "불완전성 정리 증명",
    },
    "SNAP": {
        "number": 8,
        "pronunciation": "스냅",
        "person": "아이작 뉴턴",
        "quote": "우주의 법칙을 수학으로 풀어낸 거인!",
        "tendency": "고향에 홀로 머물며(S) 미적분을(N) 치밀하게 분석해(A) 우주 물리학에 응용(P)",
        "achievement": "미적분학 및 고전역학 완성",
    },
    "TVIR": {
        "number": 9,
        "pronunciation": "트비르",
        "person": "레온하르트 오일러",
        "quote": "새로운 수학의 지도를 그린 열정가!",
        "tendency": "동료들과 소통하며(T) 점과 선의 연결을(V) 직관적으로 파악해(I) 탐구(R)",
        "achievement": "한붓그리기(그래프 이론) 창시",
    },
    "TVIP": {
        "number": 10,
        "pronunciation": "트빕",
        "person": "피타고라스",
        "quote": "세상이 수로 이루어졌다고 믿은 마스터!",
        "tendency": "학파를 이끌며(T) 삼각형의 비율을(V) 직관적으로 깨달아(I) 음악과 건축에 응용(P)",
        "achievement": "피타고라스의 정리 증명",
    },
    "TVAR": {
        "number": 11,
        "pronunciation": "트바르",
        "person": "다비트 힐베르트",
        "quote": "수학자들의 23가지 숙제를 내준 대장!",
        "tendency": "제자들을 양성하며(T) 기하학의 토대를(V) 논리적으로 분석해(A) 미래 과제 탐구(R)",
        "achievement": "현대 수학의 23가지 미해결 문제 제시",
    },
    "TVAP": {
        "number": 12,
        "pronunciation": "트밥",
        "person": "캐서린 존슨",
        "quote": "달로 가는 길을 계산해 낸 인간 계산기!",
        "tendency": "동료들과 협력하며(T) 우주선의 궤도를(V) 날카로운 논리로 분석해(A) 우주 탐사에 응용(P)",
        "achievement": "아폴로 11호 달 착륙 궤도 계산",
    },
    "TNIR": {
        "number": 13,
        "pronunciation": "트니르",
        "person": "폴 에르되시",
        "quote": "전 세계를 돌아다닌 수학 배낭여행자!",
        "tendency": "전 세계 학자들과 협업하며(T) 숫자의 규칙을(N) 엄청난 직관으로(I) 순수하게 탐구(R)",
        "achievement": "조합론 및 그래프 이론의 대가",
    },
    "TNIP": {
        "number": 14,
        "pronunciation": "트닙",
        "person": "존 폰 노이만",
        "quote": "컴퓨터 구조를 처음 만든 아이디어 뱅크!",
        "tendency": "거대한 팀을 이끌며(T) 엄청난 연산을(N) 직관적으로 처리해(I) 컴퓨터와 경제학에 응용(P)",
        "achievement": "게임 이론 창시 및 현대 컴퓨터 구조 설계",
    },
    "TNAR": {
        "number": 15,
        "pronunciation": "트나르",
        "person": "에미 뇌터",
        "quote": "우주의 대칭성을 밝혀낸 위대한 스승!",
        "tendency": "제자들과 함께(T) 복잡한 수식을(N) 논리적으로 분석해(A) 물리학과 대수학을 탐구(R)",
        "achievement": "뇌터의 정리, 현대 추상대수학 확립",
    },
    "TNAP": {
        "number": 16,
        "pronunciation": "트냅",
        "person": "앨런 튜링",
        "quote": "생각하는 기계를 만든 암호 해독 천재!",
        "tendency": "암호 해독 팀과 협력해(T) 기호를(N) 논리적으로 분석하여(A) 전쟁을 끝내는 데 응용(P)",
        "achievement": "튜링 기계 고안, 현대 컴퓨터 과학의 아버지",
    },
}


PORTRAIT_DATA = {
    "SVIR": {"skin": "#d9a67d", "hair": "#4c3328", "jacket": "#28344d", "shirt": "#f7efe8", "accent": "#7d8cff", "style": "wavy", "glasses": False, "beard": False, "moustache": True},
    "SVIP": {"skin": "#d8a982", "hair": "#f1f1e8", "jacket": "#8b5f3d", "shirt": "#fff2dc", "accent": "#f0a43a", "style": "long", "glasses": False, "beard": True, "moustache": True},
    "SVAR": {"skin": "#d6a27d", "hair": "#2d241f", "jacket": "#23304a", "shirt": "#f6f0e8", "accent": "#5b86d6", "style": "long", "glasses": False, "beard": False, "moustache": True},
    "SVAP": {"skin": "#d0a184", "hair": "#e5e0d4", "jacket": "#3b4056", "shirt": "#edf7ff", "accent": "#6aa7ff", "style": "round", "glasses": True, "beard": True, "moustache": True},
    "SNIR": {"skin": "#8f5b3c", "hair": "#1e1714", "jacket": "#24515f", "shirt": "#f5ead8", "accent": "#6ac5ff", "style": "short", "glasses": False, "beard": False, "moustache": False},
    "SNIP": {"skin": "#d4a37f", "hair": "#3b2f2b", "jacket": "#4b3b67", "shirt": "#f7efe7", "accent": "#ac8cff", "style": "wavy", "glasses": False, "beard": False, "moustache": False},
    "SNAR": {"skin": "#d2a181", "hair": "#231f20", "jacket": "#1f2b3e", "shirt": "#f2f0ec", "accent": "#8395ff", "style": "short", "glasses": True, "beard": False, "moustache": False},
    "SNAP": {"skin": "#d8a982", "hair": "#f4f0df", "jacket": "#41506a", "shirt": "#fff7e8", "accent": "#f7c86a", "style": "long", "glasses": False, "beard": False, "moustache": False},
    "TVIR": {"skin": "#d7a782", "hair": "#efe6d6", "jacket": "#2f4460", "shirt": "#f8f1e6", "accent": "#67a8ff", "style": "round", "glasses": False, "beard": False, "moustache": False},
    "TVIP": {"skin": "#d0a077", "hair": "#e8e1d3", "jacket": "#6b4b36", "shirt": "#fff1d8", "accent": "#eaa846", "style": "long", "glasses": False, "beard": True, "moustache": True},
    "TVAR": {"skin": "#d3a07d", "hair": "#d4d0c6", "jacket": "#27324c", "shirt": "#f2f4fb", "accent": "#8a9cff", "style": "short", "glasses": False, "beard": False, "moustache": True},
    "TVAP": {"skin": "#8f5f46", "hair": "#1c1514", "jacket": "#2f5f7b", "shirt": "#fff5ea", "accent": "#79c8ff", "style": "bob", "glasses": False, "beard": False, "moustache": False},
    "TNIR": {"skin": "#d1a284", "hair": "#f0eee5", "jacket": "#36445a", "shirt": "#f8f5ee", "accent": "#71b6ff", "style": "wispy", "glasses": True, "beard": False, "moustache": False},
    "TNIP": {"skin": "#d7a37f", "hair": "#2b2422", "jacket": "#252d40", "shirt": "#f4f2ed", "accent": "#4ea3ff", "style": "short", "glasses": False, "beard": False, "moustache": False},
    "TNAR": {"skin": "#d5a17d", "hair": "#5b463b", "jacket": "#3d465d", "shirt": "#f7eee5", "accent": "#9b8cff", "style": "bun", "glasses": False, "beard": False, "moustache": False},
    "TNAP": {"skin": "#d5a27e", "hair": "#4c3529", "jacket": "#26334f", "shirt": "#f3f6fb", "accent": "#5aa2ff", "style": "wavy", "glasses": False, "beard": False, "moustache": False},
}


def rerun() -> None:
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


def initialize_state() -> None:
    defaults = {
        "screen": "home",
        "current_question": 0,
        "answers": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url("https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800;900&family=Press+Start+2P&family=Space+Grotesk:wght@400;500;600;700&display=swap");

        :root {
            --ink: #1d1d1f;
            --muted: #6e6e73;
            --blue: #0071e3;
            --blue-dark: #0057b8;
            --paper: #f5f5f7;
            --line: rgba(0, 0, 0, 0.08);
            --inu-blue: #005bac;
            --inu-blue-dark: #003f88;
            --inu-blue-light: #dcecff;
            --inu-blue-soft: #eef6ff;
        }

        .stApp {
            background:
                radial-gradient(circle at 50% 24%, rgba(0, 91, 172, 0.22), rgba(0, 91, 172, 0.08) 30%, rgba(255,255,255,0) 58%),
                radial-gradient(circle at 18% 18%, rgba(0, 130, 210, 0.13), transparent 28%),
                radial-gradient(circle at 82% 18%, rgba(0, 63, 136, 0.12), transparent 28%),
                linear-gradient(180deg, #ffffff 0%, #f6fbff 18%, #eaf5ff 42%, #f7fbff 72%, #f5f5f7 100%);
            background-attachment: fixed;
            color: var(--ink);
            font-family: "Space Grotesk", "Noto Sans KR", -apple-system,
                BlinkMacSystemFont, "Apple SD Gothic Neo", sans-serif;
        }

        .main .block-container {
            max-width: 1120px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        div[data-testid="stToolbar"],
        div[data-testid="stDecoration"] {
            visibility: hidden;
            height: 0;
        }

        h1, h2, h3, p {
            letter-spacing: 0;
        }

        .home-wrap {
            position: relative;
            min-height: 700px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            border-radius: 0;
            margin: -2rem calc(50% - 50vw) 0 calc(50% - 50vw);
            padding: 5.5rem 2rem 6.7rem;
            background:
                radial-gradient(circle at 50% 48%, rgba(0, 91, 172, 0.42), rgba(0, 91, 172, 0.13) 32%, transparent 58%),
                radial-gradient(circle at 18% 18%, rgba(0, 130, 210, 0.18), transparent 28%),
                radial-gradient(circle at 82% 18%, rgba(0, 63, 136, 0.16), transparent 28%),
                linear-gradient(180deg, rgba(255,255,255,0.8) 0%, rgba(246,251,255,0.88) 17%, rgba(230,243,255,0.9) 47%, rgba(238,247,255,0.72) 78%, rgba(245,245,247,0) 100%);
        }

        .home-inner {
            position: relative;
            z-index: 3;
            width: min(100%, 1040px);
            margin: 0 auto;
            text-align: center;
        }

        .home-title {
            width: 100%;
            margin: 0 auto;
            color: #242428;
            text-align: center;
            font-family: "Press Start 2P", "Space Grotesk", "Noto Sans KR", -apple-system,
                BlinkMacSystemFont, sans-serif;
            font-size: clamp(3rem, 9.4vw, 8.4rem);
            line-height: 1.05;
            font-weight: 400;
            letter-spacing: 0;
            text-shadow: 0 22px 44px rgba(0, 63, 136, 0.15);
        }

        .home-subtitle {
            width: 100%;
            max-width: calc(100vw - 2rem);
            margin: 0.8rem auto 0;
            color: #2f3036;
            text-align: center;
            font-family: "Space Grotesk", "Noto Sans KR", -apple-system,
                BlinkMacSystemFont, sans-serif;
            font-size: clamp(1.45rem, 4.1vw, 2.95rem);
            line-height: 1.08;
            font-weight: 850;
            letter-spacing: 0;
            white-space: nowrap;
        }

        .home-copy {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            max-width: 760px;
            margin: 2rem auto 0;
            color: rgba(29, 29, 31, 0.62);
            font-family: "Noto Sans KR", -apple-system, BlinkMacSystemFont,
                "Apple SD Gothic Neo", sans-serif;
            font-size: clamp(1.05rem, 2vw, 1.28rem);
            line-height: 1.65;
            font-weight: 300;
            text-align: center;
        }

        .home-copy span {
            display: block;
            width: 100%;
            text-align: center;
        }

        .hero-object {
            position: absolute;
            z-index: 1;
            display: grid;
            place-items: center;
            pointer-events: none;
            border-radius: 999px;
            color: var(--inu-blue);
            font-family: "Space Grotesk", "Noto Sans KR", -apple-system,
                BlinkMacSystemFont, sans-serif;
            font-weight: 850;
            background:
                radial-gradient(circle, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.78) 43%, rgba(255,255,255,0.28) 66%, rgba(255,255,255,0) 82%);
            box-shadow: 0 24px 70px rgba(0, 63, 136, 0.14);
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
            text-shadow: 0 14px 28px rgba(0, 63, 136, 0.2);
            animation: floaty 6.5s ease-in-out infinite;
        }

        .obj-large {
            left: 50%;
            bottom: 0.9rem;
            width: clamp(92px, 10vw, 136px);
            height: clamp(92px, 10vw, 136px);
            transform: translateX(-50%);
            color: var(--inu-blue-dark);
            font-size: clamp(3.8rem, 6.6vw, 5.7rem);
        }

        .emoji-object {
            font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif;
            color: inherit;
            text-shadow: none;
        }

        .obj-1 { left: 10%; top: 16%; width: 82px; height: 82px; font-size: 2.8rem; animation-delay: -1s; }
        .obj-2 { right: 10%; top: 16%; width: 82px; height: 82px; font-size: 2.65rem; animation-delay: -2s; }
        .obj-3 { left: 6%; top: 46%; width: 88px; height: 88px; font-size: 3rem; animation-delay: -3s; }
        .obj-4 { right: 6%; top: 46%; width: 88px; height: 88px; font-size: 2.8rem; animation-delay: -0.5s; }
        .obj-5 { left: 18%; bottom: 13%; width: 86px; height: 86px; font-size: 2.65rem; animation-delay: -4s; }
        .obj-6 { right: 18%; bottom: 13%; width: 86px; height: 86px; font-size: 2.75rem; animation-delay: -1.8s; }
        .obj-rainbow-a { left: 50%; top: 5%; transform: translateX(-50%); width: 82px; height: 82px; font-size: 2.8rem; color: #0075c9; }
        .obj-emoji-a { left: 27%; top: 11%; width: 76px; height: 76px; font-size: 2.15rem; animation-delay: -2.7s; }
        .obj-emoji-b { right: 27%; top: 11%; width: 76px; height: 76px; font-size: 2.15rem; animation-delay: -3.4s; }
        .obj-emoji-c { left: 34%; bottom: 4%; width: 74px; height: 74px; font-size: 2.05rem; animation-delay: -1.4s; }
        .obj-emoji-d { right: 34%; bottom: 4%; width: 74px; height: 74px; font-size: 2.05rem; animation-delay: -4.2s; }

        @keyframes floaty {
            0%, 100% { margin-top: 0; }
            50% { margin-top: -18px; }
        }

        .start-zone {
            max-width: 360px;
            margin: -4.2rem auto 0;
            position: relative;
            z-index: 4;
        }

        .start-zone::before {
            content: "";
            position: absolute;
            inset: -5rem -45vw -7rem;
            z-index: -1;
            pointer-events: none;
            background: linear-gradient(180deg, rgba(238,247,255,0.12), rgba(245,245,247,0));
        }

        .apple-shell {
            padding: 1.2rem 0 0;
        }

        .topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 3.8rem;
            color: rgba(29, 29, 31, 0.82);
            font-size: 0.95rem;
            font-weight: 650;
        }

        .brand-mark {
            display: flex;
            align-items: center;
            gap: 0.65rem;
        }

        .brand-dot {
            width: 2rem;
            height: 2rem;
            display: grid;
            place-items: center;
            border-radius: 50%;
            color: #fff;
            background: #1d1d1f;
            font-weight: 850;
        }

        .progress-text {
            color: var(--muted);
            font-weight: 600;
        }

        .question-stage {
            text-align: center;
            margin: 0 auto 2.6rem;
            max-width: 860px;
        }

        .progress-track {
            height: 8px;
            max-width: 520px;
            margin: 0 auto 2.4rem;
            border-radius: 999px;
            background: rgba(0, 0, 0, 0.08);
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(90deg, #0071e3, #7f7cff);
        }

        .question-number {
            color: #86868b;
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
        }

        .question-title {
            color: var(--ink);
            font-size: clamp(2.4rem, 6vw, 4.7rem);
            line-height: 1.05;
            font-weight: 820;
            margin: 0 auto;
        }

        .choice-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 1.1rem;
            margin: 0 auto;
            max-width: 980px;
        }

        .choice-card {
            min-height: 240px;
            padding: 2rem;
            border-radius: 28px;
            background: #ffffff;
            border: 1px solid rgba(0, 0, 0, 0.06);
            box-shadow: 0 22px 54px rgba(0, 0, 0, 0.07);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }

        .choice-card.selected {
            border-color: rgba(0, 113, 227, 0.44);
            box-shadow: 0 26px 64px rgba(0, 113, 227, 0.18);
            background:
                linear-gradient(180deg, rgba(255,255,255,1), rgba(248,251,255,1)),
                radial-gradient(circle at top right, rgba(0,113,227,0.12), transparent 38%);
        }

        .choice-code {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 3.1rem;
            height: 3.1rem;
            margin-bottom: 1.2rem;
            border-radius: 50%;
            background: #f5f5f7;
            color: #1d1d1f;
            font-size: 1.2rem;
            font-weight: 820;
        }

        .choice-card.selected .choice-code {
            background: #0071e3;
            color: #fff;
        }

        .choice-title {
            margin-bottom: 0.8rem;
            color: #1d1d1f;
            font-size: clamp(1.45rem, 3vw, 2.1rem);
            line-height: 1.16;
            font-weight: 760;
        }

        .choice-body {
            color: #6e6e73;
            font-size: 1.02rem;
            line-height: 1.62;
            font-weight: 500;
        }

        .endpoint-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 1rem;
            max-width: 980px;
            margin: 0 auto 1.1rem;
        }

        .endpoint-card {
            min-height: 178px;
            padding: 1.55rem;
            border-radius: 26px;
            background: #ffffff;
            border: 1px solid rgba(0, 0, 0, 0.06);
            box-shadow: 0 18px 48px rgba(0, 0, 0, 0.06);
        }

        .endpoint-card.right {
            background:
                linear-gradient(180deg, rgba(255,255,255,1), rgba(248,251,255,1)),
                radial-gradient(circle at top right, rgba(127, 124, 255, 0.12), transparent 42%);
        }

        .endpoint-topline {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.8rem;
            margin-bottom: 0.9rem;
        }

        .endpoint-code {
            display: inline-grid;
            place-items: center;
            width: 2.8rem;
            height: 2.8rem;
            border-radius: 50%;
            background: #f5f5f7;
            color: #1d1d1f;
            font-size: 1.1rem;
            font-weight: 840;
        }

        .endpoint-side {
            color: #86868b;
            font-size: 0.88rem;
            font-weight: 760;
        }

        .endpoint-title {
            color: #1d1d1f;
            font-size: clamp(1.25rem, 2.4vw, 1.75rem);
            line-height: 1.18;
            font-weight: 820;
            margin-bottom: 0.55rem;
        }

        .endpoint-body {
            color: #6e6e73;
            font-size: 0.98rem;
            line-height: 1.58;
            font-weight: 500;
        }

        .likert-guide {
            max-width: 980px;
            margin: 0 auto 0.8rem;
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            color: #6e6e73;
            font-size: 0.92rem;
            font-weight: 700;
        }

        .likert-selected {
            max-width: 980px;
            margin: 0.85rem auto 0;
            padding: 0.9rem 1rem;
            border-radius: 18px;
            background: rgba(0, 113, 227, 0.08);
            color: #0057b8;
            text-align: center;
            font-size: 0.98rem;
            font-weight: 720;
        }

        .nav-row {
            max-width: 980px;
            margin: 1.8rem auto 0;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.8rem;
        }

        .result-wrap {
            text-align: center;
        }

        .result-title {
            margin: 1.5rem auto 0.8rem;
            color: #1d1d1f;
            font-size: clamp(2.4rem, 7vw, 5.4rem);
            line-height: 1;
            font-weight: 840;
        }

        .result-copy {
            max-width: 620px;
            margin: 0 auto 1.5rem;
            color: #6e6e73;
            font-size: 1.08rem;
            line-height: 1.68;
            font-weight: 520;
        }

        .score-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.9rem;
            margin: 1.8rem auto;
            max-width: 980px;
        }

        .score-card {
            padding: 1.2rem;
            border-radius: 22px;
            background: #fff;
            border: 1px solid rgba(0,0,0,0.06);
            box-shadow: 0 16px 44px rgba(0, 0, 0, 0.05);
            text-align: left;
        }

        .score-label {
            display: flex;
            justify-content: space-between;
            color: #1d1d1f;
            font-size: 0.95rem;
            font-weight: 760;
            margin-bottom: 0.8rem;
        }

        .score-track {
            height: 10px;
            border-radius: 999px;
            background: #f0f0f2;
            overflow: hidden;
        }

        .score-fill {
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(90deg, #0071e3, #8b7cff);
        }

        .axis-guide-section {
            max-width: 980px;
            margin: 2.4rem auto 2rem;
            text-align: left;
        }

        .axis-guide-title {
            margin: 0 0 0.35rem;
            color: #1d1d1f;
            font-size: clamp(1.65rem, 3.2vw, 2.45rem);
            line-height: 1.12;
            font-weight: 840;
            text-align: center;
        }

        .axis-guide-copy {
            max-width: 620px;
            margin: 0 auto 1.4rem;
            color: #6e6e73;
            font-size: 1rem;
            line-height: 1.58;
            font-weight: 420;
            text-align: center;
        }

        .axis-guide-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.9rem;
        }

        .axis-guide-card {
            min-height: 190px;
            padding: 1.15rem;
            border-radius: 22px;
            background:
                linear-gradient(180deg, rgba(255,255,255,0.98), rgba(248,251,255,0.96));
            border: 1px solid rgba(0, 0, 0, 0.06);
            box-shadow: 0 16px 44px rgba(0, 0, 0, 0.05);
            position: relative;
            overflow: hidden;
        }

        .axis-guide-card.active {
            border-color: rgba(0, 91, 172, 0.25);
            background:
                radial-gradient(circle at 90% 0%, rgba(0, 113, 227, 0.2), transparent 34%),
                linear-gradient(180deg, #ffffff, #eef7ff);
            box-shadow: 0 20px 52px rgba(0, 91, 172, 0.14);
        }

        .axis-guide-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.7rem;
            margin-bottom: 0.9rem;
        }

        .axis-guide-code {
            display: inline-grid;
            place-items: center;
            width: 2.7rem;
            height: 2.7rem;
            border-radius: 50%;
            background: #f5f5f7;
            color: #1d1d1f;
            font-family: "Space Grotesk", "Noto Sans KR", sans-serif;
            font-size: 1.1rem;
            font-weight: 850;
        }

        .axis-guide-card.active .axis-guide-code {
            background: #005bac;
            color: #ffffff;
            box-shadow: 0 10px 24px rgba(0, 91, 172, 0.24);
        }

        .axis-guide-badge {
            color: #005bac;
            font-size: 0.78rem;
            font-weight: 760;
            opacity: 0;
        }

        .axis-guide-card.active .axis-guide-badge {
            opacity: 1;
        }

        .axis-guide-name {
            color: #1d1d1f;
            font-size: 1.05rem;
            line-height: 1.2;
            font-weight: 820;
            margin-bottom: 0.25rem;
        }

        .axis-guide-label {
            color: #005bac;
            font-size: 0.9rem;
            font-weight: 720;
            margin-bottom: 0.65rem;
        }

        .axis-guide-desc {
            color: #6e6e73;
            font-size: 0.92rem;
            line-height: 1.55;
            font-weight: 430;
        }

        .stButton > button {
            min-height: 3.25rem;
            border-radius: 999px;
            border: 0;
            background: #0071e3;
            color: #ffffff;
            font-weight: 720;
            font-size: 1rem;
            letter-spacing: 0;
            box-shadow: 0 16px 30px rgba(0, 113, 227, 0.23);
            transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
        }

        .stButton > button:hover {
            background: #0077ed;
            color: #ffffff;
            transform: translateY(-1px);
            box-shadow: 0 18px 36px rgba(0, 113, 227, 0.28);
        }

        .stButton > button:focus {
            color: #ffffff;
            box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.18), 0 18px 36px rgba(0, 113, 227, 0.28);
        }

        div:has(.likert-guide) + div div[data-testid="stButton"] > button {
            min-height: 4.1rem !important;
            border-radius: 22px !important;
            border: 1px solid rgba(0, 91, 172, 0.16) !important;
            background:
                linear-gradient(180deg, rgba(255,255,255,0.98), rgba(247,251,255,0.96)) !important;
            color: #1d1d1f !important;
            font-family: "Noto Sans KR", "Space Grotesk", -apple-system,
                BlinkMacSystemFont, sans-serif !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
            box-shadow: 0 12px 28px rgba(0, 63, 136, 0.08) !important;
            transition: transform 0.18s ease, box-shadow 0.18s ease,
                border-color 0.18s ease, background 0.18s ease !important;
        }

        div:has(.likert-guide) + div div[data-testid="stButton"] > button:hover {
            border-color: rgba(0, 91, 172, 0.34) !important;
            background:
                linear-gradient(180deg, #ffffff, #eef7ff) !important;
            color: #005bac !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 18px 40px rgba(0, 91, 172, 0.16) !important;
        }

        div:has(.likert-guide) + div div[data-testid="stButton"] > button[kind="primary"],
        div:has(.likert-guide) + div div[data-testid="stButton"] > button[data-testid="stBaseButton-primary"] {
            border-color: rgba(0, 91, 172, 0.26) !important;
            background:
                radial-gradient(circle at 22% 18%, rgba(255,255,255,0.42), transparent 30%),
                linear-gradient(135deg, #005bac, #0077ed 58%, #4b8dff) !important;
            color: #ffffff !important;
            box-shadow: 0 18px 42px rgba(0, 91, 172, 0.28) !important;
        }

        div:has(.likert-guide) + div div[data-testid="stButton"] > button[kind="primary"]:hover,
        div:has(.likert-guide) + div div[data-testid="stButton"] > button[data-testid="stBaseButton-primary"]:hover {
            color: #ffffff !important;
            transform: translateY(-3px) !important;
            box-shadow: 0 22px 48px rgba(0, 91, 172, 0.34) !important;
        }

        div[data-testid="stAlert"] {
            max-width: 720px;
            margin-left: auto;
            margin-right: auto;
            border-radius: 20px;
        }

        @media (max-width: 760px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .home-wrap {
                min-height: 660px;
                padding: 4.8rem 1rem 6.2rem;
            }

            .home-title {
                margin-top: 0;
                font-size: clamp(2.35rem, 12vw, 4.1rem);
                line-height: 1.12;
            }

            .home-subtitle {
                margin-top: 0.75rem;
                font-size: clamp(0.82rem, 3.45vw, 1.45rem);
                line-height: 1.04;
            }

            .home-copy {
                max-width: 330px;
                margin-top: 1.25rem;
                font-size: 1rem;
                line-height: 1.58;
            }

            .obj-1 { left: 5%; top: 13%; width: 52px; height: 52px; font-size: 1.75rem; }
            .obj-2 { left: auto; right: 5%; top: 13%; width: 52px; height: 52px; font-size: 1.7rem; }
            .obj-3 { left: 4%; top: 64%; width: 54px; height: 54px; font-size: 1.85rem; }
            .obj-4 { right: 4%; left: auto; top: 64%; width: 54px; height: 54px; font-size: 1.75rem; }
            .obj-5 { left: 10%; bottom: 8%; width: 58px; height: 58px; font-size: 1.85rem; }
            .obj-6 { right: 10%; bottom: 8%; width: 58px; height: 58px; font-size: 1.85rem; }
            .obj-large { bottom: 0.6rem; width: 72px; height: 72px; font-size: 2.8rem; }
            .obj-rainbow-a { left: 50%; top: 3%; width: 64px; height: 64px; font-size: 2.25rem; }
            .obj-emoji-a { left: 24%; top: 8%; width: 52px; height: 52px; font-size: 1.5rem; }
            .obj-emoji-b { right: 24%; top: 8%; width: 52px; height: 52px; font-size: 1.5rem; }
            .obj-emoji-c { left: 30%; bottom: 2%; width: 50px; height: 50px; font-size: 1.42rem; }
            .obj-emoji-d { right: 30%; bottom: 2%; width: 50px; height: 50px; font-size: 1.42rem; }

            .topbar {
                margin-bottom: 2.6rem;
            }

            .choice-grid,
            .endpoint-grid,
            .score-grid,
            .axis-guide-grid,
            .nav-row {
                grid-template-columns: 1fr;
            }

            .choice-card {
                min-height: 0;
                padding: 1.4rem;
                border-radius: 22px;
            }

            .endpoint-card {
                min-height: 0;
                padding: 1.3rem;
                border-radius: 22px;
            }

            .likert-guide {
                font-size: 0.82rem;
            }

            .axis-guide-section {
                margin-top: 2rem;
            }

            .axis-guide-card {
                min-height: 0;
            }

            .question-title {
                font-size: 2.35rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_home() -> None:
    st.markdown(
        f"""
        <section class="home-wrap">
            <div class="hero-object obj-rainbow-a">✦</div>
            <div class="hero-object obj-1">∫</div>
            <div class="hero-object obj-2">△</div>
            <div class="hero-object obj-3">≈</div>
            <div class="hero-object obj-large">∞</div>
            <div class="hero-object obj-4">◇</div>
            <div class="hero-object obj-5">⌁</div>
            <div class="hero-object obj-6">⟡</div>
            <div class="hero-object emoji-object obj-emoji-a">🧠</div>
            <div class="hero-object emoji-object obj-emoji-b">🚀</div>
            <div class="hero-object emoji-object obj-emoji-c">🔥</div>
            <div class="hero-object emoji-object obj-emoji-d">🌈</div>
            <div class="home-inner">
                <div class="home-title">{APP_TITLE}</div>
                <div class="home-subtitle">Mathematical Behavior Type Indicator</div>
                <div class="home-copy">
                    <span>수학을 대하는 나의 행동 유형이 무엇인지 알아보아요!</span>
                    <span>나는 어떤 수학자와 비슷할까요?</span>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="start-zone">', unsafe_allow_html=True)
    if st.button("테스트 시작하기", use_container_width=True):
        st.session_state.screen = "quiz"
        st.session_state.current_question = 0
        st.session_state.answers = {}
        rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def render_topbar() -> None:
    answered = answered_count()
    st.markdown(
        f"""
        <div class="topbar">
            <div class="brand-mark">
                <div class="brand-dot">M</div>
                <div>{APP_TITLE} <span style="color:#86868b;">{APP_SUBTITLE}</span></div>
            </div>
            <div class="progress-text">{answered}/{TOTAL_QUESTIONS}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def answered_count() -> int:
    return sum(1 for question in QUESTIONS if question["id"] in st.session_state.answers)


def render_endpoint_card(question: dict, side: str, side_label: str) -> None:
    option = question[side]
    class_name = "endpoint-card right" if side == "right" else "endpoint-card"
    st.markdown(
        f"""
        <div class="{class_name}">
            <div class="endpoint-topline">
                <div class="endpoint-code">{escape(option["code"])}</div>
                <div class="endpoint-side">{escape(side_label)}</div>
            </div>
            <div class="endpoint-title">{escape(option["title"])}</div>
            <div class="endpoint-body">{escape(option["body"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def selected_likert_label(value: int) -> str:
    for option_value, title, caption in LIKERT_OPTIONS:
        if option_value == value:
            return f"{title} - {caption}"
    return ""


def render_likert_scale(question: dict) -> None:
    selected_value = st.session_state.answers.get(question["id"])
    st.markdown(
        """
        <div class="likert-guide">
            <span>왼쪽 성향에 가까움</span>
            <span>오른쪽 성향에 가까움</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    columns = st.columns(len(LIKERT_OPTIONS), gap="small")
    for column, (value, title, caption) in zip(columns, LIKERT_OPTIONS):
        is_selected = selected_value == value
        marker = "✓ " if is_selected else ""
        with column:
            if st.button(
                f"{marker}{title}",
                key=f"{question['id']}_likert_{value}",
                use_container_width=True,
                help=caption,
                type="primary" if is_selected else "secondary",
            ):
                st.session_state.answers[question["id"]] = value
                if st.session_state.current_question < TOTAL_QUESTIONS - 1:
                    st.session_state.current_question += 1
                rerun()

    if isinstance(selected_value, int):
        st.markdown(
            f"""
            <div class="likert-selected">
                현재 선택: {escape(selected_likert_label(selected_value))}
            </div>
            """,
            unsafe_allow_html=True,
        )


def advance_to_next_question() -> None:
    if st.session_state.current_question < TOTAL_QUESTIONS - 1:
        st.session_state.current_question += 1
    else:
        st.session_state.screen = "result"
    rerun()


def render_quiz() -> None:
    st.markdown('<main class="apple-shell">', unsafe_allow_html=True)
    render_topbar()

    index = st.session_state.current_question
    question = QUESTIONS[index]
    progress = (index + 1) / TOTAL_QUESTIONS * 100
    st.markdown(
        f"""
        <section class="question-stage">
            <div class="progress-track">
                <div class="progress-fill" style="width: {progress:.1f}%;"></div>
            </div>
            <div class="question-number">Question {index + 1:02d}</div>
            <h1 class="question-title">{escape(question["question"])}</h1>
        </section>
        """,
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns(2, gap="large")
    with left_col:
        render_endpoint_card(question, "left", "왼쪽 성향")
    with right_col:
        render_endpoint_card(question, "right", "오른쪽 성향")

    render_likert_scale(question)

    st.markdown('<div class="nav-row">', unsafe_allow_html=True)
    previous_col, next_col = st.columns(2)
    with previous_col:
        if st.button("이전", use_container_width=True, disabled=index == 0):
            st.session_state.current_question -= 1
            rerun()
    with next_col:
        has_answer = question["id"] in st.session_state.answers
        is_last = index == TOTAL_QUESTIONS - 1
        label = "결과보기" if is_last else "다음"
        if st.button(label, use_container_width=True, disabled=not has_answer):
            if is_last:
                missing = [item for item in QUESTIONS if item["id"] not in st.session_state.answers]
                if missing:
                    st.warning("아직 답하지 않은 문항이 있습니다.")
                else:
                    st.session_state.screen = "result"
            else:
                st.session_state.current_question += 1
            rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</main>", unsafe_allow_html=True)


def calculate_scores() -> dict:
    scores = {letter: 0 for letter in AXIS_META}
    for question in QUESTIONS:
        answer = st.session_state.answers.get(question["id"])
        left_code = question["left"]["code"]
        right_code = question["right"]["code"]

        if isinstance(answer, int):
            if answer < 0:
                scores[left_code] += abs(answer)
            elif answer > 0:
                scores[right_code] += answer
        elif answer in scores:
            scores[answer] += 1
    return scores


def calculate_type_code(scores: dict) -> str:
    pairs = [("S", "T"), ("V", "N"), ("I", "A"), ("R", "P")]
    code = ""
    for left, right in pairs:
        code += left if scores[left] >= scores[right] else right
    return code


def render_portrait_svg(type_code: str, result: dict) -> str:
    portrait = PORTRAIT_DATA[type_code]
    skin = portrait["skin"]
    hair = portrait["hair"]
    jacket = portrait["jacket"]
    shirt = portrait["shirt"]
    accent = portrait["accent"]
    style = portrait["style"]

    if style == "long":
        hair_shape = f"""
            <path d="M86 145 C76 92 101 48 158 48 C215 48 243 92 232 148 C218 130 204 101 158 101 C113 101 99 130 86 145Z" fill="{hair}"/>
            <path d="M82 127 C58 164 66 228 105 253 C95 211 96 166 116 122Z" fill="{hair}" opacity="0.9"/>
            <path d="M234 127 C258 164 250 228 211 253 C221 211 220 166 200 122Z" fill="{hair}" opacity="0.9"/>
        """
    elif style == "bob":
        hair_shape = f"""
            <path d="M87 140 C74 84 106 48 159 48 C213 48 244 84 231 140 C224 201 205 230 159 230 C113 230 94 201 87 140Z" fill="{hair}"/>
            <path d="M104 118 C121 96 195 96 214 118 C204 89 182 70 159 70 C136 70 114 89 104 118Z" fill="#ffffff" opacity="0.13"/>
        """
    elif style == "bun":
        hair_shape = f"""
            <circle cx="216" cy="78" r="28" fill="{hair}"/>
            <path d="M88 143 C80 89 110 53 158 53 C207 53 235 89 228 143 C205 118 192 101 158 101 C124 101 111 118 88 143Z" fill="{hair}"/>
            <path d="M92 132 C79 177 87 218 115 240 C106 199 109 161 125 125Z" fill="{hair}" opacity="0.85"/>
        """
    elif style == "round":
        hair_shape = f"""
            <path d="M78 142 C67 95 98 55 142 48 C176 30 224 60 236 105 C252 161 222 205 158 207 C97 204 65 179 78 142Z" fill="{hair}"/>
            <path d="M100 112 C124 84 193 82 218 116 C201 91 184 73 157 73 C130 73 111 91 100 112Z" fill="#ffffff" opacity="0.16"/>
        """
    elif style == "wispy":
        hair_shape = f"""
            <path d="M90 136 C76 88 110 52 158 52 C210 52 237 90 225 143 C205 121 194 105 158 105 C121 105 109 121 90 136Z" fill="{hair}"/>
            <path d="M105 83 C93 78 81 80 70 88 C84 62 106 51 133 54Z" fill="{hair}" opacity="0.8"/>
            <path d="M197 62 C223 55 241 67 251 92 C235 81 222 78 209 84Z" fill="{hair}" opacity="0.78"/>
        """
    else:
        hair_shape = f"""
            <path d="M90 136 C79 89 109 55 158 55 C207 55 237 89 226 136 C210 114 194 99 158 99 C122 99 106 114 90 136Z" fill="{hair}"/>
            <path d="M100 103 C117 72 190 70 214 105 C183 89 138 88 100 103Z" fill="#ffffff" opacity="0.13"/>
        """

    glasses = ""
    if portrait["glasses"]:
        glasses = """
            <g fill="none" stroke="#27324a" stroke-width="5" stroke-linecap="round">
                <circle cx="133" cy="146" r="18"/>
                <circle cx="183" cy="146" r="18"/>
                <path d="M151 146 L165 146"/>
            </g>
        """

    beard = ""
    if portrait["beard"]:
        beard = f"""
            <path d="M110 171 C113 223 133 251 158 251 C184 251 204 223 207 171 C193 196 124 196 110 171Z" fill="{hair}" opacity="0.78"/>
            <path d="M128 209 C144 221 172 221 188 209" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.24" stroke-linecap="round"/>
        """

    moustache = ""
    if portrait["moustache"]:
        moustache = f"""
            <path d="M137 177 C147 168 158 174 158 181 C158 174 170 168 181 177 C172 188 144 188 137 177Z" fill="{hair}" opacity="0.86"/>
        """

    return f"""
        <svg class="portrait-svg" viewBox="0 0 320 360" role="img" aria-label="{escape(result["person"])} 부드러운 초상화">
            <title>{escape(result["person"])} stylized portrait</title>
            <defs>
                <filter id="softPortraitShadow" x="-25%" y="-25%" width="150%" height="150%">
                    <feDropShadow dx="0" dy="18" stdDeviation="16" flood-color="#17396b" flood-opacity="0.22"/>
                </filter>
                <linearGradient id="portraitShirt" x1="0" x2="1" y1="0" y2="1">
                    <stop offset="0%" stop-color="{shirt}"/>
                    <stop offset="100%" stop-color="#ffffff"/>
                </linearGradient>
            </defs>
            <g filter="url(#softPortraitShadow)">
                <path d="M69 339 C77 282 110 249 159 249 C208 249 241 282 250 339Z" fill="{jacket}"/>
                <path d="M126 260 L159 334 L192 260 C181 252 137 252 126 260Z" fill="url(#portraitShirt)"/>
                <path d="M142 236 L142 266 C149 274 169 274 176 266 L176 236Z" fill="{skin}"/>
                <ellipse cx="96" cy="150" rx="20" ry="25" fill="{skin}"/>
                <ellipse cx="220" cy="150" rx="20" ry="25" fill="{skin}"/>
                {hair_shape}
                <ellipse cx="158" cy="151" rx="62" ry="79" fill="{skin}"/>
                <path d="M105 122 C121 101 195 101 212 123 C198 111 179 106 158 106 C137 106 118 111 105 122Z" fill="{hair}" opacity="0.95"/>
                <circle cx="134" cy="148" r="5.4" fill="#272329"/>
                <circle cx="183" cy="148" r="5.4" fill="#272329"/>
                <path d="M159 151 C153 164 153 172 162 174" fill="none" stroke="#8b6048" stroke-width="4" stroke-linecap="round"/>
                {glasses}
                {beard}
                {moustache}
                <path d="M137 198 C150 209 170 209 183 198" fill="none" stroke="#7a473c" stroke-width="5" stroke-linecap="round"/>
                <path d="M95 303 C115 285 133 276 159 276 C185 276 205 285 225 303" fill="none" stroke="{accent}" stroke-width="10" stroke-linecap="round" opacity="0.9"/>
            </g>
        </svg>
    """


def render_flip_card(type_code: str, result: dict) -> None:
    front_title = f"{type_code} ({result['pronunciation']})"
    portrait_svg = render_portrait_svg(type_code, result)
    card_html = f"""
    <!doctype html>
    <html lang="ko">
    <head>
    <meta charset="utf-8">
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap");

        * {{
            box-sizing: border-box;
        }}
        body {{
            margin: 0;
            min-height: 600px;
            display: grid;
            place-items: center;
            background: transparent;
            font-family: "Space Grotesk", "Noto Sans KR", -apple-system,
                BlinkMacSystemFont, "Apple SD Gothic Neo", sans-serif;
        }}
        .scene {{
            width: min(420px, 92vw);
            height: 560px;
            perspective: 1300px;
        }}
        .card {{
            position: relative;
            width: 100%;
            height: 100%;
            padding: 0;
            border: 0;
            background: transparent;
            cursor: pointer;
            text-align: left;
            font: inherit;
            transform-style: preserve-3d;
            transition: transform 0.78s cubic-bezier(.2,.75,.2,1);
        }}
        .card.is-flipped {{
            transform: rotateY(180deg);
        }}
        .card:focus-visible {{
            outline: 4px solid rgba(0, 113, 227, 0.38);
            outline-offset: 8px;
            border-radius: 34px;
        }}
        .side {{
            position: absolute;
            inset: 0;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden;
            backface-visibility: hidden;
            border-radius: 34px;
            border: 1px solid rgba(255, 255, 255, 0.66);
            box-shadow: 0 34px 90px rgba(42, 52, 118, 0.26);
        }}
        .front {{
            padding: 2rem;
            color: #1d1d1f;
            background:
                radial-gradient(circle at 50% 30%, rgba(255,255,255,0.9), rgba(255,255,255,0.08) 32%, transparent 46%),
                linear-gradient(145deg, #ffffff 0%, #eff1ff 38%, #aeb4ff 100%);
        }}
        .front::before {{
            content: "";
            position: absolute;
            width: 280px;
            height: 310px;
            left: 50%;
            top: 51%;
            transform: translate(-50%, -50%) rotate(5deg);
            border-radius: 45% 45% 38% 38%;
            background:
                radial-gradient(circle at 50% 18%, rgba(255,255,255,0.9), transparent 34%),
                linear-gradient(145deg, #ffffff, #bfd7ff 50%, #6e88ff);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.74), 0 30px 56px rgba(77, 65, 173, 0.2);
        }}
        .portrait-wrap {{
            position: absolute;
            left: 50%;
            top: 52%;
            z-index: 1;
            width: 290px;
            height: 326px;
            transform: translate(-50%, -50%);
            display: grid;
            place-items: center;
            pointer-events: none;
        }}
        .portrait-svg {{
            width: 100%;
            height: 100%;
            display: block;
        }}
        .back {{
            padding: 2rem;
            transform: rotateY(180deg);
            color: #f5f5f7;
            background:
                radial-gradient(circle at 22% 15%, rgba(128, 178, 255, 0.46), transparent 32%),
                radial-gradient(circle at 80% 88%, rgba(179, 136, 255, 0.38), transparent 34%),
                linear-gradient(145deg, #101218, #202037 52%, #493b8f);
        }}
        .kicker {{
            position: relative;
            z-index: 2;
            color: rgba(29, 29, 31, 0.58);
            font-size: 0.92rem;
            font-weight: 760;
        }}
        .type {{
            position: relative;
            z-index: 2;
            margin-top: 0.35rem;
            color: #1d1d1f;
            font-size: 2.35rem;
            line-height: 1;
            font-weight: 860;
        }}
        .person {{
            position: relative;
            z-index: 2;
            color: rgba(29, 29, 31, 0.7);
            font-size: 1.18rem;
            font-weight: 720;
            margin-top: 0.6rem;
        }}
        .quote {{
            position: relative;
            z-index: 3;
            margin-top: auto;
            padding-top: 16.5rem;
            color: #1d1d1f;
            font-size: 1.56rem;
            line-height: 1.22;
            font-weight: 820;
            text-shadow: 0 1px 0 rgba(255,255,255,0.48);
        }}
        .back-title {{
            font-size: 2.1rem;
            line-height: 1.08;
            font-weight: 840;
        }}
        .back-code {{
            color: rgba(255,255,255,0.64);
            font-size: 1rem;
            font-weight: 720;
            margin-bottom: 0.7rem;
        }}
        .info-block {{
            padding: 1.15rem;
            border-radius: 22px;
            background: rgba(255,255,255,0.11);
            border: 1px solid rgba(255,255,255,0.16);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            margin-top: 1rem;
        }}
        .info-label {{
            color: rgba(255,255,255,0.62);
            font-size: 0.88rem;
            font-weight: 760;
            margin-bottom: 0.45rem;
        }}
        .info-text {{
            color: rgba(255,255,255,0.94);
            font-size: 1.05rem;
            line-height: 1.58;
            font-weight: 560;
        }}
        .number {{
            align-self: flex-start;
            padding: 0.52rem 0.85rem;
            border-radius: 999px;
            color: rgba(255,255,255,0.9);
            background: rgba(255,255,255,0.13);
            font-size: 0.92rem;
            font-weight: 780;
        }}
        @media (prefers-reduced-motion: reduce) {{
            .card {{
                transition: none;
            }}
        }}
    </style>
    </head>
    <body>
        <div class="scene">
            <button class="card" type="button" aria-label="결과 카드 뒤집기" onclick="this.classList.toggle('is-flipped')">
                <section class="side front">
                    <div>
                        <div class="kicker">Mathematics Behavior Type Indicator</div>
                        <div class="type">{escape(front_title)}</div>
                        <div class="person">{escape(result["person"])}</div>
                    </div>
                    <div class="portrait-wrap">{portrait_svg}</div>
                    <div class="quote">“{escape(result["quote"])}”</div>
                </section>
                <section class="side back">
                    <div>
                        <div class="back-code">{escape(front_title)}</div>
                        <div class="back-title">{escape(result["person"])}</div>
                        <div class="info-block">
                            <div class="info-label">성향</div>
                            <div class="info-text">{escape(result["tendency"])}</div>
                        </div>
                        <div class="info-block">
                            <div class="info-label">업적</div>
                            <div class="info-text">{escape(result["achievement"])}</div>
                        </div>
                    </div>
                    <div class="number">Card {result["number"]:02d}</div>
                </section>
            </button>
        </div>
    </body>
    </html>
    """
    components.html(card_html, height=620, scrolling=False)


def render_score_cards(scores: dict) -> None:
    pairs = [("S", "T"), ("V", "N"), ("I", "A"), ("R", "P")]
    st.markdown('<div class="score-grid">', unsafe_allow_html=True)
    for left, right in pairs:
        left_score = scores[left]
        right_score = scores[right]
        winner = left if left_score >= right_score else right
        width = max(left_score, right_score) / 6 * 100
        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-label">
                    <span>{left}/{right}</span>
                    <span>{winner} {AXIS_META[winner]["label"]}</span>
                </div>
                <div class="score-track">
                    <div class="score-fill" style="width:{width:.0f}%;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def render_axis_guide(type_code: str) -> None:
    selected_letters = set(type_code)
    cards = []
    for letter in ["S", "T", "V", "N", "I", "A", "R", "P"]:
        meta = AXIS_META[letter]
        active_class = " active" if letter in selected_letters else ""
        badge = "내 결과" if letter in selected_letters else "&nbsp;"
        cards.append(
            f"""
            <div class="axis-guide-card{active_class}">
                <div class="axis-guide-top">
                    <div class="axis-guide-code">{escape(letter)}</div>
                    <div class="axis-guide-badge">{badge}</div>
                </div>
                <div class="axis-guide-name">{escape(meta["name"])}</div>
                <div class="axis-guide-label">{escape(meta["label"])}</div>
                <div class="axis-guide-desc">{escape(meta["description"])}</div>
            </div>
            """
        )

    st.markdown(
        f"""
        <section class="axis-guide-section">
            <h2 class="axis-guide-title">8가지 수학 행동 성향</h2>
            <p class="axis-guide-copy">
                결과 코드는 네 개의 축에서 더 가까운 성향을 하나씩 조합해 만들어집니다.
            </p>
            <div class="axis-guide-grid">
                {''.join(cards)}
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_result() -> None:
    if answered_count() < TOTAL_QUESTIONS:
        st.session_state.screen = "quiz"
        rerun()

    scores = calculate_scores()
    type_code = calculate_type_code(scores)
    result = TYPE_DATA[type_code]

    st.markdown('<main class="apple-shell result-wrap">', unsafe_allow_html=True)
    render_topbar()
    st.markdown(
        f"""
        <h1 class="result-title">당신의 수학 MBTI는 {escape(type_code)}</h1>
        <p class="result-copy">
            {escape(result["person"])}처럼 수학을 바라보는 경향이 있습니다.
            아래 카드는 앞면과 뒷면으로 결과를 보여줍니다.
        </p>
        """,
        unsafe_allow_html=True,
    )
    render_flip_card(type_code, result)
    render_score_cards(scores)
    render_axis_guide(type_code)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("다시 검사하기", use_container_width=True):
            st.session_state.screen = "quiz"
            st.session_state.current_question = 0
            st.session_state.answers = {}
            rerun()
    with col2:
        if st.button("홈으로", use_container_width=True):
            st.session_state.screen = "home"
            st.session_state.current_question = 0
            st.session_state.answers = {}
            rerun()

    st.markdown("</main>", unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(
        page_title="MBTI 수학 성향 검사",
        page_icon="∑",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    initialize_state()
    inject_css()

    if st.session_state.screen == "home":
        render_home()
    elif st.session_state.screen == "quiz":
        render_quiz()
    else:
        render_result()


if __name__ == "__main__":
    main()
