# Template Parser for MW
'''
    Copyright (C) 2018 apple502j

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import re

class TemplateParserError(Exception):
    pass
class WrongPageNameError(TemplateParserError):
    pass
class TemplateWriterError(Exception):
    pass
class WriterDictTypeError(TemplateWriterError):
    pass
def parseMWT(text):
    x=re.match("^\{\{[^\{\}\[\]\]#<>\|]{1,255}(|((|.{1,100}=)(.{1,10000})){1,100})\}\}$",text)
    if not(x):
        raise WrongPageNameError()
    dic={"name":"","data":{}}
    tmpstr=""
    tmpstr2=""
    args=0
    haskey=0
    pipecount=0
    count=-1
    for c in text:
        count += 1
        if c=="{":
            if count > 3:
                if haskey:
                    tmpstr2+=c
                else:
                    tmpstr+=c
        elif c=="}":
            if count < len(text)-2:
                if haskey:
                    tmpstr2+=c
                else:
                    tmpstr+=c
        elif c=="|":
            if args:
                if haskey:
                    dic["data"][tmpstr] = tmpstr2
                else:
                    pipecount += 1
                    dic["data"][str(pipecount)]=tmpstr
                haskey=0
                tmpstr=""
                tmpstr2=""
            else:
                args=1
                dic["name"]=tmpstr
                tmpstr=""
        elif c=="=":
            haskey=1
        else:
            if haskey:
                tmpstr2 += c
            else:
                tmpstr += c
    if not(args):
        dic["name"]=tmpstr
    if text[-3] != "|":
        if haskey:
            dic["data"][tmpstr] = tmpstr2
        else:
            dic["data"][str(pipecount + 1)]=tmpstr
    return dic

def writeMWT(mwtDict,putNewline=False):
    try:
        temp="{{" + mwtDict["name"]
        for mwkey in mwtDict["data"]:
            if putNewline:
                temp += "\n"
            temp += "|" + mwkey + "=" + mwtDict["data"][mwkey]
        temp += "}}"
        return temp
    except:
        raise WriterDictTypeError
