class Recommender:
    try:
        import pandas as pd
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
    except Exception as e:
        print(e)
    def __init__(self,filename,show=False):
        self.df = self.pd.read_csv(filename)
        self.df = self.df.rename(columns={self.df.columns[0]:'title'})
        if show:
            print(self.df.head())
        
    def process(self,columns,replace_col):
        for i in range(len(columns)):
            temp = []
            for j in self.df[columns[i]].values:
                try:
                    temp.append(str(j).replace(replace_col[i],''))
                except Exception as e:
                    print(e)
                    temp.append(str(j))
            self.df[columns[i]] = temp
    
    def columns_to_select(self,columns):
        self.df["toUse"] = [" ".join([str(j) for j in self.df[columns].values[i]]) for i in range(self.df.shape[0])]
        
    def fit(self):
        self.count_vector = self.CountVectorizer().fit_transform(self.df["toUse"])
        from sklearn.metrics.pairwise import cosine_similarity
        self.cosine = cosine_similarity(self.count_vector)

    def recomend(self,movies,num):
        index = []
        movies_recomended = set()
        temp = []
        for i in movies:
            index.append(self.df[self.df['title']==i].index[0])
        for i in index:
            m = 0
            for j,k in sorted(enumerate(self.cosine[i]),key=lambda x:x[1],reverse=True):
                if j not in index:
                    m += 1
                    temp.append((j,k))
                    if m==num+1:break
        temp = sorted(temp,key=lambda x:x[1],reverse=True)
        i=0
        while len(movies_recomended)!=num and i<len(temp):
            movies_recomended.add(self.df['title'].values[temp[i][0]])
            i+=1
        return movies_recomended

    def save(self,filename):
        import numpy as np
        np.savez(filename,np.array(self.cosine))

    def load(self,filename,url=False):
        import numpy as np
        if url:
            import requests
            from io import BytesIO
            self.cosine = np.load(BytesIO(requests.get(filename,stream=True).raw.read()))['arr_0']
        else:
            self.cosine = np.load(filename)['arr_0']
