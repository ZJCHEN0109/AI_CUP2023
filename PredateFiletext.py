import os
import re
class GetfileTxtContent:
    def __init__(self,File_text):
        self.my_File=File_text
        #print('\n接收到File')
        #print(self.my_File)
        #print(self.my_datafram)
        
    # 取得各種資訊類別函式庫    
    @classmethod
    def GetPatientInfo(self,my_File):
        # 提取患者信息
        patient_info_pattern = r"^(Lab No|D.O.B|Sex): (.+)$"
        patient_info = re.findall(patient_info_pattern, my_File, re.MULTILINE)
        patient_info = {key.strip(): value.strip() for key, value in patient_info}
        # 打印提取的信息
        #print("患者信息:")
        for key, value in patient_info.items():
            print(f"{key}: {value}") 
        return patient_info 
        
    @classmethod
    def GetIDMnum(self,my_File):
        # 取得ID訊息 例如[(36E107413X) 36E10741, 36E10741]
        IDNum_info_pattern = r'\d{2,12}\.[A-Za-z]{1,12}'
        IDNum_info_match = re.findall(IDNum_info_pattern, my_File, re.MULTILINE)      
        IDNum_info = IDNum_info_match[0].strip() if IDNum_info_match else "PHI: NULL"       
        IDNum_Identy=('PHI:MEDICALRECORD')
        GetIDNumPositions=self.Get_position(IDNum_info,my_File)
        ALL_Info=IDNum_info,GetIDNumPositions[2],GetIDNumPositions[3],IDNum_Identy       
        IDNum_info_dict={'IDMnum':ALL_Info}
        return IDNum_info_dict,GetIDNumPositions,IDNum_Identy    

    @classmethod
    def GetIDnum(cls, my_File):
        IDNum_info_pattern = r'(\d+[A-Za-z]+\d+[A-Za-zU]?)|(\d+[A-Za-z]+\d+)'
        IDNum_info_match = re.findall(IDNum_info_pattern, my_File, re.MULTILINE)
        if IDNum_info_match:
            IDNum_info = IDNum_info_match[0][0].strip() if IDNum_info_match[0][0] else IDNum_info_match[0][1].strip()
            IDNum_Identy = ('PHI:MEDICALRECORD')
            GetIDNumPositions = cls.Get_position(IDNum_info, my_File)
            ALL_Info = IDNum_info, GetIDNumPositions[2], GetIDNumPositions[3], IDNum_Identy
            IDNum_info_dict = {'IDnum': ALL_Info}
            return IDNum_info_dict, GetIDNumPositions, IDNum_Identy
        
    @classmethod
    def GetSPRno(self,my_File):
        SPRno_info_pattern = r"SPR no:([^\n]+)" or r'SPRID\n([^\n]+)'
        SPRno_info_match = re.search(SPRno_info_pattern, my_File, re.MULTILINE | re.DOTALL)
        SPRno_info = SPRno_info_match.group(1).strip() if SPRno_info_match else "PHI: NULL"
        SPRno_Identy = ('PHI:MEDICALRECORD')
        GetSPRnoPositions = self.Get_position(SPRno_info, my_File)
        ALL_Info = SPRno_info, GetSPRnoPositions[2], GetSPRnoPositions[3], SPRno_Identy        
        SPRno_info_dict={'SPR_no': ALL_Info}          
        #print("\nSPR 編號:")
        #print(diagnosis_info)
        return SPRno_info_dict,GetSPRnoPositions,SPRno_Identy

    @classmethod
    def GetSPRID(self,my_File):
        SPRID_info_pattern = r'SPRID\n([^\n]+)'
        SPRID_info_match = re.search(SPRID_info_pattern, my_File, re.MULTILINE | re.DOTALL)
        SPRID_info = SPRID_info_match.group(1).strip() if SPRID_info_match else "PHI: NULL"
        SPRID_Identy = ('PHI:MEDICALRECORD')
        GetSPRIDPositions = self.Get_position(SPRID_info, my_File)
        ALL_Info = SPRID_info, GetSPRIDPositions[2], GetSPRIDPositions[3], SPRID_Identy        
        SPRID_info_dict={'SPRID': ALL_Info}          
        #print("\nSPR 編號:")
        #print(diagnosis_info)
        return SPRID_info_dict,GetSPRIDPositions,SPRID_Identy
    
    @classmethod
    def GetMRNNo(self,my_File):
        MRNNo_info_pattern = r"MRN no:([^\n]+)"
        MRNNo_info_match = re.search(MRNNo_info_pattern, my_File, re.MULTILINE | re.DOTALL)
        MRNNo_info = MRNNo_info_match.group(1).strip() if MRNNo_info_match else "PHI: NULL"
        MRNNo_Identy = ('PHI:MEDICALRECORD')
        GetMRNNoPositions = self.Get_position(MRNNo_info, my_File)
        ALL_Info = MRNNo_info, GetMRNNoPositions[2], GetMRNNoPositions[3], MRNNo_Identy                
        MRNNo_info_dict={'MRN_no': ALL_Info}        
        #print("\nMRN 號碼:")
        #print(diagnosis_info)
        return MRNNo_info_dict,GetMRNNoPositions,MRNNo_Identy

    @classmethod
    def GetMRN(self,my_File):
        MRN_info_pattern = r"MRN\n([^\n]+)"
        MRN_info_match = re.search(MRN_info_pattern, my_File, re.MULTILINE | re.DOTALL)
        MRN_info = MRN_info_match.group(1).strip() if MRN_info_match else "PHI: NULL"
        MRN_Identy = ('PHI:MEDICALRECORD')
        GetMRNPositions = self.Get_position(MRN_info, my_File)
        ALL_Info = MRN_info, GetMRNPositions[2], GetMRNPositions[3], MRN_Identy                
        MRN_info_dict={'MRN': ALL_Info}        
        return MRN_info_dict,GetMRNPositions,MRN_Identy    
    
    
    @classmethod
    def GetPatientname(self,my_File):
        name_pattern = r"([A-Z]{1,10}\w,\s*[A-Z]{1,8})" or "([A-Z]{1,10}\w,\s*[A-Z]{1,8}+\s*[^\n]+?)"
        # 使用正则表达式搜索姓名
        #name_matches = re.findall(name_pattern, my_File)
        PTname_search_match = re.search(name_pattern, my_File, re.MULTILINE | re.DOTALL) # 提取姓名（通常是第一个匹配项）
        #print(PTname_search_match)
        PTname_Info =PTname_search_match.group(1) if PTname_search_match else "PHI: NULL"
        PTname_Identy=('PHI:PATIENT')
        GetPTNamePositions=self.Get_position(PTname_Info,my_File)
        ALL_Info=PTname_Info,GetPTNamePositions[2],GetPTNamePositions[3],PTname_Identy
        PTname_dict={'PATIENT':ALL_Info}  # 提取姓名（通常是第一个匹配项）        
        return PTname_dict,PTname_Info,PTname_Identy

    @classmethod
    def GetName(self,my_File):
        name_pattern = r"Name:([^\n]+)[^\n]" 
        # 使用正则表达式搜索姓名
        #name_matches = re.findall(name_pattern, my_File)
        Firstname_search_match = re.search(name_pattern, my_File, re.MULTILINE | re.DOTALL) # 提取姓名（通常是第一个匹配项）
        Firstname_Info =Firstname_search_match.group(1) if Firstname_search_match else "PHI: NULL"
        Firstname_Identy=('PHI:PATIENT')
        GetFirstNamePositions=self.Get_position(Firstname_Info,my_File)
        ALL_Info=Firstname_Info,GetFirstNamePositions[2],GetFirstNamePositions[3],Firstname_Identy
        Firstname_Info_dict={'Name':ALL_Info}  # 提取姓名（通常是第一个匹配项）        
        return Firstname_Info_dict,Firstname_Info,Firstname_Identy     
    
    @classmethod
    def GetFirsname(self,my_File):
        name_pattern = r"FirstName\n([a-zA-Z]+)[^\n]" 
        # 使用正则表达式搜索姓名
        #name_matches = re.findall(name_pattern, my_File)
        Firstname_search_match = re.search(name_pattern, my_File, re.MULTILINE | re.DOTALL) # 提取姓名（通常是第一个匹配项）
        Firstname_Info =Firstname_search_match.group(1) if Firstname_search_match else "PHI: NULL"
        Firstname_Identy=('PHI:PATIENT')
        GetFirstNamePositions=self.Get_position(Firstname_Info,my_File)
        ALL_Info=Firstname_Info,GetFirstNamePositions[2],GetFirstNamePositions[3],Firstname_Identy
        Firstname_Info_dict={'FirstName':ALL_Info}  # 提取姓名（通常是第一个匹配项）        
        return Firstname_Info_dict,Firstname_Info,Firstname_Identy,Firstname_Info 

    @classmethod
    def GetMiddlename(self,my_File):
        name_pattern = r"MiddleName\n([a-zA-Z]+)[^\n]" 
        # 使用正则表达式搜索姓名
        Middlename_search_match = re.search(name_pattern, my_File, re.MULTILINE | re.DOTALL) # 提取姓名（通常是第一个匹配项）
        Middlename_Info =Middlename_search_match.group(1) if Middlename_search_match else "PHI: NULL"
        Middlename_Identy=('PHI:PATIENT')
        GetMiddlenamePositions=self.Get_position(Middlename_Info,my_File)
        ALL_Info=Middlename_Info,GetMiddlenamePositions[2],GetMiddlenamePositions[3],Middlename_Identy
        Middlename_Info_dict={'MiddleName':ALL_Info}  # 提取姓名（通常是第一个匹配项）        
        return Middlename_Info_dict,Middlename_Info,Middlename_Identy,Middlename_Info  
    
    @classmethod
    def GetLastname(self,my_File):
        name_pattern = r"LastName\n([a-zA-Z]+)[^\n]" 
        # 使用正则表达式搜索姓名
        #name_matches = re.findall(name_pattern, my_File)
        Lastname_search_match = re.search(name_pattern, my_File, re.MULTILINE | re.DOTALL) # 提取姓名（通常是第一个匹配项）
        Lastname_Info =Lastname_search_match.group(1) if Lastname_search_match else "PHI: NULL"
        Lastname_Identy=('PHI:PATIENT')
        GetLastNamePositions=self.Get_position(Lastname_Info,my_File)
        ALL_Info=Lastname_Info,GetLastNamePositions[2],GetLastNamePositions[3],Lastname_Identy
        Lastname_Info_dict={'LastName':ALL_Info}  # 提取姓名（通常是第一个匹配项）        
        return Lastname_Info_dict,Lastname_Info,Lastname_Identy,Lastname_Info     
    
    @classmethod
    def GetDRname(self,my_File):
        # 定义正则表达式模式来匹配姓名
        name_pattern = r'DR\s([^()]*?)(?:\n|$)'
        # 使用正则表达式搜索姓名
        Drname_search_match = re.search(name_pattern, my_File, re.MULTILINE | re.DOTALL) 
        Drname_Info =Drname_search_match.group(1) if  Drname_search_match else "PHI: NULL"
        Drname_Identy=('PHI:DOCTOR')
        GetDOCPositions=self.Get_position(Drname_Info,my_File)        
        ALL_Info=Drname_Info,GetDOCPositions[2],GetDOCPositions[3],Drname_Identy
        DR_name_dict={'DR':ALL_Info}  # 提取姓名（通常是第一个匹配项）
        return DR_name_dict,Drname_Info,Drname_Identy                 

    @classmethod
    def GetDoctorname(self,my_File):
        # 定义正则表达式模式来匹配姓名
        name_pattern = r'MICROSCOPIC: ([^\n]+)'
        # 使用正则表达式搜索姓名
        Drname_search_match = re.search(name_pattern, my_File, re.MULTILINE | re.DOTALL) 
        Drname_Info =Drname_search_match.group(1) if  Drname_search_match else "PHI: NULL"
        Drname_Identy=('PHI:DOCTOR')
        GetDOCPositions=self.Get_position(Drname_Info,my_File)        
        ALL_Info=Drname_Info,GetDOCPositions[2],GetDOCPositions[3],Drname_Identy
        DR_name_dict={'Doctorname':ALL_Info}  # 提取姓名（通常是第一个匹配项）
        return DR_name_dict,Drname_Info,Drname_Identy      
    
    @classmethod
    def GetDOB(self,my_File):
        DOB_info_pattern=r"D.O.B: ([^\n]+)"
        DOB_info_match = re.search(DOB_info_pattern, my_File, re.MULTILINE)
        DOB_info = DOB_info_match.group(1).strip() if DOB_info_match else "PHI: NULL"
        GetDOBPositions=self.Get_position(DOB_info,my_File)
        # DOB_Identy={'PHI':'DATE'}
        DOB_Identy=('PHI:DATE')        
        ALL_Info=DOB_info,GetDOBPositions[2],GetDOBPositions[3],DOB_Identy
        DOB_info_dict={'D.O.B':ALL_Info}
        return DOB_info_dict,DOB_info,DOB_Identy    
    
    @classmethod
    def GetDateOfBirth(self,my_File):
        name_pattern = r"DateOfBirth\n([0-9]+)" 
        # 使用正则表达式搜索姓名
        #name_matches = re.findall(name_pattern, my_File)
        DateOfBirth_search_match = re.search(name_pattern, my_File, re.MULTILINE | re.DOTALL)
        DateOfBirth_Info =DateOfBirth_search_match.group(1) if DateOfBirth_search_match else "PHI: NULL"
        DateOfBirth_Identy=('PHI:DATE')
        GetDateOfBirthPositions=self.Get_position(DateOfBirth_Info,my_File)
        ALL_Info=DateOfBirth_Info,GetDateOfBirthPositions[2],GetDateOfBirthPositions[3],DateOfBirth_Identy
        DateOfBirth_Info_dict={'DateOfBirth':ALL_Info}         
        return DateOfBirth_Info_dict,DateOfBirth_Info,DateOfBirth_Identy        
                    
    @classmethod
    def Sex_info(self,my_File):
        Sex_info_pattern=r"Sex: ([^\n]+)"
        Sex_info_match = re.search(Sex_info_pattern, my_File, re.MULTILINE)
        Sex_info = Sex_info_match.group(1).strip() if Sex_info_match else "PHI: NULL"
        GetSexPositions=self.Get_position(Sex_info,my_File)
        Sex_Idemty=('PHI:Sex')        
        ALL_Info=Sex_info,GetSexPositions[2],GetSexPositions[3],Sex_Idemty        
        Sex_info_dict={'Sex':ALL_Info}        
        #print("\n性別:")
        return Sex_info_dict,Sex_info,Sex_Idemty        

    @classmethod
    def GetGender(self,my_File):
        Sex_info_pattern=r"Gender\n([a-zA-Z]+)"
        Sex_info_match = re.search(Sex_info_pattern, my_File, re.MULTILINE)
        Sex_info = Sex_info_match.group(1).strip() if Sex_info_match else "PHI: NULL"
        GetSexPositions=self.Get_position(Sex_info,my_File)
        Sex_Idemty=('PHI:Sex')        
        ALL_Info=Sex_info,GetSexPositions[2],GetSexPositions[3],Sex_Idemty        
        Sex_info_dict={'Gender':ALL_Info}        
        #print("\n性別:")
        return Sex_info_dict,Sex_info,Sex_Idemty        

    @classmethod
    def Collected_info(self,my_File):
        Collected_info_pattern=r"Collected: ([^\n]+)"
        Collected_info_match = re.search(Collected_info_pattern, my_File, re.MULTILINE)
        Collected_info = Collected_info_match.group(1).strip() if Collected_info_match else "PHI: NULL"
        # Collected_Identy=('PHI:DATE')
        GetCollPositions=self.Get_position(Collected_info,my_File)
        date_format2 = r"(\d{1,2}/\d{1,2}/\d{4}) at :"
        match2 = re.search(date_format2, Collected_info)
        if match2:
            Collected_Identy=('PHI:DATE')
        else:    
            Collected_Identy=('PHI:TIME')
        ALL_Info=Collected_info,GetCollPositions[2],GetCollPositions[3],Collected_Identy        
        Collected_info_dict={'Collected':ALL_Info}
        #print("\n收集日期:")
        return Collected_info_dict,Collected_info,Collected_Identy

    @classmethod
    def GetCollected(self,my_File):
        Collected_info_pattern=r"SpecimenReceivedDate\n([^\n]+)"
        Collected_info_match = re.search(Collected_info_pattern, my_File, re.MULTILINE)
        Collected_info = Collected_info_match.group(1).strip() if Collected_info_match else "PHI: NULL"
        Collected_Identy=('PHI:TIME')
        GetCollPositions=self.Get_position(Collected_info,my_File)        
        ALL_Info=Collected_info,GetCollPositions[2],GetCollPositions[3],Collected_Identy
        Collected_info_dict={'SpecimenReceivedDate':ALL_Info}        
        #print("\n收集日期:")
        return Collected_info_dict,Collected_info,Collected_Identy
        
    @classmethod
    def Location_info(self,my_File):
        Location_info_pattern=r"Location: ([^\n]+)"
        Location_info_match = re.search(Location_info_pattern, my_File, re.MULTILINE)
        Location_info = Location_info_match.group(1).strip() if Location_info_match else "PHI: NULL"
        GetLocatPositions=self.Get_position(Location_info,my_File)
        Location_Identify=('PHI:HOSPITAL')
        ALL_Info=Location_info,GetLocatPositions[2],GetLocatPositions[3],Location_Identify        
        Location_info_dict={'Location':ALL_Info}        
        #print("\n醫院地址:")
        return Location_info_dict,Location_info,Location_Identify

    @classmethod
    def GetSiteName(self,my_File):
        SiteName_info_pattern=r"SiteName\n([A-Z, -]+ [A-Z]+)"
        SiteName_info_match = re.search(SiteName_info_pattern, my_File, re.MULTILINE)
        SiteName_info = SiteName_info_match.group(1).strip() if SiteName_info_match else "PHI: NULL"
        GetSiteNamePositions=self.Get_position(SiteName_info,my_File)
        SiteName_Identify=('PHI:HOSPITAL')
        ALL_Info=SiteName_info,GetSiteNamePositions[2],GetSiteNamePositions[3],SiteName_Identify        
        SiteName_info_dict={'SiteName':ALL_Info}        
        #print("\n醫院地址:")
        return SiteName_info_dict,SiteName_info,SiteName_Identify
    
    @classmethod
    def SiteName_info(self,my_File):
        SiteName_info_pattern = r"Site_name:([A-Z, -]+ [A-Z]+)"
        SiteName_info_match = re.search(SiteName_info_pattern, my_File, re.MULTILINE | re.DOTALL)
        SiteName_info = SiteName_info_match.group(1).strip() if SiteName_info_match else "PHI: NULL"
        GetSiteNamePositions=self.Get_position(SiteName_info,my_File)        
        SiteName_Identify=('PHI:HOSPITAL')        
        ALL_Info=SiteName_info,GetSiteNamePositions[2],GetSiteNamePositions[3],SiteName_Identify                
        SiteName_info_dict={'Site_name': ALL_Info}          
        #print("\n機構名稱:")
        #print(diagnosis_info)
        return SiteName_info_dict,SiteName_info,SiteName_Identify       

    @classmethod
    def Specimen_info(self,my_File):
        Specimen_info_pattern=r"Specimen_type:\s*(.*)"
        Specimen_info_match = re.search(Specimen_info_pattern, my_File, re.MULTILINE)
        Specimen_info = Specimen_info_match.group(1).strip() if Specimen_info_match else "PHI: NULL"
        Specimen_info_dict={'Specimen':Specimen_info}                                                                
        #print("\n標本:")
        #print(Specimen_info)
        return Specimen_info_dict
    
    @classmethod
    def Distribution_info(self,my_File):
        Distribution_info_pattern=r"Distribution: ([^\n]+)"
        Distribution_info_match = re.search(Distribution_info_pattern, my_File, re.MULTILINE)
        Distribution_info = Distribution_info_match.group(1).strip() if Distribution_info_match else "PHI: NULL"
        Distribution_info_dict={'Distribution':Distribution_info}                                                        
        #print("\n資料描述:")
        #print(Distribution_info)
        return Distribution_info_dict          

    @classmethod
    def HISTORY_info(self,my_File):
        HISTORY_info_pattern=r'HISTORY:(.*?)MACROSCOPIC:'
        HISTORY_info_match = re.search(HISTORY_info_pattern, my_File, re.MULTILINE|re.DOTALL)
        HISTORY_info = HISTORY_info_match.group(1).strip() if HISTORY_info_match else "PHI: NULL"
        HISTORY_info_dict={'HISTORY':HISTORY_info}                                                                        
        #print("\n患者病史:")
        #print(Histological_info)
        return HISTORY_info_dict

    @classmethod
    def MACROSCOPIC_info(self,my_File):    
        MACROSCOPIC_info_pattern = r"^MACROSCOPIC(.+?):(.+?)(?=DIAGNOSIS|$)"
        MACROSCOPIC_info_match=re.search(MACROSCOPIC_info_pattern,my_File,re.MULTILINE | re.DOTALL)
        MACROSCOPIC_info=MACROSCOPIC_info_match.group(1).strip() if MACROSCOPIC_info_match else "PHI: NULL"
        MACROSCOPIC_info_dict={'MACROSCOPIC':MACROSCOPIC_info}                
        #print("\n宏觀訊息:")
        #print(MACROSCOPIC_info)
        return MACROSCOPIC_info_dict
        
    @classmethod
    def Immunohistochemistry_info(self,my_File):
        Immunohistochemistry_info_pattern=r'Immunohistochemistry:(.*?)COMMENT:'
        Immunohistochemistry_info_match = re.search(Immunohistochemistry_info_pattern, my_File, re.MULTILINE|re.DOTALL)
        Immunohistochemistry_info = Immunohistochemistry_info_match.group(1).strip() if Immunohistochemistry_info_match else "PHI: NULL"
        Immunohistochemistry_info_dict={'Immunohistochemistry':Immunohistochemistry_info}                                                      #print("\n免疫組織化學:")
        #print(Histological_info)
        return Immunohistochemistry_info_dict

    @classmethod
    def COMMENTS_info(self,my_File):    
        COMMENTS_info_pattern = r"^COMMENTS(.+?):(.+?)(?=DIAGNOSIS|$)"
        COMMENTS_info_match=re.search(COMMENTS_info_pattern,my_File,re.MULTILINE | re.DOTALL)
        COMMENTS_info=COMMENTS_info_match.group(1).strip() if COMMENTS_info_match else "PHI: NULL"
        COMMENTS_info_dict={'CLINICAL':COMMENTS_info}                
        #print("\n臨床診斷:")
        #print(MACROSCOPIC_info)
        return COMMENTS_info_dict    
        
    @classmethod
    def DIAGNOSIS_info(self,my_File):
        diagnosis_info_pattern = r"^DIAGNOSIS:(.+)$"
        diagnosis_info_match = re.search(diagnosis_info_pattern, my_File, re.MULTILINE | re.DOTALL)
        diagnosis_info = diagnosis_info_match.group(1).strip() if diagnosis_info_match else "PHI: NULL"
        diagnosis_info_dict={'DIAGNOSIS': diagnosis_info}          
        #print("\n診斷信息:")
        #print(diagnosis_info)
        return diagnosis_info_dict

    @classmethod
    def Get_position(self,match_text,my_File):
        #print('match_text:',match_text)
        info_pattern=match_text
        info_match = re.search(info_pattern,my_File, re.MULTILINE)
        match_info = info_match.group(0).strip() if info_match else "PHI: NULL"
        #print(match_info)          
        if info_match:
            start_position = info_match.start()
            end_position = info_match.end()
            #print("Match found at positions:", start_position, end_position)
            Matched_text = my_File[start_position:end_position]
            #print("Match content:",Matched_text)
        else:
            start_position = end_position = "PHI: NULL"
            Matched_text = "PHI: NULL"
            #print("No match found")
        #print('================\n')
        return info_match,Matched_text,start_position,end_position











    

























