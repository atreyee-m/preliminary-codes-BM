deprels = []; #gov_dep = defaultdict(list); dep_dep = defaultdict(list)
        for i in root.findall('.//dependencies[@type="basic-dependencies"]/*'):
            ###############################################################################################
            #print(i.items()); print(i,i.items(),i.getchildren())
            #deprel_dict = dep rel:(governor,dependent)
            #self.deprel_dict[self.getDepID(i.attrib['type'])]=int(i[0].attrib['idx']),int(i[1].attrib['idx']) 
            #print(self.getDepID(i.attrib['type']))
            #self.other_dict[int(i[0].attrib['idx'])] = self.getDepID(i.attrib['type']),int(i[1].attrib['idx'])
            
            #with integer dependencies
            #self.governor_of[int(i[0].attrib['idx'])] = self.getDepID(i.attrib['type']),int(i[1].attrib['idx'])
            #self.dependent_of[int(i[1].attrib['idx'])] = self.getDepID(i.attrib['type']),int(i[0].attrib['idx'])
            ###
            
            #print(i.items())
#             self.gov_tup.append((int(i[0].attrib['idx']),i.attrib['type'],int(i[1].attrib['idx'])))
#             self.dep_tup.append((int(i[1].attrib['idx']),i.attrib['type'],int(i[0].attrib['idx'])))
            #self.governor_of[int(i[0].attrib['idx'])] = i.attrib['type'],int(i[1].attrib['idx'])
            #print(self.governor_of)
            #self.dependent_of[int(i[1].attrib['idx'])] = i.attrib['type'],int(i[0].attrib['idx'])
            #print(self.dependent_of)
            #print('--------------------------------')

        #print(self.governor_of)
            ###############################################################################################
            print(i[0].text,i[1].text)
            #self.governor_of[i[0].text]=(i.attrib['type'],i[1].text)
            #self.gov_list.append(self.governor_of.copy())
            #print(self.governor_of)
        
        #print(self.gov_list)
        #print(self.governor_of)
        # for i in self.gov_list:
        #     print(i)
        #
        # #print(self.gov_tup);print(self.dep_tup)
        # print('--------------------------------')
        #
        # #print(self.dependent_of)

        #return(self.consolidate(self.governor_of,self.dependent_of))
        return
    
    def lists(self,root):
        for i in root.findall('.//dependencies[@type="basic-dependencies"]/*'):
            
            self.gov_list.append(i[0].text)
            self.dep_list.append(i[1].text)
        #print(set(self.gov_list),set(self.dep_list))   
        
        self.gov_list = set(self.gov_list);self.dep_list = set(self.dep_list)
             
        return(self.gov_list,self.dep_list)
    
    def parseDeps(self,root):
        
        
        gov_lst,dep_lst = self.lists(root)
        l = []
        
        for i in root.findall('.//dependencies[@type="basic-dependencies"]/*'):
            if i[0].text in gov_lst:
                #print(i[0].text)
                #self.governor_of[i[0].text].append((i.attrib['type'],i[1].text))
               #print(self.governor_of)
                self.governor_of[i[0].text] = i.attrib['type'],i[1].text
                l.append(self.governor_of)
        
        print(l)
        
        
        return
