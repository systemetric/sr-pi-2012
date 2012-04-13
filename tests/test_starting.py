from systemetric import Robot
from systemetric.map import Map
from tests.gui.maprenderer import MapRenderer
from systemetric.mapping.arenamaps import S007ArenaMap

def main(R):
	m = Map(arena=S007ArenaMap())
	mr = MapRenderer(m)
	mr.startInNewWindow()
	
	def whileLoading(R):
		while True:
			see = R.see()
			processed = see.processed()
			m.updateEntities(processed)

	R.executeUntilStart(whileLoading)
	R.power.beep(40, 3)