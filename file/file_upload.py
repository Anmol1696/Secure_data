from os import listdir
from os.path import join, isfile
from main_aes import Main_Encrypt, Main_Decrypt
from main_md5 import main
import zlib

def folder(file_name):
	if isfile(file_name):
		return file_name
	
	else:
		out = ''
		temp = listdir(file_name)
		for name in temp:
			out += str(folder(join(file_name,name))) + '\n'
		return out

def one_file(file_list,key):
	file_list = file_list.split('\n')
	while True:
		try:
			file_list.remove('')
		except:
			break
	
	final = open('/home/anmol/Django/git/Secure_data/file/upload.txt','a')
	
	for name in file_list:
		f = open(name,'r')
		r = f.readlines()
		f.close()
		total = ''
		for x in r:
			total += x
		total = zlib.compress(Main_Encrypt(total,key))
		pad_prefix = '\n<!--%s>\n' % (name)
		pad_sufix = '\n<%s-->\n' % (name)
		total = pad_prefix + total + pad_sufix
		
		final.write(total)
	final.close()

def main_file(file_name,key):
	one_file(folder(file_name),key)

if __name__ == '__main__':
	name = raw_input('Enter the folder -> ')
	key = raw_input('Key -> ')
	main_file(name,key)
