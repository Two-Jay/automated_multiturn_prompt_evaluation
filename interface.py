import streamlit as st
from classes import TempData
from controller import Controller
import json

config = json.load(open("config.json", "r"))

default_prompt = "You are a helpful assistant."
fixed_user_query = "9.9와 9.11 중에서 더 큰 숫자는 무엇인가요?"
whole_interface_height = 800

def input_page():
  st.write("테스트 설정")
  col1, col2 = st.columns(2)
  with col1:
    prompt = st.text_area("시스템 프롬프트", value=default_prompt, height=whole_interface_height - 200)
    user_query = st.text_area("유저 쿼리", value=fixed_user_query, height=whole_interface_height - 750, disabled=True)
    st.write(config)
  with col2:
    output_container = st.container(height=whole_interface_height)
    with output_container:
      st.write("싱글 테스트 결과")
      single_test_result_element = st.empty()
      single_test_token_usage_element = st.empty()
    run_single_test_button = st.button("싱글 테스트 실행")
    run_multiple_test_button = st.button("멀티플 테스트 실행")
    run_count = st.number_input("실행 횟수", min_value=2, max_value=50, value=2)
    
  return TempData({
    "prompt": prompt if prompt != "" else "",
    "config": config,
    "single_test_button": run_single_test_button,
    "multiple_test_button": run_multiple_test_button,
    "single_test_result_element": single_test_result_element,
    "single_test_token_usage_element": single_test_token_usage_element,
    "run_count": run_count
  })

control = Controller()

def result_page(data):
  st.write("테스트 결과")
  if data.key_check("multiple_test_results"):
    col1, col2 = st.columns([0.8, 0.2])
    
    with col1:
      result_list = data.get("multiple_test_results")
      if result_list:
        st.write(result_list)
    with col2:
      st.write("단건 최대 사용 토큰")
      st.write(f"{data.get("longest_token_count")} 토큰")

def render():
  st.title("Interface")
  tab1, tab2 = st.tabs(["테스트 설정", "테스트 결과"])
  with tab1:
    data = input_page()
    if data.get("prompt") != "":
      control.set_parameters(config, data.get("prompt"))
      control.control(data)

  with tab2:
    result_page(data)

class Interface:
  def __init__(self):
    self.name = "Interface"
    st.set_page_config(layout="wide")

  def run(self):
    data = render()