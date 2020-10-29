import datetime

# World Records
def worldRecord(file):
    if 'ROWWSCULL1-L' in file:
        WR = datetime.timedelta(minutes=7,seconds=24.46) # LW1x
    elif 'ROWWSCULL1' in file:
        WR = datetime.timedelta(minutes=7,seconds=7.71) # W1x
    elif 'ROWMSCULL1-L' in file:
        WR = datetime.timedelta(minutes=6,seconds=41.03) # LM1x
    elif 'ROWMSCULL1' in file:
        WR = datetime.timedelta(minutes=6,seconds=30.74) # M1x
    elif 'ROWWNOCOX2-L' in file:
        WR = datetime.timedelta(minutes=7,seconds=18.32) # LW2-
    elif 'ROWWNOCOX2' in file:
        WR = datetime.timedelta(minutes=6,seconds=49.08) # W2-
    elif 'ROWMNOCOX2-L' in file:
        WR = datetime.timedelta(minutes=6,seconds=22.91) # LM2-
    elif 'ROWMNOCOX2' in file:
        WR = datetime.timedelta(minutes=6,seconds=8.5) # M2-
    elif 'ROWMCOXED2' in file:
        WR = datetime.timedelta(minutes=6,seconds=33.26) # M2+
    elif 'ROWWSCULL2-L' in file:
        WR = datetime.timedelta(minutes=6,seconds=47.69) # LW2x
    elif 'ROWWSCULL2' in file:
        WR = datetime.timedelta(minutes=6,seconds=37.31) # W2x
    elif 'ROWMSCULL2-L' in file:
        WR = datetime.timedelta(minutes=6,seconds=5.36) # LM2x
    elif 'ROWMSCULL-2' in file:
        WR = datetime.timedelta(minutes=5,seconds=59.72) # M2x
    elif 'ROWWNOCOX4-L' in file:
        WR = datetime.timedelta(minutes=6,seconds=36.4) # LW4-
    elif 'ROWWNOCOX4' in file:
        WR = datetime.timedelta(minutes=6,seconds=14.36) # W4-
    elif 'ROWMNOCOX4-L' in file:
        WR = datetime.timedelta(minutes=5,seconds=43.16) # LM4-
    elif 'ROWMNOCOX4' in file:
        WR = datetime.timedelta(minutes=5,seconds=37.86) # M4-
    elif 'ROWMCOXED4' in file:
        WR = datetime.timedelta(minutes=5,seconds=58.96) # M4+
    elif 'ROWWCOXED4' in file:
        WR = datetime.timedelta(minutes=6,seconds=43.86) # W4+
    elif 'ROWMSCULL4-L' in file:
        WR = datetime.timedelta(minutes=5,seconds=42.75) # LM4x
    elif 'ROWMSCULL4' in file:
        WR = datetime.timedelta(minutes=5,seconds=32.26) # M4x
    elif 'ROWWSCULL4-L' in file:
        WR = datetime.timedelta(minutes=6,seconds=15.95) # LW4x
    elif 'ROWWSCULL4' in file:
        WR = datetime.timedelta(minutes=6,seconds=6.84) # W4x
    elif 'ROWMCOXED8-L' in file:
        WR = datetime.timedelta(minutes=5,seconds=30.24) # LM8+
    elif 'ROWMCOXED8' in file:
        WR = datetime.timedelta(minutes=5,seconds=18.68) # M8+
    elif 'ROWWCOXED8' in file:
        WR = datetime.timedelta(minutes=5,seconds=54.16) # W8+
    else:
        WR = None

    return WR
