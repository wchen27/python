import sys; args = sys.argv[1:]

idx = int(args[0])-40



myRegexLst = [

  r"/^[xo.]{64}$/i",
  r"/^[xo]*\.[xo]*$/i",
  r"/^(x+o*)?\..*|.*\.(o*x+)$/i",
  r"/^.(..)*$/s",
  r"/(^0([01][01])*$)|(^1[01]([01][01])*$)/",
  r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i",
  r"/^(1|10)*1*$/",
  r"/^\b[bc]*a?[bc]*\b$/",
  r"/^(([bc]*a){2})*[bc]*\b/",
  r"/^(1[02]*1|2)(1[02]*1|[02])*$/",


  r"/(\w)*\w*\1\w*/i",
  r"/(\w)*(\w*\1\w*){3}/i",
  r"/^([01]|(0|1)[01]*\2)$/",
  r"/(?=\b\w{6}\b)\w*cat\w*/i",
  r"/(?=\b\w{5,9}\b)(?=\w*ing)\w*bri\w*/i",
  r"/(?=\b\w{6}\b)(?!\w*cat)\w+/i",
  r"/\b(?!(\w)*\w*\1)\w+/i",
  r"/^((?!10011)[01])*$/",
  r"/\b\w*([aeiou])(?!\1)[aeiou]\w*/i",
  r"/^(?![01]*(101|111))[01]*$/"
  ]



if idx < len(myRegexLst):

  print(myRegexLst[idx])

# Wilson Chen 1 2023