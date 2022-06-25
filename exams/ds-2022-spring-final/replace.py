# The following code will search 'MM/DD/YYYY' (e.g. 11/30/2016 or NOV/30/2016, etc ),
# and replace with 'MM-DD-YYYY' in multi-line mode.
import re
with open ('_build/latex/ds-2022-spring-final.tex', 'r', encoding='utf-8') as f:
    content = f.read()
    content_new = re.sub(r'\\sphinxAtStartPar[\s\n]*\\sphinxstylestrong\{Answer:\}',
        r'\\sphinxAtStartPar\n{\\color{blue}\n\\sphinxstylestrong{Answer:}', content, flags = re.M)
    #content_new = re.sub(r'\\sphinxAtStartPar[\s\n]*\\\(\\square\\\)[\s\n]*',
    #    r'\\sphinxAtStartPar\n\\(\\square\\)\n}% end blue\n', content_new, flags = re.M)
    content_new = re.sub(r'\\sphinxAtStartPar[\s\n]*\\\(\\square\\\)[\s\n]*',
        r'}% end blue\n', content_new, flags = re.M)


with open ('_build/latex/ds-2022-spring-final.tex', 'w', encoding='utf-8') as fout:
    fout.write(content_new)
    fout.close
