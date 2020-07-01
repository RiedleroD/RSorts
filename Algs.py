#!/usr/bin/python3
import os,sys
import random

PASS=None
READ=0
SWAP=1
INSERT=2
NEW_BUCK=3
BUCKSWAP=4
BUCKINSERT=5
DEL_BUCK=6
FIN=7

class BaseAlgorithm():
	name="Base Algorithm"
	desc="This is the Base algorithm,\nit doesn't sort, but lays the foundation\nfor other algorithms."
	s=0#step counter; optional
	a=0#current action; optional
	b=0#current bucket; optional
	i=0#current index;optional
	v1=None#current value;optional
	v2=None#current value;optional
	f=False#var to store if finished
	def __init__(self,l):
		self.l=l#array length
	#cycle returns a tuple that tells the main program what to do - it doesn't have access to the list.
	#None		→ does nothing
	#(0,x,i)	→ reads value of item x in bucket i and puts it into the value param next cycle; None means there is no item at this index
	#(1,x,y,i)	→ swaps item x with item y in bucket i
	#(2,x,y,i)	→ inserts item x at index y and pushes all items between one index to the old index
	#(3,x,i)	→ creates a new bucket and optionally transfers item x from bucket i to it (if only one argument is passed, bucket is empty)
	#(4,x,i,y,j)→ swaps item x in bucket i to index y in bucket j
	#(5,x,i,y,j)→inserts item x in bucket i at index y in bucket j
	#(6,i)		→ destroys bucket i (only empty buckets can be destroyed)
	#(7)		→ finish
	def cycle(self,v=None):
		self.s+=1
		return None

class BubbleSort(BaseAlgorithm):
	name="Bubble Sort"
	desc="Bubble Sort checks two adjacent items.\nIf the first is greater, swap them.\nThen do this for each index in the list, until the list is sorted"
	def cycle(self,v=None):
		a=self.a
		if a==0:#read current item
			self.a=1
			self.f=True
			return (READ,self.i,0)
		elif a==1:#store current item & read next item
			if self.v1==None:
				self.v1=v
			self.a=2
			return (READ,self.i+1,0)
		elif a==2:#store next item & compare current and next item, then either swap the items or advance and read the next item
			if v==None or self.i+self.s>self.l:#if end of unsorted list is reached (previously last item is always sorted)
				self.s+=1
				if self.f:#if finished: finish
					self.a=7
					return (FIN,)
				else:#if unfinished: start over & read first item
					self.i=0
					self.a=1
					self.f=True
					self.v1=None
					return (READ,self.i,0)
			else:
				self.v2=v
				self.i+=1
				if self.v1<=self.v2:
					self.a=2
					self.v1=self.v2
					return (READ,self.i+1,0)
				else:
					self.a=1
					self.f=False
					return (SWAP,self.i-1,self.i,0)
		elif a==7:
			raise Exception("BubbleSort: Unexpected cycle after finishing")

