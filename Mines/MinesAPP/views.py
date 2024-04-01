from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from Database import Database
import datetime

db=Database()
output=[]


class NameForm(forms.Form):
    name=forms.CharField(label="Mine name :")
    start=forms.CharField(label="From :",initial=str(datetime.date.today().year-14))
    end=forms.CharField(label="To :",initial=str(datetime.date.today().year))


# zrobić year jako wybieralną listę
class TypeForm(forms.Form):
    types=forms.CharField(label="Mineral type")
    start1 = forms.CharField(label="From:", initial=str(datetime.date.today().year - 14))
    end1 = forms.CharField(label="To:", initial=str(datetime.date.today().year))

class Temp(forms.Form):
    name=forms.CharField()
    start=forms.CharField()
    end=forms.CharField()
class CountyForm(forms.Form):
    county=forms.ChoiceField(choices=[
    ('01', 'Wrocław'),
    ('02', 'Jelenia Góra'),
    ('03', 'Legnica'),
    ('04', 'Wałbrzych'),
    ('05', 'bolesławiecki'),
    ('06', 'dzierżoniowski'),
    ('07', 'głogowski'),
    ('08', 'górowski'),
    ('09', 'jaworski'),
    ('10', 'jeleniogórski'),
    ('11', 'kamiennogórski'),
    ('12', 'kłodzki'),
    ('13', 'legnicki'),
    ('14', 'lubański'),
    ('15', 'lubiński'),
    ('16', 'lwówecki'),
    ('17', 'milicki'),
    ('18', 'oleśnicki'),
    ('19', 'oławski'),
    ('20', 'polkowicki'),
    ('21', 'strzeliński'),
    ('22', 'średzki'),
    ('23', 'świdnicki'),
    ('24', 'trzebnicki'),
    ('25', 'wałbrzyski'),
    ('26', 'wołowski'),
    ('27', 'wrocławski'),
    ('28', 'ząbkowicki'),
    ('29', 'zgorzelecki'),
    ('30', 'złotoryjski'),
    ('31', 'Bydgoszcz'),
    ('32', 'Toruń'),
    ('33', 'Włocławek'),
    ('34', 'Grudziądz'),
    ('35', 'aleksandrowski'),
    ('36', 'brodnicki'),
    ('37', 'bydgoski'),
    ('38', 'chełmiński'),
    ('39', 'golubsko-dobrzyński'),
    ('40', 'grudziądzki'),
    ('41', 'inowrocławski'),
    ('42', 'lipnowski'),
    ('43', 'mogileński'),
    ('44', 'nakielski'),
    ('45', 'radziejowski'),
    ('46', 'rypiński'),
    ('47', 'sępoleński'),
    ('48', 'świecki'),
    ('49', 'toruński'),
    ('50', 'tucholski'),
    ('51', 'wąbrzeski'),
    ('52', 'włocławski'),
    ('53', 'żniński'),
    ('54', 'Lublin'),
    ('55', 'Biała Podlaska'),
    ('56', 'Chełm'),
    ('57', 'Zamość'),
    ('58', 'bialski'),
    ('59', 'biłgorajski'),
    ('60', 'chełmski'),
    ('61', 'hrubieszowski'),
    ('62', 'janowski'),
    ('63', 'krasnostawski'),
    ('64', 'kraśnicki'),
    ('65', 'lubartowski'),
    ('66', 'lubelski'),
    ('67', 'łęczyński'),
    ('68', 'łukowski'),
    ('69', 'opolski'),
    ('70', 'parczewski'),
    ('71', 'puławski'),
    ('72', 'radzyński'),
    ('73', 'rycki'),
    ('74', 'świdnicki'),
    ('75', 'tomaszowski'),
    ('76', 'włodawski'),
    ('77', 'zamojski'),
    ('78', 'Gorzów Wielkopolski'),
    ('79', 'Zielona Góra'),
    ('80', 'gorzowski'),
    ('81', 'krośnieński'),
    ('82', 'międzyrzecki'),
    ('83', 'nowosolski'),
    ('84', 'słubicki'),
    ('85', 'strzelecko-drezdenecki'),
    ('86', 'sulęciński'),
    ('87', 'świebodziński'),
    ('88', 'wschowski'),
    ('89', 'zielonogórski'),
    ('90', 'żagański'),
    ('91', 'żarski'),
    ('92', 'Łódź'),
    ('93', 'Piotrków Trybunalski'),
    ('94', 'Skierniewice'),
    ('95', 'bełchatowski'),
    ('96', 'brzeziński'),
    ('97', 'kutnowski'),
    ('98', 'łaski'),
    ('99', 'łęczycki'),
    ('100', 'łowicki'),
    ('101', 'łódzki wschodni'),
    ('102', 'opoczyński'),
    ('103', 'pabianicki'),
    ('104', 'pajęczański'),
    ('105', 'piotrkowski'),
    ('106', 'poddębicki'),
    ('107', 'radomszczański'),
    ('108', 'rawski'),
    ('109', 'sieradzki'),
    ('110', 'skierniewicki'),
    ('111', 'tomaszowski'),
    ('112', 'wieluński'),
    ('113', 'wieruszowski'),
    ('114', 'zduńskowolski'),
    ('115', 'zgierski'),
    ('116', 'Kraków'),
    ('117', 'Nowy Sącz'),
    ('118', 'Tarnów'),
    ('119', 'bocheński'),
    ('120', 'brzeski'),
    ('121', 'chrzanowski'),
    ('122', 'dąbrowski'),
    ('123', 'gorlicki'),
    ('124', 'krakowski'),
    ('125', 'limanowski'),
    ('126', 'miechowski'),
    ('127', 'myślenicki'),
    ('128', 'nowosądecki'),
    ('129', 'nowotarski'),
    ('130', 'olkuski'),
    ('131', 'oświęcimski'),
    ('132', 'proszowicki'),
    ('133', 'suski'),
    ('134', 'tarnowski'),
    ('135', 'tatrzański'),
    ('136', 'wadowicki'),
    ('137', 'wielicki'),
    ('138', 'Warszawa'),
    ('139', 'Ostrołęka'),
    ('140', 'Płock'),
    ('141', 'Radom'),
    ('142', 'Siedlce'),
    ('143', 'białobrzeski'),
    ('144', 'ciechanowski'),
    ('145', 'garwoliński'),
    ('146', 'gostyniński'),
    ('147', 'grodziski'),
    ('148', 'grójecki'),
    ('149', 'kozienicki'),
    ('150', 'legionowski'),
    ('151', 'lipski'),
    ('152', 'łosicki'),
    ('153', 'makowski'),
    ('154', 'miński'),
    ('155', 'mławski'),
    ('156', 'nowodworski'),
    ('157', 'ostrołęcki'),
    ('158', 'ostrowski'),
    ('159', 'otwocki'),
    ('160', 'piaseczyński'),
    ('161', 'płocki'),
    ('162', 'płoński'),
    ('163', 'pruszkowski'),
    ('164', 'przasnyski'),
    ('165', 'przysuski'),
    ('166', 'pułtuski'),
    ('167', 'radomski'),
    ('168', 'siedlecki'),
    ('169', 'sierpecki'),
    ('170', 'sochaczewski'),
    ('171', 'sokołowski'),
    ('172', 'szydłowiecki'),
    ('173', 'warszawski zachodni'),
    ('174', 'węgrowski'),
    ('175', 'wołomiński'),
    ('176', 'wyszkowski'),
    ('177', 'zwoleński'),
    ('178', 'żuromiński'),
    ('179', 'żyrardowski'),
    ('180', 'Opole'),
    ('181', 'brzeski'),
    ('182', 'głubczycki'),
    ('183', 'kędzierzyńsko-kozielski'),
    ('184', 'kluczborski'),
    ('185', 'krapkowicki'),
    ('186', 'namysłowski'),
    ('187', 'nyski'),
    ('188', 'oleski'),
    ('189', 'opolski'),
    ('190', 'prudnicki'),
    ('191', 'strzelecki'),
    ('192', 'Rzeszów'),
    ('193', 'Krosno'),
    ('194', 'Przemyśl'),
    ('195', 'Tarnobrzeg'),
    ('196', 'bieszczadzki'),
    ('197', 'brzozowski'),
    ('198', 'dębicki'),
    ('199', 'jarosławski'),
    ('200', 'jasielski'),
    ('201', 'kolbuszowski'),
    ('202', 'krośnieński'),
    ('203', 'leski'),
    ('204', 'leżajski'),
    ('205', 'lubaczowski'),
    ('206', 'łańcucki'),
    ('207', 'mielecki'),
    ('208', 'niżański'),
    ('209', 'przemyski'),
    ('210', 'przeworski'),
    ('211', 'ropczycko-sędziszowski'),
    ('212', 'rzeszowski'),
    ('213', 'sanocki'),
    ('214', 'stalowowolski'),
    ('215', 'strzyżowski'),
    ('216', 'tarnobrzeski'),
    ('217', 'Białystok'),
    ('218', 'Łomża'),
    ('219', 'Suwałki'),
    ('220', 'augustowski'),
    ('221', 'białostocki'),
    ('222', 'bielski'),
    ('223', 'grajewski'),
    ('224', 'hajnowski'),
    ('225', 'kolneński'),
    ('226', 'łomżyński'),
    ('227', 'moniecki'),
    ('228', 'sejneński'),
    ('229', 'siemiatycki'),
    ('230', 'sokólski'),
    ('231', 'suwalski'),
    ('232', 'wysokomazowiecki'),
    ('233', 'zambrowski'),
    ('234', 'Gdańsk'),
    ('235', 'Gdynia'),
    ('236', 'Słupsk'),
    ('237', 'Sopot'),
    ('238', 'bytowski'),
    ('239', 'chojnicki'),
    ('240', 'człuchowski'),
    ('241', 'kartuski'),
    ('242', 'kościerski'),
    ('243', 'kwidzyński'),
    ('244', 'lęborski'),
    ('245', 'malborski'),
    ('246', 'nowodworski'),
    ('247', 'gdański'),
    ('248', 'pucki'),
    ('249', 'słupski'),
    ('250', 'starogardzki'),
    ('251', 'sztumski'),
    ('252', 'tczewski'),
    ('253', 'wejherowski'),
    ('254', 'Katowice'),
    ('255', 'Bielsko-Biała'),
    ('256', 'Bytom'),
    ('257', 'Chorzów'),
    ('258', 'Częstochowa'),
    ('259', 'Dąbrowa Górnicza'),
    ('260', 'Gliwice'),
    ('261', 'Jastrzębie-Zdrój'),
    ('262', 'Jaworzno'),
    ('263', 'Mysłowice'),
    ('264', 'Piekary Śląskie'),
    ('265', 'Ruda Śląska'),
    ('266', 'Rybnik'),
    ('267', 'Siemianowice Śląskie'),
    ('268', 'Sosnowiec'),
    ('269', 'Świętochłowice'),
    ('270', 'Tychy'),
    ('271', 'Zabrze'),
    ('272', 'Żory'),
    ('273', 'będziński'),
    ('274', 'bielski'),
    ('275', 'bieruńsko-lędziński'),
    ('276', 'cieszyński'),
    ('277', 'częstochowski'),
    ('278', 'gliwicki'),
    ('279', 'kłobucki'),
    ('280', 'lubliniecki'),
    ('281', 'mikołowski'),
    ('282', 'myszkowski'),
    ('283', 'pszczyński'),
    ('284', 'raciborski'),
    ('285', 'rybnicki'),
    ('286', 'tarnogórski'),
    ('287', 'wodzisławski'),
    ('288', 'zawierciański'),
    ('289', 'żywiecki'),
    ('290', 'Kielce'),
    ('291', 'buski'),
    ('292', 'jędrzejowski'),
    ('293', 'kazimierski'),
    ('294', 'kielecki'),
    ('295', 'konecki'),
    ('296', 'opatowski'),
    ('297', 'ostrowiecki'),
    ('298', 'pińczowski'),
    ('299', 'sandomierski'),
    ('300', 'skarżyski'),
    ('301', 'starachowicki'),
    ('302', 'staszowski'),
    ('303', 'włoszczowski'),
    ('304', 'Olsztyn'),
    ('305', 'Elbląg'),
    ('306', 'bartoszycki'),
    ('307', 'braniewski'),
    ('308', 'działdowski'),
    ('309', 'elbląski'),
    ('310', 'ełcki'),
    ('311', 'giżycki'),
    ('312', 'gołdapski'),
    ('313', 'iławski'),
    ('314', 'kętrzyński'),
    ('315', 'lidzbarski'),
    ('316', 'mrągowski'),
    ('317', 'nidzicki'),
    ('318', 'nowomiejski'),
    ('319', 'olecki'),
    ('320', 'olsztyński'),
    ('321', 'ostródzki'),
    ('322', 'piski'),
    ('323', 'szczycieński'),
    ('324', 'węgorzewski'),
    ('325', 'Poznań'),
    ('326', 'Kalisz'),
    ('327', 'Konin'),
    ('328', 'Leszno'),
    ('329', 'chodzieski'),
    ('330', 'czarnkowsko-trzcianecki'),
    ('331', 'gnieźnieński'),
    ('332', 'gostyński'),
    ('333', 'grodziski'),
    ('334', 'jarociński'),
    ('335', 'kaliski'),
    ('336', 'kępiński'),
    ('337', 'kolski'),
    ('338', 'koniński'),
    ('339', 'kościański'),
    ('340', 'krotoszyński'),
    ('341', 'leszczyński'),
    ('342', 'międzychodzki'),
    ('343', 'nowotomyski'),
    ('344', 'obornicki'),
    ('345', 'ostrowski'),
    ('346', 'ostrzeszowski'),
    ('347', 'pilski'),
    ('348', 'pleszewski'),
    ('349', 'poznański'),
    ('350', 'rawicki'),
    ('351', 'słupecki'),
    ('352', 'szamotulski'),
    ('353', 'średzki'),
    ('354', 'śremski'),
    ('355', 'turecki'),
    ('356', 'wągrowiecki'),
    ('357', 'wolsztyński'),
    ('358', 'wrzesiński'),
    ('359', 'złotowski'),
    ('360', 'Szczecin'),
    ('361', 'Koszalin'),
    ('362', 'Świnoujście'),
    ('363', 'białogardzki'),
    ('364', 'choszczeński'),
    ('365', 'drawski'),
    ('366', 'goleniowski'),
    ('367', 'gryficki'),
    ('368', 'gryfiński'),
    ('369', 'kamieński'),
    ('370', 'kołobrzeski'),
    ('371', 'koszaliński'),
    ('372', 'łobeski'),
    ('373', 'myśliborski'),
    ('374', 'policki'),
    ('375', 'pyrzycki'),
    ('376', 'sławieński'),
    ('377', 'stargardzki'),
    ('378', 'szczecinecki'),
    ('379', 'świdwiński'),
    ('380', 'wałecki')
])

    def get_county_name(self, value):
        for code, name in self.fields['county'].choices:
            if code == value:
                return name
        return None


