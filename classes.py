from typing import List, Dict, Any

class TempData:
  def __init__(self, data : Dict[str, Any]):
    self.data = data

  def get(self, key : str) -> Any:
    return self.data[key]

  def set(self, key : str, value : Any) -> None:
    self.data[key] = value

  def turn_all_boolean_false(self) -> None:
    for key in self.data:
      if isinstance(self.data[key], bool):
        self.data[key] = False

  def turn_all_boolean_true(self) -> None:
    for key in self.data:
      if isinstance(self.data[key], bool):
        self.data[key] = True
        
  def key_check(self, key : str) -> bool:
    try:
      if self.data[key]:
        return True
    except KeyError:
      return False
