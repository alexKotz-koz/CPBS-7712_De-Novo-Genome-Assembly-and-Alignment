from components.readsToKmers import ReadsToKmers
class SearchString:
    def __init__(self, queryData, contigsIndexTable) -> None:
        self.queryData = queryData
        self.contigsIndexTable = contigsIndexTable
    
    def queryToKmers(self):
        pass

    # Hamming Distance not Smith waterman