#TODO: MergeSort doesn't work for numbers that aren't 2**n, though it is almost fixed
class MergeSort(BaseAlgorithm):
	name="Merge Sort"
	desc="Merges buckets until sorted"
	s=1#merge block size
	il=0#left bucket index
	ir=0#right bucket index
	def cycle(self,v=None):
		a=self.a
		if a==0:#new bucket with item 0
			if self.s>=self.l:
				if self.i==2:
					return (FIN,)
				else:
					self.i+=1
					return (DEL_BUCK,1)
			self.a=1
			self.il=1
			if self.f:
				return (BUCKINSERT,self.i,0,0,1)
			else:
				return (NEW_BUCK,self.i,0)
		elif a==1:#fill left bucket,then create new bucket with item 0
			if self.il==self.s:
				self.il=0
				self.a=2
				self.ir=1
				if self.f:
					return (BUCKINSERT,self.i,0,0,2)
				else:
					self.f=True
					return (NEW_BUCK,self.i,0)
			elif self.il>self.s:
				raise Exception("MergeSort: il unexpectedly bigger than s in s1")
			else:
				self.il+=1
				return (BUCKINSERT,self.i,0,self.il-1,1)
		elif a==2:#fill right bucket, then read first item of left bucket
			if self.ir==self.s:
				self.ir=0
				self.a=3
				return (READ,0,1)
			elif self.ir>self.s:
				raise Exception("MergeSort: ir unexpectedly bigger than s in a2")
			else:
				self.ir+=1
				return (BUCKINSERT,self.i,0,self.ir-1,2)
		elif a==3:#stores in v1, then read first item of right bucket
			self.v1=v
			self.v2=None
			self.a=5
			return (READ,0,2)
		elif self.a==4:#reads ir if v2 is None, or il if v1 is none
			self.a=5
			if self.v1==None:
				return (READ,0,1)
			elif self.v2==None:
				return (READ,0,2)
			else:
				raise Exception("MergeSort: Unexpected call of a4 without v1 or v2 being empty")
		elif a==5:#stores in empty v, then insert first left item to i if v1 is smaller than v2, else insert first right item to i
			if self.v2==None:
				if v==None:
					self.a=6
					self.ir=1
					return self.cycle()
				self.v2=v
			elif self.v1==None:
				if v==None:
					self.a=6
					self.il=self.ir
					self.ir=2
					return self.cycle()
				self.v1=v
			self.a=4
			self.i+=1
			if self.v1<self.v2:
				self.v1=None
				self.il+=1
				return (BUCKINSERT,0,1,self.i-1,0)
			else:
				self.v2=None
				self.ir+=1
				return (BUCKINSERT,0,2,self.i-1,0)
		elif a==6:#dumps second bucket to i, then delete it
			if self.il==self.s:
				self.a=0
				if self.i>=self.l:
					self.s*=2
					self.i=0
				return self.cycle()
			elif self.il>self.s:
				raise Exception("Mergesort: il is unexpectedly bigger than s in a6")
			else:
				self.il+=1
				self.i+=1
				return (BUCKINSERT,0,self.ir,self.i-1,0)
		elif a==7:
			raise Exception("MergeSort: Unexpected cycle after finishing")

class BogoSort(BaseAlgorithm):
	name="Bogo Sort"
	desc="Randomizes the whole set, then checks if it's sorted"
	def cycle(self,v=None):
		a=self.a
		if a==0:#read item
			self.a=1
			return (READ,self.i,0)
		elif a==1:#store v1 and read item
			self.v1=v
			self.a=2
			self.i+=1
			return (READ,self.i,0)
		elif a==2:#store v2 and see below
			self.v2=v
			self.i+=1
			if self.v1>self.v2:#if not sorted
				self.a=3
				self.i=0
				return (SWAP,self.i,random.randrange(self.l),0)
			elif self.i==self.l:#if end of list is reached
				self.a=7
				return (FIN,)
			else:
				self.v1=self.v2
				return (READ,self.i,0)
		elif a==3:#randomize list, then read item and goto a1
			self.i+=1
			if self.i==self.l:
				self.a=1
				self.i=0
				return (READ,self.i,0)
			else:
				return (SWAP,self.i,random.randrange(self.l),0)
		elif a==7:
			raise Exception("BogoSort: Unexpected cycle after finishing")

class InsertionSort(BaseAlgorithm):
	name="InsertionSort"
	desc="Inserts first unsorted item into sorted subarray\nuntil no unsorted items remain"
	i2=0
	def cycle(self,v=None):
		a=self.a
		if a==0:
			self.a=1
			self.i+=1
			if self.i==self.l:
				return (FIN,)
			self.i2=self.i-1
			return (READ,self.i,0)
		elif a==1:
			self.a=2
			self.v1=v
			return (READ,self.i2,0)
		elif a==2:
			self.v2=v
			if self.v2<self.v1:
				self.a=0
				return (INSERT,self.i,self.i2+1,0)
			elif self.i2==0:
				self.a=0
				return (INSERT,self.i,self.i2,0)
			else:
				self.i2-=1
				return (READ,self.i2,0)

