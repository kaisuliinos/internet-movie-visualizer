import warnings

from bokeh.colors import HSL

warnings.filterwarnings("ignore", category=DeprecationWarning)

def string_to_rgb(name):
  value = sum(bytearray(name, 'utf-8'))
  hue = round(value % 360 / 10)*10
  # print('{}: {}, {}'.format(name, value, hue))
  return HSL(hue, 0.75, 0.8)

def create_name_strings(row):
  name = row.primaryName
  roles = row.primaryProfession

  roles = str(roles).replace('_', ' ')
  roles = roles.split(',')
  if 'miscellaneous' in roles: roles.remove('miscellaneous')

  return '{} ({})'.format(name, ', '.join(roles))