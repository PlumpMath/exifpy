fn = "image_0329.jpg"
f = open(fn)

def read(f, bytes):
  return buff2hex(f.read(bytes))

def read_until_null(f, l):
  s = ''
  char = f.read(1)
  l -= 1

  while '\x00' != char:
    s += char
    char = f.read(1)
    l -= 1

  s += char
  return [s, l]

def buff2hex(buff):
  H = 0
  i = len(buff) - 1

  for char in buff:
    H += ord(char) << i*8
    i -= 1

  return H

def APP(f):
  APP = read(f, 2)
  length = read(f, 2)

  if 0xFFE0 == APP or 0xFFE1 == APP or 0xFFE2 == APP:
    name, length = read_until_null(f, length)
    print name

    if 0xFFE1 == APP:
      f.read(1) # padding
      EXIF(f)
  else:
    print 'No APP'
    f.seek(-4, 1)
    return -1

  return length

def EXIF(f):
  Endian = f.read(2)
  if Endian == 'MM':
    print 'big endian'
  else:
    print 'little endian'

  fourty_two = read(f, 2)
  if 0x002A != fourty_two:
    print 'ERROR :: 42 is invalid'
    return

  IFD_offset = read(f, 4)
  if 0x00000008 != IFD_offset:
    print 'ERROR :: large IFD offset'

  IFD = read(f, 2)
  

SOI = read(f, 2)
if 0xFFD8 != SOI:
  print 'ERROR :: Invalid Start of Image'
  print '[DUMP] 0x%04x' % SOI
  quit()

length = APP(f)
while length > 0:
  f.seek(length - 2, 1)
  length = APP(f)

print '0x%04x' % read(f, 2)
