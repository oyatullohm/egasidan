from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .utils import unique_slug


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='sub_category/', blank=True, null=True)
    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.region.name})"


class Image(models.Model):
    image = models.ImageField(upload_to='product_images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} uploaded at {self.uploaded_at}"


class Brand(models.Model):
    BRAND_TYPE = (
        ("avto","avto"),
        ("electronics","electronics"),
        ("boshqa","boshqa"),
    ) 
    
    type = models.CharField(max_length=100, choices=BRAND_TYPE, default='avto' )
    name = models.CharField(max_length=100, unique=True)


class Modell(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)


class BaseProduct(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Yangi'),
        ('like_new', 'Yangi kabi'),
        ('excellent', 'Aʼlo'),
        ('good', 'Yaxshi'),
        ('fair', 'Qoniqarli'),
        ('needs_repair', 'Taʼmirlash talab qiladi'),
        ('for_parts', 'Ehtiyot qismlar uchun'),
    ]

    SOLD_CHOICES = [
        ('sold', 'Sotilgan'),
        ('not_sold', 'Sotilmagan'),
    ]
      # <-- slug
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    old_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    condition = models.CharField(max_length=55, choices=CONDITION_CHOICES, default='new')
    sold = models.CharField(max_length=55, choices=SOLD_CHOICES, default='not_sold')

    category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    district = models.ForeignKey('District', on_delete=models.SET_NULL, null=True)
    image = models.ManyToManyField('Image',blank=True)
    address = models.TextField(blank=True)
    produced = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=13)

    is_active = models.BooleanField(default=True)
    is_vip = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    lan = models.CharField(max_length=155, blank=True)
    long = models.CharField(max_length=155, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_products')
    telegram = models.CharField(max_length=100, blank=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


# transport vositalari
class Vehicle(BaseProduct):
    VEHICLE_TYPES = [
    # Yengil avtomobillar
    ('sedan', 'Sedan'),
    ('hatchback', 'Hatchback'),
    ('universal', 'Universal'),
    ('coupe', 'Kupe'),
    ('cabrio', 'Kabriolet'),
    ('limousine', 'Limuzin'),
    ('pickup', 'Pikap'),
    ('crossover', 'Krossover'),
    ('suv', 'SUV'),
    ('minivan', 'Miniven'),
    ('van', 'Furgon'),
    
    # Mototsikllar
    ('sportbike', 'Sport mototsikl'),
    ('cruiser', 'Kruzer mototsikl'),
    ('touring', 'Turing mototsikl'),
    ('scooter', 'Skuter'),
    ('atv', 'KVADROTSIKL (ATV)'),
    ('enduro', 'Enduro mototsikl'),
    ('chopper', 'Chopper'),
    ('naked', 'Neyked bik'),
    ('motocross', 'Motokross'),
    
    # Yuk mashinalari
    ('light_truck', 'Yengil yuk mashinasi'),
    ('medium_truck', 'Oʻrta yuk mashinasi'),
    ('heavy_truck', 'Ogʻir yuk mashinasi'),
    ('tractor', 'Traktor'),
    ('dump_truck', 'Samosval'),
    ('tanker', 'Tsisterna'),
    ('refrigerator', 'Refrijerator'),
    ('tow_truck', 'Evakuator'),
    
    # Avtobuslar
    ('minibus', 'Mikroavtobus'),
    ('city_bus', 'Shahar avtobusi'),
    ('intercity_bus', 'Qatnovlararo avtobus'),
    ('tourist_bus', 'Turist avtobusi'),
    ('school_bus', 'Maktab avtobusi'),
    
    # Maxsus texnika
    ('construction', 'Qurilish texnikasi'),
    ('agricultural', 'Qishloq xoʻjalik texnikasi'),
    ('municipal', 'Kommunal texnika'),
    ('military', 'Harbiy texnika'),
    
    # Ehtiyot qismlar va aksessuarlar
    ('parts', 'Ehtiyot qismlar'),
    ('tires', 'Shinalar va gʻildiraklar'),
    ('accessories', 'Aksessuarlar'),
    ('audio', 'Avtoaudio va multimedia'),
    ('security', 'Xavfsizlik tizimlari'),
    ('tools', 'Asbob-uskunalar'),
    ('tuning', 'Tuning va stylish'),
    ('electronics', 'Avtoelektronika'),
    ('lights', 'Chiroq va yoritish'),
    ('engine_parts', 'Dvigatel ehtiyot qismlari'),
    ('transmission_parts', 'Transmissiya ehtiyot qismlari'),
    ('suspension_parts', 'Osma qismlari'),
    ('brake_system', 'Tormoz tizimi'),
    ('exhaust_system', 'Chiqqish tizimi'),
    ('cooling_system', 'Sovutish tizimi'),
    ('fuel_system', 'Yoqilgʻi tizimi'),
    ('electrical_system', 'Elektr tizimi'),
    ('body_parts', 'Kuzov ehtiyot qismlari'),
    ('interior_parts', 'Salon ehtiyot qismlari'),
    ('glass', 'Shisha va oynalar'),
    ('oil_fluids', 'Moylar va suyuqliklar'),
    ('filters', 'Filtrlar'),
    ('belts_hoses', 'Kamarlar va shlanglar'),
    ('batteries', 'Akkumulyatorlar'),
    
    # Qo'shimcha toifalar
    ('trailer', 'Treler va yarimtreyler'),
    ('caravan', 'Karavan'),
    ('water_transport', 'Suv transporti'),
    ('air_transport', 'Havo transporti'),
    ('other', 'Boshqa transport vositalari'),
]
    
    FUEL_TYPES = [
        ('petrol', 'Benzin'),
        ('diesel', 'Dizel'),
        ('electric', 'Elektro'),
        ('hybrid', 'Gibrid'),
        ('gas-metan', 'gaz-metan'),
        ('gas-propan', 'gaz-propan'),
        ('petrol + gas-metan', 'Benzin + gaz-metan'),
        ('petrol + gas-propan', 'Benzin + gaz-propan'),
        ('other', 'Boshqa'),
    ]
    
    TRANSMISSION_TYPES = [
        ('manual', 'Mexanika'),
        ('automatic', 'Avtomat'),
        ('semi_automatic', 'Yarim avtomat'),
        ('other', 'Boshqa'),
    ]

    vehicle_type = models.CharField(max_length=55, choices=VEHICLE_TYPES )
    brand = models.CharField(max_length=100)
    model = models.ForeignKey(Modell, on_delete=models.SET_NULL, null=True, blank=True)
    # year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField(help_text="Km da")
    engine_size = models.DecimalField(max_digits=3, decimal_places=1, help_text="Litrda")
    fuel_type = models.CharField(max_length=55, choices=FUEL_TYPES)
    transmission = models.CharField(max_length=55, choices=TRANSMISSION_TYPES)
    color = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

# ko'chmas mulk
class Property(BaseProduct):
    PROPERTY_TYPES = [
    # Kvartiralar
    ('apartment', 'Kvartira'),
    ('studio', 'Studiya kvartira'),
    ('1_room', '1 xonali kvartira'),
    ('2_room', '2 xonali kvartira'),
    ('3_room', '3 xonali kvartira'),
    ('4_room', '4 xonali kvartira'),
    ('5_room', '5+ xonali kvartira'),
    ('penthouse', 'Penthaus'),
    ('apartment_floor', 'Butun qavat kvartirasi'),
    ('apartment_building', 'Kvartiralar binosi'),
    ('new_apartment', 'Yangi qurilgan kvartira'),
    ('secondary_apartment', 'Ikkilamchi kvartira'),
    
    # Uylar
    ('house', 'Uy'),
    ('cottage', 'Kottej'),
    ('villa', 'Villa'),
    ('townhouse', 'Taunhaus'),
    ('duplex', 'Dyupleks'),
    ('triplex', 'Tripleks'),
    ('mansion', 'Imonat uy'),
    ('country_house', 'Dacha'),
    ('farmhouse', 'Ferma uyi'),
    ('guest_house', 'Mehmonxona uyi'),
    ('prefabricated_house', 'Yigʻma uy'),
    ('log_house', 'Yogʻoch uy'),
    ('eco_house', 'Ekologik uy'),
    
    # Tijorat binolari
    ('commercial', 'Tijorat binosi'),
    ('office', 'Ofis'),
    ('office_building', 'Ofis binosi'),
    ('shop', 'Doʻkon'),
    ('shopping_center', 'Savdo markazi'),
    ('mall', 'Torgoviy markaz'),
    ('store', 'Magazin'),
    ('supermarket', 'Supermarket'),
    ('market_stall', 'Bozor doʻkoni'),
    ('shopping_area', 'Savdo maydoni'),
    ('restaurant', 'Restoran'),
    ('cafe', 'Kafe'),
    ('bar', 'Bar'),
    ('teahouse', 'Choyxona'),
    ('hotel', 'Mehmonxona'),
    ('motel', 'Motel'),
    ('hostel', 'Hostel'),
    ('guesthouse', 'B&B'),
    ('warehouse', 'Ombor'),
    ('storage', 'Saqlash binosi'),
    ('industrial', 'Sanoat binosi'),
    ('factory', 'Fabrika'),
    ('manufacturing', 'Ishlab chiqarish binosi'),
    ('workshop', 'Ustaxona'),
    ('gas_station', 'Yoqilgʻi shaxobchasi'),
    ('car_service', 'Avtoservis'),
    ('car_wash', 'Avtomoyka'),
    ('showroom', 'Shourum'),
    ('exhibition_hall', 'Koʻrgazma zali'),
    ('conference_hall', 'Konferensiya zali'),
    ('sports_facility', 'Sport inshooti'),
    ('gym', 'Sport zali'),
    ('fitness_center', 'Fitnes markazi'),
    ('spa', 'SPA markazi'),
    ('beauty_salon', 'Goʻzallik saloni'),
    ('barbershop', 'Sartaroshxona'),
    ('clinic', 'Klinika'),
    ('pharmacy', 'Dorixona'),
    ('school', 'Maktab'),
    ('kindergarten', 'Bogʻcha'),
    ('university', 'Universitet'),
    ('training_center', 'Oʻquv markazi'),
    ('cinema', 'Kinoteatr'),
    ('theater', 'Teatr'),
    ('entertainment_center', 'Koʻngilochar markaz'),
    ('nightclub', 'Tungi klub'),
    
    # Er uchastkalari
    ('land', 'Er uchastkasi'),
    ('residential_land', 'Turar joy eri'),
    ('commercial_land', 'Tijorat eri'),
    ('agricultural_land', 'Qishloq xoʻjalik eri'),
    ('farm_land', 'Ferma eri'),
    ('industrial_land', 'Sanoat eri'),
    ('recreational_land', 'Dam olish eri'),
    ('forest_land', 'Oʻrmon eri'),
    ('waterfront_land', 'Suv qirgʻogʻi eri'),
    ('mountain_land', 'Togʻ eri'),
    ('plot', 'Er uchastkasi (lot)'),
    ('field', 'Dala'),
    ('orchard', 'Bogʻ'),
    ('vineyard', 'Vino uzum bogʻi'),
    ('garden', 'Bogʻcha'),
    ('pasture', 'Yaylov'),
    
    # Garajlar va avtoturargohlar
    ('garage', 'Garaj'),
    ('car_park', 'Avtoturargoh'),
    ('parking_space', 'Parkovka joyi'),
    ('underground_parking', 'Er osti parkovkasi'),
    ('multi_story_parking', 'Koʻp qavatli parkovka'),
    
    # Xususiy mulklar
    ('basement', 'Podval'),
    ('cellar', 'Yertoʻla'),
    ('attic', 'Cherdak'),
    ('loft', 'Loft'),
    ('commercial_space', 'Tijorat maydoni'),
    ('retail_space', 'Chakana savdo maydoni'),
    ('office_space', 'Ofis maydoni'),
    ('industrial_space', 'Sanoat maydoni'),
    ('storage_space', 'Saqlash maydoni'),
    ('co_working', 'Koworking'),
    
    # Qishloq xoʻjalik binolari
    ('barn', 'Omborxona'),
    ('stable', 'Ot uyasi'),
    ('greenhouse', 'Issiqxona'),
    ('poultry_house', 'Parrandaxona'),
    ('livestock_building', 'Chorvadorlik binosi'),
    ('silo', 'Silo'),
    ('mill', 'Tegirmon'),
    
    # Maxsus mulklar
    ('historical', 'Tarixiy bino'),
    ('religious', 'Diniy bino'),
    ('castle', 'Qasr'),
    ('palace', 'Saroy'),
    ('lighthouse', 'Mayak'),
    ('windmill', 'Shamol tegirmoni'),
    ('watermill', 'Suv tegirmoni'),
    
    # Turizm va dam olish
    ('resort', 'Turizm bazasi'),
    ('camping', 'Kemping'),
    ('caravan_park', 'Karavan park'),
    ('holiday_home', 'Dam olish uyi'),
    ('ski_resort', 'Changʻi kurorti'),
    ('beach_house', 'Plyaj uyi'),
    ('island', 'Orol'),
    
    # Qurilish va rivojlanish
    ('construction_site', 'Qurilish maydoni'),
    ('development_land', 'Rivojlanish eri'),
    ('renovation_project', 'Renovatsiya loyihasi'),
    ('investment_property', 'Investitsion mulk'),
    
    # Boshqa mulk turlari
    ('mobile_home', 'Mobil uy'),
    ('container_home', 'Konteyner uy'),
    ('tree_house', 'Daraxt uyi'),
    ('houseboat', 'Uy qayiqi'),
    ('cave_house', 'Gʻor uyi'),
    ('underground_house', 'Er osti uyi'),
    
    # Boshqa
    ('other', 'Boshqa koʻchmas mulk'),
    ]
    property_type = models.CharField(max_length=55, choices=PROPERTY_TYPES )
    area = models.DecimalField(max_digits=8, decimal_places=2, help_text="m² da")
    rooms = models.PositiveIntegerField()

    
    def __str__(self):
        return f"{self.get_property_type_display()} - {self.rooms} xona"

# elektronika va maishiy texnika
class Electronics(BaseProduct):
    ELECTRONIC_TYPES = [
    # Telefonlar va aksessuarlar
    ('smartphone', 'Smartfon'),
    ('feature_phone', 'Oddiy telefon'),
    ('phone_case', 'Telefon qopqogʻi'),
    ('phone_charger', 'Zaryadlovchi'),
    ('power_bank', 'Powerbank'),
    ('phone_holder', 'Telefon ushlagichi'),
    ('headphones', 'Naushniklar'),
    ('earphones', 'Quloqchinlar'),
    ('bluetooth_speaker', 'Bluetooth kolonka'),
    ('phone_repair', 'Telefon taʼmirlash'),
    ('phone_accessories', 'Telefon aksessuarlari'),
    
    # Noutbuklar va kompyuterlar
    ('laptop', 'Noutbuk'),
    ('ultrabook', 'Ultrabuk'),
    ('gaming_laptop', 'Geyming noutbuk'),
    ('business_laptop', 'Biznes noutbuk'),
    ('desktop', 'Stol kompyuteri'),
    ('monitor', 'Monitor'),
    ('keyboard', 'Klaviatura'),
    ('mouse', 'Sichqoncha'),
    ('webcam', 'Veb-kamera'),
    ('laptop_bag', 'Noutbuk sumkasi'),
    ('laptop_stand', 'Noutbuk stendi'),
    ('laptop_charger', 'Noutbuk zaryadlovchisi'),
    ('laptop_cooler', 'Noutbuk sovutgichi'),
    ('laptop_repair', 'Noutbuk taʼmirlash'),
    
    # Planshetlar va e-kitoblar
    ('tablet', 'Planshet'),
    ('graphic_tablet', 'Grafik planshet'),
    ('ebook_reader', 'Elektron kitob oʻqishgich'),
    ('tablet_case', 'Planshet qopqogʻi'),
    ('tablet_pen', 'Planshet qalami'),
    ('tablet_stand', 'Planshet stendi'),
    ('tablet_charger', 'Planshet zaryadlovchisi'),
    
    # Televizorlar va proektorlar
    ('tv', 'Televizor'),
    ('smart_tv', 'Smart TV'),
    ('oled_tv', 'OLED TV'),
    ('qled_tv', 'QLED TV'),
    ('projector', 'Proektor'),
    ('tv_stand', 'TV stendi'),
    ('tv_wall_mount', 'TV devor braketti'),
    ('tv_antenna', 'TV antennasi'),
    ('tv_box', 'TV box'),
    ('remote_control', 'Pult boshqaruv'),
    
    # Kameralar va foto
    ('camera', 'Kamera'),
    ('dslr', 'DSLR kamera'),
    ('mirrorless', 'Mirrorless kamera'),
    ('action_camera', 'Ekşn kamera'),
    ('drone', 'Dron'),
    ('camera_lens', 'Kamera obʼektivi'),
    ('tripod', 'Tripod'),
    ('camera_bag', 'Kamera sumkasi'),
    ('memory_card', 'Xotira kartasi'),
    ('camera_filter', 'Kamera filtri'),
    ('camera_flash', 'Kamera chirogʻi'),
    ('camera_battery', 'Kamera batareyasi'),
    ('camera_charger', 'Kamera zaryadlovchisi'),
    
    # Audio texnika
    ('headphones', 'Naushniklar'),
    ('earbuds', 'Quloqchinlar'),
    ('headset', 'Garnitura'),
    ('soundbar', 'Soundbar'),
    ('home_theater', 'Uy kinoteatri'),
    ('speaker', 'Kolonkalar'),
    ('microphone', 'Mikrofon'),
    ('amplifier', 'Kuchaytirgich'),
    ('receiver', 'Qabul qilgich'),
    ('mixer', 'Mikser'),
    ('audio_cable', 'Audio kabellari'),
    ('audio_interface', 'Audio interfeys'),
    ('vinyl_player', 'Vinil pleer'),
    ('karaoke', 'Karaoke apparati'),
    
    # Oʻyin uchun texnika
    ('gaming_console', 'Oʻyin konsoli'),
    ('gaming_pc', 'Geyming kompyuter'),
    ('vr_headset', 'VR shlyapa'),
    ('gamepad', 'Gamepad'),
    ('gaming_chair', 'Geyming stul'),
    ('gaming_desk', 'Geyming stol'),
    ('gaming_mouse', 'Geyming sichqoncha'),
    ('gaming_keyboard', 'Geyming klaviatura'),
    ('gaming_monitor', 'Geyming monitor'),
    ('gaming_headset', 'Geyming garnitura'),
    ('game_controller', 'Oʻyin kontrolleri'),
    ('gaming_accessories', 'Geyming aksessuarlari'),
    
    # Uy ofis texnikasi
    ('printer', 'Printer'),
    ('scanner', 'Skanner'),
    ('copier', 'Kopiya apparati'),
    ('fax', 'Faks'),
    ('shredder', 'Hujjat yoʻqotgich'),
    ('calculator', 'Kalkulyator'),
    ('label_maker', 'Yorliq printeri'),
    ('laminator', 'Laminator'),
    ('binding_machine', 'Jildlash mashinasi'),
    
    # Tarmoq va internet
    ('router', 'Router'),
    ('modem', 'Modem'),
    ('switch', 'Switch'),
    ('access_point', 'Access point'),
    ('network_cable', 'Tarmoq kabeli'),
    ('wifi_adapter', 'Wi-Fi adapter'),
    ('wifi_extender', 'Wi-Fi kengaytirgich'),
    ('nas', 'NAS server'),
    ('vpn_router', 'VPN router'),
    
    # Maishiy texnika
    ('smart_home', 'Aqlli uy'),
    ('smart_lighting', 'Aqlli yoritish'),
    ('smart_lock', 'Aqlli qulf'),
    ('smart_thermostat', 'Aqlli termostat'),
    ('security_camera', 'Xavfsizlik kameralari'),
    ('doorbell_camera', 'Qoʻngʻiroq kamera'),
    ('robot_vacuum', 'Robot changyutgich'),
    ('air_purifier', 'Havo tozalagich'),
    ('smart_plug', 'Aqlli rozetka'),
    ('smart_speaker', 'Aqlli kolonka'),
    
    # Elektronika ehtiyot qismlari
    ('battery', 'Batareya'),
    ('adapter', 'Adapter'),
    ('charger', 'Zaryadlovchi'),
    ('cable', 'Kabel'),
    ('connector', 'Konnektor'),
    ('docking_station', 'Dok stansiya'),
    ('hub', 'Hab'),
    ('cooling_pad', 'Sovutish podstavkasi'),
    ('screen_protector', 'Ekran himoyasi'),
    ('stylus', 'Stylus qalam'),
    ('memory_card', 'Xotira kartasi'),
    ('ssd', 'SSD disk'),
    ('hdd', 'HDD disk'),
    ('ram', 'Operativ xotira'),
    ('graphics_card', 'Video karta'),
    ('motherboard', 'Motherboard'),
    ('processor', 'Protsessor'),
    ('power_supply', 'Blok pitaniya'),
    ('computer_case', 'Kompyuter korpusi'),
    ('thermal_paste', 'Termopasta'),
    
    # Elektronika taʼmirlash
    ('phone_repair', 'Telefon taʼmirlash'),
    ('laptop_repair', 'Noutbuk taʼmirlash'),
    ('tablet_repair', 'Planshet taʼmirlash'),
    ('tv_repair', 'Televizor taʼmirlash'),
    ('camera_repair', 'Kamera taʼmirlash'),
    ('console_repair', 'Konsol taʼmirlash'),
    ('pc_repair', 'Kompyuter taʼmirlash'),
    
    # Boshqa elektronika
    ('smart_watch', 'Aqlli soat'),
    ('fitness_tracker', 'Fitnes brasleti'),
    ('digital_frame', 'Raqamli ramka'),
    ('digital_photo_frame', 'Raqamli foto ramka'),
    ('e_scooter', 'Elektrosamokat'),
    ('e_bike', 'Elektrovelosiped'),
    ('power_tool', 'Elektrik asboblar'),
    ('soldering_iron', 'Lehimlash apparati'),
    ('multimeter', 'Multimetr'),
    ('oscilloscope', 'Oscilloscope'),
    ('drone_accessories', 'Dron aksessuarlari'),
    ('electronic_components', 'Elektron komponentlar'),
    ('arduino', 'Arduino'),
    ('raspberry_pi', 'Raspberry Pi'),
    ('robotics', 'Robototexnika'),
    ('diy_electronics', 'Elektronika DIY'),
    
    # Boshqa
    ('other', 'Boshqa elektronika'),
]
    electronic_type = models.CharField(max_length=55, choices=ELECTRONIC_TYPES )
    brand = models.CharField(max_length=100)
    model = models.ForeignKey(Modell, on_delete=models.CASCADE, related_name='electronics')
    warranty = models.BooleanField(default=False)
    warranty_months = models.PositiveIntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.brand} {self.model}"

# Ish o'rinlari
class Job(BaseProduct):
    JOB_TYPES = [
    ('hybrid', 'Gibrid ish'),
    ('contract', 'Shartnoma asosida'),
    ('temporary', 'Vaqtinchalik'),
    ('seasonal', 'Mavsumiy'),
    ('project_based', 'Loyiha asosida'),
    ('hourly', 'Soatbay ish'),
    ('daily', 'Kunbay ish'),
    ('weekly', 'Haftabay ish'),
    ('monthly', 'Oylik ish'),

    ('expert', 'Ekspert'),
    ('manager', 'Menejer'),
    ('director', 'Direktor'),
    ('executive', 'Rahbar'),
    ('volunteer', 'Koʻngilli'),

    ('it', 'IT va Dasturiy taʼminot'),
    ('finance', 'Moliya va Bank ishi'),
    ('healthcare', 'Sogʻliqni saqlash'),
    ('education', 'Taʼlim'),
    ('construction', 'Qurilish'),
    ('manufacturing', 'Ishlab chiqarish'),
    ('retail', 'Chakana savdo'),
    ('hospitality', 'Mehmondoʻstlik'),
    ('transportation', 'Transport va Logistika'),
    ('marketing', 'Marketing va Reklama'),
    ('sales', 'Sotuv'),
    ('customer_service', 'Mijozlar xizmati'),
    ('hr', 'HR va Rekruting'),
    ('legal', 'Huquq va Yurisprudensiya'),
    ('design', 'Dizayn va Sanʼat'),
    ('media', 'Media va Nashriyot'),
    ('engineering', 'Muhandislik'),
    ('science', 'Fan va Tadqiqot'),
    ('government', 'Davlat xizmati'),
    ('non_profit', 'Notijorat tashkilotlar'),
    ('agriculture', 'Qishloq xoʻjaligi'),
    ('energy', 'Energetika'),
    ('telecom', 'Telekommunikatsiya'),
    ('real_estate', 'Koʻchmas mulk'),
    ('insurance', 'Sugʻurta'),
    ('consulting', 'Konsalting'),
    ('security', 'Xavfsizlik'),
    ('cleaning', 'Tozalash xizmati'),
    ('beauty', 'Goʻzallik va Salomatlik'),
    ('fitness', 'Fitnes va Sport'),
    ('entertainment', 'Koʻngilochar'),
    ('tourism', 'Turizm'),
    ('automotive', 'Avtomobilsozlik'),
    ('aviation', 'Aviatsiya'),
    ('maritime', 'Dengizchilik'),
    ('mining', 'Konchilik'),
    ('pharmaceutical', 'Farmatsevtika'),
    ('biotech', 'Biotexnologiya'),

    # Boshqa
    ('other', 'Boshqa ish turi'),
    ]
    job_type = models.CharField(max_length=55, choices=JOB_TYPES )
    company = models.CharField(max_length=200)
    application_deadline = models.DateField(blank=True, null=True)
    remote_work = models.BooleanField(default=False)
    
    def __str__(self):
        return f" {self.company}"

# Xizmatlar
class Service(BaseProduct):
    SERVICE_TYPES = [
    # Ta'mirlash xizmatlari
    ('repair', 'Taʼmirlash'),
    ('electronics_repair', 'Elektronika taʼmirlash'),
    ('phone_repair', 'Telefon taʼmirlash'),
    ('computer_repair', 'Kompyuter taʼmirlash'),
    ('tv_repair', 'Televizor taʼmirlash'),
    ('appliance_repair', 'Maishiy texnika taʼmirlash'),
    ('car_repair', 'Avtomobil taʼmirlash'),
    ('bike_repair', 'Velosiped taʼmirlash'),
    ('watch_repair', 'Soat taʼmirlash'),
    ('shoe_repair', 'Poʻyabzal taʼmirlash'),
    ('clothing_repair', 'Kiyim-kechak taʼmirlash'),
    ('furniture_repair', 'Mebel taʼmirlash'),
    ('jewelry_repair', 'Zargarlik buyumlari taʼmirlash'),
    ('instrument_repair', 'Musiqa asboblari taʼmirlash'),
    
    # Tozalash xizmatlari
    ('cleaning', 'Tozalash'),
    ('house_cleaning', 'Uy tozalash'),
    ('office_cleaning', 'Ofis tozalash'),
    ('carpet_cleaning', 'Gilam tozalash'),
    ('window_cleaning', 'Deraza tozalash'),
    ('after_repair_cleaning', 'Taʼmirdan keyin tozalash'),
    ('industrial_cleaning', 'Sanoat tozalash'),
    ('pool_cleaning', 'Basseyn tozalash'),
    ('vehicle_cleaning', 'Transport vositalarini tozalash'),
    ('curtain_cleaning', 'Pardalar tozalash'),
    ('furniture_cleaning', 'Mebel tozalash'),
    ('disinfection', 'Dezinfeksiya'),
    ('pest_control', 'Zararkunandalarga qarshi kurash'),
    
    # Go'zallik va salomatlik
    ('beauty', 'Goʻzallik'),
    ('hair_salon', 'Soch olish'),
    ('barber', 'Sartarosh'),
    ('manicure', 'Manikyur'),
    ('pedicure', 'Pedikyur'),
    ('makeup', 'Makiyaj'),
    ('spa', 'SPA'),
    ('massage', 'Massaj'),
    ('cosmetology', 'Kosmetologiya'),
    ('eyelashes', 'Kiprik koshish'),
    ('eyebrows', 'Qosh koshish'),
    ('tattoo', 'Tatu'),
    ('piercing', 'Teshish'),
    ('barber', 'Sartarosh'),
    ('esthetics', 'Estetika'),
    ('nails', 'Tirnoq koshish'),
    ('hair_removal', 'Soch tozalash'),
    
    # Ta'lim xizmatlari
    ('education', 'Taʼlim'),
    ('tutoring', 'Dars berish'),
    ('language_courses', 'Til kurslari'),
    ('music_lessons', 'Musiqa darslari'),
    ('dance_lessons', 'Raqs darslari'),
    ('art_lessons', 'Sanʼat darslari'),
    ('sports_coaching', 'Sport murabbiyligi'),
    ('test_preparation', 'Imtihonga tayyorlash'),
    ('computer_courses', 'Kompyuter kurslari'),
    ('cooking_classes', 'Oshpazlik darslari'),
    ('driving_lessons', 'Haydovchilik darslari'),
    ('preschool_education', 'Maktabgacha taʼlim'),
    ('special_education', 'Maxsus taʼlim'),
    ('online_education', 'Onlayn taʼlim'),
    
    # Transport xizmatlari
    ('transport', 'Transport'),
    ('taxi', 'Taksi'),
    ('delivery', 'Yetkazib berish'),
    ('moving', 'Koʻchirish xizmati'),
    ('car_rental', 'Avtomobil ijarasi'),
    ('truck_rental', 'Yuk mashinasi ijarasi'),
    ('airport_transfer', 'Aeroport transferi'),
    ('courier', 'Kuryer xizmati'),
    ('freight', 'Yuk tashish'),
    ('passenger_transport', 'Yoʻlovchi tashish'),
    ('bike_delivery', 'Velosiped yetkazish'),
    ('food_delivery', 'Ovqat yetkazish'),
    ('international_shipping', 'Xalqaro yuk tashish'),
    
    # Qurilish va ta'mirlash
    ('construction', 'Qurilish'),
    ('renovation', 'Renovatsiya'),
    ('plumbing', 'Santexnika'),
    ('electrical', 'Elektrika'),
    ('carpentry', 'Duradgorlik'),
    ('painting', 'Boʻyash'),
    ('plastering', 'Gipslash'),
    ('tiling', 'Plitka ishlari'),
    ('roofing', 'Tom ishlari'),
    ('flooring', 'Pol ishlari'),
    ('masonry', 'Bino qurish'),
    ('welding', 'Payvandlash'),
    ('demolition', 'Buzish'),
    ('landscaping', 'Landshaft dizayni'),
    ('fence_installation', 'Devor oʻrnatish'),
    
    # IT va texnologiya xizmatlari
    ('it_services', 'IT xizmatlar'),
    ('web_development', 'Veb dasturlash'),
    ('app_development', 'Mobil dastur yaratish'),
    ('software_development', 'Dasturiy taʼminot'),
    ('graphic_design', 'Grafik dizayn'),
    ('seo', 'SEO'),
    ('social_media', 'Ijtimoiy tarmoqlar'),
    ('video_editing', 'Video tahrirlash'),
    ('photo_editing', 'Foto tahrirlash'),
    ('data_recovery', 'Maʼlumotlarni tiklash'),
    ('network_setup', 'Tarmoq oʻrnatish'),
    ('tech_support', 'Texnik yordam'),
    ('cybersecurity', 'Kiberxavfsizlik'),
    ('cloud_services', 'Bulut xizmatlari'),
    
    # Tadbir va bayram xizmatlari
    ('event_services', 'Tadbir xizmatlari'),
    ('photography', 'Fotosurat'),
    ('videography', 'Video suratga olish'),
    ('catering', 'Oziq-ovqat xizmati'),
    ('decoration', 'Bezash'),
    ('entertainment', 'Koʻngilochar'),
    ('music_band', 'Musiqa guruhi'),
    ('dj', 'DJ'),
    ('host', 'Mehmonlarni kutib olish'),
    ('event_planning', 'Tadbir rejalashtirish'),
    ('wedding_services', 'Toʻy xizmatlari'),
    ('birthday_services', 'Tugʻilgan kun xizmatlari'),
    ('corporate_events', 'Korporativ tadbirlar'),
    
    # Xususiy xizmatlar
    ('personal_services', 'Xususiy xizmatlar'),
    ('personal_trainer', 'Shaxsiy murabbiy'),
    ('nutritionist', 'Dietolog'),
    ('psychologist', 'Psixolog'),
    ('lawyer', 'Advokat'),
    ('accountant', 'Buxgalter'),
    ('translator', 'Tarjimon'),
    ('interpreter', 'Tilltarjimon'),
    ('personal_assistant', 'Shaxsiy yordamchi'),
    ('elderly_care', 'Keksalarga gʻamxoʻrlik'),
    ('child_care', 'Bolalarga gʻamxoʻrlik'),
    ('pet_care', 'Hayvonlarga gʻamxoʻrlik'),
    ('house_sitting', 'Uy qorovulligi'),
    ('gardening', 'Bogʻbonlik'),
    
    # Savdo va marketing
    ('marketing', 'Marketing'),
    ('sales', 'Sotuv'),
    ('market_research', 'Bozor tadqiqoti'),
    ('branding', 'Brending'),
    ('printing', 'Bosish xizmatlari'),
    ('promotion', 'Promoution'),
    ('market_analysis', 'Bozor tahlili'),
    ('customer_research', 'Mijozlar tadqiqoti'),
    
    # Sog'liqni saqlash
    ('healthcare', 'Sogʻliqni saqlash'),
    ('nursing', 'Hamshiralik'),
    ('physiotherapy', 'Fizioterapiya'),
    ('dental', 'Stomatologiya'),
    ('optical', 'Koʻz kasalliklari'),
    ('pharmacy', 'Dorixona'),
    ('medical_equipment', 'Tibbiy uskunalar'),
    ('home_healthcare', 'Uyda tibbiy yordam'),
    
    # Ko'ngilochar va madaniyat
    ('entertainment', 'Koʻngilochar'),
    ('art', 'Sanʼat'),
    ('music', 'Musiqa'),
    ('dance', 'Raqs'),
    ('theater', 'Teatr'),
    ('film', 'Kino'),
    ('literature', 'Adabiyot'),
    ('crafts', 'Hunarmandchilik'),
    
    # Boshqa xizmatlar
    ('financial_services', 'Moliya xizmatlari'),
    ('insurance_services', 'Sugʻurta xizmatlari'),
    ('real_estate_services', 'Koʻchmas mulk xizmatlari'),
    ('travel_services', 'Sayohat xizmatlari'),
    ('consulting', 'Konsalting'),
    ('security_services', 'Xavfsizlik xizmatlari'),
    ('environmental_services', 'Atrof-muhit xizmatlari'),
    ('agricultural_services', 'Qishloq xoʻjaligi xizmatlari'),
    ('other', 'Boshqa xizmatlar'),
]
    service_type = models.CharField(max_length=55, choices=SERVICE_TYPES )
    experience_years = models.PositiveIntegerField(default=0)
    availability = models.CharField(max_length=100, default="Dushanba - Juma, 9:00 - 18:00")
    
    def __str__(self):
        return f"{self.get_service_type_display()} "

# Maishiy texnika va uy-ro'zg'or buyumlari
class HouseholdItems(BaseProduct):
    HOUSEHOLD_TYPES = [
    # Mebel
    ('furniture', 'Mebel'),
    ('sofa', 'Divan'),
    ('armchair', 'Kreslo'),
    ('bed', 'Krovat'),
    ('mattress', 'Matras'),
    ('wardrobe', 'Garderob'),
    ('closet', 'Shkaf'),
    ('dresser', 'Komed'),
    ('table', 'Stol'),
    ('desk', 'Yozuv stoli'),
    ('dining_table', 'Ovqatlanish stoli'),
    ('chair', 'Stul'),
    ('bookshelf', 'Kitob javoni'),
    ('cabinet', 'Shkafcha'),
    ('shelf', 'Javon'),
    ('rack', 'Dastalagich'),
    ('tv_stand', 'TV stendi'),
    ('coffee_table', 'Jurnal stoli'),
    ('nightstand', 'Tumba'),
    ('children_furniture', 'Bolalar mebeli'),
    ('office_furniture', 'Ofis mebeli'),
    ('garden_furniture', 'Bogʻ mebeli'),
    ('antique_furniture', 'Antikvar mebel'),
    
    # Maishiy texnika
    ('appliances', 'Maishiy texnika'),
    ('refrigerator', 'Muzlatgich'),
    ('washing_machine', 'Kir yuvish mashinasi'),
    ('dishwasher', 'Idish yuvish mashinasi'),
    ('oven', 'Pechka'),
    ('stove', 'Plita'),
    ('microwave', 'Mikrotoʻlqinli pech'),
    ('hood', 'Ventilyator'),
    ('air_conditioner', 'Konditsioner'),
    ('heater', 'Isitgich'),
    ('fan', 'Ventilyator'),
    ('vacuum_cleaner', 'Changyutgich'),
    ('iron', 'Dazmol'),
    ('sewing_machine', 'Tikuv mashinasi'),
    
    # Oshxona buyumlari
    ('kitchen', 'Oshxona buyumlari'),
    ('cookware', 'Oshxona idishlari'),
    ('cutlery', 'Pichogʻ-aslaha'),
    ('dishes', 'Idish-tovoq'),
    ('glassware', 'Shisha idishlar'),
    ('kitchen_knives', 'Oshxona pichoqlari'),
    ('pots', 'Kastryulalar'),
    ('pans', 'Tovalar'),
    ('kitchen_utensils', 'Oshxona asboblari'),
    ('kitchen_accessories', 'Oshxona aksessuarlari'),
    ('food_processor', 'Oziq-ovqat protsessori'),
    ('blender', 'Blender'),
    ('mixer', 'Mikser'),
    ('toaster', 'Toster'),
    ('coffee_maker', 'Kofe qaynatgich'),
    ('kettle', 'Choynak'),
    ('thermos', 'Termos'),
    
    # Interyer va bezaklar
    ('decor', 'Interyer va bezaklar'),
    ('carpet', 'Gilam'),
    ('rug', 'Kichik gilam'),
    ('curtain', 'Parda'),
    ('blinds', 'Jalyuzi'),
    ('mirror', 'Koʻzgu'),
    ('picture', 'Rasm'),
    ('photo_frame', 'Foto ramka'),
    ('vase', 'Guldasta'),
    ('clock', 'Soat'),
    ('candle', 'Sham'),
    ('statue', 'Haykal'),
    ('wall_decor', 'Devor bezagi'),
    ('table_decor', 'Stol bezagi'),
    ('shelf_decor', 'Javon bezagi'),
    
    # Yoritish
    ('lighting', 'Yoritish'),
    ('chandelier', 'Lyustra'),
    ('ceiling_light', 'Shift chirogʻi'),
    ('wall_light', 'Devor chirogʻi'),
    ('table_lamp', 'Stol chirogʻi'),
    ('floor_lamp', 'Poldagi chiroq'),
    ('spotlight', 'Projektor'),
    ('led_light', 'LED chiroq'),
    ('night_light', 'Tungi chiroq'),
    ('garden_light', 'Bogʻ chirogʻi'),
    ('emergency_light', 'Favqulodda chiroq'),
    
    # To'shak va chorshalar
    ('bedding', "To'shak va chorshalar"),
    ('bed_linen', 'Choyshab'),
    ('blanket', 'Adyol'),
    ('quilt', 'Korpusli adyol'),
    ('pillow', 'Yostiq'),
    ('mattress_pad', 'Matras prokladkasi'),
    ('bedspread', 'Krovat yopgichi'),
    ('duvet_cover', 'Adyol qopqogʻi'),
    ('pillowcase', 'Yostiq qopqogʻi'),
    ('mosquito_net', 'Chivin toʻri'),
    
    # Hojatxona va hammom
    ('bathroom', 'Hojatxona va hammom'),
    ('towel', 'Sochiq'),
    ('bath_mat', 'Hammom gilami'),
    ('shower_curtain', 'Dush parda'),
    ('toiletries', 'Hojatxona aksessuarlari'),
    ('soap_dish', 'Sovunqadogʻ'),
    ('toothbrush_holder', 'Tish choʻtka ushlagichi'),
    ('bathroom_cabinet', 'Hojatxona shkafi'),
    ('mirror_cabinet', 'Koʻzguli shkaf'),
    ('laundry_basket', 'Kir savati'),
    
    # Bolalar uchun
    ('kids', 'Bolalar uchun'),
    ('toys', 'Oʻyinchoqlar'),
    ('stroller', 'Aravacha'),
    ('crib', 'Bolalar karavati'),
    ('high_chair', 'Bolalar stulchasi'),
    ('playpen', 'Oʻyin maydonchasi'),
    ('baby_monitor', 'Bolalar kuzatuvchisi'),
    ('baby_carrier', 'Bolalar koʻtaragichi'),
    ('children_toys', 'Bolalar oʻyinchoqlari'),
    ('educational_toys', 'Oʻquv oʻyinchoqlari'),
    ('outdoor_toys', 'Koʻcha oʻyinchoqlari'),
    
    # Bogʻ va hovli
    ('garden', 'Bogʻ va hovli'),
    ('lawn_mower', 'Maysazor kesgich'),
    ('grill', 'Mangal'),
    ('garden_tools', 'Bogʻ asboblari'),
    ('watering_can', 'Suv sepagich'),
    ('hose', 'Shlang'),
    ('flower_pot', 'Gultuvak'),
    ('garden_decor', 'Bogʻ bezaklari'),
    ('outdoor_furniture', 'Koʻcha mebeli'),
    ('swing', 'Belanchak'),
    ('swimming_pool', 'Suzish havzasi'),
    ('greenhouse', 'Issiqxona'),
    
    # Saqlash idishlari
    ('storage', 'Saqlash idishlari'),
    ('box', 'Quti'),
    ('basket', 'Savat'),
    ('container', 'Konteyner'),
    ('bag', 'Sumka'),
    ('suitcase', 'Chamadon'),
    ('trunk', 'Sandiq'),
    ('plastic_container', 'Plastik konteyner'),
    ('glass_container', 'Shisha idish'),
    ('metal_container', 'Metall idish'),
    
    # Temir-junnalar
    ('hardware', 'Temir-junnalar'),
    ('tools', 'Asbob-uskunalar'),
    ('ladder', 'Narvon'),
    ('safety_equipment', 'Xavfsizlik uskunalari'),
    ('lock', 'Qulf'),
    ('key', 'Kalit'),
    ('chain', 'Zanjir'),
    ('hook', 'Ilmoq'),
    ('nail', 'Mix'),
    ('screw', 'Vint'),
    ('hammer', 'Bolgʻa'),
    ('screwdriver', 'Shurupovyort'),
    ('wrench', 'Gayka'),
    ('pliers', 'Pompa'),
    
    # Elektronika va texnika
    ('electronics', 'Elektronika'),
    ('tv', 'Televizor'),
    ('audio_system', 'Audio tizim'),
    ('speaker', 'Kolonka'),
    ('headphones', 'Naushniklar'),
    ('camera', 'Kamera'),
    ('phone', 'Telefon'),
    ('tablet', 'Planshet'),
    ('laptop', 'Noutbuk'),
    ('computer', 'Kompyuter'),
    ('printer', 'Printer'),
    ('router', 'Router'),
    
    # Idish-tovoq
    ('tableware', 'Idish-tovoq'),
    ('plate', 'Lagʻmon'),
    ('bowl', 'Piyola'),
    ('cup', 'Kosa'),
    ('glass', 'Stakan'),
    ('mug', 'Krujka'),
    ('spoon', 'Qoshiq'),
    ('fork', 'Vilka'),
    ('knife', 'Pichoq'),
    ('serving_dish', 'Xizmat idishi'),
    ('teapot', 'Choynak'),
    ('coffee_set', 'Kofe toʻplami'),
    ('tea_set', 'Choy toʻplami'),
    
    # Tozalash vositalari
    ('cleaning', 'Tozalash vositalari'),
    ('broom', 'Supurgi'),
    ('mop', 'Lattacha'),
    ('dustpan', 'Changʻirtak'),
    ('bucket', 'Chelak'),
    ('sponge', 'Shimgich'),
    ('detergent', 'Yuvish vositalari'),
    ('trash_can', 'Chiqindiq qutisi'),
    ('duster', 'Chang artgich'),
    
    # Qishgi buyumlar
    ('winter', 'Qishgi buyumlar'),
    ('heater', 'Isitgich'),
    ('blanket', 'Adyol'),
    ('hot_water_bottle', 'Issiq suv idishi'),
    ('warm_clothing', 'Issiq kiyimlar'),
    ('snow_removal', 'Qor tozalash asboblari'),
    
    # Boshqa uy-ro'zg'or buyumlari
    ('other_household', 'Boshqa uy-roʻzgʻor buyumlari'),
    ('pet_supplies', 'Hayvonlar uchun buyumlar'),
    ('fitness_equipment', 'Sport anjomlari'),
    ('musical_instruments', 'Musiqa asboblari'),
    ('art_supplies', 'Sanʼat materiallari'),
    ('books', 'Kitoblar'),
    ('collectibles', 'Kolleksionerlik buyumlari'),
    ('antiques', 'Antikvar buyumlar'),
    ('vintage', 'Vintaj buyumlar'),
    ('handmade', 'Qoʻl mehnati buyumlari'),
    
    # Boshqa
    ('other', 'Boshqa'),
]
    hourse_type = models.CharField(max_length=55, choices=HOUSEHOLD_TYPES )
    model = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.model}"

