import sys; args = sys.argv[1:]

idx = int(args[0])-30



myRegexLst = [

  r"/^0$|^100$|^101$/",
  r"/^[01]*$/",
  r"/0$/",
  r"/\b\w*[aeiou]\w*[aeiou]\w*\b/i",
  r"/^0$|^1[01]*0$/",
  r"/^[01]*110[01]*$/",
  r"/^.{2,4}$/s",
  r"/\d{3}\s*-?\s*\d{2}\s*-?\s*\d{4}/"
  r"/\bd.*\b/"
  r"/^0$|^1$|^0[01]*0$|^1[01]*1$/"
  ]



if idx < len(myRegexLst):

  print(myRegexLst[idx])

# Wilson Chen 1 2023