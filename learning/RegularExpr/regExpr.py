import re
t='<Tom Paris> fsd.dff@microsoft.com'
t=re.split(r'\s',t)[-1]
print t
company='microsoft'
rgmail=re.compile(r'(^[^\_\#\|\\\/\?\"\'\;\:\<\>\,\`\~\$\^\&\*\(\)\-+=\s\@\!.]+[^_#\|\\\/\?\"\'\;\:\<\>\,\`\~\$\^\&\*\(\)\-+=\s\@\!]*)@({}.com)$'.format(company))
ma=rgmail.match(t)
if ma:
    print(ma.group(0))
