
class Ant:
	def __init__(self,x=0,y=0,color='black'):
		self.x=x
		self.y=y
		self.color=color
	def crawl(self,x,y):
		self.x=x
		self.y=y
		print('爬行。。。')
		self.info()
	def info(self):
		print('当前位置：（%d,%d)' %(self.x,self.y))
	def attack(self):
		print('用嘴咬：')
class FlyAnt(Ant):
	def attack(self):
		print('用尾针!')
	def fly(self,x,y):
		print("飞行...")
		self.x=x
		self.y=y
		self.info()
flyant=FlyAnt(color='red')
flyant.crawl(3,5)
flyant.fly(10,14)
flyant.attack()
