import re


class SpaceEncoder:
  separator = '++'
  tokens = [
    [r'See below', f'See{separator}below'],
    [r'([<\u2193\u2191]) ((?=.?\d)\d*[.,]?\d*)', fr'\1{separator}\2'],
    [r'([\u2193\u2191]) ([<>])', fr'\1{separator}\2'],
    [r'< ([0-9]*[.,]{0,1}[0-9]*)', fr'<{separator}\1'],
  ]

  def encode(self, input: any) -> str|list:
    match input:
      case str():
        for token in self.tokens:
          input = re.sub(
            token[0], f'{__class__.__qualname__}[{token[1]}]', input)
        return input
      case list():
        return list(map(self.encode, input))


  def decode(self, input: any) -> str|list:
    match input:
      case str():
        input = re.sub(fr'{__class__.__qualname__}\[(.*?)(?=\])\]', r'\1', input)
        input = input.replace(self.separator, ' ')
        return input
      case list():
        return list(map(self.decode, input))
