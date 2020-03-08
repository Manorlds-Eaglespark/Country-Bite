import re

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Register_Validation():
    
    def __init__(self, user_data):
        self.name = user_data["name"]
        self.country = user_data["country"]
        self.email = user_data["email"]
        self.password = user_data["password"]
        self.phonenumber = user_data["phonenumber"]

    def check_input(self):
        if not (self.name and self.password and self.email):
            return [400, "Make sure you add all the required fields"]
        elif (not isinstance(self.name, str) or not isinstance(self.country, int)):
            return [406, "Make sure to use alphabetical characters use only "]
        elif self.password.isspace() or len(self.password) < 4 or not isinstance(self.password, str):
            return [406, "Make sure your password has atlest 4 letters"]
        elif re.search('[0-9]', self.password) is None:
            return [406, "Make sure your password has a number in it"]
        elif re.search('[A-Z]', self.password) is None:
            return [406, "Make sure your password has a capital letter in it"]
        elif not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", self.email) is not None:
            return [406, "Please enter a valid Email."]
        return [1, "All Good"]


all_countries = [
                    {
              		"id": 1,
                        "flag": "https://restcountries.eu/data/afg.svg",
                        "name": "Afghanistan"
                    },
                    {
			"id": 2,
                        "flag": "https://restcountries.eu/data/ala.svg",
                        "name": "Åland Islands"
                    },
                    {
			"id": 3,
                        "flag": "https://restcountries.eu/data/alb.svg",
                        "name": "Albania"
                    },
                    {	
			"id": 4,
		         "flag": "https://restcountries.eu/data/dza.svg",
                        "name": "Algeria"
                    },
                    {
			"id":5,
                        "flag": "https://restcountries.eu/data/asm.svg",
                        "name": "American Samoa"
                    },
                    {
			"id":6,
                        "flag": "https://restcountries.eu/data/and.svg",
                        "name": "Andorra"
                    },
                    {
			"id":7,
                        "flag": "https://restcountries.eu/data/ago.svg",
                        "name": "Angola"
                    },
                    {
			"id":8,
                        "flag": "https://restcountries.eu/data/aia.svg",
                        "name": "Anguilla"
                    },
                    {
			"id":9,
                        "flag": "https://restcountries.eu/data/ata.svg",
                        "name": "Antarctica"
                    },
                    {
			"id":10,
                        "flag": "https://restcountries.eu/data/atg.svg",
                        "name": "Antigua and Barbuda"
                    },
                    {
			"id":11,
                        "flag": "https://restcountries.eu/data/arg.svg",
                        "name": "Argentina"
                    },
                    {
			"id":12,
                        "flag": "https://restcountries.eu/data/arm.svg",
                        "name": "Armenia"
                    },
                    {
			"id":13,
                        "flag": "https://restcountries.eu/data/abw.svg",
                        "name": "Aruba"
                    },
                    {
			"id":14,
                        "flag": "https://restcountries.eu/data/aus.svg",
                        "name": "Australia"
                    },
                    {
			"id":15,
                        "flag": "https://restcountries.eu/data/aut.svg",
                        "name": "Austria"
                    },
                    {
			"id":16,
                        "flag": "https://restcountries.eu/data/aze.svg",
                        "name": "Azerbaijan"
                    },
                    {
			"id":17,
                        "flag": "https://restcountries.eu/data/bhs.svg",
                        "name": "Bahamas"
                    },
                    {
			"id":18,
                        "flag": "https://restcountries.eu/data/bhr.svg",
                        "name": "Bahrain"
                    },
                    {
			"id":19,
                        "flag": "https://restcountries.eu/data/bgd.svg",
                        "name": "Bangladesh"
                    },
                    {
			"id":20,
                        "flag": "https://restcountries.eu/data/brb.svg",
                        "name": "Barbados"
                    },
                    {
			"id":21,
                        "flag": "https://restcountries.eu/data/blr.svg",
                        "name": "Belarus"
                    },
                    {
			"id":22,
                        "flag": "https://restcountries.eu/data/bel.svg",
                        "name": "Belgium"
                    },
                    {
			"id":23,
                        "flag": "https://restcountries.eu/data/blz.svg",
                        "name": "Belize"
                    },
                    {
			"id":24,
                        "flag": "https://restcountries.eu/data/ben.svg",
                        "name": "Benin"
                    },
                    {
			"id":25,
                        "flag": "https://restcountries.eu/data/bmu.svg",
                        "name": "Bermuda"
                    },
                    {
			"id":26,
                        "flag": "https://restcountries.eu/data/btn.svg",
                        "name": "Bhutan"
                    },
                    {
			"id":27,
                        "flag": "https://restcountries.eu/data/bol.svg",
                        "name": "Bolivia (Plurinational State of)"
                    },
                    {
			"id":28,
                        "flag": "https://restcountries.eu/data/bes.svg",
                        "name": "Bonaire, Sint Eustatius and Saba"
                    },
                    {
			"id":29,
                        "flag": "https://restcountries.eu/data/bih.svg",
                        "name": "Bosnia and Herzegovina"
                    },
                    {
			"id":30,
                        "flag": "https://restcountries.eu/data/bwa.svg",
                        "name": "Botswana"
                    },
                    {
			"id":31,
                        "flag": "https://restcountries.eu/data/bvt.svg",
                        "name": "Bouvet Island"
                    },
                    {
			"id":32,
                        "flag": "https://restcountries.eu/data/bra.svg",
                        "name": "Brazil"
                    },
                    {
			"id":33,
                        "flag": "https://restcountries.eu/data/iot.svg",
                        "name": "British Indian Ocean Territory"
                    },
                    {
			"id":34,
                        "flag": "https://restcountries.eu/data/umi.svg",
                        "name": "United States Minor Outlying Islands"
                    },
                    {
			"id":35,
                        "flag": "https://restcountries.eu/data/vgb.svg",
                        "name": "Virgin Islands (British)"
                    },
                    {
			"id":36,
                        "flag": "https://restcountries.eu/data/vir.svg",
                        "name": "Virgin Islands (U.S.)"
                    },
                    {
			"id":37,
                        "flag": "https://restcountries.eu/data/brn.svg",
                        "name": "Brunei Darussalam"
                    },
                    {
			"id":38,
                        "flag": "https://restcountries.eu/data/bgr.svg",
                        "name": "Bulgaria"
                    },
                    {
			"id":39,
                        "flag": "https://restcountries.eu/data/bfa.svg",
                        "name": "Burkina Faso"
                    },
                    {
			"id":40,
                        "flag": "https://restcountries.eu/data/bdi.svg",
                        "name": "Burundi"
                    },
                    {
			"id":41,
                        "flag": "https://restcountries.eu/data/khm.svg",
                        "name": "Cambodia"
                    },
                    {
			"id":42,
                        "flag": "https://restcountries.eu/data/cmr.svg",
                        "name": "Cameroon"
                    },
                    {
			"id":43,
                        "flag": "https://restcountries.eu/data/can.svg",
                        "name": "Canada"
                    },
                    {
			"id":44,
                        "flag": "https://restcountries.eu/data/cpv.svg",
                        "name": "Cabo Verde"
                    },
                    {
			"id":45,
                        "flag": "https://restcountries.eu/data/cym.svg",
                        "name": "Cayman Islands"
                    },
                    {
			"id":46,
                        "flag": "https://restcountries.eu/data/caf.svg",
                        "name": "Central African Republic"
                    },
                    {
			"id":47,
                        "flag": "https://restcountries.eu/data/tcd.svg",
                        "name": "Chad"
                    },
                    {
			"id":48,
                        "flag": "https://restcountries.eu/data/chl.svg",
                        "name": "Chile"
                    },
                    {
			"id":49,
                        "flag": "https://restcountries.eu/data/chn.svg",
                        "name": "China"
                    },
                    {
			"id":50,
                        "flag": "https://restcountries.eu/data/cxr.svg",
                        "name": "Christmas Island"
                    },
                    {
			"id":51,
                        "flag": "https://restcountries.eu/data/cck.svg",
                        "name": "Cocos (Keeling) Islands"
                    },
                    {
			"id":52,
                        "flag": "https://restcountries.eu/data/col.svg",
                        "name": "Colombia"
                    },
                    {
			"id":53,
                        "flag": "https://restcountries.eu/data/com.svg",
                        "name": "Comoros"
                    },
                    {
			"id":54,
                        "flag": "https://restcountries.eu/data/cog.svg",
                        "name": "Congo"
                    },
                    {
			"id":55,
                        "flag": "https://restcountries.eu/data/cod.svg",
                        "name": "Congo (Democratic Republic of the)"
                    },
                    {
			"id":56,
                        "flag": "https://restcountries.eu/data/cok.svg",
                        "name": "Cook Islands"
                    },
                    {
			"id":57,
                        "flag": "https://restcountries.eu/data/cri.svg",
                        "name": "Costa Rica"
                    },
                    {
			"id":58,
                        "flag": "https://restcountries.eu/data/hrv.svg",
                        "name": "Croatia"
                    },
                    {
			"id":59,
                        "flag": "https://restcountries.eu/data/cub.svg",
                        "name": "Cuba"
                    },
                    {
			"id":60,
                        "flag": "https://restcountries.eu/data/cuw.svg",
                        "name": "Curaçao"
                    },
                    {
			"id":61,
                        "flag": "https://restcountries.eu/data/cyp.svg",
                        "name": "Cyprus"
                    },
                    {
			"id":62,
                        "flag": "https://restcountries.eu/data/cze.svg",
                        "name": "Czech Republic"
                    },
                    {
			"id":63,
                        "flag": "https://restcountries.eu/data/dnk.svg",
                        "name": "Denmark"
                    },
                    {
		        "id":64,
                        "flag": "https://restcountries.eu/data/dji.svg",
                        "name": "Djibouti"
                    },
                    {
			"id":65,
                        "flag": "https://restcountries.eu/data/dma.svg",
                        "name": "Dominica"
                    },
                    {
			"id":66,
                        "flag": "https://restcountries.eu/data/dom.svg",
                        "name": "Dominican Republic"
                    },
                    {
			"id":67,
                        "flag": "https://restcountries.eu/data/ecu.svg",
                        "name": "Ecuador"
                    },
                    {
			"id":68,
                        "flag": "https://restcountries.eu/data/egy.svg",
                        "name": "Egypt"
                    },
                    {
			"id":69,
                        "flag": "https://restcountries.eu/data/slv.svg",
                        "name": "El Salvador"
                    },
                    {
			"id":70,
                        "flag": "https://restcountries.eu/data/gnq.svg",
                        "name": "Equatorial Guinea"
                    },
                    {
			"id":71,
                        "flag": "https://restcountries.eu/data/eri.svg",
                        "name": "Eritrea"
                    },
                    {
			"id":72,
                        "flag": "https://restcountries.eu/data/est.svg",
                        "name": "Estonia"
                    },
                    {
			"id":73,
                        "flag": "https://restcountries.eu/data/eth.svg",
                        "name": "Ethiopia"
                    },
                    {
			"id":74,
                        "flag": "https://restcountries.eu/data/flk.svg",
                        "name": "Falkland Islands (Malvinas)"
                    },
                    {
			"id":75,
                        "flag": "https://restcountries.eu/data/fro.svg",
                        "name": "Faroe Islands"
                    },
                    {
			"id":76,
                        "flag": "https://restcountries.eu/data/fji.svg",
                        "name": "Fiji"
                    },
                    {
			"id":77,
                        "flag": "https://restcountries.eu/data/fin.svg",
                        "name": "Finland"
                    },
                    {
			"id":78,
                        "flag": "https://restcountries.eu/data/fra.svg",
                        "name": "France"
                    },
                    {
			"id":79,
                        "flag": "https://restcountries.eu/data/guf.svg",
                        "name": "French Guiana"
                    },
                    {
			"id":80,
                        "flag": "https://restcountries.eu/data/pyf.svg",
                        "name": "French Polynesia"
                    },
                    {
			"id":81,
                        "flag": "https://restcountries.eu/data/atf.svg",
                        "name": "French Southern Territories"
                    },
                    {
			"id":82,
                        "flag": "https://restcountries.eu/data/gab.svg",
                        "name": "Gabon"
                    },
                    {
			"id":83,
                        "flag": "https://restcountries.eu/data/gmb.svg",
                        "name": "Gambia"
                    },
                    {
			"id":84,
                        "flag": "https://restcountries.eu/data/geo.svg",
                        "name": "Georgia"
                    },
                    {
			"id":85,
                        "flag": "https://restcountries.eu/data/deu.svg",
                        "name": "Germany"
                    },
                    {
			"id":86,
                        "flag": "https://restcountries.eu/data/gha.svg",
                        "name": "Ghana"
                    },
                    {
			"id":87,
                        "flag": "https://restcountries.eu/data/gib.svg",
                        "name": "Gibraltar"
                    },
                    {
			"id":88,
                        "flag": "https://restcountries.eu/data/grc.svg",
                        "name": "Greece"
                    },
                    {
			"id":89,
                        "flag": "https://restcountries.eu/data/grl.svg",
                        "name": "Greenland"
                    },
                    {
			"id":90,
                        "flag": "https://restcountries.eu/data/grd.svg",
                        "name": "Grenada"
                    },
                    {
			"id":91,
                        "flag": "https://restcountries.eu/data/glp.svg",
                        "name": "Guadeloupe"
                    },
                    {
			"id":92,
                        "flag": "https://restcountries.eu/data/gum.svg",
                        "name": "Guam"
                    },
                    {
			"id":93,
                        "flag": "https://restcountries.eu/data/gtm.svg",
                        "name": "Guatemala"
                    },
                    {
			"id":94,
                        "flag": "https://restcountries.eu/data/ggy.svg",
                        "name": "Guernsey"
                    },
                    {
			"id":95,
                        "flag": "https://restcountries.eu/data/gin.svg",
                        "name": "Guinea"
                    },
                    {
			"id":96,
                        "flag": "https://restcountries.eu/data/gnb.svg",
                        "name": "Guinea-Bissau"
                    },
                    {
			"id":97,
                        "flag": "https://restcountries.eu/data/guy.svg",
                        "name": "Guyana"
                    },
                    {
			"id":98,
                        "flag": "https://restcountries.eu/data/hti.svg",
                        "name": "Haiti"
                    },
                    {
			"id":99,
                        "flag": "https://restcountries.eu/data/hmd.svg",
                        "name": "Heard Island and McDonald Islands"
                    },
                    {
			"id":100,
                        "flag": "https://restcountries.eu/data/vat.svg",
                        "name": "Holy See"
                    },
                    {
			"id":101,
                        "flag": "https://restcountries.eu/data/hnd.svg",
                        "name": "Honduras"
                    },
                    {
			"id":102,
                        "flag": "https://restcountries.eu/data/hkg.svg",
                        "name": "Hong Kong"
                    },
                    {
			"id":103,
                        "flag": "https://restcountries.eu/data/hun.svg",
                        "name": "Hungary"
                    },
                    {
			"id":104,
                        "flag": "https://restcountries.eu/data/isl.svg",
                        "name": "Iceland"
                    },
                    {
			"id":105,
                        "flag": "https://restcountries.eu/data/ind.svg",
                        "name": "India"
                    },
                    {
			"id":106,
                        "flag": "https://restcountries.eu/data/idn.svg",
                        "name": "Indonesia"
                    },
                    {
			"id":107,
                        "flag": "https://restcountries.eu/data/civ.svg",
                        "name": "Côte d'Ivoire"
                    },
                    {
			"id":108,
                        "flag": "https://restcountries.eu/data/irn.svg",
                        "name": "Iran (Islamic Republic of)"
                    },
                    {
			"id":109,
                        "flag": "https://restcountries.eu/data/irq.svg",
                        "name": "Iraq"
                    },
                    {
			"id":110,
                        "flag": "https://restcountries.eu/data/irl.svg",
                        "name": "Ireland"
                    },
                    {
			"id":111,
                        "flag": "https://restcountries.eu/data/imn.svg",
                        "name": "Isle of Man"
                    },
                    {
			"id":112,
                        "flag": "https://restcountries.eu/data/isr.svg",
                        "name": "Israel"
                    },
                    {
			"id":113,
                        "flag": "https://restcountries.eu/data/ita.svg",
                        "name": "Italy"
                    },
                    {
			"id":114,
                        "flag": "https://restcountries.eu/data/jam.svg",
                        "name": "Jamaica"
                    },
                    {
			"id":115,
                        "flag": "https://restcountries.eu/data/jpn.svg",
                        "name": "Japan"
                    },
                    {
			"id":116,
                        "flag": "https://restcountries.eu/data/jey.svg",
                        "name": "Jersey"
                    },
                    {
			"id":117,
                        "flag": "https://restcountries.eu/data/jor.svg",
                        "name": "Jordan"
                    },
                    {
			"id":118,
                        "flag": "https://restcountries.eu/data/kaz.svg",
                        "name": "Kazakhstan"
                    },
                    {
			"id":119,
                        "flag": "https://restcountries.eu/data/ken.svg",
                        "name": "Kenya"
                    },
                    {
			"id":120,
                        "flag": "https://restcountries.eu/data/kir.svg",
                        "name": "Kiribati"
                    },
                    {
			"id":121,
                        "flag": "https://restcountries.eu/data/kwt.svg",
                        "name": "Kuwait"
                    },
                    {
			"id":122,
                        "flag": "https://restcountries.eu/data/kgz.svg",
                        "name": "Kyrgyzstan"
                    },
                    {
			"id":123,
                        "flag": "https://restcountries.eu/data/lao.svg",
                        "name": "Lao People's Democratic Republic"
                    },
                    {
			"id":124,
                        "flag": "https://restcountries.eu/data/lva.svg",
                        "name": "Latvia"
                    },
                    {
			"id":125,
                        "flag": "https://restcountries.eu/data/lbn.svg",
                        "name": "Lebanon"
                    },
                    {
			"id":126,
                        "flag": "https://restcountries.eu/data/lso.svg",
                        "name": "Lesotho"
                    },
                    {
			"id":127,
                        "flag": "https://restcountries.eu/data/lbr.svg",
                        "name": "Liberia"
                    },
                    {
			"id":128,
                        "flag": "https://restcountries.eu/data/lby.svg",
                        "name": "Libya"
                    },
                    {
			"id":129,
                        "flag": "https://restcountries.eu/data/lie.svg",
                        "name": "Liechtenstein"
                    },
                    {
			"id":130,
                        "flag": "https://restcountries.eu/data/ltu.svg",
                        "name": "Lithuania"
                    },
                    {
			"id":131,
                        "flag": "https://restcountries.eu/data/lux.svg",
                        "name": "Luxembourg"
                    },
                    {
			"id":132,
                        "flag": "https://restcountries.eu/data/mac.svg",
                        "name": "Macao"
                    },
                    {
			"id":133,
                        "flag": "https://restcountries.eu/data/mkd.svg",
                        "name": "Macedonia (the former Yugoslav Republic of)"
                    },
                    {
			"id":134,
                        "flag": "https://restcountries.eu/data/mdg.svg",
                        "name": "Madagascar"
                    },
                    {
			"id":135,
                        "flag": "https://restcountries.eu/data/mwi.svg",
                        "name": "Malawi"
                    },
                    {
			"id":136,
                        "flag": "https://restcountries.eu/data/mys.svg",
                        "name": "Malaysia"
                    },
                    {
			"id":137,
                        "flag": "https://restcountries.eu/data/mdv.svg",
                        "name": "Maldives"
                    },
                    {
			"id":138,
                        "flag": "https://restcountries.eu/data/mli.svg",
                        "name": "Mali"
                    },
                    {
			"id":139,
                        "flag": "https://restcountries.eu/data/mlt.svg",
                        "name": "Malta"
                    },
                    {
			"id":140,
                        "flag": "https://restcountries.eu/data/mhl.svg",
                        "name": "Marshall Islands"
                    },
                    {
			"id":141,
                        "flag": "https://restcountries.eu/data/mtq.svg",
                        "name": "Martinique"
                    },
                    {
			"id":142,
                        "flag": "https://restcountries.eu/data/mrt.svg",
                        "name": "Mauritania"
                    },
                    {
			"id":143,
                        "flag": "https://restcountries.eu/data/mus.svg",
                        "name": "Mauritius"
                    },
                    {
			"id":144,
                        "flag": "https://restcountries.eu/data/myt.svg",
                        "name": "Mayotte"
                    },
                    {
			"id":145,
                        "flag": "https://restcountries.eu/data/mex.svg",
                        "name": "Mexico"
                    },
                    {
			"id":146,
                        "flag": "https://restcountries.eu/data/fsm.svg",
                        "name": "Micronesia (Federated States of)"
                    },
                    {
			"id":147,
                        "flag": "https://restcountries.eu/data/mda.svg",
                        "name": "Moldova (Republic of)"
                    },
                    {
			"id":148,
                        "flag": "https://restcountries.eu/data/mco.svg",
                        "name": "Monaco"
                    },
                    {
			"id":149,
                        "flag": "https://restcountries.eu/data/mng.svg",
                        "name": "Mongolia"
                    },
                    {
			"id":150,
                        "flag": "https://restcountries.eu/data/mne.svg",
                        "name": "Montenegro"
                    },
                    {
			"id":151,
                        "flag": "https://restcountries.eu/data/msr.svg",
                        "name": "Montserrat"
                    },
                    {
			"id":152,
                        "flag": "https://restcountries.eu/data/mar.svg",
                        "name": "Morocco"
                    },
                    {
			"id":153,
                        "flag": "https://restcountries.eu/data/moz.svg",
                        "name": "Mozambique"
                    },
                    {
			"id":154,
                        "flag": "https://restcountries.eu/data/mmr.svg",
                        "name": "Myanmar"
                    },
                    {
			"id":155,
                        "flag": "https://restcountries.eu/data/nam.svg",
                        "name": "Namibia"
                    },
                    {
			"id":156,
                        "flag": "https://restcountries.eu/data/nru.svg",
                        "name": "Nauru"
                    },
                    {
			"id":157,
                        "flag": "https://restcountries.eu/data/npl.svg",
                        "name": "Nepal"
                    },
                    {
			"id":158,
                        "flag": "https://restcountries.eu/data/nld.svg",
                        "name": "Netherlands"
                    },
                    {
			"id":159,
                        "flag": "https://restcountries.eu/data/ncl.svg",
                        "name": "New Caledonia"
                    },
                    {
			"id":160,
                        "flag": "https://restcountries.eu/data/nzl.svg",
                        "name": "New Zealand"
                    },
                    {
			"id":161,
                        "flag": "https://restcountries.eu/data/nic.svg",
                        "name": "Nicaragua"
                    },
                    {
			"id":162,
                        "flag": "https://restcountries.eu/data/ner.svg",
                        "name": "Niger"
                    },
                    {
			"id":163,
                        "flag": "https://restcountries.eu/data/nga.svg",
                        "name": "Nigeria"
                    },
                    {
			"id":164,
                        "flag": "https://restcountries.eu/data/niu.svg",
                        "name": "Niue"
                    },
                    {
			"id":165,
                        "flag": "https://restcountries.eu/data/nfk.svg",
                        "name": "Norfolk Island"
                    },
                    {
			"id":166,
                        "flag": "https://restcountries.eu/data/prk.svg",
                        "name": "Korea (Democratic People's Republic of)"
                    },
                    {
			"id":167,
                        "flag": "https://restcountries.eu/data/mnp.svg",
                        "name": "Northern Mariana Islands"
                    },
                    {
			"id":168,
                        "flag": "https://restcountries.eu/data/nor.svg",
                        "name": "Norway"
                    },
                    {
			"id":169,
                        "flag": "https://restcountries.eu/data/omn.svg",
                        "name": "Oman"
                    },
                    {
			"id":170,
                        "flag": "https://restcountries.eu/data/pak.svg",
                        "name": "Pakistan"
                    },
                    {
			"id":171,
                        "flag": "https://restcountries.eu/data/plw.svg",
                        "name": "Palau"
                    },
                    {
			"id":172,
                        "flag": "https://restcountries.eu/data/pse.svg",
                        "name": "Palestine, State of"
                    },
                    {
			"id":173,
                        "flag": "https://restcountries.eu/data/pan.svg",
                        "name": "Panama"
                    },
                    {
			"id":174,
                        "flag": "https://restcountries.eu/data/png.svg",
                        "name": "Papua New Guinea"
                    },
                    {
			"id":175,
                        "flag": "https://restcountries.eu/data/pry.svg",
                        "name": "Paraguay"
                    },
                    {
			"id":176,
                        "flag": "https://restcountries.eu/data/per.svg",
                        "name": "Peru"
                    },
                    {
			"id":177,
                        "flag": "https://restcountries.eu/data/phl.svg",
                        "name": "Philippines"
                    },
                    {
			"id":178,
                        "flag": "https://restcountries.eu/data/pcn.svg",
                        "name": "Pitcairn"
                    },
                    {
			"id":179,
                        "flag": "https://restcountries.eu/data/pol.svg",
                        "name": "Poland"
                    },
                    {
			"id":180,
                        "flag": "https://restcountries.eu/data/prt.svg",
                        "name": "Portugal"
                    },
                    {
			"id":181,
                        "flag": "https://restcountries.eu/data/pri.svg",
                        "name": "Puerto Rico"
                    },
                    {
			"id":182,
                        "flag": "https://restcountries.eu/data/qat.svg",
                        "name": "Qatar"
                    },
                    {
			"id":183,
                        "flag": "https://restcountries.eu/data/kos.svg",
                        "name": "Republic of Kosovo"
                    },
                    {
			"id":184,
                        "flag": "https://restcountries.eu/data/reu.svg",
                        "name": "Réunion"
                    },
                    {
			"id":185,
                        "flag": "https://restcountries.eu/data/rou.svg",
                        "name": "Romania"
                    },
                    {
			"id":186,
                        "flag": "https://restcountries.eu/data/rus.svg",
                        "name": "Russian Federation"
                    },
                    {
			"id":187,
                        "flag": "https://restcountries.eu/data/rwa.svg",
                        "name": "Rwanda"
                    },
                    {
			"id":188,
                        "flag": "https://restcountries.eu/data/blm.svg",
                        "name": "Saint Barthélemy"
                    },
                    {
			"id":189,
                        "flag": "https://restcountries.eu/data/shn.svg",
                        "name": "Saint Helena, Ascension and Tristan da Cunha"
                    },
                    {
			"id":190,
                        "flag": "https://restcountries.eu/data/kna.svg",
                        "name": "Saint Kitts and Nevis"
                    },
                    {
			"id":191,
                        "flag": "https://restcountries.eu/data/lca.svg",
                        "name": "Saint Lucia"
                    },
                    {
			"id":192,
                        "flag": "https://restcountries.eu/data/maf.svg",
                        "name": "Saint Martin (French part)"
                    },
                    {
			"id":193,
                        "flag": "https://restcountries.eu/data/spm.svg",
                        "name": "Saint Pierre and Miquelon"
                    },
                    {
			"id":194,
                        "flag": "https://restcountries.eu/data/vct.svg",
                        "name": "Saint Vincent and the Grenadines"
                    },
                    {
			"id":195,
                        "flag": "https://restcountries.eu/data/wsm.svg",
                        "name": "Samoa"
                    },
                    {
			"id":196,
                        "flag": "https://restcountries.eu/data/smr.svg",
                        "name": "San Marino"
                    },
                    {
			"id":197,
                        "flag": "https://restcountries.eu/data/stp.svg",
                        "name": "Sao Tome and Principe"
                    },
                    {
			"id":198,
                        "flag": "https://restcountries.eu/data/sau.svg",
                        "name": "Saudi Arabia"
                    },
                    {
			"id":199,
                        "flag": "https://restcountries.eu/data/sen.svg",
                        "name": "Senegal"
                    },
                    {
			"id":200,
                        "flag": "https://restcountries.eu/data/srb.svg",
                        "name": "Serbia"
                    },
                    {
			"id":201,
                        "flag": "https://restcountries.eu/data/syc.svg",
                        "name": "Seychelles"
                    },
                    {
			"id":202,
                        "flag": "https://restcountries.eu/data/sle.svg",
                        "name": "Sierra Leone"
                    },
                    {
			"id":203,
                        "flag": "https://restcountries.eu/data/sgp.svg",
                        "name": "Singapore"
                    },
                    {
			"id":204,
                        "flag": "https://restcountries.eu/data/sxm.svg",
                        "name": "Sint Maarten (Dutch part)"
                    },
                    {
			"id":205,
                        "flag": "https://restcountries.eu/data/svk.svg",
                        "name": "Slovakia"
                    },
                    {
			"id":206,
                        "flag": "https://restcountries.eu/data/svn.svg",
                        "name": "Slovenia"
                    },
                    {
			"id":207,
                        "flag": "https://restcountries.eu/data/slb.svg",
                        "name": "Solomon Islands"
                    },
                    {
			"id":208,
                        "flag": "https://restcountries.eu/data/som.svg",
                        "name": "Somalia"
                    },
                    {
			"id":209,
                        "flag": "https://restcountries.eu/data/zaf.svg",
                        "name": "South Africa"
                    },
                    {
			"id":210,
                        "flag": "https://restcountries.eu/data/sgs.svg",
                        "name": "South Georgia and the South Sandwich Islands"
                    },
                    {
			"id":211,
                        "flag": "https://restcountries.eu/data/kor.svg",
                        "name": "Korea (Republic of)"
                    },
                    {
			"id":212,
                        "flag": "https://restcountries.eu/data/ssd.svg",
                        "name": "South Sudan"
                    },
                    {
			"id":213,
                        "flag": "https://restcountries.eu/data/esp.svg",
                        "name": "Spain"
                    },
                    {
			"id":214,
                        "flag": "https://restcountries.eu/data/lka.svg",
                        "name": "Sri Lanka"
                    },
                    {
			"id":215,
                        "flag": "https://restcountries.eu/data/sdn.svg",
                        "name": "Sudan"
                    },
                    {
			"id":216,
                        "flag": "https://restcountries.eu/data/sur.svg",
                        "name": "Suriname"
                    },
                    {
			"id":217,
                        "flag": "https://restcountries.eu/data/sjm.svg",
                        "name": "Svalbard and Jan Mayen"
                    },
                    {
			"id":218,
                        "flag": "https://restcountries.eu/data/swz.svg",
                        "name": "Swaziland"
                    },
                    {
			"id":219,
                        "flag": "https://restcountries.eu/data/swe.svg",
                        "name": "Sweden"
                    },
                    {
			"id":220,
                        "flag": "https://restcountries.eu/data/che.svg",
                        "name": "Switzerland"
                    },
                    {
			"id":221,
                        "flag": "https://restcountries.eu/data/syr.svg",
                        "name": "Syrian Arab Republic"
                    },
                    {
			"id":222,
                        "flag": "https://restcountries.eu/data/twn.svg",
                        "name": "Taiwan"
                    },
                    {
			"id":223,
                        "flag": "https://restcountries.eu/data/tjk.svg",
                        "name": "Tajikistan"
                    },
                    {
			"id":224,
                        "flag": "https://restcountries.eu/data/tza.svg",
                        "name": "Tanzania, United Republic of"
                    },
                    {
			"id":225,
                        "flag": "https://restcountries.eu/data/tha.svg",
                        "name": "Thailand"
                    },
                    {
			"id":226,
                        "flag": "https://restcountries.eu/data/tls.svg",
                        "name": "Timor-Leste"
                    },
                    {
			"id":227,
                        "flag": "https://restcountries.eu/data/tgo.svg",
                        "name": "Togo"
                    },
                    {
			"id":228,
                        "flag": "https://restcountries.eu/data/tkl.svg",
                        "name": "Tokelau"
                    },
                    {
			"id":229,
                        "flag": "https://restcountries.eu/data/ton.svg",
                        "name": "Tonga"
                    },
                    {
			"id":230,
                        "flag": "https://restcountries.eu/data/tto.svg",
                        "name": "Trinidad and Tobago"
                    },
                    {
			"id":231,
                        "flag": "https://restcountries.eu/data/tun.svg",
                        "name": "Tunisia"
                    },
                    {
			"id":232,
                        "flag": "https://restcountries.eu/data/tur.svg",
                        "name": "Turkey"
                    },
                    {
			"id":233,
                        "flag": "https://restcountries.eu/data/tkm.svg",
                        "name": "Turkmenistan"
                    },
                    {
			"id":234,
                        "flag": "https://restcountries.eu/data/tca.svg",
                        "name": "Turks and Caicos Islands"
                    },
                    {
			"id":235,
                        "flag": "https://restcountries.eu/data/tuv.svg",
                        "name": "Tuvalu"
                    },
                    {
			"id":236,
                        "flag": "https://restcountries.eu/data/uga.svg",
                        "name": "Uganda"
                    },
                    {
			"id":237,
                        "flag": "https://restcountries.eu/data/ukr.svg",
                        "name": "Ukraine"
                    },
                    {
			"id":238,
                        "flag": "https://restcountries.eu/data/are.svg",
                        "name": "United Arab Emirates"
                    },
                    {
			"id":239,
                        "flag": "https://restcountries.eu/data/gbr.svg",
                        "name": "United Kingdom of Great Britain and Northern Ireland"
                    },
                    {
			"id":240,
                        "flag": "https://restcountries.eu/data/usa.svg",
                        "name": "United States of America"
                    },
                    {
			"id":241,
                        "flag": "https://restcountries.eu/data/ury.svg",
                        "name": "Uruguay"
                    },
                    {
			"id":242,
                        "flag": "https://restcountries.eu/data/uzb.svg",
                        "name": "Uzbekistan"
                    },
                    {
			"id":243,
                        "flag": "https://restcountries.eu/data/vut.svg",
                        "name": "Vanuatu"
                    },
                    {
			"id":244,
                        "flag": "https://restcountries.eu/data/ven.svg",
                        "name": "Venezuela (Bolivarian Republic of)"
                    },
                    {
			"id":245,
                        "flag": "https://restcountries.eu/data/vnm.svg",
                        "name": "Viet Nam"
                    },
                    {
			"id":246,
                        "flag": "https://restcountries.eu/data/wlf.svg",
                        "name": "Wallis and Futuna"
                    },
                    {
			"id":247,
                        "flag": "https://restcountries.eu/data/esh.svg",
                        "name": "Western Sahara"
                    },
                    {
			"id":248,
                        "flag": "https://restcountries.eu/data/yem.svg",
                        "name": "Yemen"
                    },
                    {
			"id":249,
                        "flag": "https://restcountries.eu/data/zmb.svg",
                        "name": "Zambia"
                    },
                    {
			"id":250,
                        "flag": "https://restcountries.eu/data/zwe.svg",
                        "name": "Zimbabwe"
                    }
                ]
                
def get_country_detail(c_id):
    for country in all_countries:
        if country['id'] == c_id:
            return country
