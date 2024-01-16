from NTM import *
def genMixing(M:list):
    outputTree = genMix(M, len(M))
    outputTree = hda(outputTree)
    saveTree(outputTree, './OutputTree/hda.png')

if __name__ == "__main__":
    # ratio = input('mixing ratio: ')
    ratio = '19:15:15:15'
    M = [(f'r{i}', int(x)) for i, x in enumerate(ratio.split(':'))]
    genMixing(M)