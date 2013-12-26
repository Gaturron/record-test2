from textgrid import TextGrid, Tier

def duration(textgrid):
    res = float(0)
    for i, tier in enumerate(textgrid):
        if tier.nameid == 'words':
            for row in tier.simple_transcript:
                if row[2] != 'sil' and row[2] != 'sp':
                    res += float(row[1]) - float(row[0])
                print row
    print 'resultado: '+str(res)
    return res

def dummy(textgrid):
    return '8'