def calculate_score(pitch, mfcc, energy, phoneme_score):

    # Normalize pitch (example range 50–300 Hz)
    pitch_score = min(max((pitch - 50) / (300 - 50), 0), 1)

    # Normalize mfcc (approx range -500 to 500)
    mfcc_score = min(max((mfcc + 500) / 1000, 0), 1)

    
    energy_score = min(max(energy, 0), 1)

    total = (
        0.3 * pitch_score +
        0.3 * mfcc_score +
        0.2 * energy_score +
        0.2 * phoneme_score
    )

    return round(total * 100, 2)