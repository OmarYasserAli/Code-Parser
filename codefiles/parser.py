
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import*
class win(QMainWindow):
	def __init__(self):
		super().__init__()
		self.construct()
		
	def construct(self):
		self.back=QPalette()
		self.back.setColor(self.backgroundRole(),QColor('#333'))
		self.setPalette(self.back)
		self.setGeometry(200,50,500,400)
		self.setWindowTitle("Parser")
		self.filebtn=QPushButton("Browse files",self)
		self.filebtn.setFixedSize(100,30)
		self.filebtn.move(15,40)
		self.filebtn.clicked.connect(self.getfile)
		self.filebtn.setObjectName("file")
		self.textbox=QLineEdit(self)
		self.textbox.setObjectName("textbox")
		self.textbox.setFixedSize(350,30)
		self.textbox.move(125,40)
		self.drawbtn=QPushButton("Draw",self)
		self.drawbtn.setFixedSize(100,30)
		self.drawbtn.move(220,80)
		self.drawbtn.clicked.connect(self.printcontent)
		self.drawbtn.setObjectName('draw')
		self.setStyleSheet("""QPushButton#file,QPushButton#draw{
			font: 15px arial , sans-serif;border: 2px solid black ;
			border-radius:4px; 
			background-color:#B22222; 
			color: white;}
			QPushButton#file:hover,QPushButton#draw:hover{
			background-color:darkred;
			}
			QLineEdit#textbox{
			font: 12px arial ;
			}
			""")
		self.filecontent=''
		self.show()
	
		
	def getfile(self):
		f=QFileDialog()
		o,_=f.getOpenFileName(self, 'Open file', 
		'',"Text files (*.txt)")
		f.setFileMode(QFileDialog.AnyFile)
		if o:
			self.textbox.setText(o)
			

	def printcontent(self):
		try:
 			readfile = open(self.textbox.text(), 'r')
 			self.filecontent=readfile.read()
 			co=(l.filecontent)
 			co=co+" "
 			def scanner(code,scanned):
 			    state="none"
 			    token=""
 			    reserved_Words=['if','repeat','until','read','write','then','else','end']
 			    operators=['+','-','*','/','<','>','=','(',')']
 			    special_symbols=[';']
 			    for x in code:
 			        if x=='{':
 			            state="comment"
 			        elif state== "comment":
 			            if x=="}":
 			                state="none"
 			            else:
 			                continue
 			        elif x.isdigit():
 			            token = token + x
 			            if state == "number":
 			                continue
 			            else:
 			                state = "number"
 			        elif x.isalpha():
 			            token = token + x
 			            if state == "char":
 			                continue
 			            else:
 			                state = "char"
 			        elif x ==':':
 			            state="assign"
 			            if token !="":
 			                scanned.append(token+','+"Identifier")
 			                token=""
 			        elif x=='=' and state =="assign":
 			            scanned.append(":="+','+'special symbol')
 			            state="none"
 			        else:
 			            
 			            if token !="":
 			                if state == "number":
 			                    scanned.append(token+','+state)
 			                elif token in reserved_Words:
 			                    scanned.append(token+','+"Reserved Word")
 			                else:
 			                    scanned.append(token+','+"Identifier")
 			            if x in operators:
 			               scanned.append(x +','+ "operator")
 			            if x in special_symbols:
 			            	scanned.append(x+','+"special symbol")   
 			                
 			            token=""
 			            state="none"
 			lines=[]
 			scanner(co,lines)
 			lines= ["begin,compiler"] +lines + ["finish,compiler"]
 			for i in range(len(lines)):
 			    lines[i]=lines[i].split(",")

 			scope=[0]
 			tree=[]
 			parent=0

 			def phar(tree,lines,st,fin,parent):
 			    ti=0
 			    i=st-1
 			    siz=fin+1
 			    while i < siz:
 			        i=i+1
 			        #i=i+ti
 			        if(i>fin):
 			            break
 			        #print(i,parent)
 			        if(lines[i][0]==";"):
 			            continue
 			        if(lines[i][0] == "read"):
 			            if(lines[i+1][1]!="Identifier"):
 			                print("syntax error")
 			                break
 			            else:
 			                   temp=[parent,lines[i][0]+" "+lines[i+1][0]]
 			                   tree.append(temp)
 			                   i=i+1
 			        elif(lines[i][0] == "write"):
 			                if(lines[i+1][1]!="Identifier" and lines[i+1][1]!="number" and lines[i+1][1]!="operator"):
 			                   break
 			                   print("syntax error")
 			                else:
 			                    #print("par",i, parent)
 			                    temp=[parent,lines[i][0]]
 			                    tree.append(temp)
 			                    nfn=i+1
 			                    while lines[nfn+1][0] !=";" and lines[nfn+1][0] !="end" and lines[nfn+1][0] !="until" and lines[nfn+1][0] !="finish" :
 			                    	nfn=nfn+1
 			                    new_parent=len(tree)-1
 			                    print(i+1,nfn)
 			                    phar(tree,lines,i+1,nfn,new_parent)
 			                    i=nfn

 			                    #print(tree)
 			                    #print("XXXXXXXX",i)
 			                    #i=i+1
 			        elif(lines[i][0]=="if"):
 			            nst=i+1
 			            nfn=i
 			            ti=0
 			            stack=[lines[i][0]]
 			            while len(stack)>0:
 			                nfn=nfn+1
 			                if (lines[nfn][0] =="if"):
 			                    stack.append(lines[nfn][0])
 			                elif (lines[nfn][0] =="end"):
 			                    stack.pop()
 			                
 			                if(nfn>fin):
 			                    print("syntax error")
 			            #print("test",nst,nfn)
 			            
 			            temp=[parent,lines[i][0]]
 			            tree.append(temp)
 			            new_parent=len(tree)-1
 			            phar(tree,lines,nst,nfn,new_parent)
 			            
 			            i=nfn
 			            #print("test2222 " ,ti,i)

 			        

 			        elif(lines[i][0]=="repeat"):
 			            nst=i+1
 			            nfn=i
 			            stack=[lines[i][0]]
 			            while len(stack)>0:
 			                nfn=nfn+1
 			                if (lines[nfn][0] =="repeat"):
 			                    stack.append(lines[nfn][0])
 			                elif (lines[nfn][0] =="until"):
 			                    stack.pop()
 			            
 			            nfn=nfn+1
 			            while lines[nfn][0] !=';':
 			                nfn=nfn+1
 			            #print("semicol",lines[nfn][0],nfn)
 			            if(nfn>fin):
 			                print("syntax error")
 			            #print("test",nst,nfn)
 			            #print(lines[nst][0],lines[nfn][0])
 			            temp=[parent,lines[i][0]]
 			            tree.append(temp)
 			            new_parent=len(tree)-1
 			            
 			            
 			            #phar(tree,lines,ust,ufn,new_parent)
 			            phar(tree,lines,nst,nfn,new_parent)
 			            i=nfn
 			            #print("test2" ,i)


 			        elif (lines[i][1]== 'Identifier' or lines[i][1]== 'number' ):
 			            nst=i
 			            nfn=i
 			            i=i+1
 			            #print("new finish",nfn)
 			            while (lines[nfn+1][1]== 'Identifier' or lines[nfn+1][1]== 'number' or lines[nfn+1][1]== 'operator' or lines[nfn+1][1]=="operator" or lines[nfn+1][0]==":="):
 			                nfn=nfn+1
 			    
 			            i=nfn
 			            #print(nst,"new fin",nfn)
 			            #new_parent=len(tree)-1
 			            new_parent=parent
 			            texp=[]
 			            for t in range(nst , nfn+1):
 			                texp.append(lines[t][0])
 			            syntree=syntax(texp)
 			            if(syntree.data==":="):
 			            	syntree.data="assign  " +syntree.left.data
 			            	syntree.left.data="compilerRem"
 			            que=[syntree]
 			            qi=new_parent
 			            que[0].data=[qi]+[que[0].data]
 			            qi=len(tree)
 			            ptree=[]

 			            while len(que)>0:
 			            	if que[0].data == "compilerRem":
 			            		que.pop(0)
 			            		continue

 			            	if que[0].left !=None and que[0].left.data != "compilerRem":
 			            		que[0].left.data=[qi]+[que[0].left.data]
 			            		que.append(que[0].left)
 			            	if que[0].right !=None:  
 			                    que[0].right.data=[qi]+[que[0].right.data]
 			                    que.append(que[0].right)
 			            	qi=qi+1
 			                #print(que[0].data[0])
 			            	ptree.append(que.pop(0).data)
 			            #print ("phar",nst,nfn,new_parent)
 			            #print (ptree ,"  SSSSSSSSSSSS")
 			            
 			            #print (ptree)
 			            for el in ptree:
 			                tree.append(el)
 			            
 			            #phar(tree,lines,nst,nfn,new_parent)
 			            
 			            '''
 			            for x in range(len(tree)):
                                            if(tree[x][1] == ":="):
                                                    tree[x][1] = "assign"
                                       '''             
 			        elif(lines[i][0])=="else":
 			        	temp=["else"]+[parent]
 			        	tree.append(temp) 
 			            
 			            

 			phar(tree,lines,0,len(lines)-1,-1)
 			          
 			for x in tree:
 				if type(x[0]) is int:
 					x[0],x[1]=x[1],x[0]
 			
 			for x in range (len( tree)):
 				tree[x]=tree[x]+[x]
 			
 			for x in tree:
 				print(x)	 
 				
 			self.drawcontent(tree)               
 			
		except IOError:
 			print ('\007')
 			self.info("this file does not exist! ")
	
	def drawcontent(self,treelist):
		self.foo=Example(treelist)

	def info(self,text,information=''):
		msg=QMessageBox(self)
		msg.setIcon(QMessageBox.Warning)	
		msg.setText(text)
		msg.setInformativeText(information)
		msg.setWindowTitle("import error")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.show()
		retval = msg.exec_()
