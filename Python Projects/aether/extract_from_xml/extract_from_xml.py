#-*- coding:utf-8 -*-
from xml.dom.minidom import parse
from io import BytesIO
import xml.dom.minidom
import binascii
import sys

class phraseclass:
    def __init__(self, in_path, out_path):
        DOMTree = parse(in_path)
        collection = DOMTree.documentElement
        Querys = collection.getElementsByTagName("Query")
        result = self.phrasefun(Querys)
        self.writerfun(out_path, result)
    
    def phrasefun(self, Querys):
        result = ""
        for Query in Querys:
            Text = Query.getElementsByTagName('Text')[0].childNodes[0].data if Query.getElementsByTagName('Text').length > 0 else ""
            Title = Query.getElementsByTagName('Title')[0].childNodes[0].data if Query.getElementsByTagName('Title').length > 0 else ""
            URL = Query.getElementsByTagName('URL')[0].childNodes[0].data if Query.getElementsByTagName('URL').length > 0 else ""
            DisplayURL = Query.getElementsByTagName('DisplayURL')[0].childNodes[0].data if Query.getElementsByTagName('DisplayURL').length > 0 else ""
            Snippet = Query.getElementsByTagName('Snippet')[0].childNodes[0].data if Query.getElementsByTagName('Snippet').length > 0 else ""
            Market = Query.getElementsByTagName('Market')[0].childNodes[0].data if Query.getElementsByTagName('Market').length > 0 else ""
            result += "%s\t%s\t%s\t%s\t%s\t%s\n" % (Text,Title,URL,DisplayURL,Snippet,Market)
        return result

    def writerfun(self, out_path, result):
        result = result.replace(r'\xee\x80\x80', r'<strong>').replace(r'\xee\x80\x81', r'</strong>')
        result = result.replace(r'\xe2\x80\x90', r'‐').replace(r'\xe2\x80\xa0', r'†')
        result = result.replace(r'\xe2\x80\x91', r'‑').replace(r'\xe2\x80\xa1', r'‡')
        result = result.replace(r'\xe2\x80\x92', r'‒').replace(r'\xe2\x80\xa2', r'•')
        result = result.replace(r'\xe2\x80\x93', r'–').replace(r'\xe2\x80\xa3', r'‣')
        result = result.replace(r'\xe2\x80\x94', r'—').replace(r'\xe2\x80\xa4', r'․')
        result = result.replace(r'\xe2\x80\x95', r'―').replace(r'\xe2\x80\xa5', r'‥')
        result = result.replace(r'\xe2\x80\x96', r'‖').replace(r'\xe2\x80\xa6', r'…')
        result = result.replace(r'\xe2\x80\x97', r'‗').replace(r'\xe2\x80\xa7', r'‧')
        result = result.replace(r'\xe2\x80\x98', r'‘').replace(r'\xe2\x80\xa8', r' ')
        result = result.replace(r'\xe2\x80\x99', r'’').replace(r'\xe2\x80\xa9', r' ')
        result = result.replace(r'\xe2\x80\x9a', r'‚').replace(r'\xe2\x80\xaa', r'')
        result = result.replace(r'\xe2\x80\x9b', r'‛').replace(r'\xe2\x80\xab', r'')
        result = result.replace(r'\xe2\x80\x9c', r'“').replace(r'\xe2\x80\xac', r'')
        result = result.replace(r'\xe2\x80\x9d', r'”').replace(r'\xe2\x80\xad', r'')
        result = result.replace(r'\xe2\x80\x9e', r'„').replace(r'\xe2\x80\xae', r'')
        result = result.replace(r'\xe2\x80\x9f', r'‟').replace(r'\xe2\x80\xaf', r'')
        result = result.replace(r'\x30', r'0').replace(r'\x31', r'1')
        result = result.replace(r'\x32', r'2').replace(r'\x33', r'3')
        result = result.replace(r'\x34', r'4').replace(r'\x35', r'5')
        result = result.replace(r'\x36', r'6').replace(r'\x37', r'7')
        result = result.replace(r'\x38', r'8').replace(r'\x39', r'9')
        result = result.replace(r'\x41', r'A').replace(r'\x61', r'a')
        result = result.replace(r'\x42', r'B').replace(r'\x62', r'b')
        result = result.replace(r'\x43', r'C').replace(r'\x63', r'c')
        result = result.replace(r'\x44', r'D').replace(r'\x64', r'd')
        result = result.replace(r'\x45', r'E').replace(r'\x65', r'e')
        result = result.replace(r'\x46', r'F').replace(r'\x66', r'f')
        result = result.replace(r'\x47', r'G').replace(r'\x67', r'g')
        result = result.replace(r'\x48', r'H').replace(r'\x68', r'h')
        result = result.replace(r'\x49', r'I').replace(r'\x69', r'i')
        result = result.replace(r'\x4a', r'J').replace(r'\x6a', r'j')
        result = result.replace(r'\x4b', r'K').replace(r'\x6b', r'k')
        result = result.replace(r'\x4c', r'L').replace(r'\x6c', r'l')
        result = result.replace(r'\x4d', r'M').replace(r'\x6d', r'm')
        result = result.replace(r'\x4e', r'N').replace(r'\x6e', r'n')
        result = result.replace(r'\x4f', r'O').replace(r'\x6f', r'o')
        result = result.replace(r'\x50', r'P').replace(r'\x70', r'p')
        result = result.replace(r'\x51', r'Q').replace(r'\x71', r'q')
        result = result.replace(r'\x52', r'R').replace(r'\x72', r'r')
        result = result.replace(r'\x53', r'S').replace(r'\x73', r's')
        result = result.replace(r'\x54', r'T').replace(r'\x74', r't')
        result = result.replace(r'\x55', r'U').replace(r'\x75', r'u')
        result = result.replace(r'\x56', r'V').replace(r'\x76', r'v')
        result = result.replace(r'\x57', r'W').replace(r'\x77', r'w')
        result = result.replace(r'\x58', r'X').replace(r'\x78', r'x')
        result = result.replace(r'\x59', r'Y').replace(r'\x79', r'y')
        result = result.replace(r'\x5a', r'Z').replace(r'\x7a', r'z')
        # l = result.split(r"\x")
        # resultbytes = bytes.fromhex("".join(l))
        # print(result.dec))
        with open(out_path, 'w') as tsvout: 
            tsvout.write('%s%s' % ("Query\tTitle\tURL\tDisplayURL\tSnippet\tMarket\n", result))
            

if __name__ == "__main__":
    xml_path= r"E:/03_Python Projects/aether/extract_from_xml/enus scraping result.xml" ;
    out_path = r"E:/03_Python Projects/aether/extract_from_xml/testDL.tsv"; 
    # xml_path = sys.argv[1]
    # out_path = sys.argv[2]
    phraseclass(xml_path, out_path)
    
    