import json

# List of emails to remove
emails_to_remove = [
    "anuradha.das@gmail.com", "camayankarora@yahoo.in", "duapuja@gmail.com", "singh.saurav9500@gmail.com",
    "chahatishanksahani@gmail.com", "tanyakandari96@gmail.com", "Dhwanidj.2009@gmail.com", "maansikhanna@gmail.com",
    "nehaagarwal11006@gmail.com", "vaishalijain01@gmail.com", "luckyamit@gmail.com", "patnisanskaar@gmail.com",
    "neeta.sharma010@gmail.com", "gaurvi.arora11@gmail.com", "guptaprabhav131@gmail.com", "kotwal_chetna@yahoo.com",
    "jasminejazzy@gmail.com", "jsonal@hotmail.com", "vanishka.sh@gmail.com", "raghu.leo@gmail.com",
    "rahul121286@gmail.com", "sushil.kakkar@gmail.com", "vanishka.sh@gmail.com", "divijamalhotra@gmail.com",
    "aryangogu@gmail.com", "kotwal_chetna@yahoo.com", "rashmiarora20.ra@gmail.com", "apurvakedia1999@gmail.com",
    "smitagoyal81@gmail.com", "neha.bedi82@gmail.com", "aliazizk@gmail.com", "kshitizarora2000@gmail.com",
    "muskan.mohan1@gmail.com", "roopa.narayan@ctlindia.org", "surbhimalik374@gmail.com", "kanikapuri.chugh@gmail.com",
    "shubhamdubey339@gmail.com", "shilpa.tayal@gmail.com", "vipulx201@gmail.com", "Prernanegi72@gmail.com",
    "deeksha.s456@gmail.com", "yashikachawla150@gmail.com", "kaushikgargi11@gmail.com", "kanikapatni15@gmail.com",
    "kanikapatni15@gmail.com", "priyank.agg6@gmail.com", "singhalshivek24@gmail.com", "singhalshivek24@gmail.com",
    "advanjali.rajput@gmail.com", "deepa@dialdforparty.com", "nancygulani@gmail.com", "ishanig97@gmail.com",
    "aseeskaur711@gmail.com", "gujraljami@gmail.com", "singhalshivek24@gmail.com", "raina.vidushi@gmail.com",
    "khyatigupta199@gmail.com", "sidskaul@gmail.com", "rdas51474@gmail.com", "richakale2@gmail.com",
    "aarushichopra@ymail.com", "sur.gupta@gmail.com", "abhishek.tewari@gmail.com", "Pallavi_sharma1435@yahoo.com",
    "kanchansaharsh@gmail.com", "aadhayakapila@gmail.com", "tanyakandari96@gmail.com", "swatika1991@gmail.com",
    "shreya.arun.yadav@gmail.com", "ziakrishan@gmail.com", "vanishka.sh@gmail.com", "chopraa.nehaa@gmail.com",
    "jahnvisingh2502@gmail.com", "ankit.wahal78@gmail.com", "kshitij.kalra@yahoo.com", "uppalshagun18@gmail.com",
    "aashnagupta.in@gmail.com", "hemadriyadav@gmail.com", "jayabhadauria@rediffmail.com", "mishaka89@gmail.com",
    "ditadsouza@gmail.com", "jainharshita2602@gmail.com", "shriiya20@gmail.com", "adiyadav.1729@gmail.com",
    "aditimalhotra85@gmail.com", "aashima.cs@gmail.com", "junejakunal@hotmail.com", "shreyatiwari0000@gmail.com",
    "kritika90sharma@gmail.com", "aparnapande20@gmail.com", "deepali.dhar7@gmail.com", "vermakumar663@gmail.com",
    "anshitakubba@gmail.com", "brinda.anand27@gmail.com", "nainikaburman1@gmail.com", "suparnapopli@gmail.com",
    "anvi.anjali@gmail.com", "chakhaiyar.lipi@gmail.com", "1392divyasharma@gmail.com", "anvisoni86@gmail.com",
    "Alok@swastikpolymers.net", "anvibhagat1@gmail.com", "ravisha.madan@makemytrip.in", "dishaberry1@gmail.com",
    "ankitadhingra@gmail.com", "rahulbagga2006@yahoo.co.in", "muskan1011@outlook.com", "sarahbatra9@gmail.com",
    "prernasinghal38@gmail.com", "shwetabansal228@gmail.com", "goelmansi3097@gmail.com", "adv.abhishek84@gmail.com",
    "ca.dhruvjoshi@gmail.com", "singhania.neha2008@gmail.com", "charujain05@gmail.com", "kashishsareesuit@gmail.com",
    "bansalarshiya05@gmail.com", "darshikathakur@gmail.com", "prerna1308@gmail.com", "aseeskaur711@gmail.com",
    "ammritabakshi7@gmail.com", "simransehgal2297@gmail.com", "aasyat915@gmail.com", "divijamalhotra@gmail.com",
    "deeksha.s456@gmail.com", "kaul.arjun2@gmail.com", "canehajain389@gmail.com", "guptaavani74@gmail.com",
    "neha93bansal@gmail.com", "kajaltalreja1012@gmail.com", "jasvinder.chawla78@gmail.com", "himanikalra18@gmail.com",
    "surbhimalik374@gmail.com", "doc_triveni@yahoo.com", "arpita.bose90@yahoo.com", "deepanshi.kamboj12@gmail.com",
    "tejasvgupta.12@gmail.com", "iamshubhamsainii@gmail.com", "vibhu.sagar96@gmail.com", "vaastavjain@gmail.com",
    "sarvagyavij@gmail.com", "vish.onein@gmail.com", "shruti1487k@gmail.com", "shagunparuthi@ms.du.ac.in",
    "ritu_aggarwal_k@yahoo.com", "shwet1404@gmail.com", "kabirmaan91@gmail.com", "sehgalanu83@gmail.com",
    "abhishek.tewari@gmail.com", "wadhawanvaishanavi@gmail.com", "mehek.ky@gmail.com", "bhasin.rahul1838@gmail.com",
    "rashi.miranda@gmail.com", "vanshikadhawan606@gmail.com", "dani.alisha26@gmail.com", "manas210890@gmail.com",
    "akanksha.sharma2497@gmail.com", "kerrysharma1903@gmail.com", "drsamratha23@gmail.com", "snigdhabanrji@gmail.com",
    "esha.s.lall@gmail.com", "komal.agarwal2083@yahoo.com", "mmkmgm86@gmail.com", "urvashiijagota@gmail.com",
    "duapuja@gmail.com", "priyanka.canadianstudy@gmail.com", "muskann.2812@gmail.com", "chawla20richa@gmail.com",
    "shwet1404@gmail.com", "priyanka.canadianstudy@gmail.com", "rupali_1785@gmail.com", "rummy.gupta2gmail.com",
    "yashika2798@gmail.com", "kanikapuri.chugh@gmail.com", "Taranjeetk40@gmail.com", "dranu1982@yahoo.co.in",
    "aanyachandna26@gmail.com"
]

# Load the JSON file
with open('promo_code.json', 'r') as file:
    data = json.load(file)

# Function to check if an object contains any of the specified emails
def contains_email(obj, emails):
    return any(email in obj.get('email', '') for email in emails)

# Filter out objects containing the specified emails
filtered_data = [obj for obj in data if not contains_email(obj, emails_to_remove)]

# Save the updated JSON file
with open('promo_code.json', 'w') as file:
    json.dump(filtered_data, file, indent=4)

print("Filtered data saved to 'filtered_data.json'")
