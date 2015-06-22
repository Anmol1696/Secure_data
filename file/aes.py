from tables import *

class AesClass:
	
	def __init__(self,a):
		self.key = []
		self.do = a
		self.encrypt = ''
		self.decrypt = ''
		self.number = 0
		self.node = []
	
	# Plain text to node
	def text_node(self,inp):
		noder = len(inp)/16 + 1
		self.number = noder
		box = [0 for x in range(noder)]
		for u in range(noder):
			temp = [[0 for x in range(4)]for x in range(4)]
			for v in range(16):
				q = 0
				if len(inp) > (u*16)+v: q = ord(inp[(u*16)+v])
				temp[v/4][v%4] = q
			box[u] = temp
		self.node = box
		
	# Cipher text to node
	def cipher_node(self,a):
		noder = len(a)/22
		self.number = noder 
		box = [0 for x in range(noder)]
		for o in range(0,len(a),22):
			Bin = []
			fin = []
			temp = [[0 for x in range(4)]for x in range(4)]
			for t in range(22):
				for i in range(5,-1,-1):
					q = 0
					if (((ord(a[o+t])-32)>>i)%2==1): q=1
					Bin.append(q)
			for t in range(4): del Bin[-1]
			for e in range(0,128,8):
				w = 0
				for q in range(8):
					w+=(pow(2,7-q)*Bin[e+q])
				fin.append(w)
			for u in range(16):
				temp[u/4][u%4] = fin[u]
			box[o/22] = temp
		self.node = box
		
	# key to node
	def key_node(self,a):
		key_pad = ')!(@*#&$%^<+*/>?'
		for x in range(0,16-len(a)) :	a += key_pad[x]
		keytemp = [0 for x in range(11)]
		keytemp[0] = [[(ord(a[i])^ord(key_pad[i])) for i in range(0+x,4+x)]for x in range(0,16,4)]
		self.key = keytemp
	
	# making of the Round keys
	def Roundkeys(self):
		
		for rnd  in range(10) :
			coltemp = [self.key[rnd][0][x] for x in range(4)]
			colcur = [self.key[rnd][3][x] for x in range(4)]
			(colcur[0],colcur[1],colcur[2],colcur[3]) = (colcur[1],colcur[2],colcur[3],colcur[0])
			
			for x in range(4):
				r = (colcur[x]>>4) & 0x0F
				c = (colcur[x]>>0) & 0x0F
				colcur[x] = S_box[r][c]
				colcur[x] = (coltemp[x]^colcur[x]^Rcon[rnd][x])
			tempkey = [[0 for x in range(4)]for x in range(4)]
			tempkey[0] = colcur 
			self.key[rnd+1] = tempkey 
			for i in range(1,4):
				for j in range(4):
					coltemp[j] = self.key[rnd][i][j]
					colcur[j] = self.key[rnd+1][i-1][j]
					colcur[j] = coltemp[j]^colcur[j]
					self.key[rnd+1][i][j] = colcur[j]
	
	def reverse_keys(self):
		(self.key[0],self.key[1],self.key[2],self.key[3],self.key[4],self.key[5],self.key[6],self.key[7],self.key[8],self.key[9],self.key[10])\
			= (self.key[10],self.key[9],self.key[8],self.key[7],self.key[6],self.key[5],self.key[4],self.key[3],self.key[2],self.key[1],self.key[0])
	
	def MainRounds(self):
		# Tables
		if self.do == '0':
			for rep in range(self.number):
				for rnd in range(11):
					if rnd > 0:
						# Sbox substitution
						for i in range(4):
							for j in range(4):
								r = (self.node[rep][i][j]>>4)&0x0F
								c = (self.node[rep][i][j]>>0)&0x0F
								self.node[rep][i][j] = S_box[r][c]
						
						# Shift rows
						for i in range(1,4):
							for u in range(i):
								for j in range(3):
									(self.node[rep][j][i],self.node[rep][j+1][i]) = (self.node[rep][j+1][i],self.node[rep][j][i])
						
						if rnd < 10:
							# Mix Columns
							for j in range(4):
								coltemp = [self.node[rep][j][i] for i in range(4)]
								col = [table_2[coltemp[0]]^table_3[coltemp[1]]^coltemp[2]^coltemp[3],\
									coltemp[0]^table_2[coltemp[1]]^table_3[coltemp[2]]^coltemp[3],\
									coltemp[0]^coltemp[1]^table_2[coltemp[2]]^table_3[coltemp[3]],\
									table_3[coltemp[0]]^coltemp[1]^coltemp[2]^table_2[coltemp[3]]]
								self.node[rep][j] = col
					
					# Add Round keys
					for j in range(4):
						for i in range(4):
							self.node[rep][j][i] = self.node[rep][j][i]^self.key[rnd][j][i]
		
		else :
			self.reverse_keys()
			for rep in range(self.number):
				for rnd in range(11):
					if rnd > 0:
						# Inverse Shift rows
						for i in range(1,4):
							for u in range(i*3):
								for j in range(3):
									(self.node[rep][j][i],self.node[rep][j+1][i]) = (self.node[rep][j+1][i],self.node[rep][j][i])
						# Inverse Sbox substitution
						for i in range(4):
							for j in range(4):
								r = (self.node[rep][i][j]>>4)&0x0F
								c = (self.node[rep][i][j]>>0)&0x0F
								self.node[rep][i][j] = inS_box[r][c]
					# Add Round keys
					for j in range(4):
						for i in range(4):
							self.node[rep][j][i] = self.node[rep][j][i]^self.key[rnd][j][i]
					
					if rnd<10 and rnd>0:
						# Mix Columns
						for j in range(4):
							coltemp = [self.node[rep][j][i] for i in range(4)]
							col = [table_14[coltemp[0]]^table_11[coltemp[1]]^table_13[coltemp[2]]^table_9[coltemp[3]],\
								table_9[coltemp[0]]^table_14[coltemp[1]]^table_11[coltemp[2]]^table_13[coltemp[3]],\
								table_13[coltemp[0]]^table_9[coltemp[1]]^table_14[coltemp[2]]^table_11[coltemp[3]],\
								table_11[coltemp[0]]^table_13[coltemp[1]]^table_9[coltemp[2]]^table_14[coltemp[3]]]
							self.node[rep][j] = col
					
					if rnd == 10:
						for i in range(4):
							for j in range(4):
								a = chr(self.node[rep][i][j])
								self.decrypt += a
	
	def binary_6(self):
		for rep in range(self.number):
			Bin = []
			rare = [' ' for x in range(22)]
			for x in range(4):
				for y in range(4):
					for i in range(7,-1,-1):
						if ((self.node[rep][x][y]>>i)%2==1) : q=1
						else : q=0
						Bin.append(q)
			for x in range(4): Bin.append(0) 
			for i in range(0,132,6):
				a = 0
				for q in range(6): a += (pow(2,5-q)*Bin[q+i])
				rare[i/6] = chr(a+32)
			for u in range(22): self.encrypt += rare[u]  
	
	def Decrypted(self):
		return self.decrypt
	
	def Encrypted(self):
		return self.encrypt