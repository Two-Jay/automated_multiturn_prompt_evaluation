from openai import OpenAI

fixed_user_query = "9.9와 9.11 중에서 더 큰 숫자는 무엇인가요?"

class Caller:
  def __init__(self, config, system_prompt):
    self.client = OpenAI()
    self.config = config
    self.system_prompt = system_prompt

  def call(self):
    res = self.client.chat.completions.create(
      model=self.config["model_name"],
      messages=[
        {"role": "system", "content": self.system_prompt},
        {"role": "user", "content": fixed_user_query}
      ],
      temperature=self.config["temperature"],
      max_tokens=self.config["max_tokens"],
      top_p=self.config["top_p"],
      frequency_penalty=self.config["frequency_penalty"],
      presence_penalty=self.config["presence_penalty"],
    )
    return res.choices[0].message.content

import tiktoken

def calculate_token_usage(prompt : str, response : str):
  encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
  num_tokens = len(encoding.encode(prompt)) + len(encoding.encode(response))
  return num_tokens

class Controller:
  def __init__(self):
    self.client = OpenAI()

  def set_parameters(self, config, system_prompt):
    self.config = config
    self.system_prompt = system_prompt

  def control(self, data):
    caller = Caller(self.config, data.get("prompt"))
    if data.get("single_test_button"):
      res = caller.call()
      token_usage = calculate_token_usage(data.get("prompt"), res)
      data.get("single_test_result_element").write(res)
      data.get("single_test_token_usage_element").write(f"토큰 사용량: {token_usage} 토큰")

    elif data.get("multiple_test_button"):
      run_count = data.get("run_count")
      result_list, longest_token_count = self.run_multiple_test(caller, run_count)
      data.set("multiple_test_results", result_list)
      data.set("longest_token_count", longest_token_count)

  def run_multiple_test(self, caller, run_count):
    result_list = []
    longest_token_count = 0
    for i in range(run_count):
      res = caller.call()
      token_usage = calculate_token_usage(caller.system_prompt, res)
      if token_usage > longest_token_count:
        longest_token_count = token_usage
      result_list.append(res)
    return result_list, longest_token_count
