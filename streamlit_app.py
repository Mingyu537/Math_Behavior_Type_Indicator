import base64
from html import escape
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


APP_TITLE = "MBTI"
APP_SUBTITLE = "Mathematics Behavior Type Indicator"
TOTAL_QUESTIONS = 12
TYPE_AXIS_PAIRS = [("S", "T"), ("V", "N"), ("I", "A"), ("R", "P")]
FIGURE_DIR = Path(__file__).resolve().parent / "assets" / "figures"
LOGO_DIR = Path(__file__).resolve().parent / "assets" / "logos"


TYPE_IMAGE_FILES = {
    "SVIR": "poincare.png",
    "SVIP": "archimedes.png",
    "SVAR": "descartes.png",
    "SVAP": "mandelbrot.png",
    "SNIR": "ramanujan.png",
    "SNIP": "pascal.png",
    "SNAR": "godel.png",
    "SNAP": "newton.png",
    "TVIR": "euler.png",
    "TVIP": "pythagoras.png",
    "TVAR": "hilbert.png",
    "TVAP": "katherine_johnson.png",
    "TNIR": "erdos.png",
    "TNIP": "von_neumann.png",
    "TNAR": "noether.png",
    "TNAP": "turing.png",
}


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
        "description": "혼자 깊게 몰입해 도형과 공간의 큰 그림을 떠올리는 유형입니다. 정답을 바로 계산하기보다 구조를 상상하고, 원리의 연결을 발견할 때 강해집니다.",
        "tendency": "혼자서[S] 공간 형태를[V] 직관적으로 상상하며[I] 탐구[R]",
        "achievement": "위상수학의 기초를 세우고 푸앵카레 추측을 제기했으며, 삼체 문제 연구로 현대 동역학계 이론의 문을 열었습니다.",
    },
    "SVIP": {
        "number": 2,
        "pronunciation": "스빕",
        "person": "아르키메데스",
        "quote": "유레카! 실용 수학의 끝판왕!",
        "description": "혼자 관찰하고 상상한 아이디어를 실제 문제 해결로 이어 가는 유형입니다. 도형적 감각이 뛰어나고, 떠오른 원리를 도구나 발명으로 바꾸는 힘이 있습니다.",
        "tendency": "홀로 사색하다[S] 도형의 원리를[V] 번뜩이는 직관으로 깨달아[I] 발명에 응용[P]",
        "achievement": "부력의 원리, 지레의 법칙, 원주율 근사, 구와 원기둥의 부피 관계를 밝혔고 나선 양수기를 고안했습니다.",
    },
    "SVAR": {
        "number": 3,
        "pronunciation": "스바르",
        "person": "르네 데카르트",
        "quote": "도형의 위치를 지도로 그린 사색가!",
        "description": "혼자 차분히 생각하며 눈에 보이는 형태를 논리적으로 정리하는 유형입니다. 그림과 좌표, 조건을 연결해 복잡한 문제를 분석하는 데 강합니다.",
        "tendency": "혼자 누워[S] 기하학을[V] 논리적으로 분석해[A] 좌표평면을 탐구[R]",
        "achievement": "좌표평면을 도입해 기하와 대수를 연결한 해석기하학을 만들고, 데카르트 좌표계의 토대를 세웠습니다.",
    },
    "SVAP": {
        "number": 4,
        "pronunciation": "스밥",
        "person": "브누아 망델브로",
        "quote": "끝없는 반복 무늬를 찾아낸 마법사!",
        "description": "시각적 패턴을 꼼꼼히 분석해 현실의 복잡한 모양을 설명하는 유형입니다. 혼자 탐색하면서도 결과물을 그래픽, 모델, 자료로 구현하는 데 능합니다.",
        "tendency": "홀로 개척하며[S] 자연의 복잡한 모양을[V] 컴퓨터로 분석해[A] 그래픽에 응용[P]",
        "achievement": "망델브로 집합을 대중화하고 프랙탈 기하학을 개척해 구름, 해안선, 산맥 같은 자연 형태를 수학으로 설명했습니다.",
    },
    "SNIR": {
        "number": 5,
        "pronunciation": "스니르",
        "person": "스리니바사 라마누잔",
        "quote": "숫자의 비밀을 꿰뚫어 본 마술사!",
        "description": "숫자와 식에서 남들이 놓치는 규칙을 직관적으로 잡아내는 유형입니다. 조용히 몰입할수록 아이디어가 깊어지고, 공식의 숨은 질서를 찾는 데 강합니다.",
        "tendency": "고향에서 홀로[S] 숫자의 규칙을[N] 직관으로 찾아내어[I] 수많은 공식을 탐구[R]",
        "achievement": "분할수, 타우 함수, 모듈러 형식, 무한급수와 연분수 등 수론 전반에 수많은 독창적인 공식을 남겼습니다.",
    },
    "SNIP": {
        "number": 6,
        "pronunciation": "스닙",
        "person": "블레즈 파스칼",
        "quote": "주사위 게임에서 수학의 미래를 발견!",
        "description": "숫자 감각과 빠른 아이디어를 실제 계산과 확률적 판단에 연결하는 유형입니다. 혼자 생각을 정리하다가도 쓸모 있는 방식으로 수학을 바꾸는 힘이 있습니다.",
        "tendency": "사색에 빠져[S] 통계를[N] 직관적으로 떠올려[I] 최초의 계산기와 확률에 응용[P]",
        "achievement": "파스칼의 삼각형을 체계화하고 페르마와 함께 확률론을 열었으며, 기계식 계산기 파스칼린을 제작했습니다.",
    },
    "SNAR": {
        "number": 7,
        "pronunciation": "스나르",
        "person": "쿠르트 괴델",
        "quote": "수학의 한계를 증명해 낸 은둔자!",
        "description": "기호와 명제를 끝까지 따져 보며 논리의 빈틈을 찾는 유형입니다. 혼자 깊게 생각할 때 강하고, 수학 체계 자체를 탐구하는 질문에 끌립니다.",
        "tendency": "고독한 환경에서[S] 수학 기호를[N] 철저히 논리적으로 분석해[A] 한계를 탐구[R]",
        "achievement": "불완전성 정리로 형식 수학 체계의 한계를 증명하고, 논리학과 집합론, 계산 가능성 이론에 큰 영향을 남겼습니다.",
    },
    "SNAP": {
        "number": 8,
        "pronunciation": "스냅",
        "person": "아이작 뉴턴",
        "quote": "우주의 법칙을 수학으로 풀어낸 거인!",
        "description": "숫자와 식을 치밀하게 분석해 현실의 법칙을 설명하는 유형입니다. 혼자 집중해 계산과 원리를 다듬고, 이론을 실제 현상에 적용하는 데 강합니다.",
        "tendency": "고향에 홀로 머물며[S] 미적분을[N] 치밀하게 분석해[A] 우주 물리학에 응용[P]",
        "achievement": "미적분학을 발전시키고 운동 법칙과 만유인력 법칙을 세웠으며, 프린키피아로 고전역학의 체계를 완성했습니다.",
    },
    "TVIR": {
        "number": 9,
        "pronunciation": "트비르",
        "person": "레온하르트 오일러",
        "quote": "새로운 수학의 지도를 그린 열정가!",
        "description": "사람들과 생각을 나누며 시각적 관계와 연결 구조를 빠르게 파악하는 유형입니다. 큰 그림을 직관적으로 잡고 새로운 탐구 주제로 확장하는 데 능합니다.",
        "tendency": "동료들과 소통하며[T] 점과 선의 연결을[V] 직관적으로 파악해[I] 탐구[R]",
        "achievement": "쾨니히스베르크의 다리 문제로 그래프 이론을 열고, 오일러 공식, 수론, 해석학에 폭넓게 기여했습니다.",
    },
    "TVIP": {
        "number": 10,
        "pronunciation": "트빕",
        "person": "피타고라스",
        "quote": "세상이 수로 이루어졌다고 믿은 마스터!",
        "description": "함께 배우고 토론하면서 도형적 직관을 생활 속 질서로 연결하는 유형입니다. 비율, 조화, 형태를 빠르게 감지하고 실제 활용 가능성을 찾습니다.",
        "tendency": "학파를 이끌며[T] 삼각형의 비율을[V] 직관적으로 깨달아[I] 음악과 건축에 응용[P]",
        "achievement": "피타고라스 정리를 대표로 수와 비율의 조화, 음계와 수학의 관계를 탐구해 수학적 세계관의 출발점을 만들었습니다.",
    },
    "TVAR": {
        "number": 11,
        "pronunciation": "트바르",
        "person": "다비트 힐베르트",
        "quote": "수학자들의 23가지 숙제를 내준 대장!",
        "description": "여럿이 논의하는 장에서 도형과 구조를 체계적으로 분석하는 유형입니다. 문제를 명확히 세우고, 앞으로 탐구할 방향을 정리하는 데 강합니다.",
        "tendency": "제자들을 양성하며[T] 기하학의 토대를[V] 논리적으로 분석해[A] 미래 과제 탐구[R]",
        "achievement": "힐베르트의 23문제를 제시하고 공리주의 수학을 이끌었으며, 힐베르트 공간과 불변식 이론 등 현대 수학의 기반을 넓혔습니다.",
    },
    "TVAP": {
        "number": 12,
        "pronunciation": "트밥",
        "person": "캐서린 존슨",
        "quote": "달로 가는 길을 계산해 낸 인간 계산기!",
        "description": "팀 안에서 시각적 경로와 조건을 정확히 분석해 실제 목표를 달성하는 유형입니다. 복잡한 상황을 차분히 계산하고 적용하는 실전 감각이 좋습니다.",
        "tendency": "동료들과 협력하며[T] 우주선의 궤도를[V] 날카로운 논리로 분석해[A] 우주 탐사에 응용[P]",
        "achievement": "NASA에서 머큐리와 아폴로 임무의 궤도 계산을 수행했고, 아폴로 11호 달 착륙과 아폴로 13호 귀환에 기여했습니다.",
    },
    "TNIR": {
        "number": 13,
        "pronunciation": "트니르",
        "person": "폴 에르되시",
        "quote": "전 세계를 돌아다닌 수학 배낭여행자!",
        "description": "다른 사람과 문제를 주고받으며 숫자 세계의 새로운 아이디어를 찾아내는 유형입니다. 직관적인 패턴 감각이 좋고, 순수한 탐구 자체에서 에너지를 얻습니다.",
        "tendency": "전 세계 학자들과 협업하며[T] 숫자의 규칙을[N] 엄청난 직관으로[I] 순수하게 탐구[R]",
        "achievement": "조합론, 그래프 이론, 수론에서 수많은 논문을 남겼고, 에르되시 수와 확률적 방법으로 협업 수학의 상징이 되었습니다.",
    },
    "TNIP": {
        "number": 14,
        "pronunciation": "트닙",
        "person": "존 폰 노이만",
        "quote": "컴퓨터 구조를 처음 만든 아이디어 뱅크!",
        "description": "팀과 함께 복잡한 계산 아이디어를 빠르게 떠올리고 실제 시스템으로 연결하는 유형입니다. 수치적 직관과 응용 감각이 모두 강합니다.",
        "tendency": "거대한 팀을 이끌며[T] 엄청난 연산을[N] 직관적으로 처리해[I] 컴퓨터와 경제학에 응용[P]",
        "achievement": "게임 이론, 폰 노이만 구조, 셀룰러 오토마타, 양자역학의 수학적 기초 등 응용수학과 컴퓨터 과학의 기반을 세웠습니다.",
    },
    "TNAR": {
        "number": 15,
        "pronunciation": "트나르",
        "person": "에미 뇌터",
        "quote": "우주의 대칭성을 밝혀낸 위대한 스승!",
        "description": "함께 토론하면서 수식과 구조를 엄밀하게 분석하는 유형입니다. 복잡한 개념의 핵심 원리를 정리하고, 깊은 이론으로 발전시키는 데 강합니다.",
        "tendency": "제자들과 함께[T] 복잡한 수식을[N] 논리적으로 분석해[A] 물리학과 대수학을 탐구[R]",
        "achievement": "뇌터의 정리로 대칭성과 보존 법칙을 연결하고, 환과 아이디얼 이론을 발전시켜 현대 추상대수학의 기초를 세웠습니다.",
    },
    "TNAP": {
        "number": 16,
        "pronunciation": "트냅",
        "person": "앨런 튜링",
        "quote": "생각하는 기계를 만든 암호 해독 천재!",
        "description": "팀 안에서 기호와 규칙을 논리적으로 분석해 실제 문제를 해결하는 유형입니다. 추상적인 계산 원리를 기술, 암호, 알고리즘 같은 응용으로 바꾸는 데 능합니다.",
        "tendency": "암호 해독 팀과 협력해[T] 기호를[N] 논리적으로 분석하여[A] 전쟁을 끝내는 데 응용[P]",
        "achievement": "튜링 기계와 계산 가능성 이론을 세우고, 제2차 세계대전 암호 해독과 인공지능 개념 형성에 결정적으로 기여했습니다.",
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
        "manual_letters": {},
        "quiz_progress_previous": 0.0,
        "manual_progress_previous": 0.0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_quiz_state() -> None:
    st.session_state.current_question = 0
    st.session_state.answers = {}
    st.session_state.quiz_progress_previous = 0.0


def reset_manual_state() -> None:
    st.session_state.manual_letters = {}
    st.session_state.manual_progress_previous = 0.0


def pair_key(left: str, right: str) -> str:
    return f"{left}{right}"


def manual_letters() -> list:
    selected = st.session_state.manual_letters
    return [selected.get(pair_key(left, right), "") for left, right in TYPE_AXIS_PAIRS]


def manual_type_code() -> str:
    return "".join(manual_letters())


def manual_answered_count() -> int:
    return sum(1 for letter in manual_letters() if letter)


def manual_input_complete() -> bool:
    return manual_answered_count() == len(TYPE_AXIS_PAIRS)


def render_html(markup: str) -> None:
    clean_markup = "\n".join(line.strip() for line in markup.strip().splitlines())
    if hasattr(st, "html"):
        st.html(clean_markup)
    else:
        st.markdown(clean_markup, unsafe_allow_html=True)


def progress_bar_markup(progress: float, state_key: str) -> str:
    target = max(0.0, min(100.0, progress))
    start = float(st.session_state.get(state_key, 0.0))
    start = max(0.0, min(100.0, start))
    st.session_state[state_key] = target

    return (
        '<div class="progress-track">'
        f'<div class="progress-fill" style="--progress-start: {start:.1f}%; --progress-target: {target:.1f}%;"></div>'
        "</div>"
    )


def inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url("https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap");

        :root {
            color-scheme: dark;
            --ink: #f6fbff;
            --muted: rgba(223, 232, 246, 0.68);
            --quiet: rgba(223, 232, 246, 0.46);
            --panel: rgba(13, 20, 37, 0.72);
            --panel-strong: rgba(18, 27, 48, 0.92);
            --line: rgba(255, 255, 255, 0.11);
            --cyan: #6ee7ff;
            --blue: #4f8cff;
            --violet: #a78bfa;
            --lime: #b9f66a;
            --shadow: rgba(0, 0, 0, 0.44);
        }

        .stApp {
            background:
                radial-gradient(circle at 12% -8%, rgba(79, 140, 255, 0.22), transparent 34%),
                radial-gradient(circle at 88% 8%, rgba(167, 139, 250, 0.18), transparent 34%),
                linear-gradient(180deg, #060912 0%, #091120 42%, #101827 100%);
            color: var(--ink);
            font-family: "Space Grotesk", "Noto Sans KR", -apple-system,
                BlinkMacSystemFont, "Apple SD Gothic Neo", sans-serif;
        }

        .main .block-container {
            max-width: 1180px;
            padding-top: 0.45rem;
            padding-bottom: 2.2rem;
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
            min-height: 820px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            isolation: isolate;
            border-radius: 0;
            margin: -2rem calc(50% - 50vw) 0 calc(50% - 50vw);
            padding: 7rem 2rem 8.5rem;
            background:
                radial-gradient(circle at 50% 50%, rgba(110, 231, 255, 0.16), transparent 28%),
                radial-gradient(circle at 30% 32%, rgba(79, 140, 255, 0.2), transparent 36%),
                radial-gradient(circle at 74% 28%, rgba(167, 139, 250, 0.18), transparent 35%),
                linear-gradient(180deg, #060912 0%, #081120 48%, #0b1424 100%);
        }

        .home-wrap::before {
            content: "";
            position: absolute;
            inset: -16% -18%;
            z-index: 0;
            background:
                conic-gradient(from 138deg at 50% 50%, transparent 0deg, rgba(110, 231, 255, 0.2) 54deg, transparent 116deg, rgba(167, 139, 250, 0.18) 174deg, transparent 236deg, rgba(185, 246, 106, 0.12) 296deg, transparent 360deg);
            filter: blur(46px);
            opacity: 0.74;
            animation: slow-spin 24s linear infinite;
        }

        .home-wrap::after {
            content: "";
            position: absolute;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            background:
                linear-gradient(rgba(255,255,255,0.045) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
            background-size: 54px 54px;
            mask-image: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.46) 18%, rgba(0,0,0,0.28) 72%, transparent 100%);
            -webkit-mask-image: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.46) 18%, rgba(0,0,0,0.28) 72%, transparent 100%);
        }

        .home-visual {
            position: absolute;
            inset: 0;
            z-index: 1;
            pointer-events: none;
        }

        .orbital-frame {
            position: absolute;
            left: 50%;
            top: 49%;
            width: min(78vw, 920px);
            aspect-ratio: 1 / 0.46;
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 999px;
            transform: translate(-50%, -50%) rotate(-7deg);
            box-shadow:
                inset 0 0 80px rgba(110, 231, 255, 0.04),
                0 0 120px rgba(79, 140, 255, 0.08);
        }

        .orbital-frame.secondary {
            width: min(90vw, 1080px);
            transform: translate(-50%, -50%) rotate(9deg);
            opacity: 0.48;
        }

        .data-ribbon {
            position: absolute;
            left: 50%;
            top: 50%;
            width: min(90vw, 1080px);
            height: 1px;
            transform: translate(-50%, -50%) rotate(-18deg);
            background: linear-gradient(90deg, transparent, rgba(110, 231, 255, 0.58), rgba(167, 139, 250, 0.44), transparent);
            box-shadow: 0 0 42px rgba(110, 231, 255, 0.28);
        }

        .data-ribbon.alt {
            transform: translate(-50%, -50%) rotate(18deg);
            opacity: 0.52;
        }

        .signal-node {
            position: absolute;
            border-radius: 999px;
            background:
                radial-gradient(circle at 34% 28%, rgba(255,255,255,0.95), rgba(255,255,255,0.14) 34%, transparent 62%),
                linear-gradient(135deg, rgba(110,231,255,0.28), rgba(167,139,250,0.16));
            border: 1px solid rgba(255, 255, 255, 0.16);
            box-shadow:
                0 0 34px rgba(110, 231, 255, 0.18),
                inset 0 1px 0 rgba(255,255,255,0.18);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            animation: drift 8s ease-in-out infinite;
        }

        .node-a { width: 84px; height: 84px; left: 12%; top: 22%; animation-delay: -1s; }
        .node-b { width: 118px; height: 118px; right: 11%; top: 18%; animation-delay: -3.8s; }
        .node-c { width: 64px; height: 64px; left: 21%; bottom: 18%; animation-delay: -2.4s; }
        .node-d { width: 92px; height: 92px; right: 23%; bottom: 15%; animation-delay: -5.2s; }

        .mesh-chip {
            position: absolute;
            width: 220px;
            height: 132px;
            border-radius: 28px;
            border: 1px solid rgba(255,255,255,0.1);
            background:
                linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.02)),
                repeating-linear-gradient(90deg, rgba(255,255,255,0.06) 0 1px, transparent 1px 18px);
            box-shadow: 0 34px 80px rgba(0, 0, 0, 0.32);
            transform: rotate(-10deg);
            opacity: 0.54;
        }

        .chip-left { left: 8%; bottom: 31%; }
        .chip-right { right: 8%; bottom: 32%; transform: rotate(11deg); }

        @keyframes slow-spin {
            to { transform: rotate(360deg); }
        }

        @keyframes drift {
            0%, 100% { transform: translate3d(0, 0, 0); }
            50% { transform: translate3d(0, -18px, 0); }
        }

        .home-inner {
            position: relative;
            z-index: 3;
            width: min(100%, 1120px);
            margin: 0 auto;
            text-align: center;
        }

        .home-title {
            width: 100%;
            margin: 0 auto;
            color: transparent;
            background: linear-gradient(180deg, #ffffff 0%, #bdefff 42%, #6fa8ff 76%, #a78bfa 100%);
            -webkit-background-clip: text;
            background-clip: text;
            text-align: center;
            font-family: "Space Grotesk", "Noto Sans KR", -apple-system,
                BlinkMacSystemFont, sans-serif;
            font-size: clamp(5.3rem, 15vw, 13.4rem);
            line-height: 0.82;
            font-weight: 700;
            letter-spacing: -0.045em;
            filter: drop-shadow(0 34px 76px rgba(79, 140, 255, 0.24));
        }

        .home-subtitle {
            width: 100%;
            max-width: calc(100vw - 2.5rem);
            margin: 1.9rem auto 0;
            color: rgba(246, 251, 255, 0.92);
            text-align: center;
            font-family: "Space Grotesk", "Noto Sans KR", -apple-system,
                BlinkMacSystemFont, sans-serif;
            font-size: clamp(1.25rem, 3.2vw, 3rem);
            line-height: 1.02;
            font-weight: 600;
            letter-spacing: -0.025em;
            white-space: nowrap;
        }

        .home-copy {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            max-width: 780px;
            margin: 2rem auto 0;
            color: rgba(223, 232, 246, 0.68);
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

        .home-motto {
            width: 100%;
            max-width: 720px;
            margin: -5.6rem auto 1.45rem;
            position: relative;
            z-index: 5;
            color: rgba(246, 251, 255, 0.84);
            font-family: "Noto Sans KR", -apple-system, BlinkMacSystemFont,
                "Apple SD Gothic Neo", sans-serif;
            font-size: clamp(1.18rem, 2.35vw, 1.68rem);
            line-height: 1.5;
            font-weight: 300;
            text-align: center;
        }

        .start-zone {
            max-width: min(540px, calc(100vw - 2rem));
            margin: 0 auto 5rem;
            position: relative;
            z-index: 5;
        }

        .app-footer {
            width: min(100%, 1760px);
            margin: 1.35rem auto 0;
            padding: 1.5rem clamp(1rem, 4vw, 2.5rem) 0;
            display: grid;
            grid-template-columns: minmax(150px, 1fr) minmax(260px, 520px) minmax(150px, 1fr);
            align-items: end;
            gap: clamp(0.8rem, 3vw, 2.5rem);
            color: rgba(223, 232, 246, 0.62);
            font-family: "Noto Sans KR", "Space Grotesk", -apple-system,
                BlinkMacSystemFont, sans-serif;
        }

        .footer-center {
            width: 100%;
            justify-self: center;
            text-align: center;
        }

        .footer-credit {
            color: rgba(246, 251, 255, 0.78);
            font-family: "Space Grotesk", "Noto Sans KR", -apple-system,
                BlinkMacSystemFont, sans-serif;
            font-size: 0.96rem;
            font-weight: 600;
            letter-spacing: 0;
        }

        .footer-logo-slot {
            display: flex;
            align-items: flex-end;
            min-height: 1px;
        }

        .footer-logo-slot.left {
            justify-content: flex-start;
        }

        .footer-logo-slot.right {
            justify-content: flex-end;
        }

        .footer-corner-logo {
            display: block;
            height: auto;
            object-fit: contain;
            opacity: 0.9;
            filter: drop-shadow(0 14px 30px rgba(0, 0, 0, 0.16));
        }

        .footer-corner-logo.signature {
            width: clamp(160px, 19vw, 270px);
        }

        .footer-corner-logo.slogan {
            width: clamp(150px, 18vw, 260px);
        }

        .footer-school {
            margin-top: 0.55rem;
            color: rgba(223, 232, 246, 0.7);
            font-size: 0.94rem;
            font-weight: 500;
        }

        .footer-motto {
            margin-top: 0.28rem;
            color: rgba(223, 232, 246, 0.48);
            font-size: 0.9rem;
            font-weight: 300;
        }

        .theme-toggle-row {
            max-width: 1180px;
            margin: 0 auto 0.9rem;
            display: flex;
            justify-content: flex-end;
        }

        .theme-toggle-row .stButton {
            width: min(190px, 46vw);
        }

        .theme-toggle-row .stButton > button {
            min-height: 2.7rem !important;
            border-radius: 999px !important;
            font-size: 0.88rem !important;
            font-weight: 760 !important;
            box-shadow: 0 16px 38px rgba(0, 0, 0, 0.18) !important;
        }

        .experience-shell {
            padding: 1.2rem 0 0;
            color: var(--ink);
        }

        .topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 1.45rem;
            padding: 0.72rem 1rem;
            border-radius: 999px;
            color: rgba(246, 251, 255, 0.86);
            background: rgba(9, 16, 32, 0.58);
            border: 1px solid var(--line);
            box-shadow: 0 24px 70px rgba(0, 0, 0, 0.24);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            font-size: 0.95rem;
            font-weight: 650;
        }

        .brand-mark {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            min-width: 0;
        }

        .brand-text {
            min-width: 0;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .brand-dot {
            width: 2rem;
            height: 2rem;
            display: grid;
            place-items: center;
            border-radius: 50%;
            color: #06111f;
            background: linear-gradient(135deg, var(--cyan), var(--lime));
            font-weight: 850;
            box-shadow: 0 0 24px rgba(110, 231, 255, 0.24);
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

        .quiz-shell .question-stage {
            margin-bottom: 1.2rem;
        }

        .progress-track {
            height: 8px;
            max-width: 520px;
            margin: 0 auto 1.35rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.08);
            overflow: hidden;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.06);
        }

        .progress-fill {
            position: relative;
            height: 100%;
            width: var(--progress-target, 0%);
            border-radius: inherit;
            background: linear-gradient(90deg, var(--cyan), var(--blue), var(--violet));
            box-shadow: 0 0 26px rgba(110, 231, 255, 0.38);
            overflow: hidden;
            animation: progress-fill-grow 1.35s cubic-bezier(0.16, 1, 0.3, 1) both;
            will-change: width, filter;
        }

        .progress-fill::after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(
                90deg,
                transparent 0%,
                rgba(255, 255, 255, 0.36) 46%,
                transparent 78%
            );
            transform: translateX(-120%);
            animation: progress-sheen 1.8s ease-in-out infinite;
            opacity: 0.72;
        }

        @keyframes progress-sheen {
            0% { transform: translateX(-120%); }
            58%, 100% { transform: translateX(120%); }
        }

        @keyframes progress-fill-grow {
            from {
                width: var(--progress-start, 0%);
                filter: saturate(0.92) brightness(0.94);
            }
            68% {
                filter: saturate(1.14) brightness(1.08);
            }
            to {
                width: var(--progress-target, 0%);
                filter: saturate(1) brightness(1);
            }
        }

        .question-number {
            color: var(--quiet);
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
        }

        .quiz-shell .question-number {
            margin-bottom: 0.42rem;
        }

        .question-title {
            color: var(--ink);
            font-size: clamp(2.4rem, 6vw, 4.7rem);
            line-height: 1.05;
            font-weight: 820;
            margin: 0 auto;
        }

        .quiz-shell .question-title {
            font-size: clamp(2.15rem, 5.2vw, 4.1rem);
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
            border-radius: 26px;
            background: var(--panel);
            border: 1px solid var(--line);
            box-shadow: 0 22px 54px var(--shadow);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }

        .choice-card.selected {
            border-color: rgba(110, 231, 255, 0.42);
            box-shadow: 0 26px 64px rgba(79, 140, 255, 0.22);
            background:
                radial-gradient(circle at top right, rgba(110,231,255,0.18), transparent 38%),
                var(--panel-strong);
        }

        .choice-code {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 3.1rem;
            height: 3.1rem;
            margin-bottom: 1.2rem;
            border-radius: 50%;
            background: rgba(255,255,255,0.08);
            color: var(--ink);
            font-size: 1.2rem;
            font-weight: 820;
        }

        .choice-card.selected .choice-code {
            background: linear-gradient(135deg, var(--cyan), var(--blue));
            color: #06111f;
        }

        .choice-title {
            margin-bottom: 0.8rem;
            color: var(--ink);
            font-size: clamp(1.45rem, 3vw, 2.1rem);
            line-height: 1.16;
            font-weight: 760;
        }

        .choice-body {
            color: var(--muted);
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
            border-radius: 28px;
            background:
                linear-gradient(180deg, rgba(255,255,255,0.085), rgba(255,255,255,0.035)),
                rgba(12, 19, 35, 0.74);
            border: 1px solid var(--line);
            box-shadow: 0 24px 70px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
        }

        .quiz-shell .endpoint-card {
            min-height: 146px;
            padding: 1.15rem;
            border-radius: 22px;
        }

        .endpoint-card.right {
            background:
                radial-gradient(circle at 96% 0%, rgba(167, 139, 250, 0.18), transparent 42%),
                linear-gradient(180deg, rgba(255,255,255,0.085), rgba(255,255,255,0.035)),
                rgba(12, 19, 35, 0.74);
        }

        .endpoint-topline {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.8rem;
            margin-bottom: 0.9rem;
        }

        .quiz-shell .endpoint-topline {
            margin-bottom: 0.55rem;
        }

        .endpoint-code {
            display: inline-grid;
            place-items: center;
            width: 2.8rem;
            height: 2.8rem;
            border-radius: 50%;
            background: rgba(255,255,255,0.08);
            color: var(--ink);
            font-size: 1.1rem;
            font-weight: 840;
        }

        .quiz-shell .endpoint-code {
            width: 2.35rem;
            height: 2.35rem;
        }

        .endpoint-side {
            color: var(--quiet);
            font-size: 0.88rem;
            font-weight: 760;
        }

        .endpoint-title {
            color: var(--ink);
            font-size: clamp(1.25rem, 2.4vw, 1.75rem);
            line-height: 1.18;
            font-weight: 820;
            margin-bottom: 0.55rem;
        }

        .quiz-shell .endpoint-title {
            margin-bottom: 0.35rem;
        }

        .endpoint-body {
            color: var(--muted);
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
            color: var(--quiet);
            font-size: 0.92rem;
            font-weight: 700;
        }

        .quiz-shell .likert-guide {
            margin-bottom: 0.5rem;
        }

        .likert-selected {
            max-width: 980px;
            margin: 0.85rem auto 0;
            padding: 0.9rem 1rem;
            border-radius: 18px;
            background: rgba(110, 231, 255, 0.1);
            border: 1px solid rgba(110, 231, 255, 0.16);
            color: #c9f6ff;
            text-align: center;
            font-size: 0.98rem;
            font-weight: 720;
        }

        .quiz-shell .likert-selected {
            margin-top: 0.55rem;
            padding: 0.72rem 1rem;
        }

        .nav-row {
            max-width: 980px;
            margin: 1.8rem auto 0;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.8rem;
        }

        .quiz-shell .nav-row {
            margin-top: 1rem;
        }

        .result-wrap {
            text-align: center;
        }

        .result-hero {
            width: min(100%, 840px);
            margin: 1.5rem auto 1.8rem;
            text-align: center;
        }

        .result-title {
            margin: 0 auto 0.8rem;
            color: var(--ink);
            font-size: clamp(2.4rem, 7vw, 5.4rem);
            line-height: 1;
            font-weight: 840;
            text-align: center;
        }

        .result-copy {
            max-width: 620px;
            margin: 0 auto 1.5rem;
            color: var(--muted);
            font-size: 1.08rem;
            line-height: 1.68;
            font-weight: 520;
            text-align: center !important;
        }

        .result-copy span {
            display: block;
        }

        .result-copy span + span {
            margin-top: 0.12rem;
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
            background: var(--panel);
            border: 1px solid var(--line);
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.24);
            text-align: left;
        }

        .score-label {
            display: flex;
            justify-content: space-between;
            color: var(--ink);
            font-size: 0.95rem;
            font-weight: 760;
            margin-bottom: 0.8rem;
        }

        .score-track {
            height: 10px;
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
            overflow: hidden;
        }

        .score-fill {
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(90deg, var(--cyan), var(--blue), var(--violet));
        }

        .axis-guide-section {
            max-width: 980px;
            margin: 2.4rem auto 2rem;
            text-align: left;
        }

        .axis-guide-title {
            margin: 0 0 0.35rem;
            color: var(--ink);
            font-size: clamp(1.65rem, 3.2vw, 2.45rem);
            line-height: 1.12;
            font-weight: 840;
            text-align: center;
        }

        .axis-guide-copy {
            max-width: 620px;
            margin: 0 auto 1.4rem;
            color: var(--muted);
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
                linear-gradient(180deg, rgba(255,255,255,0.075), rgba(255,255,255,0.032));
            border: 1px solid var(--line);
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.22);
            position: relative;
            overflow: hidden;
        }

        .axis-guide-card.active {
            border-color: rgba(110, 231, 255, 0.32);
            background:
                radial-gradient(circle at 90% 0%, rgba(110, 231, 255, 0.18), transparent 34%),
                linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0.04));
            box-shadow: 0 22px 60px rgba(79, 140, 255, 0.18);
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
            background: rgba(255,255,255,0.08);
            color: var(--ink);
            font-family: "Space Grotesk", "Noto Sans KR", sans-serif;
            font-size: 1.1rem;
            font-weight: 850;
        }

        .axis-guide-card.active .axis-guide-code {
            background: linear-gradient(135deg, var(--cyan), var(--lime));
            color: #06111f;
            box-shadow: 0 10px 26px rgba(110, 231, 255, 0.22);
        }

        .axis-guide-badge {
            color: var(--cyan);
            font-size: 0.78rem;
            font-weight: 760;
            opacity: 0;
        }

        .axis-guide-card.active .axis-guide-badge {
            opacity: 1;
        }

        .axis-guide-name {
            color: var(--ink);
            font-size: 1.05rem;
            line-height: 1.2;
            font-weight: 820;
            margin-bottom: 0.25rem;
        }

        .axis-guide-label {
            color: var(--cyan);
            font-size: 0.9rem;
            font-weight: 720;
            margin-bottom: 0.65rem;
        }

        .axis-guide-desc {
            color: var(--muted);
            font-size: 0.92rem;
            line-height: 1.55;
            font-weight: 430;
        }

        .percent-section,
        .type-detail-section {
            max-width: 980px;
            margin: 2.4rem auto 2rem;
            text-align: left;
        }

        .percent-title,
        .type-detail-title {
            margin: 0 0 0.35rem;
            color: var(--ink);
            font-size: clamp(1.65rem, 3.2vw, 2.45rem);
            line-height: 1.12;
            font-weight: 840;
            text-align: center;
        }

        .percent-copy,
        .type-detail-copy {
            max-width: 650px;
            margin: 0 auto 1.4rem;
            color: var(--muted);
            font-size: 1rem;
            line-height: 1.58;
            font-weight: 420;
            text-align: center;
        }

        .percent-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.9rem;
        }

        .percent-card,
        .type-detail-card {
            border-radius: 22px;
            background:
                linear-gradient(180deg, rgba(255,255,255,0.075), rgba(255,255,255,0.032));
            border: 1px solid var(--line);
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.22);
        }

        .percent-card {
            padding: 1.15rem;
        }

        .percent-card-title {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.7rem;
            margin-bottom: 0.85rem;
            color: var(--ink);
            font-size: 1.02rem;
            font-weight: 820;
        }

        .percent-winner {
            color: var(--cyan);
            font-size: 0.86rem;
            font-weight: 780;
            white-space: nowrap;
        }

        .percent-row {
            margin-top: 0.8rem;
        }

        .percent-row-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.7rem;
            margin-bottom: 0.42rem;
            color: var(--muted);
            font-size: 0.92rem;
            font-weight: 720;
        }

        .percent-letter {
            color: var(--ink);
            font-weight: 860;
        }

        .percent-track {
            height: 11px;
            overflow: hidden;
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.06);
        }

        .percent-fill {
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(90deg, var(--cyan), var(--blue), var(--violet));
            box-shadow: 0 0 22px rgba(110, 231, 255, 0.28);
        }

        .type-detail-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.9rem;
        }

        .type-detail-card {
            min-height: 255px;
            padding: 1.2rem;
            position: relative;
            overflow: hidden;
        }

        .type-detail-card.active {
            border-color: rgba(110, 231, 255, 0.34);
            background:
                radial-gradient(circle at 92% 0%, rgba(110, 231, 255, 0.18), transparent 34%),
                linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0.04));
            box-shadow: 0 24px 64px rgba(79, 140, 255, 0.2);
        }

        .type-detail-top {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 0.8rem;
            margin-bottom: 0.7rem;
        }

        .type-detail-code {
            color: var(--ink);
            font-family: "Space Grotesk", "Noto Sans KR", sans-serif;
            font-size: 1.28rem;
            line-height: 1;
            font-weight: 860;
        }

        .type-detail-badge {
            color: var(--cyan);
            font-size: 0.78rem;
            font-weight: 800;
            white-space: nowrap;
        }

        .type-detail-person {
            color: var(--cyan);
            font-size: 1rem;
            line-height: 1.28;
            font-weight: 780;
            margin-bottom: 0.55rem;
        }

        .type-detail-desc {
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.58;
            font-weight: 430;
            margin-bottom: 0.9rem;
        }

        .type-detail-meta {
            display: grid;
            gap: 0.55rem;
            padding-top: 0.85rem;
            border-top: 1px solid rgba(255,255,255,0.08);
        }

        .type-detail-meta-item {
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.48;
            font-weight: 430;
        }

        .type-detail-meta-item strong {
            color: var(--ink);
            font-weight: 800;
        }

        .personality-section {
            max-width: 1120px;
            margin: 3.4rem auto 2.2rem;
            color: var(--ink);
        }

        .personality-heading {
            display: flex;
            align-items: center;
            gap: 0.9rem;
            margin-bottom: 1.25rem;
        }

        .personality-number {
            width: 3.1rem;
            height: 3.1rem;
            display: grid;
            place-items: center;
            flex: 0 0 auto;
            border-radius: 50%;
            border: 2px solid #e5ad29;
            color: var(--ink);
            background: rgba(255,255,255,0.05);
            font-family: "Space Grotesk", "Noto Sans KR", sans-serif;
            font-size: 1.25rem;
            font-weight: 860;
        }

        .personality-title {
            margin: 0;
            color: var(--ink);
            font-size: clamp(1.75rem, 3.2vw, 2.8rem);
            line-height: 1.08;
            font-weight: 860;
        }

        .personality-layout {
            display: grid;
            grid-template-columns: minmax(0, 1.5fr) minmax(290px, 0.7fr);
            gap: 1.2rem;
            align-items: stretch;
            padding: 1.4rem;
            border-radius: 28px;
            background: rgba(255,255,255,0.06);
            border: 1px solid var(--line);
            box-shadow: 0 24px 76px rgba(0,0,0,0.26);
        }

        .trait-panel {
            display: grid;
            gap: 1.45rem;
            padding: 1.3rem;
            border-radius: 22px;
            background: rgba(255,255,255,0.05);
        }

        .trait-row {
            --axis-color: var(--cyan);
        }

        .trait-value {
            margin-bottom: 0.48rem;
            color: var(--axis-color);
            text-align: center;
            font-size: 1.16rem;
            font-weight: 860;
        }

        .trait-value strong {
            color: var(--ink);
            font-weight: 860;
        }

        .trait-track {
            position: relative;
            height: 13px;
            border-radius: 999px;
            background: var(--axis-color);
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.24);
        }

        .trait-knob {
            position: absolute;
            top: 50%;
            left: var(--knob-left);
            width: 1.45rem;
            height: 1.45rem;
            border-radius: 50%;
            border: 4px solid #ffffff;
            background: var(--axis-color);
            transform: translate(-50%, -50%);
            box-shadow: 0 10px 24px rgba(0,0,0,0.22);
        }

        .trait-labels {
            display: flex;
            justify-content: space-between;
            gap: 0.9rem;
            margin-top: 0.5rem;
            color: var(--muted);
            font-size: 0.93rem;
            font-weight: 720;
        }

        .trait-summary {
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 0.9rem;
            padding: 1.35rem;
            border-radius: 22px;
            background: rgba(255,255,255,0.08);
            text-align: left;
        }

        .trait-summary-kicker {
            color: var(--muted);
            font-size: 0.9rem;
            font-weight: 720;
        }

        .trait-summary-title {
            color: var(--ink);
            font-size: 1.65rem;
            line-height: 1.14;
            font-weight: 860;
        }

        .trait-summary-code {
            color: #e5ad29;
            font-size: 1.06rem;
            font-weight: 840;
        }

        .trait-summary-image {
            width: 145px;
            height: 145px;
            border-radius: 20px;
            object-fit: cover;
            object-position: center top;
            background: rgba(255,255,255,0.08);
            border: 1px solid var(--line);
        }

        .trait-summary-desc {
            color: var(--muted);
            font-size: 1rem;
            line-height: 1.62;
            font-weight: 430;
        }

        .manual-trait-list {
            display: grid;
            gap: 0.85rem;
        }

        .manual-trait-item {
            padding: 1rem;
            border-radius: 18px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.08);
        }

        .manual-trait-name {
            color: var(--ink);
            font-size: 1.06rem;
            line-height: 1.22;
            font-weight: 840;
            margin-bottom: 0.35rem;
        }

        .manual-trait-name span {
            color: #e5ad29;
        }

        .manual-trait-desc {
            color: var(--muted);
            font-size: 0.94rem;
            line-height: 1.55;
            font-weight: 430;
        }

        .story-copy {
            max-width: 1000px;
            margin: 1.8rem auto 0;
            color: rgba(223, 232, 246, 0.78);
            font-size: clamp(1.02rem, 1.65vw, 1.2rem);
            line-height: 1.82;
            font-weight: 430;
        }

        .story-copy p {
            margin: 0 0 1.05rem;
            color: inherit;
        }

        .manual-stage {
            text-align: center;
            max-width: 980px;
            margin: 0 auto 1rem;
        }

        .manual-title {
            color: var(--ink);
            font-size: clamp(2.4rem, 6.8vw, 5rem);
            line-height: 1.04;
            font-weight: 840;
            margin: 0;
        }

        .manual-copy {
            max-width: 680px;
            margin: 0.65rem auto 1rem;
            color: var(--muted);
            font-size: 1.05rem;
            line-height: 1.62;
            font-weight: 460;
            text-align: center !important;
        }

        .manual-code-row {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.8rem;
            max-width: 520px;
            margin: 0 auto;
        }

        .manual-code-slot {
            min-height: 4.25rem;
            display: grid;
            place-items: center;
            border-radius: 24px;
            border: 1px solid var(--line);
            background:
                linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03)),
                rgba(12, 19, 35, 0.7);
            color: rgba(223, 232, 246, 0.38);
            font-family: "Space Grotesk", "Noto Sans KR", sans-serif;
            font-size: 2rem;
            font-weight: 860;
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.22);
        }

        .manual-code-slot.filled {
            color: #06111f;
            background:
                radial-gradient(circle at 18% 18%, rgba(255,255,255,0.34), transparent 32%),
                linear-gradient(135deg, var(--cyan), var(--blue), var(--violet));
            border-color: rgba(210, 250, 255, 0.42);
            box-shadow: 0 22px 60px rgba(79, 140, 255, 0.28);
        }

        .manual-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.9rem;
            max-width: 980px;
            margin: 0 auto 1.6rem;
        }

        .manual-card-spacer {
            height: 0.65rem;
        }

        .manual-card {
            min-height: 178px;
            padding: 1rem;
            border-radius: 24px;
            background:
                linear-gradient(180deg, rgba(255,255,255,0.075), rgba(255,255,255,0.032)),
                rgba(12, 19, 35, 0.7);
            border: 1px solid var(--line);
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.22);
            text-align: left;
        }

        .manual-card.active {
            border-color: rgba(110, 231, 255, 0.34);
            background:
                radial-gradient(circle at 90% 0%, rgba(110, 231, 255, 0.18), transparent 34%),
                linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0.04)),
                rgba(12, 19, 35, 0.82);
            box-shadow: 0 24px 64px rgba(79, 140, 255, 0.2);
        }

        .manual-card-kicker {
            color: var(--quiet);
            font-size: 0.82rem;
            font-weight: 760;
            margin-bottom: 0.48rem;
        }

        .manual-card-title {
            color: var(--ink);
            font-size: 1.3rem;
            line-height: 1.18;
            font-weight: 840;
            margin-bottom: 0.68rem;
        }

        .manual-option {
            padding: 0.55rem 0;
            border-top: 1px solid rgba(255,255,255,0.08);
        }

        .manual-option-code {
            color: var(--cyan);
            font-size: 1.08rem;
            font-weight: 860;
        }

        .manual-option-name {
            margin-left: 0.25rem;
            color: var(--ink);
            font-size: 0.98rem;
            font-weight: 760;
        }

        .manual-option-desc {
            margin-top: 0.2rem;
            color: var(--muted);
            font-size: 0.87rem;
            line-height: 1.45;
            font-weight: 420;
        }

        .stButton > button {
            min-height: 3.05rem;
            border-radius: 999px;
            border: 1px solid rgba(255, 255, 255, 0.14);
            background:
                radial-gradient(circle at 18% 18%, rgba(255,255,255,0.3), transparent 30%),
                linear-gradient(135deg, #6ee7ff 0%, #4f8cff 48%, #a78bfa 100%);
            color: #06111f;
            font-weight: 760;
            font-size: 1rem;
            letter-spacing: 0;
            box-shadow: 0 20px 52px rgba(79, 140, 255, 0.25), inset 0 1px 0 rgba(255,255,255,0.28);
            transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
        }

        .stButton > button:hover {
            background:
                radial-gradient(circle at 18% 18%, rgba(255,255,255,0.34), transparent 30%),
                linear-gradient(135deg, #93f1ff 0%, #5d96ff 50%, #b99cff 100%);
            color: #06111f;
            transform: translateY(-2px);
            box-shadow: 0 26px 68px rgba(79, 140, 255, 0.34), inset 0 1px 0 rgba(255,255,255,0.32);
        }

        .stButton > button:focus {
            color: #06111f;
            box-shadow: 0 0 0 4px rgba(110, 231, 255, 0.16), 0 18px 36px rgba(79, 140, 255, 0.28);
        }

        .stButton > button,
        .stButton > button[kind],
        .stButton > button[data-testid^="stBaseButton"] {
            font-family: "Noto Sans KR", "Space Grotesk", -apple-system,
                BlinkMacSystemFont, sans-serif !important;
            line-height: 1.15 !important;
            white-space: nowrap !important;
        }

        .stButton > button *,
        .stButton > button p,
        .stButton > button span {
            color: inherit !important;
            opacity: 1 !important;
            white-space: nowrap !important;
        }

        .stButton > button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]),
        .stButton > button[kind="secondary"],
        .stButton > button[data-testid="stBaseButton-secondary"] {
            min-height: 3.85rem !important;
            border-radius: 20px !important;
            border: 1px solid rgba(255, 255, 255, 0.24) !important;
            background:
                radial-gradient(circle at 18% 12%, rgba(255, 255, 255, 0.13), transparent 34%),
                linear-gradient(145deg, rgba(17, 27, 48, 0.94), rgba(8, 14, 28, 0.86)) !important;
            color: #ffffff !important;
            font-size: 1rem !important;
            font-weight: 780 !important;
            text-shadow: 0 1px 12px rgba(0, 0, 0, 0.26) !important;
            box-shadow:
                0 18px 46px rgba(0, 0, 0, 0.24),
                inset 0 1px 0 rgba(255,255,255,0.18) !important;
            backdrop-filter: blur(18px) saturate(1.22) !important;
            -webkit-backdrop-filter: blur(18px) saturate(1.22) !important;
        }

        .stButton > button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]):hover,
        .stButton > button[kind="secondary"]:hover,
        .stButton > button[data-testid="stBaseButton-secondary"]:hover {
            border-color: rgba(110, 231, 255, 0.38) !important;
            background:
                radial-gradient(circle at 18% 12%, rgba(110, 231, 255, 0.2), transparent 34%),
                linear-gradient(145deg, rgba(19, 36, 65, 0.96), rgba(9, 18, 35, 0.9)) !important;
            color: #ffffff !important;
            transform: translateY(-3px) !important;
            box-shadow:
                0 24px 58px rgba(79, 140, 255, 0.2),
                inset 0 1px 0 rgba(255,255,255,0.22) !important;
        }

        .stButton > button[kind="primary"],
        .stButton > button[data-testid="stBaseButton-primary"] {
            min-height: 3.85rem !important;
            border-radius: 20px !important;
            border: 1px solid rgba(210, 250, 255, 0.52) !important;
            background:
                radial-gradient(circle at 22% 18%, rgba(255,255,255,0.44), transparent 30%),
                linear-gradient(135deg, rgba(124,236,255,0.86) 0%, rgba(91,152,255,0.74) 52%, rgba(170,140,255,0.7) 100%) !important;
            color: #06111f !important;
            font-size: 1rem !important;
            font-weight: 860 !important;
            box-shadow:
                0 22px 58px rgba(79, 140, 255, 0.34),
                inset 0 1px 0 rgba(255,255,255,0.4) !important;
            backdrop-filter: blur(18px) saturate(1.25) !important;
            -webkit-backdrop-filter: blur(18px) saturate(1.25) !important;
        }

        .stButton > button[kind="primary"]:hover,
        .stButton > button[data-testid="stBaseButton-primary"]:hover {
            color: #06111f !important;
            transform: translateY(-3px) !important;
            box-shadow:
                0 28px 68px rgba(79, 140, 255, 0.42),
                inset 0 1px 0 rgba(255,255,255,0.46) !important;
        }

        div[data-testid="column"] .stButton > button {
            min-height: 4.15rem !important;
            width: 100% !important;
            padding: 0.85rem 0.9rem !important;
        }

        .stButton > button:disabled,
        .stButton > button[disabled] {
            border-color: rgba(255, 255, 255, 0.1) !important;
            background:
                linear-gradient(145deg, rgba(255,255,255,0.055), rgba(255,255,255,0.018)) !important;
            color: rgba(223, 232, 246, 0.44) !important;
            box-shadow: none !important;
            opacity: 1 !important;
            transform: none !important;
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
                padding-top: 0.35rem;
                padding-bottom: 2rem;
            }

            .home-wrap {
                min-height: 720px;
                padding: 5.6rem 1rem 7.6rem;
            }

            .home-title {
                margin-top: 0;
                font-size: clamp(4.8rem, 23vw, 7rem);
                line-height: 0.86;
            }

            .home-subtitle {
                margin-top: 1.15rem;
                font-size: clamp(0.82rem, 3.6vw, 1.25rem);
                line-height: 1.08;
            }

            .home-copy {
                max-width: 330px;
                margin-top: 1.25rem;
                font-size: 1rem;
                line-height: 1.58;
            }

            .home-motto {
                max-width: 330px;
                margin: -4.7rem auto 1.2rem;
                font-size: 1.12rem;
                line-height: 1.54;
            }

            .orbital-frame {
                width: 720px;
                left: 50%;
                top: 50%;
            }

            .mesh-chip {
                display: none;
            }

            .node-a { width: 58px; height: 58px; left: 7%; top: 18%; }
            .node-b { width: 72px; height: 72px; right: 6%; top: 22%; }
            .node-c { width: 48px; height: 48px; left: 13%; bottom: 18%; }
            .node-d { width: 62px; height: 62px; right: 13%; bottom: 17%; }

            .start-zone {
                margin-top: 0;
                margin-bottom: 4rem;
            }

            .app-footer {
                margin-top: 1.35rem;
                padding-top: 1rem;
                grid-template-columns: 1fr 1fr;
                grid-template-areas:
                    "center center"
                    "signature slogan";
                align-items: end;
                row-gap: 1rem;
            }

            .footer-center {
                grid-area: center;
            }

            .footer-logo-slot.left {
                grid-area: signature;
                justify-content: flex-start;
            }

            .footer-logo-slot.right {
                grid-area: slogan;
                justify-content: flex-end;
            }

            .footer-corner-logo.signature {
                width: min(190px, 43vw);
            }

            .footer-corner-logo.slogan {
                width: min(180px, 41vw);
            }

            .topbar {
                margin-bottom: 1.3rem;
                font-size: 0.82rem;
            }

            .choice-grid,
            .endpoint-grid,
            .manual-grid,
            .percent-grid,
            .personality-layout,
            .score-grid,
            .axis-guide-grid,
            .type-detail-grid,
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

            .type-detail-card {
                min-height: 0;
            }

            .personality-heading {
                align-items: flex-start;
                gap: 0.85rem;
            }

            .personality-number {
                width: 2.7rem;
                height: 2.7rem;
                font-size: 1.08rem;
                border-width: 2px;
            }

            .personality-layout {
                padding: 0.85rem;
                border-radius: 22px;
            }

            .trait-panel,
            .trait-summary {
                padding: 1rem;
            }

            .question-title {
                font-size: 2.35rem;
            }

            .manual-code-row {
                gap: 0.55rem;
            }

            .manual-code-slot {
                min-height: 3.8rem;
                border-radius: 18px;
                font-size: 1.7rem;
            }

            .manual-card {
                min-height: 0;
                padding: 1rem;
                border-radius: 22px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        @media (prefers-color-scheme: light) {
            :root {
                color-scheme: light;
                --ink: #0c1728;
                --muted: rgba(31, 48, 74, 0.68);
                --quiet: rgba(31, 48, 74, 0.48);
                --panel: rgba(255, 255, 255, 0.72);
                --panel-strong: rgba(255, 255, 255, 0.92);
                --line: rgba(20, 45, 82, 0.12);
                --cyan: #0077c8;
                --blue: #005bac;
                --violet: #6252d8;
                --lime: #43bf76;
                --shadow: rgba(24, 54, 92, 0.16);
            }

            .stApp {
                background:
                    radial-gradient(circle at 14% -8%, rgba(0, 91, 172, 0.18), transparent 34%),
                    radial-gradient(circle at 86% 4%, rgba(98, 82, 216, 0.12), transparent 32%),
                    linear-gradient(180deg, #f8fbff 0%, #edf6ff 42%, #ffffff 100%);
                color: var(--ink);
            }

            .home-wrap {
                background:
                    radial-gradient(circle at 50% 48%, rgba(0, 91, 172, 0.14), transparent 30%),
                    radial-gradient(circle at 28% 28%, rgba(0, 119, 200, 0.16), transparent 36%),
                    radial-gradient(circle at 74% 28%, rgba(98, 82, 216, 0.12), transparent 35%),
                    linear-gradient(180deg, #f8fbff 0%, #edf6ff 52%, #ffffff 100%);
            }

            .home-wrap::before {
                background:
                    conic-gradient(from 138deg at 50% 50%, transparent 0deg, rgba(0, 119, 200, 0.14) 54deg, transparent 116deg, rgba(98, 82, 216, 0.12) 174deg, transparent 236deg, rgba(67, 191, 118, 0.1) 296deg, transparent 360deg);
                opacity: 0.92;
            }

            .home-wrap::after {
                background:
                    linear-gradient(rgba(0,91,172,0.05) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(0,91,172,0.044) 1px, transparent 1px);
                mask-image: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.3) 18%, rgba(0,0,0,0.18) 72%, transparent 100%);
                -webkit-mask-image: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.3) 18%, rgba(0,0,0,0.18) 72%, transparent 100%);
            }

            .home-title {
                background: linear-gradient(180deg, #06111f 0%, #005bac 54%, #6252d8 100%);
                -webkit-background-clip: text;
                background-clip: text;
                filter: drop-shadow(0 28px 64px rgba(0, 91, 172, 0.18));
            }

            .home-subtitle {
                color: rgba(12, 23, 40, 0.92);
            }

            .home-copy,
            .home-motto,
            .app-footer,
            .footer-school {
                color: rgba(31, 48, 74, 0.66);
            }

            .footer-credit {
                color: rgba(12, 23, 40, 0.78);
            }

            .footer-motto {
                color: rgba(31, 48, 74, 0.48);
            }

            .orbital-frame {
                border-color: rgba(0, 91, 172, 0.16);
                box-shadow:
                    inset 0 0 70px rgba(0, 119, 200, 0.05),
                    0 0 110px rgba(0, 91, 172, 0.08);
            }

            .data-ribbon {
                background: linear-gradient(90deg, transparent, rgba(0, 119, 200, 0.4), rgba(98, 82, 216, 0.28), transparent);
                box-shadow: 0 0 38px rgba(0, 91, 172, 0.18);
            }

            .signal-node,
            .mesh-chip,
            .topbar,
            .endpoint-card,
            .manual-card,
            .manual-code-slot,
            .percent-card,
            .personality-layout,
            .trait-panel,
            .trait-summary,
            .manual-trait-item,
            .score-card,
            .axis-guide-card,
            .type-detail-card {
                background:
                    linear-gradient(145deg, rgba(255,255,255,0.82), rgba(255,255,255,0.44)) !important;
                border-color: rgba(20, 45, 82, 0.12) !important;
                box-shadow: 0 24px 70px rgba(24, 54, 92, 0.13) !important;
            }

            .topbar {
                color: rgba(12, 23, 40, 0.84);
            }

            .progress-text {
                color: rgba(31, 48, 74, 0.58);
            }

            .endpoint-card.right,
            .manual-card.active,
            .axis-guide-card.active,
            .type-detail-card.active {
                background:
                    radial-gradient(circle at 96% 0%, rgba(98, 82, 216, 0.12), transparent 42%),
                    linear-gradient(145deg, rgba(255,255,255,0.86), rgba(255,255,255,0.46)) !important;
            }

            .brand-text span {
                color: rgba(31, 48, 74, 0.52) !important;
            }

            .brand-dot,
            .choice-card.selected .choice-code,
            .axis-guide-card.active .axis-guide-code {
                color: #ffffff !important;
                background: linear-gradient(135deg, #005bac, #0077c8) !important;
            }

            .progress-track,
            .score-track {
                background: rgba(20, 45, 82, 0.09);
                box-shadow: inset 0 0 0 1px rgba(20, 45, 82, 0.06);
            }

            .choice-card,
            .endpoint-card,
            .manual-card,
            .manual-code-slot,
            .percent-card,
            .personality-layout,
            .trait-panel,
            .trait-summary,
            .manual-trait-item,
            .score-card,
            .axis-guide-card,
            .type-detail-card {
                backdrop-filter: blur(18px) saturate(1.08);
                -webkit-backdrop-filter: blur(18px) saturate(1.08);
            }

            .personality-number {
                background: rgba(255,255,255,0.7);
            }

            .story-copy {
                color: rgba(31, 48, 74, 0.76);
            }

            .choice-code,
            .endpoint-code,
            .axis-guide-code {
                background: rgba(0, 91, 172, 0.08);
                color: var(--ink);
            }

            .choice-card.selected {
                border-color: rgba(0, 91, 172, 0.22);
                box-shadow: 0 24px 60px rgba(0, 91, 172, 0.16);
                background:
                    radial-gradient(circle at top right, rgba(0,119,200,0.12), transparent 38%),
                    rgba(255,255,255,0.88);
            }

            .manual-code-slot.filled {
                color: #ffffff !important;
                background:
                    radial-gradient(circle at 18% 18%, rgba(255,255,255,0.28), transparent 32%),
                    linear-gradient(135deg, #005bac, #0077c8, #6252d8) !important;
                border-color: rgba(0, 91, 172, 0.2) !important;
            }

            .likert-selected {
                background: rgba(0, 91, 172, 0.08);
                border-color: rgba(0, 91, 172, 0.14);
                color: #005bac;
            }

            .stButton > button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]),
            .stButton > button[kind="secondary"],
            .stButton > button[data-testid="stBaseButton-secondary"] {
                border-color: rgba(20, 45, 82, 0.14) !important;
                background:
                    radial-gradient(circle at 18% 12%, rgba(255,255,255,0.9), transparent 34%),
                    linear-gradient(145deg, rgba(255,255,255,0.76), rgba(255,255,255,0.38)) !important;
                color: #0c1728 !important;
                text-shadow: none !important;
                box-shadow:
                    0 18px 46px rgba(24, 54, 92, 0.12),
                    inset 0 1px 0 rgba(255,255,255,0.65) !important;
            }

            .stButton > button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]):hover,
            .stButton > button[kind="secondary"]:hover,
            .stButton > button[data-testid="stBaseButton-secondary"]:hover {
                border-color: rgba(0, 91, 172, 0.28) !important;
                background:
                    radial-gradient(circle at 18% 12%, rgba(255,255,255,0.96), transparent 34%),
                    linear-gradient(145deg, rgba(230,244,255,0.86), rgba(255,255,255,0.5)) !important;
                color: #005bac !important;
            }

            .stButton > button[kind="primary"],
            .stButton > button[data-testid="stBaseButton-primary"] {
                color: #ffffff !important;
                background:
                    radial-gradient(circle at 22% 18%, rgba(255,255,255,0.32), transparent 30%),
                    linear-gradient(135deg, #005bac 0%, #0077c8 54%, #6252d8 100%) !important;
                box-shadow: 0 22px 58px rgba(0, 91, 172, 0.24), inset 0 1px 0 rgba(255,255,255,0.28) !important;
            }

            .stButton > button:disabled,
            .stButton > button[disabled] {
                border-color: rgba(20, 45, 82, 0.08) !important;
                background: rgba(20, 45, 82, 0.045) !important;
                color: rgba(31, 48, 74, 0.34) !important;
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
            <div class="home-visual" aria-hidden="true">
                <div class="orbital-frame"></div>
                <div class="orbital-frame secondary"></div>
                <div class="data-ribbon"></div>
                <div class="data-ribbon alt"></div>
                <div class="signal-node node-a"></div>
                <div class="signal-node node-b"></div>
                <div class="signal-node node-c"></div>
                <div class="signal-node node-d"></div>
                <div class="mesh-chip chip-left"></div>
                <div class="mesh-chip chip-right"></div>
            </div>
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
    render_html('<div class="home-motto">수학으로 세상을 읽고, 교육으로 내일을 잇다.</div>')
    st.markdown('<div class="start-zone">', unsafe_allow_html=True)
    left_col, right_col = st.columns(2, gap="small")
    with left_col:
        if st.button("결과 입력하기", use_container_width=True, type="primary"):
            st.session_state.screen = "input"
            reset_manual_state()
            rerun()
    with right_col:
        if st.button("테스트 하기", use_container_width=True, type="primary"):
            st.session_state.screen = "quiz"
            reset_quiz_state()
            rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def render_footer() -> None:
    signature_uri = logo_data_uri("inu_signature")
    slogan_uri = logo_data_uri("inu_slogan")
    slogan_markup = (
        f'<img class="footer-corner-logo slogan" src="{slogan_uri}" alt="인천대학교 슬로건">'
        if slogan_uri
        else ""
    )
    signature_markup = (
        f'<img class="footer-corner-logo signature" src="{signature_uri}" alt="인천대학교 로고">'
        if signature_uri
        else ""
    )

    footer_markup = f"""
        <footer class="app-footer">
            <div class="footer-logo-slot left">{signature_markup}</div>
            <div class="footer-center">
                <div class="footer-credit">Designed and developed by Mingyu Kim</div>
                <div class="footer-school">인천대학교 수학교육과</div>
            </div>
            <div class="footer-logo-slot right">{slogan_markup}</div>
        </footer>
        """
    clean_markup = "\n".join(line.strip() for line in footer_markup.strip().splitlines())
    st.markdown(clean_markup, unsafe_allow_html=True)


def render_topbar(progress_label=None) -> None:
    answered = answered_count()
    if progress_label is None:
        progress_label = f"{answered}/{TOTAL_QUESTIONS}"
    st.markdown(
        f"""
        <div class="topbar">
            <div class="brand-mark">
                <div class="brand-dot">M</div>
                <div class="brand-text">{APP_TITLE} <span style="color:rgba(223,232,246,0.52);">{APP_SUBTITLE}</span></div>
            </div>
            <div class="progress-text">{escape(str(progress_label))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def answered_count() -> int:
    return sum(1 for question in QUESTIONS if question["id"] in st.session_state.answers)


def logo_data_uri(filename: str) -> str:
    requested = Path(filename)
    candidate_names = [requested.name]
    if requested.suffix == "":
        candidate_names = [
            f"{requested.name}.svg",
            f"{requested.name}.png",
            f"{requested.name}.jpg",
            f"{requested.name}.jpeg",
        ]

    search_dirs = [
        LOGO_DIR,
        FIGURE_DIR,
        Path.cwd() / "assets" / "logos",
        Path.cwd() / "assets" / "figures",
    ]
    candidate_paths = [directory / name for directory in search_dirs for name in candidate_names]
    logo_path = next((path for path in candidate_paths if path.exists()), None)
    if logo_path is None:
        return ""

    mime_by_suffix = {
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }
    mime = mime_by_suffix.get(logo_path.suffix.lower(), "image/svg+xml")
    encoded = base64.b64encode(logo_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def render_manual_slots() -> None:
    slots = []
    for letter in manual_letters():
        class_name = "manual-code-slot filled" if letter else "manual-code-slot"
        slots.append(f'<div class="{class_name}">{escape(letter or "·")}</div>')

    st.markdown(
        f"""
        <div class="manual-code-row">
            {''.join(slots)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_manual_axis_card(index: int, left: str, right: str) -> None:
    selected = st.session_state.manual_letters.get(pair_key(left, right), "")
    active_class = " active" if selected else ""
    status = f"{selected} 선택됨" if selected else "선택 대기"
    left_meta = AXIS_META[left]
    right_meta = AXIS_META[right]
    st.markdown(
        f"""
        <div class="manual-card{active_class}">
            <div class="manual-card-kicker">{index:02d} · {escape(status)}</div>
            <div class="manual-card-title">
                {escape(left_meta["label"])} / {escape(right_meta["label"])}
            </div>
            <div class="manual-option">
                <span class="manual-option-code">{escape(left)}</span>
                <span class="manual-option-name">{escape(left_meta["name"])}</span>
                <div class="manual-option-desc">{escape(left_meta["description"])}</div>
            </div>
            <div class="manual-option">
                <span class="manual-option-code">{escape(right)}</span>
                <span class="manual-option-name">{escape(right_meta["name"])}</span>
                <div class="manual-option-desc">{escape(right_meta["description"])}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def select_manual_letter(left: str, right: str, letter: str) -> None:
    st.session_state.manual_letters[pair_key(left, right)] = letter
    if manual_input_complete():
        st.session_state.screen = "input_result"
    rerun()


def render_manual_input() -> None:
    progress_count = manual_answered_count()
    progress = progress_count / len(TYPE_AXIS_PAIRS) * 100

    st.markdown('<main class="experience-shell">', unsafe_allow_html=True)
    render_topbar(f"입력 {progress_count}/{len(TYPE_AXIS_PAIRS)}")
    st.markdown(
        f"""
        <section class="manual-stage">
            {progress_bar_markup(progress, "manual_progress_previous")}
            <h1 class="manual-title">결과 입력하기</h1>
            <p class="manual-copy">
                네 개의 축에서 알파벳을 하나씩 선택하면 결과 코드가 완성됩니다.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    render_manual_slots()
    st.markdown('<div class="manual-card-spacer"></div>', unsafe_allow_html=True)

    columns = st.columns(len(TYPE_AXIS_PAIRS), gap="small")
    for index, (column, (left, right)) in enumerate(zip(columns, TYPE_AXIS_PAIRS), start=1):
        selected = st.session_state.manual_letters.get(pair_key(left, right), "")
        with column:
            render_manual_axis_card(index, left, right)
            left_col, right_col = st.columns(2, gap="small")
            with left_col:
                if st.button(
                    left,
                    key=f"manual_{left}{right}_{left}",
                    use_container_width=True,
                    type="primary" if selected == left else "secondary",
                    help=f'{AXIS_META[left]["name"]} · {AXIS_META[left]["label"]}',
                ):
                    select_manual_letter(left, right, left)
            with right_col:
                if st.button(
                    right,
                    key=f"manual_{left}{right}_{right}",
                    use_container_width=True,
                    type="primary" if selected == right else "secondary",
                    help=f'{AXIS_META[right]["name"]} · {AXIS_META[right]["label"]}',
                ):
                    select_manual_letter(left, right, right)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("선택 초기화", use_container_width=True):
            reset_manual_state()
            rerun()
    with col2:
        if st.button("테스트 하기", use_container_width=True):
            st.session_state.screen = "quiz"
            reset_quiz_state()
            rerun()
    with col3:
        if st.button("홈으로", use_container_width=True):
            st.session_state.screen = "home"
            reset_manual_state()
            rerun()

    st.markdown("</main>", unsafe_allow_html=True)


def render_manual_result() -> None:
    if not manual_input_complete():
        st.session_state.screen = "input"
        rerun()

    type_code = manual_type_code()
    result = TYPE_DATA[type_code]

    render_topbar("입력 완료")
    render_html(
        f"""
        <section class="result-hero">
            <h1 class="result-title">입력한 수학 MBTI는 {escape(type_code)}</h1>
            <p class="result-copy">
                <span>{escape(result["person"])}처럼 수학을 바라보는 경향이 있습니다.</span>
                <span>아래 카드는 앞면과 뒷면으로 결과를 보여줍니다.</span>
            </p>
        </section>
        """,
    )
    render_flip_card(type_code, result)
    render_manual_trait_profile(type_code)
    render_axis_guide(type_code)
    render_type_descriptions(type_code)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("다시 입력하기", use_container_width=True):
            st.session_state.screen = "input"
            reset_manual_state()
            rerun()
    with col2:
        if st.button("테스트 하기", use_container_width=True):
            st.session_state.screen = "quiz"
            reset_quiz_state()
            rerun()
    with col3:
        if st.button("홈으로", use_container_width=True):
            st.session_state.screen = "home"
            reset_manual_state()
            rerun()

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
    st.markdown('<main class="experience-shell quiz-shell">', unsafe_allow_html=True)
    render_topbar()

    index = st.session_state.current_question
    question = QUESTIONS[index]
    progress = (index + 1) / TOTAL_QUESTIONS * 100
    st.markdown(
        f"""
        <section class="question-stage">
            {progress_bar_markup(progress, "quiz_progress_previous")}
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
    code = ""
    for left, right in TYPE_AXIS_PAIRS:
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


def image_data_uri(type_code: str) -> str:
    image_file = TYPE_IMAGE_FILES.get(type_code)
    if not image_file:
        return ""

    candidate_paths = [
        FIGURE_DIR / image_file,
        Path.cwd() / "assets" / "figures" / image_file,
    ]
    image_path = next((path for path in candidate_paths if path.exists()), None)
    if image_path is None:
        return ""

    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def render_result_portrait(type_code: str, result: dict) -> str:
    data_uri = image_data_uri(type_code)
    if data_uri:
        return (
            f'<img class="portrait-image" src="{data_uri}" '
            f'alt="{escape(result["person"])} 결과 이미지">'
        )
    missing_file = TYPE_IMAGE_FILES.get(type_code, "unknown.png")
    return (
        '<div class="portrait-missing">'
        '<strong>이미지 파일을 찾을 수 없습니다.</strong>'
        f'<span>assets/figures/{escape(missing_file)}</span>'
        '</div>'
    )


def render_flip_card(type_code: str, result: dict) -> None:
    front_title = f"{type_code} [{result['pronunciation']}]"
    portrait_markup = render_result_portrait(type_code, result)
    portrait_accent = PORTRAIT_DATA.get(type_code, {}).get("accent", "#4f8cff")
    accent_hex = portrait_accent.lstrip("#")
    try:
        accent_rgb = tuple(int(accent_hex[index:index + 2], 16) for index in (0, 2, 4))
    except ValueError:
        accent_rgb = (79, 140, 255)
    portrait_accent_soft = f"rgba({accent_rgb[0]}, {accent_rgb[1]}, {accent_rgb[2]}, 0.22)"
    light_card_css = """
        @media (prefers-color-scheme: light) {
            :root {
                color-scheme: light;
            }
            .side {
                border-color: rgba(20, 45, 82, 0.12);
                box-shadow: 0 34px 94px rgba(24, 54, 92, 0.18);
            }
            .front {
                color: var(--front-ink);
                background: var(--front-bg);
            }
            .back {
                color: #f6fbff;
                background:
                    radial-gradient(circle at 22% 15%, rgba(0, 119, 200, 0.32), transparent 32%),
                    radial-gradient(circle at 80% 88%, rgba(98, 82, 216, 0.24), transparent 34%),
                    linear-gradient(145deg, #0c1728, #173457 52%, #005bac);
            }
            .kicker {
                color: var(--front-muted);
            }
            .type {
                color: var(--front-ink);
            }
            .person {
                color: var(--front-muted-strong);
            }
            .quote {
                color: var(--front-ink);
                text-shadow:
                    0 1px 0 rgba(255,255,255,0.62),
                    0 14px 34px rgba(68, 92, 132, 0.18);
            }
        }
    """
    card_html = f"""
    <!doctype html>
    <html lang="ko">
    <head>
    <meta charset="utf-8">
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap");

        :root {{
            color-scheme: dark;
            --card-accent: {portrait_accent};
            --front-ink: #091528;
            --front-muted: rgba(48, 63, 86, 0.62);
            --front-muted-strong: rgba(48, 63, 86, 0.78);
            --front-bg-top: #f8fbff;
            --front-bg-mid: #e9f3ff;
            --front-bg-bottom: #d7e8ff;
            --portrait-edge: rgba(220, 234, 255, 0.96);
            --front-bg:
                radial-gradient(circle at 20% 10%, rgba(255,255,255,0.96), transparent 28%),
                radial-gradient(circle at 82% 2%, {portrait_accent_soft}, transparent 34%),
                linear-gradient(150deg, var(--front-bg-top) 0%, var(--front-bg-mid) 48%, var(--front-bg-bottom) 100%);
        }}

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
            outline: 4px solid rgba(110, 231, 255, 0.34);
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
            border: 1px solid rgba(255, 255, 255, 0.13);
            box-shadow: 0 34px 100px rgba(0, 0, 0, 0.42);
        }}
        .front {{
            padding: 2rem;
            color: var(--front-ink);
            background: var(--front-bg);
        }}
        .portrait-wrap {{
            position: absolute;
            left: 50%;
            top: 53%;
            z-index: 1;
            width: min(342px, 82vw);
            height: 386px;
            transform: translate(-50%, -50%);
            display: grid;
            place-items: center;
            pointer-events: none;
            overflow: hidden;
            border-radius: 30px;
            border: 0;
            background:
                radial-gradient(circle at 50% 42%, rgba(255,255,255,0.34), transparent 42%),
                linear-gradient(160deg, var(--front-bg-mid), var(--front-bg-bottom));
            box-shadow:
                0 24px 58px rgba(72, 104, 158, 0.16),
                inset 0 0 38px rgba(255,255,255,0.48);
            isolation: isolate;
        }}
        .portrait-wrap::after {{
            content: "";
            position: absolute;
            inset: -2px;
            z-index: 2;
            pointer-events: none;
            border-radius: 32px;
            box-shadow:
                inset 0 0 36px 32px var(--portrait-edge),
                inset 0 -34px 46px 14px var(--front-bg-bottom),
                inset 0 28px 42px 8px rgba(248,251,255,0.74);
        }}
        .portrait-image,
        .portrait-svg {{
            width: 100%;
            height: 100%;
            display: block;
        }}
        .portrait-image {{
            object-fit: cover;
            object-position: center top;
            border-radius: 30px;
            filter: saturate(1.02) contrast(1.01);
        }}
        .portrait-missing {{
            width: 100%;
            height: 100%;
            display: grid;
            place-items: center;
            gap: 0.4rem;
            padding: 1.2rem;
            text-align: center;
            color: #f6fbff;
            background: rgba(239, 68, 68, 0.22);
            font-family: "Noto Sans KR", sans-serif;
            line-height: 1.45;
        }}
        .portrait-missing strong,
        .portrait-missing span {{
            display: block;
        }}
        .portrait-missing span {{
            color: rgba(255,255,255,0.72);
            font-size: 0.88rem;
            word-break: break-all;
        }}
        .back {{
            padding: 1.7rem;
            transform: rotateY(180deg);
            color: #f6fbff;
            background:
                radial-gradient(circle at 22% 15%, rgba(110, 231, 255, 0.24), transparent 32%),
                radial-gradient(circle at 80% 88%, rgba(167, 139, 250, 0.22), transparent 34%),
                linear-gradient(145deg, #070b16, #111a2e 52%, #18243a);
        }}
        .kicker {{
            position: relative;
            z-index: 2;
            color: var(--front-muted);
            font-size: 0.92rem;
            font-weight: 760;
        }}
        .type {{
            position: relative;
            z-index: 2;
            margin-top: 0.35rem;
            color: var(--front-ink);
            font-size: 2.35rem;
            line-height: 1;
            font-weight: 860;
        }}
        .person {{
            position: relative;
            z-index: 2;
            color: var(--front-muted-strong);
            font-size: 1.18rem;
            font-weight: 720;
            margin-top: 0.6rem;
        }}
        .quote {{
            position: relative;
            z-index: 3;
            margin-top: auto;
            padding-top: 16rem;
            color: var(--front-ink);
            font-size: clamp(1.24rem, 4.5vw, 1.48rem);
            line-height: 1.28;
            font-weight: 820;
            text-shadow:
                0 1px 0 rgba(255,255,255,0.62),
                0 14px 34px rgba(68, 92, 132, 0.18);
            word-break: keep-all;
            overflow-wrap: normal;
            text-wrap: balance;
            line-break: strict;
        }}
        .back-title {{
            font-size: 1.82rem;
            line-height: 1.08;
            font-weight: 840;
        }}
        .back-code {{
            color: rgba(255,255,255,0.64);
            font-size: 0.95rem;
            font-weight: 720;
            margin-bottom: 0.58rem;
        }}
        .info-block {{
            padding: 0.95rem;
            border-radius: 18px;
            background: rgba(255,255,255,0.075);
            border: 1px solid rgba(255,255,255,0.12);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            margin-top: 0.72rem;
        }}
        .info-label {{
            color: rgba(255,255,255,0.62);
            font-size: 0.82rem;
            font-weight: 760;
            margin-bottom: 0.36rem;
        }}
        .info-text {{
            color: rgba(255,255,255,0.94);
            font-size: 0.92rem;
            line-height: 1.46;
            font-weight: 560;
            word-break: keep-all;
            line-break: strict;
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
        {light_card_css}
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
                    <div class="portrait-wrap">{portrait_markup}</div>
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
    cards = []
    for left, right in TYPE_AXIS_PAIRS:
        left_score = scores[left]
        right_score = scores[right]
        winner = left if left_score >= right_score else right
        width = max(left_score, right_score) / 6 * 100
        cards.append(
            f"""
            <div class="score-card">
                <div class="score-label">
                    <span>{escape(left)}/{escape(right)}</span>
                    <span>{escape(winner)} {escape(AXIS_META[winner]["label"])}</span>
                </div>
                <div class="score-track">
                    <div class="score-fill" style="width:{width:.0f}%;"></div>
                </div>
            </div>
            """
        )

    render_html(
        f"""
        <div class="score-grid">
            {''.join(cards)}
        </div>
        """,
    )


def percentage_pair(scores: dict, left: str, right: str) -> tuple:
    left_score = scores[left]
    right_score = scores[right]
    total = left_score + right_score
    if total == 0:
        return 50.0, 50.0
    return left_score / total * 100, right_score / total * 100


def render_percentage_bars(scores: dict, type_code: str) -> None:
    axis_colors = ["#3fa0bb", "#e5ad29", "#36a873", "#8b63a6"]
    rows = []
    for index, (left, right) in enumerate(TYPE_AXIS_PAIRS):
        left_percent, right_percent = percentage_pair(scores, left, right)
        winner = type_code[index] if index < len(type_code) else left
        winner_percent = left_percent if winner == left else right_percent
        knob_left = right_percent
        color = axis_colors[index % len(axis_colors)]
        pair_title = f"{left}/{right}"
        rows.append(
            f"""
            <div class="trait-row" style="--axis-color:{color}; --knob-left:{knob_left:.1f}%;">
                <div class="trait-value">{winner_percent:.0f}% <strong>{escape(AXIS_META[winner]["label"])}</strong></div>
                <div class="trait-track" aria-label="{escape(pair_title)} 결과">
                    <div class="trait-knob"></div>
                </div>
                <div class="trait-labels">
                    <span>{escape(left)} · {escape(AXIS_META[left]["label"])}</span>
                    <span>{escape(right)} · {escape(AXIS_META[right]["label"])}</span>
                </div>
            </div>
            """
        )

    result = TYPE_DATA[type_code]
    data_uri = image_data_uri(type_code)
    image_markup = (
        f'<img class="trait-summary-image" src="{data_uri}" alt="{escape(result["person"])} 결과 이미지">'
        if data_uri
        else ""
    )
    render_html(
        f"""
        <section class="personality-section">
            <div class="personality-heading">
                <div class="personality-number">1</div>
                <h2 class="personality-title">성격 특성</h2>
            </div>
            <div class="personality-layout">
                <div class="trait-panel">
                    {''.join(rows)}
                </div>
                <aside class="trait-summary">
                    {image_markup}
                    <div class="trait-summary-kicker">당신의 성격 유형:</div>
                    <div class="trait-summary-title">{escape(result["person"])}</div>
                    <div class="trait-summary-code">{escape(type_code)} [{escape(result["pronunciation"])}]</div>
                    <div class="trait-summary-desc">{escape(result["description"])}</div>
                </aside>
            </div>
            <div class="story-copy">
                <p>{escape(result["description"])}</p>
                <p>{escape(result["tendency"])} 성향이 두드러지며, {escape(result["person"])}의 대표 업적인 {escape(result["achievement"])}처럼 수학적 사고를 자신만의 방식으로 펼쳐 나갈 수 있습니다.</p>
            </div>
        </section>
        """,
    )


def render_manual_trait_profile(type_code: str) -> None:
    result = TYPE_DATA[type_code]
    data_uri = image_data_uri(type_code)
    image_markup = (
        f'<img class="trait-summary-image" src="{data_uri}" alt="{escape(result["person"])} 결과 이미지">'
        if data_uri
        else ""
    )
    trait_items = []
    for letter in type_code:
        meta = AXIS_META[letter]
        trait_items.append(
            f"""
            <div class="manual-trait-item">
                <div class="manual-trait-name"><span>{escape(letter)}</span> {escape(meta["label"])} · {escape(meta["name"])}</div>
                <div class="manual-trait-desc">{escape(meta["description"])}</div>
            </div>
            """
        )

    render_html(
        f"""
        <section class="personality-section">
            <div class="personality-heading">
                <div class="personality-number">1</div>
                <h2 class="personality-title">성격 특성</h2>
            </div>
            <div class="personality-layout">
                <div class="trait-panel manual-trait-list">
                    {''.join(trait_items)}
                </div>
                <aside class="trait-summary">
                    {image_markup}
                    <div class="trait-summary-kicker">당신의 성격 유형:</div>
                    <div class="trait-summary-title">{escape(result["person"])}</div>
                    <div class="trait-summary-code">{escape(type_code)} [{escape(result["pronunciation"])}]</div>
                    <div class="trait-summary-desc">{escape(result["description"])}</div>
                </aside>
            </div>
            <div class="story-copy">
                <p>{escape(result["description"])}</p>
                <p>{escape(result["tendency"])} 성향이 조합된 유형입니다. 대표적으로 {escape(result["person"])}의 {escape(result["achievement"])}처럼, 자신에게 맞는 방식으로 수학적 사고를 발전시킬 수 있습니다.</p>
            </div>
        </section>
        """
    )


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

    render_html(
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
    )


def render_type_descriptions(type_code: str) -> None:
    cards = []
    sorted_types = sorted(TYPE_DATA.items(), key=lambda item: item[1]["number"])
    for code, data in sorted_types:
        active_class = " active" if code == type_code else ""
        badge = "내 결과" if code == type_code else f'Card {data["number"]:02d}'
        title = f"{code} [{data['pronunciation']}]"
        cards.append(
            f"""
            <div class="type-detail-card{active_class}">
                <div class="type-detail-top">
                    <div class="type-detail-code">{escape(title)}</div>
                    <div class="type-detail-badge">{escape(badge)}</div>
                </div>
                <div class="type-detail-person">{escape(data["person"])}</div>
                <div class="type-detail-desc">{escape(data["description"])}</div>
                <div class="type-detail-meta">
                    <div class="type-detail-meta-item"><strong>성향</strong> {escape(data["tendency"])}</div>
                    <div class="type-detail-meta-item"><strong>대표 업적</strong> {escape(data["achievement"])}</div>
                </div>
            </div>
            """
        )

    render_html(
        f"""
        <section class="type-detail-section">
            <h2 class="type-detail-title">16가지 수학 MBTI 유형</h2>
            <p class="type-detail-copy">
                네 개의 알파벳 조합에 따라 결과 유형이 달라집니다.
                현재 결과는 강조 표시되어 있습니다.
            </p>
            <div class="type-detail-grid">
                {''.join(cards)}
            </div>
        </section>
        """,
    )


def render_result() -> None:
    if answered_count() < TOTAL_QUESTIONS:
        st.session_state.screen = "quiz"
        rerun()

    scores = calculate_scores()
    type_code = calculate_type_code(scores)
    result = TYPE_DATA[type_code]

    render_topbar()
    render_html(
        f"""
        <section class="result-hero">
            <h1 class="result-title">당신의 수학 MBTI는 {escape(type_code)}</h1>
            <p class="result-copy">
                <span>{escape(result["person"])}처럼 수학을 바라보는 경향이 있습니다.</span>
                <span>아래 카드는 앞면과 뒷면으로 결과를 보여줍니다.</span>
            </p>
        </section>
        """,
    )
    render_flip_card(type_code, result)
    render_percentage_bars(scores, type_code)
    render_axis_guide(type_code)
    render_type_descriptions(type_code)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("다시 검사하기", use_container_width=True):
            st.session_state.screen = "quiz"
            reset_quiz_state()
            rerun()
    with col2:
        if st.button("홈으로", use_container_width=True):
            st.session_state.screen = "home"
            reset_quiz_state()
            rerun()

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
    elif st.session_state.screen == "input":
        render_manual_input()
    elif st.session_state.screen == "input_result":
        render_manual_result()
    elif st.session_state.screen == "quiz":
        render_quiz()
    else:
        render_result()
    render_footer()


if __name__ == "__main__":
    main()
