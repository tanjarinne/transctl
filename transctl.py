import fire
from importlib import import_module

class Commands(object):
  """
  A cool CLI to keep track of my transition's data

  I build CLIs for companies, why not having one for myself uh?

  This is intended to act as a ETL with different data sources that get
  transformed into a format that can be loaded onto different databases for
  visualisation and housekeeping and so.

  Not yet there, but soon
  @see https://github.com/users/tanjarinne/projects/4/views/1
  """
  def __init__(
      self, inspect: bool = False, extract: bool = False,
      transform: bool = False, load: bool = False) -> None:
    if load and (not extract or not transform):
      raise ValueError("Load can't run without Extracting and Transforming")
    elif transform and not extract:
      raise ValueError("Can't transform without loading")

    self.extract_flag = extract
    self.transform = transform
    self.load = load
    self.inspect = inspect


  def extract(self, source:str, *arg, **kwargs) -> None:
    self.extract = True
    parser = import_module(f'transctl.sources.{source.lower()}.cli')
    result = parser.extract(*arg, **kwargs)
    return result


if __name__ == '__main__':
  fire.Fire(Commands)
