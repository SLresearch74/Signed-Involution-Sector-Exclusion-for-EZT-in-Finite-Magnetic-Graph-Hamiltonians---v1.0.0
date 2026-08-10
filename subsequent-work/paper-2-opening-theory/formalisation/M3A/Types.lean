import Mathlib

namespace M3A

/-- The six states of the locked M3A model. -/
abbrev State := Fin 6

/-- The four internal vertices carrying diagonal perturbations. -/
abbrev Internal := Fin 4

/-- The selected input port. -/
def source : State := 0

/-- The selected output port. -/
def target : State := 5

end M3A