# Sport  uchun e'lonlar modeli
class SportingGoods(BaseProduct):
    SPORT_TYPE = [
        # Futbol
        ('football', 'Futbol to‘pi'),
        ('football_boots', 'Futbol butsalari'),
        ('goalkeeper_gloves', 'Darvozabon qo‘lqoplari'),
        ('football_kit', 'Futbol formasi'),
        ('football_net', 'Darvoza to‘rlari'),

        # Basketbol
        ('basketball', 'Basketbol to‘pi'),
        ('basketball_shoes', 'Basketbol krossovkasi'),
        ('basketball_jersey', 'Basketbol formasi'),
        ('basketball_hoop', 'Basketbol halqasi'),

        # Voleybol
        ('volleyball', 'Voleybol to‘pi'),
        ('volleyball_net', 'Voleybol to‘ri'),

        # Tennis
        ('tennis_racket', 'Tennis raketkasi'),
        ('tennis_ball', 'Tennis to‘pi'),
        ('table_tennis_racket', 'Stol tennisi raketkasi'),
        ('table_tennis_ball', 'Stol tennisi to‘pi'),
        ('table_tennis_table', 'Stol tennisi stoli'),
        ('badminton_racket', 'Badminton raketkasi'),
        ('badminton_shuttlecock', 'Badminton volanchigi'),

        # Fitnes va Gimnastika
        ('dumbbell', 'Gantel'),
        ('barbell', 'Shtanga'),
        ('kettlebell', 'Girya'),
        ('yoga_mat', 'Yoga mati'),
        ('resistance_band', 'Rezina lenta'),
        ('jump_rope', 'Skakalka'),
        ('fitness_ball', 'Fitbol'),
        ('treadmill', 'Bieguvaya yo‘l (trenajor)'),
        ('exercise_bike', 'Velotrenajor'),
        ('rowing_machine', 'Vesel trenajori'),
        ('stepper', 'Stepper'),
        ('pullup_bar', 'Turnik'),

        # Suzish va Suv sporti
        ('swimsuit', 'Suzish kiyimi'),
        ('swimming_goggles', 'Suzish ko‘zoynagi'),
        ('swimming_cap', 'Suzish shapka'),
        ('diving_equipment', 'Diving jihozlari'),
        ('snorkel', 'Snorkel'),
        ('flippers', 'Lasta'),

        # Qishki sport
        ('ski', 'Chang‘i'),
        ('ski_boots', 'Chang‘i etiklari'),
        ('snowboard', 'Snoubord'),
        ('snowboard_boots', 'Snoubord etiklari'),
        ('skates', 'Konki'),
        ('hockey_stick', 'Xokkey tayoqchasi'),
        ('hockey_puck', 'Xokkey shaybasi'),

        # Jangovar sport
        ('boxing_gloves', 'Boks qo‘lqoplari'),
        ('boxing_bag', 'Boks qopchasi'),
        ('martial_arts_uniform', 'Yakkakurash kiyimi'),
        ('mma_gloves', 'MMA qo‘lqoplari'),
        ('head_guard', 'Bosh himoyasi'),

        # Velosport
        ('bicycle', 'Velosiped'),
        ('helmet', 'Kaska'),
        ('cycling_gloves', 'Velosport qo‘lqoplari'),

        # Golf
        ('golf_club', 'Golf tayoqchasi'),
        ('golf_ball', 'Golf to‘pi'),

        # Boshqalar
        ('rugby_ball', 'Regbi to‘pi'),
        ('cricket_bat', 'Kriket tayoqchasi'),
        ('cricket_ball', 'Kriket to‘pi'),
        ('baseball_bat', 'Beysbol tayoqchasi'),
        ('baseball_ball', 'Beysbol to‘pi'),
        ('archery_bow', 'Kamondan otish'),
        ('archery_arrow', 'O‘q-yoy'),
        ('fishing_rod', 'Qarmoqlar'),
        ('roller_skates', 'Rolik konkilari'),
        ('climbing_rope', 'Alpinistik arqon'),
        ('tent', 'Palatka'),
        ('sleeping_bag', 'Spalniy meshok'),
    ]
    sport_type = models.CharField(max_length=55,choices=SPORT_TYPE )
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.brand} {self.model}"