class InsertionSortOOP(BaseAlgorithm):
	name="InsertionSort OOP"
	desc="Inserts first unsorted item into sorted bucket\nuntil no unsorted items remain"
	i2=0
	def cycle(self,v=None):
		a=self.a
		if a==0:
			self.a=1
			return (NEW_BUCK,0,0)
		elif a==1:
			self.a=2
			self.i+=1
			if self.i==self.l:
				self.a=7
				return (DEL_BUCK,0)
			self.i2=self.i-1
			return (READ,0,0)
		elif a==2:
			self.a=3
			self.v1=v
			return (READ,self.i2,1)
		elif a==3:
			self.v2=v
			if self.v2<self.v1:
				self.a=1
				return (BUCKINSERT,0,0,self.i2+1,1)
			elif self.i2==0:
				self.a=1
				return (BUCKINSERT,0,0,self.i2,1)
			else:
				self.i2-=1
				return (READ,self.i2,1)
		elif a==7:
			return (FIN,)

class SelectionSort(BaseAlgorithm):
	name="SelectionSort"
	desc="Swaps the smalles unsorted item with the first unsorted item\nuntil the list is sorted."
	i=0
	i2=0
	i3=0
	def cycle(self,v=None):
		a=self.a
		if a==0:
			self.i2=self.i
			self.v1=None
			self.a=1
			return (READ,self.i2,0)
		elif a==1:
			if self.i+2==self.l:
				self.a=7
				return (FIN,)
			if self.v1==None or v<self.v1:
				self.v1=v
				self.i3=self.i2
			if self.i2+1==self.l:
				self.a=0
				self.i+=1
				return (SWAP,self.i-1,self.i3,0)
			else:
				self.i2+=1
				return (READ,self.i2,0)

class SelectionSortOOP(BaseAlgorithm):
	name="SelectionSort OOP"
	desc="Puts the smallest item in bucket 0 to the end of bucket 1\nuntil bucket 0 is empty."
	i=0
	i2=0
	i3=0
	def cycle(self,v=None):
		a=self.a
		if a==0:
			self.a=1
			return (NEW_BUCK,)
		elif a==1:
			self.i2=0
			self.v1=None
			self.a=2
			return (READ,self.i2,0)
		elif a==2:
			if self.i==self.l:
				self.a=7
				return (DEL_BUCK,0)
			if self.v1==None or v<self.v1:
				self.v1=v
				self.i3=self.i2
			if self.i2+self.i+1==self.l:
				self.a=1
				self.i+=1
				return (BUCKINSERT,self.i3,0,self.i-1,1)
			else:
				self.i2+=1
				return (READ,self.i2,0)
		elif a==7:
			return (FIN,)

class OddEvenSort(BaseAlgorithm):
	name="Odd-Even Sort"
	desc="Like bubble sort, but parallelalizable.\nToo bad that's not possible here."
	odd=False
	f=None
	def cycle(self,v=None):
		a=self.a
		if a==0:
			if self.i+1>=self.l:
				if self.f==True:
					return (7,)
				elif self.f==None:
					self.f=True
				else:
					self.f=None
				self.odd=not self.odd	#lol
				if self.odd:
					self.i=1
				else:
					self.i=0
			self.a=1
			return (READ,self.i,0)
		elif a==1:
			self.v1=v
			self.a=2
			return (READ,self.i+1,0)
		elif a==2:
			self.v2=v
			self.a=0
			self.i+=2
			if self.v1>self.v2:
				self.f=False
				return (SWAP,self.i-2,self.i-1,0)
			else:
				return self.cycle()

class RadixLSDB2(BaseAlgorithm):
	name="Radix LSD 2"
	desc="Sorts by least significant digit in base 2."
	maxb=2
	curb=1
	i1=0
	def cycle(self,v=None):
		a=self.a
		if a==0:
			if self.i==self.l:
				self.i=0
				self.i1=0
				self.curb*=2
			if self.curb>=self.maxb:
				return (FIN,)
			self.a=1
			return (READ,self.i,0)
		elif a==1:
			self.a=0
			self.i+=1
			while v>self.maxb:
				self.maxb*=2
			if v & self.curb:
				return self.cycle()
			else:
				self.i1+=1
				if self.i1==self.i:
					return self.cycle()
				else:
					return (INSERT,self.i-1,self.i1-1,0)

