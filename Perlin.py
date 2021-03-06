
import math, random

class vec2:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def dot(self, otherVec):
		return (self.x * otherVec.x) + (self.y * otherVec.y)

sqrt2 = math.sqrt(2)
	
gradientVectors = [ vec2(-1.0, 1.0), vec2(sqrt2 , 0.0) , vec2(1.0, -1.0), vec2(0.0, sqrt2), vec2(-sqrt2 , 0.0), vec2(1.0, 1.0), vec2(0.0 , -sqrt2), vec2(-1.0, -1.0)]
	
def lerp(first, second, by):
	return (first * by) + (second * (1 - by))

def fade(t):
	return t * t * t * (t *(t * 6 - 15) + 10)

class Perlin:

	def __init__(self, grid, seed=""):
		self.seed = [151,160,137,91,90,15,
		131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,
		190, 6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,
		88,237,149,56,87,174,20,125,136,171,168, 68,175,74,165,71,134,139,48,27,166,
		77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,
		102,143,54, 65,25,63,161, 1,216,80,73,209,76,132,187,208, 89,18,169,200,196,
		135,130,116,188,159,86,164,100,109,198,173,186, 3,64,52,217,226,250,124,123,
		5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,
		223,183,170,213,119,248,152, 2,44,154,163, 70,221,153,101,155,167, 43,172,9,
		129,22,39,253, 19,98,108,110,79,113,224,232,178,185, 112,104,218,246,97,228,
		251,34,242,193,238,210,144,12,191,179,162,241, 81,51,145,235,249,14,239,107,
		49,192,214, 31,181,199,106,157,184, 84,204,176,115,121,50,45,127,4,150,254,
		138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]
		if seed == "":
			random.seed()
		else:
			random.seed(seed)
		random.shuffle(self.seed)

		self.grid = grid

	def hash(self, x, y):
		return self.seed[(self.seed[x % 256] + y) % 256]

	def getGradient(self, x, y):
		return gradientVectors[self.hash(x, y) % 8]

	#Returns a value between 0.0 and 1.0
	def genNoise(self, x, y):
		return self.noise(x, y, self.grid)
		
	#Returns a value between 0.0 and 1.0
	def noise(self, x, y, grid):
		dim = grid

		blockX = math.floor(x / dim) #calculates local grid points
		blockY = math.floor(y / dim)

		x = (x % dim) / float(dim) #normalize x and y to these grid points
		y = (y % dim) / float(dim)

		#calculate all the necessary dot products
		dot1 = vec2(x, y).dot(self.getGradient(blockX, blockY))
		dot2 = vec2(x - 1, y).dot(self.getGradient(blockX + 1, blockY))
		dot3 = vec2(x - 1, y - 1).dot(self.getGradient(blockX + 1, blockY + 1))
		dot4 = vec2(x, y - 1).dot(self.getGradient(blockX, blockY + 1))

		#lerp the results, add 1 and divide by 2 to adjust range
		return (lerp(lerp(dot3, dot4, fade(x)), lerp(dot2, dot1, fade(x)), fade(y)) + 1) / 2

	def octave(self, x, y, octaves, persistence):
		total = 0
		grid = self.grid
		amplitude = 1
		maxValue = 0
		for i in range(1, octaves + 1):
			total += self.noise(x, y, grid) * amplitude
			maxValue += amplitude

			grid /= 2
			amplitude *= persistence
		return total / maxValue