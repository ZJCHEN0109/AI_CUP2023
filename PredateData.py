import os
import re
import spacy
class GetfileContent:   
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
            #print('================\n')
        return patient_info
        
    @classmethod
    def ID_num(self,my_File):
        # 取得ID訊息 例如['9856253.FWH', '2495622.MLH', '24Y56224', '8188283.GQQ', '81X82832', '6852578.MFH', '604912.UIW']
        IDNum_info_pattern = r'\d{2,12}\.[A-Za-z]{1,12}'
        IDNum_info_match = re.findall(IDNum_info_pattern, my_File, re.MULTILINE)      
        IDNum_info = IDNum_info_match[0].strip() if IDNum_info_match else "PHI: NULL"       
        IDNum_Identy=('PHI:MEDICALRECORD')
        GetIDNumPositions=self.Get_position(IDNum_info,my_File)
        ALL_Info=IDNum_info,GetIDNumPositions[2],GetIDNumPositions[3],IDNum_Identy       
        IDNum_info_dict={'MEDICALRECORD':ALL_Info}
        return IDNum_info_dict,GetIDNumPositions,IDNum_Identy
    
    @classmethod
    def Patientname(self,my_File):
        # name_pattern = r"([A-Z, -]+ [A-Z]+)"
        name_pattern =r"^([A-Za-z]+, [A-Za-z]+ [A-Za-z]+)" or "([A-Z, -]+ [A-Z]+)"
        # 使用正则表达式搜索姓名
        #name_matches = re.findall(name_pattern, my_File)
        PTname_search_match = re.search(name_pattern, my_File, re.MULTILINE | re.DOTALL) # 提取姓名（通常是第一个匹配项）
        PTname_Info =PTname_search_match.group(1) if PTname_search_match else "PHI: NULL"
        PTname_Identy=('PHI:PATIENT')
        GetPTNamePositions=self.Get_position(PTname_Info,my_File)
        ALL_Info=PTname_Info,GetPTNamePositions[2],GetPTNamePositions[3],PTname_Identy
        PTname_dict={'PATIENT':ALL_Info}  # 提取姓名（通常是第一个匹配项）        
        return PTname_dict,PTname_Info,PTname_Identy
        
    @classmethod
    def GetDRname(self,my_File):
        # 定义正则表达式模式来匹配姓名
        name_pattern = r'DR\s([^()]*?)(?:\n|$)'
        # 使用正则表达式搜索姓名
        Drname_search_match = re.search(name_pattern, my_File, re.MULTILINE | re.DOTALL) 
        Drname_Info =Drname_search_match.group(1) if  Drname_search_match else "PHI: NULL"
        #print('DR',Drname_Info)
        Drname_Identy=('PHI:DOCTOR')
        GetDOCPositions=self.Get_position(Drname_Info,my_File)        
        ALL_Info=Drname_Info,GetDOCPositions[2],GetDOCPositions[3],Drname_Identy
        DR_name_dict={'DR':ALL_Info}  # 提取姓名（通常是第一个匹配项）
        return DR_name_dict,Drname_Info,Drname_Identy

    @classmethod
    def EpisodeNoinfo(self,my_File):
        # 定義正則表達式來提取醫療信息
        EpisodeNo_pattern=r"Episode No: ([^\n]+)"
        EpisodeNo_search_match = re.search(EpisodeNo_pattern,my_File, re.MULTILINE)
        EpisodeNo_info = EpisodeNo_search_match.group(1).strip() if EpisodeNo_search_match else "PHI: NULL"
        EpisodeNo_Identy=('PHI:IDNUM')        
        GetEpiPositions=self.Get_position(EpisodeNo_info,my_File)
        ALL_Info=EpisodeNo_info,GetEpiPositions[2],GetEpiPositions[3],EpisodeNo_Identy
        EpisodeNo_dict={'Episode No':ALL_Info}        
        return EpisodeNo_dict,EpisodeNo_info,EpisodeNo_Identy

    @classmethod
    def LabNo_info(self,my_File):
        LabNo_info_pattern=r"Lab No: ([^\n]+)"
        LabNo_info_match = re.search(LabNo_info_pattern, my_File, re.MULTILINE)
        LabNo_info = LabNo_info_match.group(1).strip() if LabNo_info_match else "PHI: NULL"
        LabNo_Identy=('PHI:IDNUM')
        GetLabNoPositions=self.Get_position(LabNo_info,my_File)
        ALL_Info=LabNo_info,GetLabNoPositions[2],GetLabNoPositions[3],LabNo_Identy        
        LabNo_info_dict={'Lab No':ALL_Info}        
        #print("\n實驗室編號:")
        return LabNo_info_dict,LabNo_info,LabNo_Identy    

    @classmethod
    def DOB_info(self,my_File):
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
    def Collected_info(self,my_File):
        Collected_info_pattern=r"Collected: ([^\n]+)"
        Collected_info_match = re.search(Collected_info_pattern, my_File, re.MULTILINE)
        Collected_info = Collected_info_match.group(1).strip() if Collected_info_match else "PHI: NULL"
        GetCollPositions=self.Get_position(Collected_info,my_File)
        date_format2 = r"(\d{1,2}/\d{1,2}/\d{4}) at :"
        match2 = re.search(date_format2, Collected_info)
        if match2:
            Collected_Identy=('PHI:DATE')
        else:    
            Collected_Identy=('PHI:TIME')
        ALL_Info=Collected_info,GetCollPositions[2],GetCollPositions[3],Collected_Identy
        Collected_info_dict={'Collected':ALL_Info}       
        return Collected_info_dict,Collected_info_match,Collected_Identy

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
    def clinicalinfo(self,my_File):
        # 提取臨床信息
        clinical_info_pattern = r"^CLINICAL:(.+?)(?=MACROSCOPIC|$)"
        clinical_info_match = re.search(clinical_info_pattern, my_File, re.MULTILINE | re.DOTALL)
        clinical_info = clinical_info_match.group(1).strip() if clinical_info_match else "PHI: NULL"
        clinical_info_dict={'CLINICAL':clinical_info}        
        #print("\n臨床診斷:")
        return clinical_info_dict

    @classmethod
    def MACROSCOPIC_info(self,my_File):    
        # 提取宏觀訊息
        MACROSCOPIC_info_pattern = r"^MACROSCOPIC(.+?):(.+?)(?=DIAGNOSIS|$)"
        MACROSCOPIC_info_match=re.search(MACROSCOPIC_info_pattern,my_File,re.MULTILINE | re.DOTALL)
        MACROSCOPIC_info=MACROSCOPIC_info_match.group(1).strip() if MACROSCOPIC_info_match else "PHI: NULL"
        MACROSCOPIC_info_dict={'MACROSCOPIC':MACROSCOPIC_info}                
        #print("\n宏觀訊息:")
        return MACROSCOPIC_info_dict    
        
    @classmethod
    def Specimen_info(self,my_File):
        Specimen_info_pattern=r"Specimen: ([^\n]+)"
        Specimen_info_match = re.search(Specimen_info_pattern, my_File, re.MULTILINE)
        Specimen_info = Specimen_info_match.group(1).strip() if Specimen_info_match else "PHI: NULL"
        Specimen_info_dict={'Specimen':Specimen_info}                
        #print("\n標本:")
        return Specimen_info_dict           
        
    @classmethod
    def Distribution_info(self,my_File):
        Distribution_info_pattern=r"Distribution: ([^\n]+)"
        Distribution_info_match = re.search(Distribution_info_pattern, my_File, re.MULTILINE)
        Distribution_info = Distribution_info_match.group(1).strip() if Distribution_info_match else "PHI: NULL"
        Distribution_info_dict={'Distribution':Distribution_info}                                                        
        #print("\n資料描述:")
        return Distribution_info_dict
    
    @classmethod
    def Histological_type_info(self,my_File):
        Histological_info_pattern=r"Histological type: ([^\n]+)"
        Histological_info_match = re.search(Histological_info_pattern, my_File, re.MULTILINE)
        Histological_info = Histological_info_match.group(1).strip() if Histological_info_match else "PHI: NULL"
        Histological_info_dict={'Histological type':Histological_info}
        #print("\n組織類型:")
        return Histological_info_dict
        
    @classmethod
    def Tumour_location_info(self,my_File):        
        Tumour_location_info_pattern=r"Tumour location: ([^\n]+)"
        Tumour_location_info_match = re.search(Tumour_location_info_pattern, my_File, re.MULTILINE)
        Tumour_location_info = Tumour_location_info_match.group(1).strip() if Tumour_location_info_match else "PHI: NULL"
        Tumour_location_info_dict={'Tumour location':Tumour_location_info}
        #print("\n腫瘤位置:")
        return Tumour_location_info_dict
        
    @classmethod
    def Dominant_nodule_info(self,my_File):
        Dominant_nodule_info_pattern=r"Dominant nodule:(.*?)Gleason score:(.*?)\n"
        Dominant_nodule_info_match = re.search(Dominant_nodule_info_pattern, my_File, re.DOTALL)
        Dominant_nodule_info = Dominant_nodule_info_match.group(1).strip() if Dominant_nodule_info_match else "PHI: NULL"
        Dominant_nodule_info_dict={'Dominant nodule': Dominant_nodule_info}
        #print("\n主要節結:")
        return Dominant_nodule_info_dict
    
    @classmethod
    def Gleason_score_info(self,my_File):
        Gleason_score_info_pattern=r"Gleason score: ([^\n]+)"
        Gleason_score_info_match = re.search(Gleason_score_info_pattern, my_File, re.MULTILINE)
        Gleason_score_info = Gleason_score_info_match.group(1).strip() if Gleason_score_info_match else "PHI: NULL"
        Gleason_score_info_dict={'Gleason score': Gleason_score_info}        
        #print("\n格里森評分:")
        return Gleason_score_info_dict
    
    @classmethod
    def Extraprostatic_extension_info(self,my_File):
        Extraprostatic_extension_info_pattern=r"Extraprostatic extension: ([^\n]+)"
        Extraprostatic_extension_info_match = re.search(Extraprostatic_extension_info_pattern, my_File, re.MULTILINE)
        Extraprostatic_extension_info = Extraprostatic_extension_info_match.group(1).strip() if Extraprostatic_extension_info_match else "PHI: NULL"
        Extraprostatic_extension_info_dict={'Extraprostatic extension': Extraprostatic_extension_info}                
        #print("\n前列腺外擴展:")
        return Extraprostatic_extension_info_dict
        
    @classmethod
    def Surgical_margins_info(self,my_File):
        Surgical_margins_info_pattern=r"Surgical margins: ([^\n]+)"
        Surgical_margins_info_match = re.search(Surgical_margins_info_pattern, my_File, re.MULTILINE)
        Surgical_margins_info = Surgical_margins_info_match.group(1).strip() if Surgical_margins_info_match else "PHI: NULL"
        Surgical_margins_info_dict={'Surgical margins': Surgical_margins_info}                
        #print("\n手術切線:")
        return Surgical_margins_info_dict
    
    @classmethod
    def Perineural_invasion_info(self,my_File):
        Perineural_invasion_info_pattern=r"Perineural invasion: ([^\n]+)"
        Perineural_invasion_info_match = re.search(Perineural_invasion_info_pattern, my_File, re.MULTILINE)
        Perineural_invasion_info = Perineural_invasion_info_match.group(1).strip() if Perineural_invasion_info_match else "PHI: NULL"
        Perineural_invasion_info_dict={'Perineural invasion': Perineural_invasion_info}                        
        #print("\n神經周圍侵犯:")
        return Perineural_invasion_info_dict
        
    @classmethod
    def Seminal_vesicles_info(self,my_File):
        Seminal_vesicles_info_pattern=r"Seminal vesicles: ([^\n]+)"
        Seminal_vesicles_info_match = re.search(Seminal_vesicles_info_pattern,my_File, re.MULTILINE)
        Seminal_vesicles_info = Seminal_vesicles_info_match.group(1).strip() if Seminal_vesicles_info_match else "PHI: NULL"
        Seminal_vesicles_info_dict={'Seminal vesicles': Seminal_vesicles_info}                        
        #print("\n精囊:")
        return Seminal_vesicles_info_dict
    
    @classmethod
    def Lymph_odes_info(self,my_File):
        Lymph_odes_info_pattern=r"Lymph nodes: ([^\n]+)"
        Lymph_odes_info_match = re.search(Lymph_odes_info_pattern, my_File, re.MULTILINE)
        Lymph_odes_info = Lymph_odes_info_match.group(1).strip() if Lymph_odes_info_match else "PHI: NULL"
        Lymph_odes_info_dict={'Lymph nodes': Lymph_odes_info}                                
        #print("\n淋巴結:")
        return Lymph_odes_info_dict
    
    @classmethod
    def Lymphovascular_invasion_info(self,my_File):
        Lymphovascular_invasion_info_pattern=r"Lymphovascular invasion: ([^\n]+)"
        Lymphovascular_invasion_info_match = re.search(Lymphovascular_invasion_info_pattern, my_File, re.MULTILINE)
        Lymphovascular_invasion_info = Lymphovascular_invasion_info_match.group(1).strip() if Lymphovascular_invasion_info_match else "PHI: NULL"
        Lymphovascular_invasion_info_dict={'Lymphovascular invasion': Lymphovascular_invasion_info}                                      
        #print("\n淋巴管侵犯:")
        return Lymphovascular_invasion_info_dict
        
    @classmethod
    def Other_info(self,my_File):
        Other_info_pattern=r"Other:(.*?)DIAGNOSIS:(.*?)\n"
        Other_info_match = re.search(Other_info_pattern, my_File, re.DOTALL)
        Other_info = Other_info_match.group(1).strip() if Other_info_match else "PHI: NULL"
        Other_info_dict={'Other': Other_info}                                        
        #print("\n其他:")
        return Other_info_dict

    @classmethod
    def DIAGNOSIS_info(self,my_File):
        diagnosis_info_pattern = r"^DIAGNOSIS:(.+)$"
        diagnosis_info_match = re.search(diagnosis_info_pattern, my_File, re.MULTILINE | re.DOTALL)
        diagnosis_info = diagnosis_info_match.group(1).strip() if diagnosis_info_match else "PHI: NULL"
        diagnosis_info_dict={'DIAGNOSIS': diagnosis_info}          
        #print("\n診斷信息:")
        return diagnosis_info_dict
    
    @classmethod
    def Blocks_info(self,my_File):
        # 腫瘤訊息
        Blocks_info_pattern=r"Blocks:(.*?)(?=\nMACROSCOPIC(.*?):|$)"
        Blocks_info_match=re.search(Blocks_info_pattern,my_File,re.MULTILINE | re.DOTALL)
        Blocks_info=Blocks_info_match.group(1).strip() if Blocks_info_match else "PHI: NULL"
        Blocks_info_dict={'Blocks':Blocks_info}                  
        #print("\n腫瘤訊息:")
        return Blocks_info_dict 
        
    @classmethod
    def GetAddress(self,my_File):
        # 提取 "Lab No" 和 "Specimen" 之间的文本
        Address_pattern = r"Lab No:(.*?)Specimen:"
        Address_match = re.search(Address_pattern, my_File, re.DOTALL)
        Address_match_text = Address_match.group(1).strip() if Address_match else"PHI: NULL"
        #print(Address_match_text)
        if Address_match_text != "PHI: NULL": 
            # 提取 "STREET"、"CITY"、"STATE" 和 "ZIP"
            STREET_pattern = r"\n([\w\s]+)\n"
            STREET_match = re.search(STREET_pattern, Address_match_text)
            #print(STREET_match)
            CITY_pattern = r"\n\n(\w+)\n(\w+)\s+(\w+)\s+(\d+)"                
            CITY_match = re.search(CITY_pattern, Address_match_text)            
            if CITY_match is None:
                CITY_pattern = r"\n(.+?)\s+(\w+)\s+(\d+)"
                CITY_match = re.search(CITY_pattern, Address_match_text)
                #print(CITY_match)                 
            else:
                CITY_pattern = r"\n(\w+)\n(\w+)\s+(\w+)\s+(\d+)"                
                CITY_match = re.search(CITY_pattern, Address_match_text)
                #print(CITY_match)
                
            STREET_ = STREET_match.group(1) if STREET_match is not None else "PHI: NULL"
            CITY_ = CITY_match.group(1) if CITY_match is not None else "PHI: NULL"
            STATE_ = CITY_match.group(2) if CITY_match is not None else "PHI: NULL"
            ZIP_ = CITY_match.group(3) if CITY_match is not None else "PHI: NULL"
            GetSTREETPositions=self.Get_position(STREET_,my_File) if STREET_ else 'PHI: NULL'                    
            GetCITYPositions=self.Get_position(CITY_,my_File) if CITY_ else 'PHI: NULL'                    
            GetSTATEPositions=self.Get_position(STATE_,my_File) if STATE_ else 'PHI: NULL'                    
            GetZIPPositions=self.Get_position(ZIP_,my_File) if ZIP_ else 'PHI: NULL' 
            STREET_Identify=r'PHI:STREET'
            STREET=STREET_,GetSTREETPositions[2],GetSTREETPositions[3],STREET_Identify
            #print("STREET:",STREET)            
            CITY_Identify=r'PHI:CITY'
            CITY=CITY_,GetCITYPositions[2],GetCITYPositions[3],CITY_Identify
            #print("CITY:", CITY)            
            STATE_Identify=r'PHI:STATE'
            STATE=STATE_,GetSTATEPositions[2],GetSTATEPositions[3],STATE_Identify
            #print("STATE:", STATE)            
            ZIP_Identify=r'PHI:ZIP'
            ZIP=ZIP_,GetZIPPositions[2],GetZIPPositions[3],ZIP_Identify           
            #print("ZIP:", ZIP)
            GetAddressPositions=self.Get_position(Address_match_text,my_File)
            Address_info_dict={"STREET":STREET,"CITY":CITY,"STATE":STATE,"ZIP":ZIP}
            #print(Address_info_dict)
            return Address_info_dict
        else:
            Address_info_dict={'Address':"PHI: NULL"}
            return Address_info_dict
    
    @classmethod
    def Get_position(self,match_text,my_File):
        #print('match_text:',match_text)
        info_pattern=match_text
        info_match = re.search(info_pattern,my_File, re.MULTILINE)
        match_info = info_match.group(0).strip() if info_match else "NULL"
        #print(match_info)          
        if info_match:
            start_position = info_match.start()
            end_position = info_match.end()
            #print("Match found at positions:", start_position, end_position)
            Matched_text = my_File[start_position:end_position]
            #print("Match content:",Matched_text)
        else:
            start_position = end_position = "Null"
            Matched_text = "NULL"
            #print("No match found")
        #print('================\n')
        return info_match,Matched_text,start_position,end_position

 