class node:
	def __init__(self,text='NODE',x=0,y=0,shape='r'):
		self.text=text
		self.x=x
		self.y=y
		self.shape=shape
class Tree:
	def __init__(self,size):
		self.nodes=[]
		self.edges=[]
		self.size=size
	def add_node(self,node):
		self.nodes.append(node)
	def add_edge(self,node1,node2):
		self.edges.append((node1,node2))	

		
class Example(QWidget):
    
	def __init__(self,treelist):
		super().__init__()
		self.list=treelist
		self.createGraph() 
		self.initUI()
	def getlevel(self,nodel):
		if(nodel[1]== -1):
			return (0)
		else:	
			return (1+self.getlevel(self.list[nodel[1]]))
	def searchInList(self,item,list,parameter):
		for i in list:
			if(i[parameter]==item):
				return (i,True)
		return 0,False				
	
	def createGraph(self):

		self.graph=Tree(1.1)
		levels=[[] for i in range (10)]
	
		for i in self.list:
			k=self.getlevel(i)
			levels[k].append(i)
		


		x=2
		y=0
		points=[]
		nodels=[[None for x in range(3)] for y in range(0)]	
		for i in levels:
			for j in i:
				if(j[0]=='else'):
					continue
				flag=False
				if('repeat' not in j[0] and 'write' not in j[0] and 'read' not in j[0] and j[0]!='if' and "assign"   not in j[0]):
					flag=True
				if(flag):
					s='c'
				else:
					s='r'
				part=[None,None,None]
				dummy,mysavior=self.searchInList(j[1],nodels,1)
				if(mysavior):
					if((dummy[0].x-1,y) not in points):
						x=dummy[0].x-1
				part[0]=node(j[0],x,y,s)
				point=(x,y)
				points.append(point)
				part[1]=self.list.index(j)
				part[2]=j[1]
				nodels.append(part)
				self.graph.add_node(part[0])
				x+=1
			x=2-y-1
			if(x<0):
				x=0
			y+=1	
			
		
	
		for i in nodels:
			special=[]
			special2=[]
			flag1=False
			flag2=False
			for j in nodels:
				if(i[2]==j[2] and i[2]==-1 and i[0].x<j[0].x):
					self.graph.add_edge(i[0],j[0])
				if(i[0].text=='if'):
					flag1=True
					if(i[1]==j[2]):
						special.append(j)
				elif(i[0].text=='repeat'):
					flag2=True
					if(i[1]==j[2]):
						special2.append(j)		
				elif(i[1]==j[2]):	
					self.graph.add_edge(i[0],j[0])
			if(flag1):		
				for z in range(len(special)):
					if(z==0 or z==1 or self.list[special[z][1]-1][0]=='else'):
						self.graph.add_edge(i[0],special[z][0])
					else:		
						self.graph.add_edge(special[z-1][0],special[z][0])
			if(flag2):		
				for z in range(len(special2)):
					if(z==0 or z==len(special2)-1):
						self.graph.add_edge(i[0],special2[z][0])
					else:		
						self.graph.add_edge(special2[z-1][0],special2[z][0])	

					
					
			
			
	

        
        
	def initUI(self):      
        
		self.setGeometry(10,30, 1400, 600)
		self.setWindowTitle('Syntax tree')
		self.show()
        

	def paintEvent(self, event):
		self.qp = QPainter()
		self.qp.begin(self)
		self.drawGraph(event)
		self.qp.end()
	
	def drawGraph(self,e):
		self.update()
		brush= QBrush(QColor('#333'))
		self.qp.setBrush(brush)
		self.qp.drawRect(0,0,8880,8300)
		self.qp.setFont(QFont("Arial",11,QFont.Bold))
		self.draw(self.graph)

	def draw(self,graph):
		for i in graph.nodes:
			self.drawNode(i,graph.size)
		for i in graph.edges:
			self.drawEdge(i[0],i[1],graph.size)	

	def drawNode(self,Node,factor):
		if(Node.shape=='r'):
			brush= QBrush(QColor('red'))
			self.qp.setBrush(brush)
			rect=QRectF((10+Node.x*120)*factor,(10+Node.y*100)*factor,80*factor,50*factor)
			pen = QPen(QColor('black'),2)
			pen.setJoinStyle(Qt.MiterJoin)
			self.qp.setPen(pen)	
			self.qp.drawRect(rect)
			pen = QPen(QColor('white'),3)
			self.qp.setPen(pen)
			self.qp.drawText(rect,Qt.AlignCenter,Node.text)
		elif(Node.shape=='c'):
			brush= QBrush(QColor('#777'))
			self.qp.setBrush(brush)
			pen = QPen(QColor('black'),2)
			pen.setJoinStyle(Qt.MiterJoin)
			self.qp.setPen(pen)	
			elipse=QRectF((10+Node.x*120)*factor,(10+Node.y*100)*factor,80*factor,50*factor)
			self.qp.drawEllipse(elipse)
			pen = QPen(QColor('white'),2)
			self.qp.setPen(pen)	
			self.qp.drawText(elipse,Qt.AlignCenter,Node.text)      
		
	def drawEdge(self,Node1,Node2,factor):
		pen = QPen(QColor('black'),2)
		pen.setJoinStyle(Qt.MiterJoin)
		self.qp.setPen(pen)	
		if(Node1.y==Node2.y):
			self.qp.drawLine((Node1.x*120+90)*factor,(Node1.y*100+35)*factor,(Node2.x*120+10)*factor,(Node2.y*100+35)*factor)
		else:	
			self.qp.drawLine((Node1.x*120+50)*factor,(Node1.y*100+60)*factor,(Node2.x*120+50)*factor,(Node2.y*100+10)*factor)	

