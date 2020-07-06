class Scales(object):
    # Major Keys
    C_MAJOR = {"label": "C_major", "scale": ['C', 'D', 'E', 'F', 'G', 'A', 'B']}
    CSHARP_MAJOR = {"label": "C#_major", "scale": ['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#']}
    Db_MAJOR = {"label": "Db_major", "scale": ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C']}
    D_MAJOR = {"label": "D_major", "scale": ['D', 'E', 'F#', 'G', 'A', 'B', 'C#']}
    DSHARP_MAJOR = {"label": "D#_major", "scale": ['D#', 'E#', 'F##', 'G#', 'A#', 'B#', 'C##']}
    Eb_MAJOR = {"label": "Eb_major", "scale": ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D']}
    E_MAJOR = {"label": "E_major", "scale": ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#']}
    F_MAJOR = {"label": "F_major", "scale": ['F', 'G', 'A', 'Bb', 'C', 'D', 'E']}
    FSHARP_MAJOR = {"label": "F#_major", "scale": ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#']}
    Gb_MAJOR = {"label": "Gb_major", "scale": ['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F']}
    G_MAJOR = {"label": "G_major", "scale": ['G', 'A', 'B', 'C', 'D', 'E', 'F#']}
    GSHARP_MAJOR = {"label": "G#_major", "scale": ['G#', 'A#', 'B#', 'C#', 'D#', 'E#', 'F##']}
    Ab_MAJOR = {"label": "Ab_MAJOR", "scale": ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G']}
    A_MAJOR = {"label": "A_MAJOR", "scale": ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#']}
    Bb_MAJOR = {"label": "Bb_major", "scale": ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A']}
    B_MAJOR = {"label": "B_major", "scale": ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#']}

    # Natural Minor Keys
    A_NATRUAL_MINOR = {"label": "A_natural_minor", "scale": ['A', 'B', 'C', 'D', 'E', 'F', 'G']}
    Bb_NATRUAL_MINOR = {"label": "Bb_natural_minor", "scale": ['Bb', 'C', 'D', 'E', 'F', 'G']}
    B_NATRUAL_MINOR = {"label": "B_natural_minor", "scale": ['A', 'B', 'C', 'D', 'E', 'F', 'G']}
    C_NATRUAL_MINOR = {"label": "C_natural_minor", "scale": ['A', 'B', 'C', 'D', 'E', 'F', 'G']}
    Db_NATRUAL_MINOR = {"label": "Dd_natural_minor", "scale": ['A', 'B', 'C', 'D', 'E', 'F', 'G']}
    D_NATRUAL_MINOR = {"label": "D_natural_minor", "scale": ['A', 'B', 'C', 'D', 'E', 'F', 'G']}
    Eb_NATRUAL_MINOR = {"label": "Eb_natural_minor", "scale": ['A', 'B', 'C', 'D', 'E', 'F', 'G']}
    E_NATRUAL_MINOR = {"label": "E_natural_minor", "scale": ['A', 'B', 'C', 'D', 'E', 'F', 'G']}
    F_NATRUAL_MINOR = {"label": "F_natural_minor", "scale": ['A', 'B', 'C', 'D', 'E', 'F', 'G']}
    Gb_NATRUAL_MINOR = {"label": "Gb_natural_minor", "scale": ['A', 'B', 'C', 'D', 'E', 'F', 'G']}
    G_NATRUAL_MINOR = {"label": "G_natural_minor", "scale": ['A', 'B', 'C', 'D', 'E', 'F', 'G']}
    Ab_NATRUAL_MINOR = {"label": "Ab_natural_minor", "scale": ['A', 'B', 'C', 'D', 'E', 'F', 'G']}

    # Modes
    # Key of C
    D_DORIAN = {"label": "D_Dorian", "scale": ['D', 'E', 'F', 'G', 'A', 'B', 'C']}
    E_PHRYGIAN = {"label": "E_Phrygian", "scale": ['E', 'F', 'G', 'A', 'B', 'C', 'D']}
    F_LYDIAN = {"label": "F_Lydian", "scale": ['F', 'G', 'A', 'B', 'C', 'D', 'E']}
    G_MIXOLYDIAN = {"label": "G_MixoLydian", "scale": ['G', 'A', 'B', 'C', 'D', 'E', 'F']}
    A_AEOLIAN = {"label": "A_Aeolian", "scale": ['A', 'B', 'C', 'D', 'E', 'F', 'G']}
    B_LOCRIAN = {"label": "B_Locrian", "scale": ['B', 'C', 'D', 'E', 'F', 'G', 'A']}

    # Key of Bb
    C_DORIAN = {"label": "C_Dorian", "scale": ['C', 'D', 'Eb', 'F', 'G', 'A', 'Bb']}
    D_PHRYGIAN = {"label": "D_Phrygian", "scale": ['D', 'Eb', 'F', 'G', 'A', 'Bb', 'C']}
    Eb_LYDIAN = {"label": "Eb_Lydian", "scale": ['Eb', 'F', 'G', 'A', 'Bb', 'C', 'D']}
    F_MIXOLYDIAN = {"label": "F_MixoLydian", "scale": ['F', 'G', 'A', 'Bb', 'C', 'D', 'Eb']}
    G_AEOLIAN = {"label": "G_Aeolian", "scale": ['G', 'A', 'Bb', 'C', 'D', 'Eb', 'F']}
    A_LOCRIAN = {"label": "A_Locrian", "scale": ['A', 'Bb', 'C', 'D', 'Eb', 'F', 'G']}

    A_HARMONIC_MINOR = {"label": "A_Harmonic_Minor", "scale": ['A', 'B', 'C', 'D', 'E', 'F', 'G#']}
    E_FIFTH_MODE_A_HARMONIC_MINOR = {"label": "E_Fifth_Mode_A_Harmonic_Minor", "scale": ['E', 'F', 'G#', 'A', 'B', 'C', 'D']}