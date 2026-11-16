# Main maut ko takiya, aur kafan ko chaadar banakar audhta hoon!

def R(b):
	c=[]
	for i in b:
		c.append(i)
	
	c[1]=b[5]
	c[3]=b[7]
	c[5]=b[9]
	c[7]=b[11]
	c[9]=b[22]
	c[11]=b[20]
	c[22]=b[1]
	c[20]=b[3]
	
	d=[]
	for i in range(23):
		if(c[i]!=c[i+1]):
			d.append(c[i])
	d.append(c[-1])
	if(len(d)==6):
		return True
	else:
		return False
		
def Rp(b):
	c=[]
	for i in b:
		c.append(i)
	
	c[5]=b[1]
	c[7]=b[3]
	c[9]=b[5]
	c[11]=b[7]
	c[22]=b[9]
	c[20]=b[11]
	c[1]=b[22]
	c[3]=b[20]
	
	d=[]
	for i in range(23):
		if(c[i]!=c[i+1]):
			d.append(c[i])
	d.append(c[-1])
	if(len(d)==6):
		return True
	else:
		return False

def U(b):
	c=[]
	for i in b:
		c.append(i)
	
	c[4]=b[16]
	c[5]=b[17]
	c[16]=b[20]
	c[17]=b[21]
	c[20]=b[12]
	c[21]=b[13]
	c[12]=b[4]
	c[13]=b[5]
	
	d=[]
	for i in range(23):
		if(c[i]!=c[i+1]):
			d.append(c[i])
	d.append(c[-1])
	if(len(d)==6):
		return True
	else:
		return False

def Up(b):
	c=[]
	for i in b:
		c.append(i)
	
	c[16]=b[4]
	c[17]=b[5]
	c[20]=b[16]
	c[21]=b[17]
	c[12]=b[20]
	c[13]=b[21]
	c[4]=b[12]
	c[5]=b[13]
	
	d=[]
	for i in range(23):
		if(c[i]!=c[i+1]):
			d.append(c[i])
	d.append(c[-1])
	if(len(d)==6):
		return True
	else:
		return False
	
def F(b):
	c=[]
	for i in b:
		c.append(i)
	
	c[13]=b[3]
	c[15]=b[2]
	c[8]=b[13]
	c[9]=b[15]
	c[18]=b[8]
	c[16]=b[9]
	c[3]=b[18]
	c[2]=b[16]
	
	d=[]
	for i in range(23):
		if(c[i]!=c[i+1]):
			d.append(c[i])
	d.append(c[-1])
	if(len(d)==6):
		return True
	else:
		return False

def Fp(b):
	c=[]
	for i in b:
		c.append(i)
	
	c[3]=b[13]
	c[2]=b[15]
	c[13]=b[8]
	c[15]=b[9]
	c[8]=b[18]
	c[9]=b[16]
	c[18]=b[3]
	c[16]=b[2]
	
	d=[]
	for i in range(23):
		if(c[i]!=c[i+1]):
			d.append(c[i])
	d.append(c[-1])
	if(len(d)==6):
		return True
	else:
		return False

	
a=list(map(int,input().split()))

if(R(a) or Rp(a) or Up(a) or U(a) or F(a) or Fp(a)):
	print("yes")
else:
	print("no")


