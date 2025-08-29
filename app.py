import streamlit as st
import math

# =============================
# 함수 정의
# =============================

# 시별 인구 수 (명)
city_population = {
    "서울": 9765000,
    "부산": 3400000,
    "대구": 2500000,
    "인천": 3000000,
    "광주": 1500000,
    "대전": 1500000,
    "울산": 1200000,
    "세종": 350000,
    "경기": 13000000,
    "강원": 1600000,
    "충북": 1600000,
    "충남": 2200000,
    "전북": 1800000,
    "전남": 1900000,
    "경북": 2600000,
    "경남": 3300000,
    "제주": 700000
}

# 1cm² 당 기공 밀도
stomatal_density = {
    "단풍잎": 72111.6,
    "테이블야자": 23041.5,
    "깻잎": 29387.2,
    "고무나무": 42760.7,
    "몬스테라": 12694.6,
    "스투키": 8675.1
}

# 면적 단위 변환 계수
unit_conversion_area = {
    "cm²": 1,
    "mm²": 0.01,
    "m²": 10000
}

# CO₂ 흡수량 단위 변환 계수
unit_conversion_co2 = {
    "µg": 1,
    "mg": 1e-3,
    "g": 1e-6,
    "kg": 1e-9
}

# 기공 1개당 하루 CO₂ 흡수량(µg)
co2_per_stomata_per_day = 0.05

# 대한민국 전체 1년 CO₂ 배출량 (kg)
total_country_co2_kg = 600_000_000_000  # 6억 톤

def calculate_stomata_airpurification_for_city(
    leaf_type, width, height, num_leaves, area_unit="cm²", co2_unit="µg", city="서울"
):
    try:
        width = float(width)
        height = float(height)
        num_leaves = int(num_leaves)
    except:
        return "숫자를 올바르게 입력해주세요."
    
    density = stomatal_density.get(leaf_type)
    if density is None:
        return "알 수 없는 잎 종류입니다."
    
    area_cm2 = width * height
    total_area_cm2 = area_cm2 * num_leaves
    total_stomata = total_area_cm2 * density
    co2_absorbed = total_stomata * co2_per_stomata_per_day  # µg/day
    
    # 스투키는 계산값 4배
    if leaf_type == "스투키":
        total_stomata *= 4
        co2_absorbed *= 4
    
    # 단위 변환
    area_converted = total_area_cm2 / unit_conversion_area.get(area_unit, 1)
    co2_absorbed_converted = co2_absorbed * unit_conversion_co2.get(co2_unit, 1)
    
    # 도시 하루 CO₂ 배출량 계산
    city_pop = city_population.get(city)
    if city_pop is None:
        return "알 수 없는 도시입니다."
    
    total_pop = sum(city_population.values())
    city_co2_per_day_kg = (total_country_co2_kg / total_pop) * city_pop  # kg/day
    city_co2_per_day_µg = city_co2_per_day_kg * 1e9  # µg/day
    
    # 필요한 잎 수 계산
    leaves_needed = math.ceil(city_co2_per_day_µg / co2_absorbed) if co2_absorbed > 0 else "계산 불가"
    
    # 결과 한국어화 + 단위 포함
    result = {
        "잎 종류": leaf_type,
        "잎 크기": f"{width} x {height} cm",
        "입력한 잎 개수": f"{num_leaves} 장",
        "총 면적": f"{area_converted:.2f} {area_unit}",
        "총 기공 수": f"{int(total_stomata):,} 개",
        "예상 CO₂ 흡수량": f"{co2_absorbed_converted:,.4f} {co2_unit}/일",
        "도시": city,
        "도시 하루 CO₂ 배출량": f"{city_co2_per_day_kg:,.2f} kg/일",
        "도시 CO₂ 흡수 위해 필요한 잎 수": f"{leaves_needed} 장"
    }
    
    return result

# =============================
# Streamlit UI
# =============================

st.title("🏙️ 도시 하루 CO₂ 배출량 기준 잎 필요 계산기")

st.markdown("입력한 잎 개수와 크기로, 선택한 도시의 하루 CO₂ 배출량을 흡수하려면 몇 장의 잎이 필요한지 계산합니다.")

# 사용자 입력
leaf_type = st.selectbox("잎 종류 선택", list(stomatal_density.keys()))
width = st.text_input("잎 가로 길이 (cm)", value="1")
height = st.text_input("잎 세로 길이 (cm)", value="1")
num_leaves = st.number_input("잎 개수", min_value=1, value=1, step=1)
area_unit = st.selectbox("면적 단위 선택", list(unit_conversion_area.keys()), index=0)
co2_unit = st.selectbox("CO₂ 흡수 단위 선택", list(unit_conversion_co2.keys()), index=0)
city = st.selectbox("도시 선택", list(city_population.keys()), index=0)

if st.button("계산하기"):
    result = calculate_stomata_airpurification_for_city(
        leaf_type, width, height, num_leaves, area_unit, co2_unit, city
    )
    
    st.subheader("계산 결과")
    for key, value in result.items():
        st.write(f"{key}: {value}")
