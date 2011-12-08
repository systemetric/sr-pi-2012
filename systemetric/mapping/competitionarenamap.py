class CompetitionArenaMap(ArenaMap):
	def __init__(self):
		ArenaMap.__init__(self, [
			{
				0: Vector2(1, 0),
				1: Vector2(2, 0), 
				2: Vector2(3, 0),
				3: Vector2(4, 0),
				4: Vector2(5, 0),
				5: Vector2(6, 0),
				6: Vector2(7, 0)
			},
			{
				7:  Vector2(8, 1),
				8:  Vector2(8, 2), 
				9:  Vector2(8, 3),
				10: Vector2(8, 4),
				11: Vector2(8, 5),
				12: Vector2(8, 6),
				13: Vector2(8, 7)
			},
			{
				14: Vector2(7, 8),
				15: Vector2(6, 8), 
				16: Vector2(5, 8),
				17: Vector2(4, 8),
				18: Vector2(3, 8),
				19: Vector2(2, 8),
				20: Vector2(1, 8)
			},
			{
				21: Vector2(0, 7),
				22: Vector2(0, 6), 
				23: Vector2(0, 5),
				24: Vector2(0, 4),
				25: Vector2(0, 3),
				26: Vector2(0, 2),
				27: Vector2(0, 1)
			}
		])