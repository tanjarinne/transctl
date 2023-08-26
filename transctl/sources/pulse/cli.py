import subprocess
import ntpath
import os
import sys
import transctl.sources.pulse as pulse
from transctl.encoders import SpaceEncoder


def extract(**kwargs):
  file   = kwargs.get('file')
  pwd    = kwargs.get('pwd')
  tokens = kwargs.get('tokens')
  output = kwargs.get('output')

  if not file: raise ValueError('Pulse needs a file')
  if not pwd: raise ValueError('Pulse needs a password for the file')
  if not tokens: raise ValueError('Pulse needs a comma-separated list of tokens')


  args = f"pdftotext -enc UTF-8 -simple2 -opw {pwd} {file} -".split()
  result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  text = result.stdout.decode('utf-8')
  lines = [l for l in text.split("\n") if l]
  tokens = _extract_tokens(tokens)
  tokenised_lines, _ = _tokenise_lines(lines, tokens)

  if not output:
    fw = sys.stdout
  else:
    outfile = _get_outfile(output, file)
    fw = open(outfile, 'a')

  for line in _process_extract_lines(tokenised_lines):
    fw.write(f'{str(line)}\n')
  fw.close()


def _get_outfile(output: str, file: str, extension : str = ".txt") -> str:
  outfile = f'{os.path.abspath(output)}/{_extract_filename(file, strip_extension=True)}{extension}'
  return outfile


def _process_extract_lines(lines: dict):
  encoder = SpaceEncoder()
  errors = []
  for group, lines in lines.items():
    schema = pulse.Schemas[group]()
    columns = schema.columns()
    for line in lines:
      encoded_line = encoder.encode(line)
      columnated_line = _columnate(encoded_line, len(columns))
      line = encoder.decode(columnated_line)
      line_errors = schema.validate(dict(zip(columns, line)))
      if not line_errors:
        yield line
      else:
        errors.append(line)


def _extract_filename(path: str, strip_extension=False) -> str:
  head, tail = ntpath.split(path)
  result = tail or ntpath.basename(head)
  if strip_extension:
    result = result.split('.')[0]
  return result


def _extract_tokens(arg:str) -> list:
  tokens = arg.split(',')
  return tokens


def _tokenise_lines(lines:list, tokens=list) -> tuple[set, str]:
  result = {k: [] for k in tokens}
  result.popitem() # the last item is the last token
  grouping = False
  token_counter = 0
  group = []
  last_token = tokens[-1]

  for idx, line in enumerate(lines):
    if last_token in line:
      break

    next_line = lines[idx + 1]
    current_token = tokens[token_counter]
    next_token = tokens[token_counter + 1]

    if current_token in line:
      grouping = True
      continue

    if grouping:
      group.append(line)

    if next_token in next_line:
      token_counter += 1
      result[current_token] = group
      grouping = False
      group = []
      continue

  return result, last_token


def _columnate(s: str, length: int) -> list:
  parts = s.split()
  if len(parts) <= length:
      return parts

  result = [" ".join(parts[:-length+1])] + parts[-length+1:]
  return result
