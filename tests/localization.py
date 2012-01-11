import systemetric
from systemetric.mapping.arenamaps import S007ArenaMap

def main():
	allTokens = {}

	R = systemetric.Robot()
	arenaMap = S007ArenaMap()
	while True:
		vision = R.see().processed()
		#print markers.tokens
		#print len(markers), markers
		transform = arenaMap.estimatePositionFrom(vision)
		if transform:
			for token in vision.tokens:
				#Transform the token to object space
				token.transform(transform)
				#Update it's position
				allTokens[token.code] = token
			
			#Print out the location of ALL THE TOKENS
			print [token.center for token in vision.tokens]
