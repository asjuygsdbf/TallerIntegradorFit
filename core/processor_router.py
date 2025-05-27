from core.process_squat import SquatProcessor
from core.process_pushup import PushUpProcessor

def get_processor(ejercicio: str, thresholds: dict, flip_frame: bool):
    if ejercicio == "sentadilla":
        return SquatProcessor(thresholds, flip_frame)
    elif ejercicio == "flexion":
        return PushUpProcessor(thresholds, flip_frame)
    elif ejercicio == "abdominal":
        raise NotImplementedError("Procesador de abdominales aún no implementado.")
    else:
        raise ValueError(f"Ejercicio no soportado: {ejercicio}")