app =QApplication(sys.argv)
l=win()
#-------------------------------------

##################################################################################
#                              Tree Class                                        #
##################################################################################
class Node:

    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data


    def PrintTree(self):
        print(self.data)

    def addLeftChild (self,node):
        if self.left is None:
            self.left = node

    def addRightChild (self,node):
        if self.right is None:
            self.right = node





##################################################################################
#                           global variables                                     #
##################################################################################
token = ['x1','*','30','+','77']
index = 0

##################################################################################
#                           find function                                        #
##################################################################################
##################################################################################
#                           syntax function                                      #
##################################################################################
def syntax (listofstring):
    global token
    global index
    token = listofstring
    index = 0
    pos = find(token,':=')

    if pos != -1 :     # if it is assign operation
        tree = Node(token[pos])
        tempnode = Node(token[0])
        tree.addLeftChild(tempnode)
        index = 2
        tree.addRightChild(exp())
        return tree

    else:

        pos = find(token,'>')
        if pos != -1 :
            tree = Node(token[pos])
            temptoken = token
            token = temptoken[:pos]
            tree.addLeftChild(exp())
            index = 0
            token = temptoken[pos+1:]
            tree.addRightChild(exp())
            return tree

        pos = find(token,'<')
        if pos != -1 :
            tree = Node(token[pos])
            temptoken = token
            token = temptoken[:pos]
            tree.addLeftChild(exp())
            token = temptoken[pos+1:]
            index = 0
            tree.addRightChild(exp())
            return tree

        pos = find(token,'=')
        if pos != -1 :
            tree = Node(token[pos])
            temptoken = token
            token = temptoken[:pos]
            tree.addLeftChild(exp())
            token = temptoken[pos+1:]
            index = 0
            tree.addRightChild(exp())
            return tree

        return exp()

##################################################################################
#                           expression function                                  #
##################################################################################
def exp ():
    temp = Node

    temp = term()
    while len(token)!=index and (token[index] == '+' or token[index] == '-'):

        newtemp =  Node(token[index])
        match(token[index])
        newtemp.addLeftChild(temp)
        newtemp.addRightChild(term())
        temp = newtemp

    return temp

##################################################################################
#                                 term function                                  #
##################################################################################
def term ():
    temp = Node

    temp = factor()

    while len(token)!=index and token[index] == '*':

        newtemp =  Node(token[index])
        match('*')
        newtemp.addLeftChild(temp)
        newtemp.addRightChild(factor())
        temp = newtemp

    return temp

##################################################################################
#                               factor function                                  #
##################################################################################
def factor ():
    temp = Node

    if len(token)!=index and token[index] == '(':

        match('(')
        temp = exp()
        match(')')

    elif len(token)!=index :
        temp = Node(token[index])
        match(token[index])
    return temp

##################################################################################
#                              match function                                    #
##################################################################################
def match (char):
    global index
    index +=1

##################################################################################
#                           find function                                        #
##################################################################################
def find (List,word):
    for i in range(len(List)):
        if List[i]==word:
            return i
    return -1

sys.exit(app.exec_())
