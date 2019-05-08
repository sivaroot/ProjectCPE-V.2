class Serie:

    IndexSerieSelected = -1

    def __init__(self,studyChildren):
        self.series = studyChildren

    def setSerieSelectedByIndex(self,index):
        Serie.IndexSerieSelected = index

    def getIndexSerieSelected(self):
        return Serie.IndexSerieSelected

    def getSeries(self):
        return self.series
    
    def getSerieChildren(self):
        if Serie.IndexSerieSelected  != -1:
            return self.series[Serie.IndexSerieSelected].children

    