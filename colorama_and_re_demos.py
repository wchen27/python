# Colorama demo
from colorama import init, Back, Fore  # Note I have imported specific things here

# Colorama first needs to be initalized so it works on any OS:
init()  # DO NOT FORGET TO DO THIS!!

# Then, Colorama works by inserting special characters into a string that change the appearance of its characters.
print("colorama library demo:")
print()
ex = "An example: " + Back.LIGHTYELLOW_EX + "this text has a yellow backing" + Back.RESET + " ...and this doesn't."
print(ex)
ex2 = "And now " + Back.LIGHTCYAN_EX + "turquoise backing." + Back.RESET
print(ex2)
ex3 = "And " + Fore.RED + "this text is red!" + Fore.RESET
print(ex3)
print()

# If you type Back. or Fore. then your IDE autocomplete should give you a list of available colors.

# Note this affects the length of the string, even though you can't see it!
# This means you will need to BE CAREFUL if inserting Colorama formatting into a string.
a = "example"
b = Back.LIGHTCYAN_EX + "example" + Back.RESET
print(a, "has", len(a), "characters")
print(b, "has", len(b), "characters ... whaaat?!")  # Whaaat?!
for char in b:
    print(str(char))
# print()
# print()
# print()




# # re demo
# import re
# print("re library demo:")
# print()

# # The string from class:
# s = "While inside they wined and dined, safe from the howling wind.\nAnd she whined, it seemed, for the 100th time, into the ear of her friend,\nWhy indeed should I wind the clocks up, if they all run down in the end?"

# # Create a compiled regular expression (note that you do NOT include the forward slashes on either side):
# exp = re.compile(r"..l")
# # NOTE: the lower case r before the quotes specifies to Python that the following string should be interpreted as
# # RAW TEXT, which means that Python just takes every character in it as is, and won't be trying to look for any escape
# # characters.  For instance, r"\n" literally makes the string with two characters, a backslash and an n.  This is
# # important because the regex engine should be the thing interpreting the escape characters, not Python.  Python should
# # send the unmodified raw text string to the regex engine; the regex engine is the one that'll notice that, for
# # instance, \w makes a word character.  Don't forget to use raw text when you specify string literals for regular
# # expressions!

# # All command line arguments are automatically processed as raw text.  If you have this:
# # s = sys.argv[1]
# # ...and you type this at the command line:
# # > my_script.py \n
# # ... then s will automatically be the 2-character string with a backslash and an n.  You don't need to specify raw
# # text in this case.  You need the r only when you're typing a string literal into Python code directly.

# # Calling regex.finditer(string) on a compiled expression regex and passing a string as an argument will find all
# # matches of that expression on that string.  Specifically, it will create an iterator that will return each match, one
# # by one, as a for loop progresses.  Matches are returned as match objects, which have various fields & methods to
# # access all kinds of useful information.  For example, look at all the stuff I can call on the match object "result"
# # at each step in this loop.
# for result in exp.finditer(s):
#     print("This regex:", result.re)
#     print("Searched in this string:")
#     print(result.string)
#     print("And found a match from index", result.start(), "to index", result.end(), "that looks like this:")
#     print(result[0])
#     print("Here are the start and end indices as a tuple:", result.span())
#     print()

# # If you want to use flags, you can pass them as a separate arg.  Multiple flags are combined bitwise with | (that's
# # the vertical bar character, on the backslash key).

# exp2 = re.compile(r"..l", re.I)
# exp3 = re.compile(r"..l", re.I | re.S | re.M)

# # exp2 and exp3 just demonstrate the syntax; they don't give interesting results based on the flags.  Experiment with
# # other regex examples from class to verify the behavior of the flags.