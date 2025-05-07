# Obtener umbrales para el modo principiante
def get_thresholds_beginner():

    _ANGLE_HIP_KNEE_VERT = {
        'NORMAL' : (0,  32),     # Ángulo normal entre cadera y rodilla
        'TRANS'  : (35, 65),     # Transición
        'PASS'   : (70, 95)      # Posición correcta (sentadilla completa)
    }    

    thresholds = {
        'HIP_KNEE_VERT': _ANGLE_HIP_KNEE_VERT,

        'HIP_THRESH'   : [10, 50],     # Umbrales para el movimiento de la cadera
        'ANKLE_THRESH' : 45,           # Ángulo mínimo en tobillo
        'KNEE_THRESH'  : [50, 70, 95], # Rangos de evaluación para la rodilla

        'OFFSET_THRESH'    : 35.0,     # Desviación máxima permitida
        'INACTIVE_THRESH'  : 15.0,     # Cuadros sin movimiento para considerar inactividad

        'CNT_FRAME_THRESH' : 50        # Cantidad de cuadros para validar la postura
    }

    return thresholds


# Obtener umbrales para el modo profesional
def get_thresholds_pro():

    _ANGLE_HIP_KNEE_VERT = {
        'NORMAL' : (0,  32),     # Ángulo normal entre cadera y rodilla
        'TRANS'  : (35, 65),     # Transición
        'PASS'   : (80, 95)      # Posición correcta (más exigente)
    }    

    thresholds = {
        'HIP_KNEE_VERT': _ANGLE_HIP_KNEE_VERT,

        'HIP_THRESH'   : [15, 50],     # Umbrales para el movimiento de la cadera
        'ANKLE_THRESH' : 30,           # Ángulo mínimo en tobillo (más estricto)
        'KNEE_THRESH'  : [50, 80, 95], # Rangos de evaluación para la rodilla

        'OFFSET_THRESH'    : 35.0,     # Desviación máxima permitida
        'INACTIVE_THRESH'  : 15.0,     # Cuadros sin movimiento para considerar inactividad

        'CNT_FRAME_THRESH' : 50        # Cantidad de cuadros para validar la postura
    }

    return thresholds