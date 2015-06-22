from aes import *

def Main_Encrypt(inp,key):
	ob = AesClass('0')
	ob.text_node(inp)
	ob.key_node(key)
	ob.Roundkeys()
	ob.MainRounds()
	ob.binary_6()
	return ob.Encrypted()
	
def Main_Decrypt(inp,key):
	ob = AesClass('1')
	ob.cipher_node(inp)
	ob.key_node(key)
	ob.Roundkeys()
	ob.MainRounds()
	return ob.Decrypted()

if __name__ == "__main__":
	w = raw_input('0. for encryption & 1. for decryption : ')
	intput = raw_input('Enter the Text : ')
	key = raw_input('Enter the key : ')
	if w == '0':
		print Main_Encrypt(intput,key)
	else : print Main_Decrypt(intput,key)