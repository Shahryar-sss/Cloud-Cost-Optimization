class Host:

    def __init__(self, id, availableRam, bw, storage, mips):
        self.id = id
        self.availableRam = availableRam
        self.bw = bw
        self.storage = storage
        self.mips = mips

    def getId(self):
        return self.id

    def getAvailableRam(self):
        return self.availableRam

    def setAvailableRam(self, availableRam):
        self.availableRam = availableRam