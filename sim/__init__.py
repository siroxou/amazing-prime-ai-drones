"""Simulator for truck-launched delivery drone fleets.

Pure Python + numpy. city.py builds the 3D city (streets, ZIP codes, zones, the
distribution centre, hills, houses, apartments, overhead lines, cranes and towers),
airspace.py holds its no-fly zones, and geometry.py answers raycasts and contact checks
against it. world.py, vehicle.py and traffic.py come from self-driving-optimized and
drive the truck. Drone dynamics come later, see ROADMAP.md.
"""