# Hayvonlar uchun e'lonlar modeli
class Pet(BaseProduct):
    ANIMAL_TYPE = [
        # It va mushuk
        ('dog', 'It'),
        ('cat', 'Mushuk'),

        # Qushlar
        ('parrot', 'Papugay'),
        ('canary', 'Kanareyka'),
        ('budgerigar', 'Volnistik papugay'),
        ('pigeon', 'Kabutar'),
        ('chicken', 'Tovuq'),
        ('duck', 'O‘rdak'),
        ('goose', 'G‘oz'),

        # Baliqlar
        ('goldfish', 'Oltinbaliq'),
        ('betta', 'Betta baliq'),
        ('guppy', 'Guppi'),
        ('koi', 'Koi karp'),

        # Kemiruvchilar
        ('hamster', 'Xomyak'),
        ('guinea_pig', 'Dengiz cho‘chqasi'),
        ('rabbit', 'Quyon'),
        ('rat', 'Kalamush'),
        ('mouse', 'Sichqon'),

        # Sudralib yuruvchilar
        ('turtle', 'Toshbaqa'),
        ('snake', 'Ilon'),
        ('lizard', 'Kaltakesak'),
        ('gecko', 'Gekkon'),

        # Otlar va katta hayvonlar
        ('horse', 'Ot'),
        ('donkey', 'Eshak'),
        ('cow', 'Sigir'),
        ('sheep', 'Qo‘y'),
        ('goat', 'Echki'),

        # Egzotik uy hayvonlari
        ('ferret', 'Fretd (tulkiga o‘xshash)'),
        ('hedgehog', 'Tipratikan'),
        ('tarantula', 'Tarantul o‘rgimchak'),
        ('scorpion', 'Chayon'),
        ('iguana', 'Iguana'),
        ('chinchilla', 'Chinchilla'),
        ('other', 'Boshqa'),
    ]
    animal_type = models.CharField(max_length=55, choices=ANIMAL_TYPE )   # hayvonning ismi
    breed = models.CharField(max_length=100, blank=True, null=True)  # zot turi
    age = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.breed}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.product}"

