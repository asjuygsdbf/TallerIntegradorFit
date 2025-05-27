def get_thresholds_pushup_beginner():
    thresholds = {
        # Ángulos del codo
        'MIN_ELBOW_FLEXION_FOR_COUNT': 85,
        'MAX_ELBOW_EXTENSION_FOR_COUNT': 170,

        # Desviación máxima permitida en la alineación del cuerpo
        'MAX_FORM_DEVIATION_OFFSET': 0.20,

        # Umbrales auxiliares (opcional, para futuras mejoras)
        'INACTIVE_FRAMES_THRESH': 15,
        'POSTURE_HOLD_FRAMES_THRESH': 30
    }

    return thresholds