class RadixLSDB2OOP(BaseAlgorithm):
	name="Radix LSD 2 OOP"
	desc="Sorts by least significant digit in base 2 out of place."
	maxb=2
	curb=1
	i1=0
	i2=0
	def cycle(self,v=None):
		a=self.a
		if a==0:
			self.a=1
			return (NEW_BUCK,)
		elif a==1:
			self.a=2
			return (NEW_BUCK,)
		elif a==2:
			if self.i==self.l:
				self.i+=1
				self.a=4
				return self.cycle()
			if self.curb>=self.maxb:
				self.a=6
				return (DEL_BUCK,1)
			self.a=3
			return (READ,0,0)
		elif a==3:
			self.a=2
			self.i+=1
			while v>self.maxb:
				self.maxb*=2
			if v & self.curb:
				self.i1+=1
				return (BUCKINSERT,0,0,self.i1-1,1)
			else:
				self.i2+=1
				return (BUCKINSERT,0,0,self.i2-1,2)
		elif a==4:
			self.i-=1
			if self.i2>0:
				self.i2-=1
				return (BUCKINSERT,0,2,self.l-self.i,0)
			else:
				self.a=5
				self.i+=1
				return self.cycle()
		elif a==5:
			self.i-=1
			if self.i1>0:
				self.i1-=1
				return (BUCKINSERT,0,1,self.l-self.i,0)
			else:
				self.curb*=2
				self.a=2
				return self.cycle()
		elif a==6:
			self.a=7
			return (DEL_BUCK,1)
		elif a==7:
			return (FIN,)

class RadixLSDB4(BaseAlgorithm):
	name="Radix LSD 4"
	desc="Sorts by least significant digit in base 4."
	maxb=4
	curb=1
	i1=0
	i2=0
	i3=0
	def cycle(self,v=None):
		a=self.a
		if a==0:
			if self.i==self.l:
				self.i=0
				self.i1=0
				self.i2=0
				self.i3=0
				self.curb*=4
			if self.curb>=self.maxb:
				return (FIN,)
			self.a=1
			return (READ,self.i,0)
		elif a==1:
			while v>self.maxb:
				self.maxb*=4
			self.a=0
			self.i+=1
			if v & self.curb*2:
				self.i1+=1
				self.i2+=1
				if v & self.curb:
					self.i3+=1
					return (INSERT,self.i-1,self.i3-1,0)
				else:
					return (INSERT,self.i-1,self.i2-1,0)
			else:
				if v & self.curb:
					self.i1+=1
					return (INSERT,self.i-1,self.i1-1,0)
				else:
					return self.cycle()

class Reverser(BaseAlgorithm):
	name="Reverser"
	desc="reverses the set"
	def cycle(self,v=None):
		self.i+=1
		if self.i*2>=self.l:
			return (7,)
		else:
			return (SWAP,self.i-1,self.l-self.i,0)

class Shuffler(BaseAlgorithm):
	name="Shuffler"
	desc="Shuffles the list"
	def cycle(self,v=None):
		self.i+=1
		if self.i+1==self.l:
			self.a=7
			return (FIN,)
		else:
			return (SWAP,self.i-1,random.randrange(self.l),0)

class ShufflerOneSide(BaseAlgorithm):
	name="One-Sided Shuffler"
	desc="Shuffles the list one-sided\n(not 100% random)"
	def cycle(self,v=None):
		self.i+=1
		if self.i+1==self.l:
			self.a=7
			return (FIN,)
		else:
			return (SWAP,self.i-1,random.randrange(self.i,self.l),0)

class ShufflerInsert(BaseAlgorithm):
	name="Shuffler"
	desc="Shuffles the list by inserting\n(pretty bad)"
	def cycle(self,v=None):
		self.i+=1
		if self.i==self.l:
			self.a=7
			return (FIN,)
		else:
			return (INSERT,self.i-1,random.randrange(self.l),0)

class ShufflerOneSideInsert(BaseAlgorithm):
	name="Shuffler"
	desc="Shuffles the list one-sided by inserting\n(very,very bad)"
	def cycle(self,v=None):
		self.i+=1
		if self.i+1==self.l:
			self.a=7
			return (FIN,)
		else:
			return (INSERT,self.i-1,random.randrange(self.i+1,self.l),0)

shufflers=[ShufflerOneSideInsert,ShufflerInsert,ShufflerOneSide,Shuffler]#shufflers from worst to best
algs=[BubbleSort,InsertionSort,InsertionSortOOP,SelectionSort,SelectionSortOOP,OddEvenSort,RadixLSDB2,RadixLSDB2OOP,RadixLSDB4,MergeSort,BogoSort]