def menu(request):
    return render(request,"MinesAPP/menu.html")


def name_search(request):
    form = NameForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        name=form.cleaned_data["name"]
        start=form.cleaned_data["start"]
        end=form.cleaned_data["end"]
        output.clear()
        output.append(db.search_by_name(str(name), start, end))
        output.append(name)
        return HttpResponseRedirect("name_search/results")
    else:
        return render(request,"MinesAPP/index1.html",{"form":form})
    return render(request,"MinesAPP/index1.html", {"form":NameForm()})


def type_search(request):
    form = TypeForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        types=form.cleaned_data["types"]
        start1=form.cleaned_data["start1"]
        end1=form.cleaned_data["end1"]
        output.clear()
        output.append(db.search_by_type(str(types), start1, end1))
        output.append(types)
        return HttpResponseRedirect("type_search/results")
    else:
        return render(request,"MinesAPP/type_search.html",{"form":form})
    return render(request,"MinesAPP/type_search.html", {"form":TypeForm()})

def area_search(request):
    form = CountyForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        num = form.cleaned_data["county"]
        county=form.get_county_name(num)
        print(county)
        '''start = form.cleaned_data["start"]
        end = form.cleaned_data["end"]'''

        output.clear()
        output.append(db.search_by_county(str(county)))
        output.append(county)
        print(output)
        return HttpResponseRedirect("county_search/results")
    else:
        return render(request, "MinesAPP/county_search.html", {"form": form})
    return render(request, "MinesAPP/county_search.html", {"form": CountyForm()})
def results(request):
    data=[]
    sums=[]
    if not output:
        return render(request, "MinesAPP/error.html")
    if output[0]:
        columns=[]
        headers1=list(output[0][0].keys())
        headers1=headers1[1:-1]
        headers2=list(output[0][0]["More"].keys())

        data=db.get_data(output, headers2)[0]
        columns=db.get_data(output, headers2)[1]
        tables=[]
        for headers,rows in zip(columns,data):
            table = {'headers': headers, 'rows': rows}
            tables.append(table)
        '''for rows in data:
            data.remove([])'''
        #sums=[db.get_data(output, headers2)[i] for i in range(1,len(db.get_data(output, headers2)))]
        return render(request, "MinesAPP/results.html",
                      {"items": output, "columns": columns, "tables": tables, "name": output[1]})
    else:
        columns=[]
        data=[[' ']]
        sums=[]
        return render(request,"MinesAPP/error.html")