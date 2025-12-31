// Mock Data - Street English Elements with IPA
const streetData = [
    { en: "Pedestrians Only", cn: "仅限行人", ipa: "/pəˈdestriənz ˈoʊnli/", style: "style-traffic-blue" },
    { en: "No Loitering", cn: "禁止徘徊/逗留", ipa: "/noʊ ˈlɔɪtərɪŋ/", style: "style-traffic-red" },
    { en: "Tow Away Zone", cn: "拖车区域", ipa: "/toʊ əˈweɪ zoʊn/", style: "style-traffic-red" },
    { en: "Yield", cn: "让行", ipa: "/jiːld/", style: "style-traffic-yellow" },
    { en: "One Way", cn: "单行道", ipa: "/wʌn weɪ/", style: "style-traffic-blue" },
    { en: "Dead End", cn: "死胡同", ipa: "/ded end/", style: "style-traffic-yellow" },
    { en: "Mind the Gap", cn: "小心空隙", ipa: "/maɪnd ðə ɡæp/", style: "style-traffic-yellow" },
    { en: "CCTV in Operation", cn: "监控运行中", ipa: "/ˌsiːsiːtiːˈviː ɪn ˌɒpəˈreɪʃn/", style: "style-industrial" },
    { en: "Staff Only", cn: "员工专用", ipa: "/stæf ˈoʊnli/", style: "style-metal-plate" },
    { en: "Loading Zone", cn: "装卸区", ipa: "/ˈloʊdɪŋ zoʊn/", style: "style-industrial" },
    { en: "Wet Paint", cn: "油漆未干", ipa: "/wet peɪnt/", style: "style-traffic-yellow" },
    { en: "Out of Order", cn: "暂停服务/坏了", ipa: "/aʊt ʌv ˈɔːrdər/", style: "style-traffic-red" },
    { en: "Clearance Sale", cn: "清仓甩卖", ipa: "/ˈklɪrəns seɪl/", style: "style-shop-window" },
    { en: "Happy Hour", cn: "欢乐时光(打折时段)", ipa: "/ˈhæpi aʊər/", style: "style-neon-real" },
    { en: "Keep Clear", cn: "保持畅通", ipa: "/kiːp klɪr/", style: "style-industrial" },
    { en: "No Trespassing", cn: "禁止入内", ipa: "/noʊ ˈtrespəsɪŋ/", style: "style-traffic-red" },
    { en: "Beware of Dog", cn: "小心恶犬", ipa: "/bɪˈwer ʌv dɔːɡ/", style: "style-traffic-yellow" },
    { en: "Valet Parking", cn: "代客泊车", ipa: "/væˈleɪ ˈpɑːrkɪŋ/", style: "style-traffic-blue icon-parking" },
    { en: "Vacancy", cn: "有空房", ipa: "/ˈveɪkənsi/", style: "style-neon-real" },
    { en: "Sold Out", cn: "售罄", ipa: "/soʊld aʊt/", style: "style-shop-window" },
    { en: "Cash Only", cn: "只收现金", ipa: "/kæʃ ˈoʊnli/", style: "style-shop-window" },
    { en: "Fitting Room", cn: "试衣间", ipa: "/ˈfɪtɪŋ ruːm/", style: "style-metal-plate" },
    { en: "Lost & Found", cn: "失物招领", ipa: "/lɔːst ænd faʊnd/", style: "style-metal-plate" },
    { en: "Emergency Exit", cn: "紧急出口", ipa: "/ɪˈmɜːrdʒənsi ˈeksɪt/", style: "style-traffic-red" },
    { en: "Under Construction", cn: "施工中", ipa: "/ˈʌndər kənˈstrʌkʃn/", style: "style-industrial" },
    { en: "Do Not Disturb", cn: "请勿打扰", ipa: "/duː nɒt dɪˈstɜːrb/", style: "style-shop-window" },
    { en: "Open 24/7", cn: "全天候营业", ipa: "/ˈoʊpən ˌtwɛnti fɔːr ˈsɛvən/", style: "style-neon-real" },
    { en: "Fragile", cn: "易碎品", ipa: "/ˈfrædʒl/", style: "style-traffic-yellow" },
    { en: "Handle with Care", cn: "轻拿轻放", ipa: "/ˈhændl wɪð ker/", style: "style-traffic-yellow" },
    { en: "Priority Seating", cn: "老弱病残专座", ipa: "/praɪˈɔːrəti ˈsiːtɪŋ/", style: "style-traffic-blue" },
    { en: "Bus Stop", cn: "公交车站", ipa: "/bʌs stɒp/", style: "style-traffic-blue" },
    { en: "Subway Station", cn: "地铁站", ipa: "/ˈsʌbweɪ ˈsteɪʃn/", style: "style-subway" },
    { en: "Taxi Stand", cn: "出租车候客区", ipa: "/ˈtæksi stænd/", style: "style-traffic-blue" },
    { en: "Bike Lane", cn: "自行车道", ipa: "/baɪk leɪn/", style: "style-traffic-blue" },
    { en: "Speed Limit", cn: "限速", ipa: "/spiːd ˈlɪmɪt/", style: "style-traffic-red" },
    { en: "No Smoking", cn: "禁止吸烟", ipa: "/noʊ ˈsmoʊkɪŋ/", style: "style-traffic-red" },
    { en: "Restroom", cn: "洗手间", ipa: "/ˈrestruːm/", style: "style-traffic-blue" },
    { en: "Information", cn: "咨询处", ipa: "/ˌɪnfərˈmeɪʃn/", style: "style-traffic-blue" },
    { en: "Ticket Office", cn: "售票处", ipa: "/ˈtɪkɪt ˈɔːfɪs/", style: "style-subway" },
    { en: "Entrance", cn: "入口", ipa: "/ˈentrəns/", style: "style-metal-plate" },
    { en: "Exit", cn: "出口", ipa: "/ˈeksɪt/", style: "style-metal-plate" },
    { en: "Push", cn: "推", ipa: "/pʊʃ/", style: "style-metal-plate" },
    { en: "Pull", cn: "拉", ipa: "/pʊl/", style: "style-metal-plate" },
    { en: "Reserved", cn: "预留/已预订", ipa: "/rɪˈzɜːrvd/", style: "style-shop-window" },
    { en: "Free Wi-Fi", cn: "免费Wi-Fi", ipa: "/friː ˈwaɪfaɪ/", style: "style-shop-window" },
    { en: "ATM Inside", cn: "内有取款机", ipa: "/ˌeɪtiːˈem ˌɪnˈsaɪd/", style: "style-neon-real" },
    { en: "Please Queue", cn: "请排队", ipa: "/pliːz kjuː/", style: "style-traffic-blue" },
    { en: "Watch Your Step", cn: "小心台阶", ipa: "/wɒtʃ jɔːr step/", style: "style-traffic-yellow" },
    { en: "No Entry", cn: "禁止通行", ipa: "/noʊ ˈentri/", style: "style-traffic-red" },
    { en: "Detour", cn: "绕行", ipa: "/ˈdiːtʊr/", style: "style-traffic-yellow" },
    
    // --- NEW ADDITIONS (Ads, Signs, Slogans) ---
    
    // Billboards & Ads
    { en: "Grand Opening", cn: "盛大开业", ipa: "/ɡrænd ˈoʊpnɪŋ/", style: "style-billboard" },
    { en: "Coming Soon", cn: "即将开业/上映", ipa: "/ˈkʌmɪŋ suːn/", style: "style-billboard" },
    { en: "Buy 1 Get 1 Free", cn: "买一送一", ipa: "/baɪ wʌn ɡet wʌn friː/", style: "style-billboard" },
    { en: "Limited Time Offer", cn: "限时优惠", ipa: "/ˈlɪmɪtɪd taɪm ˈɔːfər/", style: "style-billboard" },
    
    // Chalkboard / Cafe Signs
    { en: "Today's Special", cn: "今日特价", ipa: "/təˈdeɪz ˈspeʃl/", style: "style-chalkboard" },
    { en: "Fresh Coffee", cn: "新鲜咖啡", ipa: "/freʃ ˈkɔːfi/", style: "style-chalkboard" },
    { en: "Live Music Tonight", cn: "今晚有现场音乐", ipa: "/laɪv ˈmjuːzɪk təˈnaɪt/", style: "style-chalkboard" },
    { en: "All Day Breakfast", cn: "全天早餐", ipa: "/ɔːl deɪ ˈbrekfəst/", style: "style-chalkboard" },
    
    // Digital / LED Displays
    { en: "Next Train 2 Min", cn: "下趟列车2分钟", ipa: "/nekst treɪn tuː mɪn/", style: "style-digital" },
    { en: "Now Boarding", cn: "正在登机/车", ipa: "/naʊ ˈbɔːrdɪŋ/", style: "style-digital" },
    { en: "Please Stand Clear", cn: "请保持距离", ipa: "/pliːz stænd klɪr/", style: "style-digital" },
    { en: "System Failure", cn: "系统故障", ipa: "/ˈsɪstəm ˈfeɪljər/", style: "style-digital" },
    
    // Stickers / Slaps
    { en: "Hello My Name Is", cn: "你好，我的名字是", ipa: "/həˈloʊ maɪ neɪm ɪz/", style: "style-sticker" },
    { en: "Skate or Die", cn: "滑板或死(滑板精神)", ipa: "/skeɪt ɔːr daɪ/", style: "style-sticker" },
    { en: "Fragile", cn: "易碎", ipa: "/ˈfrædʒl/", style: "style-sticker" },
    { en: "Handle With Care", cn: "轻拿轻放", ipa: "/ˈhændl wɪð ker/", style: "style-sticker" },
    
    // Vintage / Retro
    { en: "Vacancy", cn: "有空房", ipa: "/ˈveɪkənsi/", style: "style-vintage" },
    { en: "No Vacancy", cn: "客满", ipa: "/noʊ ˈveɪkənsi/", style: "style-vintage" },
    { en: "Diner", cn: "路边餐馆", ipa: "/ˈdaɪnər/", style: "style-vintage" },
    { en: "Motel", cn: "汽车旅馆", ipa: "/moʊˈtel/", style: "style-vintage" },
    
    // --- EXPANDED COLLECTION (100+ Total) ---

    // Graffiti / Street Art
    { en: "Stay Wild", cn: "保持野性", ipa: "/steɪ waɪld/", style: "style-graffiti" },
    { en: "Dream Big", cn: "敢于梦想", ipa: "/driːm bɪɡ/", style: "style-graffiti" },
    { en: "Love is War", cn: "爱即战争", ipa: "/lʌv ɪz wɔːr/", style: "style-graffiti" },
    { en: "No Justice No Peace", cn: "没有正义就没有和平", ipa: "/noʊ ˈdʒʌstɪs noʊ piːs/", style: "style-graffiti" },
    { en: "Art is Life", cn: "艺术即生活", ipa: "/ɑːrt ɪz laɪf/", style: "style-graffiti" },

    // Cinema Marquee
    { en: "Now Showing", cn: "正在上映", ipa: "/naʊ ˈʃoʊɪŋ/", style: "style-cinema" },
    { en: "Sold Out", cn: "票已售罄", ipa: "/soʊld aʊt/", style: "style-cinema" },
    { en: "Premiere Night", cn: "首映之夜", ipa: "/prɪˈmɪr naɪt/", style: "style-cinema" },
    { en: "Double Feature", cn: "两片连映", ipa: "/ˈdʌbl ˈfiːtʃər/", style: "style-cinema" },
    { en: "Matinee", cn: "日场/午场电影", ipa: "/ˌmætəˈneɪ/", style: "style-cinema" },

    // License Plates
    { en: "FREEDOM", cn: "自由", ipa: "/ˈfriːdəm/", style: "style-license" },
    { en: "EASY 4 U", cn: "对你来说容易", ipa: "/ˈiːzi fɔːr juː/", style: "style-license" },
    { en: "NEED SPD", cn: "需要速度(Need Speed)", ipa: "/niːd spiːd/", style: "style-license" },
    { en: "GR8 DAY", cn: "美好的一天", ipa: "/ɡreɪt deɪ/", style: "style-license" },
    { en: "UBER", cn: "优步", ipa: "/ˈuːbər/", style: "style-license" },

    // Airport Flip Board
    { en: "On Time", cn: "准点", ipa: "/ɒn taɪm/", style: "style-airport" },
    { en: "Delayed", cn: "延误", ipa: "/dɪˈleɪd/", style: "style-airport" },
    { en: "Boarding", cn: "正在登机", ipa: "/ˈbɔːrdɪŋ/", style: "style-airport" },
    { en: "Gate Closed", cn: "登机口关闭", ipa: "/ɡeɪt kloʊzd/", style: "style-airport" },
    { en: "Final Call", cn: "最后登机广播", ipa: "/ˈfaɪnl kɔːl/", style: "style-airport" },
    { en: "Cancelled", cn: "取消", ipa: "/ˈkænsəld/", style: "style-airport" },

    // Blueprint / Architectural
    { en: "Floor Plan", cn: "平面图", ipa: "/flɔːr plæn/", style: "style-blueprint" },
    { en: "Emergency Exit", cn: "紧急出口", ipa: "/ɪˈmɜːrdʒənsi ˈeksɪt/", style: "style-blueprint" },
    { en: "High Voltage", cn: "高压危险", ipa: "/haɪ ˈvoʊltɪdʒ/", style: "style-blueprint" },
    { en: "Restricted Area", cn: "禁区", ipa: "/rɪˈstrɪktɪd ˈeriə/", style: "style-blueprint" },
    { en: "Main Entrance", cn: "主入口", ipa: "/meɪn ˈentrəns/", style: "style-blueprint" },

    // Post-it Notes
    { en: "Call Mom", cn: "给妈妈打电话", ipa: "/kɔːl mɒm/", style: "style-postit" },
    { en: "Buy Milk", cn: "买牛奶", ipa: "/baɪ mɪlk/", style: "style-postit" },
    { en: "Meeting at 3pm", cn: "下午3点开会", ipa: "/ˈmiːtɪŋ æt θriː piː em/", style: "style-postit" },
    { en: "Don't Forget", cn: "别忘了", ipa: "/doʊnt fərˈɡet/", style: "style-postit" },
    { en: "Clean Up", cn: "打扫卫生", ipa: "/kliːn ʌp/", style: "style-postit" },

    // Concert Tickets
    { en: "Admit One", cn: "凭票入场(一人)", ipa: "/ədˈmɪt wʌn/", style: "style-ticket" },
    { en: "VIP Access", cn: "贵宾通道", ipa: "/ˌviːaɪˈpiː ˈækses/", style: "style-ticket" },
    { en: "General Admission", cn: "普通票", ipa: "/ˈdʒenrəl ədˈmɪʃn/", style: "style-ticket" },
    { en: "Backstage Pass", cn: "后台通行证", ipa: "/ˈbæksteɪdʒ pæs/", style: "style-ticket" },
    { en: "No Re-entry", cn: "离场不得再次进入", ipa: "/noʊ riː ˈentri/", style: "style-ticket" },

    // Caution Tape
    { en: "Do Not Cross", cn: "禁止穿越", ipa: "/duː nɒt krɔːs/", style: "style-caution" },
    { en: "Crime Scene", cn: "案发现场", ipa: "/kraɪm siːn/", style: "style-caution" },
    { en: "Hazardous", cn: "危险/有害", ipa: "/ˈhæzərdəs/", style: "style-caution" },
    { en: "Wet Floor", cn: "小心地滑", ipa: "/wet flɔːr/", style: "style-caution" },
    { en: "Keep Out", cn: "禁止入内", ipa: "/kiːp aʊt/", style: "style-caution" },

    // Holographic / Sci-Fi
    { en: "Access Denied", cn: "访问被拒绝", ipa: "/ˈækses dɪˈnaɪd/", style: "style-hologram" },
    { en: "System Ready", cn: "系统就绪", ipa: "/ˈsɪstəm ˈredi/", style: "style-hologram" },
    { en: "Scanning...", cn: "正在扫描...", ipa: "/ˈskænɪŋ/", style: "style-hologram" },
    { en: "Face ID Required", cn: "需要面部识别", ipa: "/feɪs aɪdiː rɪˈkwaɪərd/", style: "style-hologram" },
    { en: "Welcome Back", cn: "欢迎回来", ipa: "/ˈwelkəm bæk/", style: "style-hologram" },

    // More Traffic / Shop
    { en: "Dead End", cn: "死胡同", ipa: "/ded end/", style: "style-traffic-yellow" },
    { en: "Drive Thru", cn: "得来速(免下车通道)", ipa: "/draɪv θruː/", style: "style-neon-real" },
    { en: "Self Service", cn: "自助服务", ipa: "/self ˈsɜːrvɪs/", style: "style-metal-plate" },
    { en: "Recycle", cn: "回收利用", ipa: "/ˌriːˈsaɪkl/", style: "style-traffic-blue" },
    { en: "Lost Property", cn: "失物招领处", ipa: "/lɔːst ˈprɒpərti/", style: "style-industrial" },

    // Postal / Logistics
    { en: "Air Mail", cn: "航空邮件", ipa: "/er meɪl/", style: "style-traffic-blue" },
    { en: "First Class", cn: "头等邮件", ipa: "/fɜːrst klæs/", style: "style-badge" },
    { en: "Express", cn: "快递", ipa: "/ɪkˈspres/", style: "style-traffic-red" },
    { en: "Priority Mail", cn: "优先邮件", ipa: "/praɪˈɔːrəti meɪl/", style: "style-ticket-stub" },
    { en: "Do Not Bend", cn: "请勿折叠", ipa: "/duː nɒt bend/", style: "style-caution" },
    { en: "Return to Sender", cn: "退回寄件人", ipa: "/rɪˈtɜːrn tuː ˈsendər/", style: "style-sticker" },

    // --- NON-RECTANGULAR SHAPES SHOWCASE (New Styles) ---
    { en: "Stop", cn: "停止", ipa: "/stɒp/", style: "style-octagon" },
    { en: "Wrong Way", cn: "逆行", ipa: "/rɔːŋ weɪ/", style: "style-octagon" },
    { en: "Route 66", cn: "66号公路", ipa: "/ruːt sɪksti sɪks/", style: "style-shield" },
    { en: "Interstate 5", cn: "5号州际公路", ipa: "/ˈɪntərsteɪt faɪv/", style: "style-shield" },
    { en: "New Arrival", cn: "新品上市", ipa: "/nuː əˈraɪvl/", style: "style-burst" },
    { en: "Best Seller", cn: "畅销品", ipa: "/best ˈselər/", style: "style-burst" },
    { en: "Turn Right", cn: "右转", ipa: "/tɜːrn raɪt/", style: "style-arrow-right" },
    { en: "Detour", cn: "绕行", ipa: "/ˈdiːtʊr/", style: "style-arrow-right" },
    { en: "Admit One", cn: "凭票入场", ipa: "/ədˈmɪt wʌn/", style: "style-ticket-stub" },
    { en: "Movie Night", cn: "电影之夜", ipa: "/ˈmuːvi naɪt/", style: "style-ticket-stub" },
    { en: "What's Up?", cn: "怎么了/你好", ipa: "/wɒts ʌp/", style: "style-speech" },
    { en: "Hey There!", cn: "嘿，你好！", ipa: "/heɪ ðer/", style: "style-speech" },
    { en: "Sheriff", cn: "警长/治安官", ipa: "/ˈʃerɪf/", style: "style-badge" },
    { en: "Security", cn: "安保", ipa: "/sɪˈkjʊrəti/", style: "style-badge" },
    { en: "Zone A", cn: "A区", ipa: "/zoʊn eɪ/", style: "style-hexagon" },
    { en: "Sector 7", cn: "第七区", ipa: "/ˈsektər ˈsevən/", style: "style-hexagon" },

    // Shop & Store Identifiers (New)
    { en: "Pizza by the Slice", cn: "披萨切片卖", ipa: "/ˈpiːtsə baɪ ðə slaɪs/", style: "style-pizza" },
    { en: "Fresh Hot Pizza", cn: "新鲜热披萨", ipa: "/freʃ hɒt ˈpiːtsə/", style: "style-pizza" },
    { en: "Pepperoni Special", cn: "意式辣香肠特价", ipa: "/ˌpepəˈroʊni ˈspeʃl/", style: "style-pizza" },
    { en: "Best Burgers", cn: "最好吃的汉堡", ipa: "/best ˈbɜːrɡərz/", style: "style-burger" },
    { en: "Cheeseburger", cn: "芝士汉堡", ipa: "/ˈtʃiːzbɜːrɡər/", style: "style-burger" },
    { en: "Drive-Thru Open", cn: "得来速开放中", ipa: "/draɪv θruː ˈoʊpən/", style: "style-burger" },
    { en: "Fresh Roasted", cn: "新鲜烘焙(咖啡)", ipa: "/freʃ ˈroʊstɪd/", style: "style-coffee" },
    { en: "Espresso Bar", cn: "浓缩咖啡吧", ipa: "/eˈspresoʊ bɑːr/", style: "style-coffee" },
    { en: "Morning Brew", cn: "早晨咖啡", ipa: "/ˈmɔːrnɪŋ bruː/", style: "style-coffee" },
    { en: "Summer Sale", cn: "夏季大促", ipa: "/ˈsʌmər seɪl/", style: "style-fashion" },
    { en: "New Collection", cn: "新系列", ipa: "/nuː kəˈlekʃn/", style: "style-fashion" },
    { en: "Fashion Week", cn: "时装周", ipa: "/ˈfæʃn wiːk/", style: "style-fashion" },

    // Medical & Health (New)
    { en: "Pharmacy", cn: "药店/药房", ipa: "/ˈfɑːrməsi/", style: "style-emergency" },
    { en: "Chemist", cn: "药剂师/药店(英)", ipa: "/ˈkemɪst/", style: "style-emergency" },
    { en: "First Aid", cn: "急救", ipa: "/ˌfɜːrst ˈeɪd/", style: "style-emergency" },
    { en: "Emergency", cn: "急诊/紧急情况", ipa: "/ɪˈmɜːrdʒənsi/", style: "style-emergency" },
    { en: "Hospital", cn: "医院", ipa: "/ˈhɒspɪtl/", style: "style-emergency" },
    { en: "Clinic", cn: "诊所", ipa: "/ˈklɪnɪk/", style: "style-emergency" },
    { en: "Ambulance", cn: "救护车", ipa: "/ˈæmbjələns/", style: "style-emergency" },
    { en: "Prescription", cn: "处方药", ipa: "/prɪˈskrɪpʃn/", style: "style-emergency" }
];

// State
let studyCards = [];
let reviewCards = [];
let completedCards = [];
let historyQueue = []; // Queue to store Sets of phrases from the last 2 refreshes

// DOM Elements
const studyGrid = document.getElementById('study-grid');
const reviewGrid = document.getElementById('review-grid');
const completedGrid = document.getElementById('completed-grid');
const shuffleBtn = document.getElementById('shuffleBtn');
const navItems = document.querySelectorAll('.nav-item');
const views = document.querySelectorAll('.view-section');
const searchInput = document.getElementById('searchInput');
const clearSearchBtn = document.getElementById('clearSearchBtn');
const searchBtn = document.getElementById('searchBtn');
const aiResponse = document.getElementById('aiResponse');
const aiResponseBody = document.getElementById('aiResponseBody');
const closeAi = document.querySelector('.close-ai');

// Initialization
function init() {
    shuffleCards();
    setupEventListeners();
}

// Logic
function shuffleCards() {
    // Pick 12 random cards for study view
    // Logic updated to prioritize NON-RECTANGULAR cards and limit repetition
    studyCards = [];
    
    const nonRectangularStyles = [
        'style-traffic-red', 
        'style-traffic-yellow', 
        'style-octagon', 
        'style-shield', 
        'style-burst', 
        'style-hexagon', 
        'style-arrow-right', 
        'style-ticket-stub', 
        'style-speech', 
        'style-badge',
        'style-pizza',
        'style-burger',
        'style-coffee',
        'style-fashion',
        'style-emergency'
    ];

    // 0. Build Ban List from History (Last 2 refreshes)
    const bannedPhrases = new Set();
    historyQueue.forEach(roundSet => {
        roundSet.forEach(phrase => bannedPhrases.add(phrase));
    });

    const shuffled = [...streetData].sort(() => 0.5 - Math.random());
    
    const selected = [];
    const styleCounts = {};
    const selectedIds = new Set(); // Track added cards to avoid dupes

    // Helper to add card if valid
    const tryAddCard = (card, ignoreHistory = false, ignoreStyleLimit = false) => {
        if (selected.length >= 12) return false;
        if (selectedIds.has(card)) return false; // Already added in this round

        // History Check
        if (!ignoreHistory && bannedPhrases.has(card.en)) return false;

        const mainStyle = card.style.split(' ')[0];
        const count = styleCounts[mainStyle] || 0;

        // Style Limit Check
        if (!ignoreStyleLimit && count >= 2) return false;

        // Add
        selected.push(card);
        selectedIds.add(card);
        styleCounts[mainStyle] = count + 1;
        return true;
    };

    // 1. Prioritize Non-Rectangular Styles (Target ~8 cards)
    const nonRectCandidates = shuffled.filter(c => 
        nonRectangularStyles.includes(c.style.split(' ')[0])
    );
    
    for (const card of nonRectCandidates) {
        if (selected.length >= 8) break; // Cap non-rect preference at 8
        tryAddCard(card);
    }

    // 2. Fill remaining slots with ANY style (Rectangular or remaining Non-Rect)
    for (const card of shuffled) {
        if (selected.length >= 12) break;
        tryAddCard(card);
    }
    
    // 3. Fallback A: Relax History Constraint (if data is small)
    if (selected.length < 12) {
        for (const card of shuffled) {
            if (selected.length >= 12) break;
            tryAddCard(card, true, false); // Ignore history
        }
    }

    // 4. Fallback B: Relax All Constraints (Panic Mode)
    if (selected.length < 12) {
        for (const card of shuffled) {
            if (selected.length >= 12) break;
            tryAddCard(card, true, true); // Ignore history & style limits
        }
    }
    
    // Update History Queue
    const currentRoundPhrases = new Set(selected.map(c => c.en));
    historyQueue.push(currentRoundPhrases);
    if (historyQueue.length > 2) {
        historyQueue.shift(); // Keep only last 2 rounds
    }
    
    // Final Shuffle: Mix the prioritized shapes with the others so they aren't segregated
    studyCards = selected.sort(() => 0.5 - Math.random());
    renderGrid(studyGrid, studyCards, 'study');
}

function createCardElement(data, id, type) {
    const card = document.createElement('div');
    card.className = `street-card ${data.style}`;
    card.draggable = true;
    card.dataset.id = id;
    card.dataset.type = type; // study, review, completed
    card.dataset.en = data.en;
    card.dataset.cn = data.cn;

    card.innerHTML = `
        <div class="card-content">
            <div class="text-en">${data.en}</div>
            <div class="text-ipa">[${data.ipa}]</div>
            <button class="audio-btn" title="Read Aloud"><i class="fas fa-volume-up"></i></button>
            <div class="text-cn">${data.cn}</div>
        </div>
    `;

    // Audio Button Logic
    const audioBtn = card.querySelector('.audio-btn');
    audioBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent card flip
        // Chrome/Safari fix: explicitly resume audio context on user gesture
        if ('speechSynthesis' in window) {
            window.speechSynthesis.resume(); 
        }
        speakText(data.en, audioBtn); // Pass button for visual feedback
    });

    // Click to toggle translation (Trigger Monster Interaction)
    card.addEventListener('click', (e) => {
        handleMonsterInteraction(card);
    });

    // Speak Chinese when clicking the Chinese text - DISABLED per user request
    const cnText = card.querySelector('.text-cn');
    /* 
    cnText.addEventListener('click', (e) => {
        e.stopPropagation();
        speakText(data.cn, null, 'zh-CN');
    });
    */

    // Drag events
    card.addEventListener('dragstart', handleDragStart);
    card.addEventListener('dragend', handleDragEnd);

    return card;
}

// Voice Selection Logic
let selectedVoice = null;

function loadVoices() {
    const voices = window.speechSynthesis.getVoices();
    if (voices.length === 0) return; 

    // Priority list for MALE voices (User Request)
    const priorities = [
        "Daniel", 
        "Google US English Male", 
        "Microsoft David", 
        "Fred",
        "Google UK English Male"
    ];
    
    selectedVoice = null; // Reset
    for (const name of priorities) {
        selectedVoice = voices.find(v => v.name === name || v.name.includes(name));
        if (selectedVoice) break;
    }

    // Fallback: Try to find any voice that is NOT female
    if (!selectedVoice) {
        selectedVoice = voices.find(v => 
            !v.name.includes('Female') && 
            !v.name.includes('Woman') && 
            !v.name.includes('Zira') &&
            !v.name.includes('Samantha') &&
            v.lang.startsWith('en')
        );
    }

    // Fallback: First en-US voice
    if (!selectedVoice) {
        selectedVoice = voices.find(v => v.lang === 'en-US');
    }
}

// Ensure voices are loaded
if ('speechSynthesis' in window) {
    window.speechSynthesis.onvoiceschanged = loadVoices;
    loadVoices(); 
}

function speakText(text, buttonElement = null, lang = 'en-US') {
    if (!('speechSynthesis' in window)) {
        alert("Sorry, your browser does not support Text-to-Speech.");
        return;
    }

    // 1. HARD RESET
    window.speechSynthesis.cancel();
    
    // 2. Force Resume
    if (window.speechSynthesis.paused) {
        window.speechSynthesis.resume();
    }

    // Reset visuals
    document.querySelectorAll('.audio-btn').forEach(btn => btn.classList.remove('playing'));

    // Re-load voices if we haven't yet
    if (!selectedVoice) loadVoices();

    // 3. Create utterance
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Global reference
    window.currentUtterance = utterance;

    // 4. Apply Voice
    if (lang === 'en-US') {
        if (selectedVoice) {
            utterance.voice = selectedVoice;
        }
    } else if (lang === 'zh-CN') {
        const voices = window.speechSynthesis.getVoices();
        const cnVoice = voices.find(v => v.lang === 'zh-CN' || v.lang === 'zh-HK' || v.lang === 'zh-TW');
        if (cnVoice) {
            utterance.voice = cnVoice;
        }
    }

    // 5. Config
    utterance.lang = lang; 
    utterance.volume = 1.0; 
    utterance.rate = 1.0;  // Keep standard speed for stability
    utterance.pitch = 1.0; // Keep standard pitch for stability

    // Debug / Visuals
    utterance.onstart = () => {
        console.log("TTS Started: " + text + " | Lang: " + lang);
        if (buttonElement) buttonElement.classList.add('playing');
    };
    
    utterance.onerror = (e) => {
        console.error('TTS Error:', e);
        if (buttonElement) buttonElement.classList.remove('playing');
        
        // AUTO-RETRY with System Default if the fancy voice failed
        if (e.error !== 'canceled' && e.error !== 'interrupted') {
             console.log("Specific voice failed. Retrying with system default...");
             const retryUtterance = new SpeechSynthesisUtterance(text);
             retryUtterance.lang = lang; // Just set lang, no specific voice
             window.speechSynthesis.speak(retryUtterance);
        }
    };
    
    utterance.onend = () => {
        window.currentUtterance = null;
        if (buttonElement) buttonElement.classList.remove('playing');
    };

    // 6. Speak
    window.speechSynthesis.speak(utterance);
    
    // 7. Watchdog
    setTimeout(() => {
        if (window.speechSynthesis.paused) {
             window.speechSynthesis.resume();
        }
    }, 100);
}

function renderGrid(gridElement, cards, type) {
    gridElement.innerHTML = '';
    cards.forEach((data, index) => {
        const card = createCardElement(data, index, type);
        gridElement.appendChild(card);
    });
}

// Drag & Drop
let draggedCard = null;

function handleDragStart(e) {
    draggedCard = this;
    setTimeout(() => this.classList.add('dragging'), 0);
}

function handleDragEnd(e) {
    this.classList.remove('dragging');
    draggedCard = null;
}

// Drop Zones
[document.getElementById('review-zone'), document.getElementById('completed-zone')].forEach(zone => {
    zone.addEventListener('dragover', e => {
        e.preventDefault();
        zone.classList.add('drag-over');
    });

    zone.addEventListener('dragleave', e => {
        zone.classList.remove('drag-over');
    });

    zone.addEventListener('drop', e => {
        e.preventDefault();
        zone.classList.remove('drag-over');
        
        if (draggedCard) {
            const id = draggedCard.dataset.id;
            const originType = draggedCard.dataset.type;
            const targetZoneId = zone.id; // review-zone or completed-zone
            
            let cardData;
            // Find data source
            if (originType === 'study') cardData = studyCards[id];
            else if (originType === 'review') cardData = reviewCards[id];
            else if (originType === 'completed') cardData = completedCards[id];

            if (!cardData) return;

            // Remove from source (if it's not study - study cards just stay or get copied? 
            // User requirement: "drag to review/completed". Let's move them.)
            if (originType === 'review') {
                reviewCards.splice(id, 1);
                renderGrid(reviewGrid, reviewCards, 'review');
            } else if (originType === 'completed') {
                completedCards.splice(id, 1);
                renderGrid(completedGrid, completedCards, 'completed');
            } else if (originType === 'study') {
                 // Optionally remove from study or keep. Let's remove to show progress.
                 studyCards.splice(id, 1);
                 renderGrid(studyGrid, studyCards, 'study');
            }

            // Add to target
            if (targetZoneId === 'review-zone') {
                reviewCards.push(cardData);
                renderGrid(reviewGrid, reviewCards, 'review');
            } else if (targetZoneId === 'completed-zone') {
                completedCards.push(cardData);
                renderGrid(completedGrid, completedCards, 'completed');
            }
        }
    });
});

function moveCard(id, originType, targetType) {
    let cardData;
    // Find & Remove from Source
    if (originType === 'study') {
        cardData = studyCards[id];
        studyCards.splice(id, 1);
        renderGrid(studyGrid, studyCards, 'study');
    } else if (originType === 'review') {
        cardData = reviewCards[id];
        reviewCards.splice(id, 1);
        renderGrid(reviewGrid, reviewCards, 'review');
    } else if (originType === 'completed') {
        cardData = completedCards[id];
        completedCards.splice(id, 1);
        renderGrid(completedGrid, completedCards, 'completed');
    }

    if (!cardData) return;

    // Add to Target
    if (targetType === 'review') {
        reviewCards.push(cardData);
        renderGrid(reviewGrid, reviewCards, 'review');
    } else if (targetType === 'completed') {
        completedCards.push(cardData);
        renderGrid(completedGrid, completedCards, 'completed');
    }
}

// Event Listeners
function setupEventListeners() {
    // Navigation & Drop Targets
    navItems.forEach(item => {
        // Click
        item.addEventListener('click', () => {
            // Update nav UI
            navItems.forEach(n => n.classList.remove('active'));
            item.classList.add('active');

            // Switch view
            const viewId = item.dataset.view;
            views.forEach(v => v.classList.remove('active'));
            document.getElementById(`${viewId}-view`).classList.add('active');
        });

        // Drop Target (Sidebar)
        item.addEventListener('dragover', (e) => {
            e.preventDefault();
            item.style.background = 'var(--traffic-yellow)';
            item.style.color = '#000';
            item.style.transform = 'scale(1.05)';
        });

        item.addEventListener('dragleave', (e) => {
            item.style.background = '';
            item.style.color = '';
            item.style.transform = '';
        });

        item.addEventListener('drop', (e) => {
            e.preventDefault();
            item.style.background = '';
            item.style.color = '';
            item.style.transform = '';

            const targetTab = item.dataset.view; // 'study', 'review', 'completed'
            
            // Only allow dropping to Review or Completed tabs
            if (draggedCard && (targetTab === 'review' || targetTab === 'completed')) {
                const id = draggedCard.dataset.id;
                const originType = draggedCard.dataset.type;
                
                if (originType === targetTab) return; // No op

                moveCard(id, originType, targetTab);
                
                // Optional: Switch to that tab to show result? 
                // User might prefer staying in current view. Let's stay.
            }
        });
    });

    // Shuffle
    shuffleBtn.addEventListener('click', shuffleCards);

    // Search
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });

    // Search Clear Logic
    searchInput.addEventListener('input', () => {
        if (searchInput.value.trim().length > 0) {
            clearSearchBtn.classList.remove('hidden');
        } else {
            clearSearchBtn.classList.add('hidden');
        }
    });

    clearSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        clearSearchBtn.classList.add('hidden');
        searchInput.focus();
    });

    // Close AI
    closeAi.addEventListener('click', () => {
        aiResponse.classList.add('hidden');
    });

    setupSentenceZone();
}

// --- SENTENCE BUILDER LOGIC ---
const sentenceZone = document.getElementById('sentenceZone');
const zoneContent = document.getElementById('zoneContent');
const refreshSentenceBtn = document.getElementById('refreshSentenceBtn');
let currentSentenceData = null; // Store { phrase, cn }

// Simple Templates (Offline "AI")
const sentenceTemplates = [
    { en: "I saw a '[PHRASE]' sign yesterday.", cn: "我昨天看到了一个'[PHRASE_CN]'标志。" },
    { en: "Make sure to obey the '[PHRASE]' rule.", cn: "请务必遵守'[PHRASE_CN]'规则。" },
    { en: "The '[PHRASE]' notice caught my eye.", cn: "那个'[PHRASE_CN]'的告示引起了我的注意。" },
    { en: "You can find the '[PHRASE]' area over there.", cn: "你可以在那边找到'[PHRASE_CN]'区域。" },
    { en: "Why is there a '[PHRASE]' sign here?", cn: "为什么这里会有个'[PHRASE_CN]'标志？" },
    { en: "This building has a '[PHRASE]' posted.", cn: "这栋楼贴了'[PHRASE_CN]'。" },
    { en: "Always look for the '[PHRASE]' indication.", cn: "一定要留意'[PHRASE_CN]'的指示。" },
    { en: "Is this strictly '[PHRASE]'?", cn: "这里严格是'[PHRASE_CN]'吗？" }
];

function setupSentenceZone() {
    sentenceZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        sentenceZone.classList.add('drag-over');
    });

    sentenceZone.addEventListener('dragleave', (e) => {
        sentenceZone.classList.remove('drag-over');
    });

    sentenceZone.addEventListener('drop', (e) => {
        e.preventDefault();
        sentenceZone.classList.remove('drag-over');
        
        if (draggedCard) {
            const en = draggedCard.dataset.en;
            const cn = draggedCard.dataset.cn;
            generateSentence(en, cn);
        }
    });

    refreshSentenceBtn.addEventListener('click', () => {
        if (currentSentenceData) {
            generateSentence(currentSentenceData.en, currentSentenceData.cn);
        }
    });
}

function generateSentence(phrase, cnPhrase) {
    currentSentenceData = { en: phrase, cn: cnPhrase };
    
    // Pick a random template
    const template = sentenceTemplates[Math.floor(Math.random() * sentenceTemplates.length)];
    
    const finalEn = template.en.replace('[PHRASE]', phrase);
    const finalCn = template.cn.replace('[PHRASE_CN]', cnPhrase);

    // Update UI
    zoneContent.innerHTML = `
        <div class="generated-sentence">${finalEn}</div>
        <div class="generated-translation">${finalCn}</div>
    `;
    
    // Show refresh button
    refreshSentenceBtn.classList.remove('hidden');
    
    // Speak the sentence automatically? Maybe just the button logic.
    // Let's make the sentence clickable to speak.
    const sentEl = zoneContent.querySelector('.generated-sentence');
    sentEl.style.cursor = 'pointer';
    sentEl.title = "Click to read aloud";
    sentEl.addEventListener('click', () => {
        speakText(finalEn);
    });
}

async function performSearch() {
    const query = searchInput.value.trim();
    if (!query) return;

    // Show AI loading
    aiResponse.classList.remove('hidden');
    aiResponseBody.innerText = "正在咨询 AI 街头向导...";

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        aiResponseBody.innerText = data.answer;

        // If AI suggests a card (future feature), we could highlight it.
    } catch (error) {
        console.error('Error:', error);
        aiResponseBody.innerText = "抱歉，AI 向导暂时离线或忙碌。";
    }
}

// Run
init();

// --- Monster & Spit Interaction Logic ---

// Mouse Tracking for Eyes
document.addEventListener('mousemove', (e) => {
    const monsters = document.querySelectorAll('.monster');
    monsters.forEach(monster => {
        const eyes = monster.querySelectorAll('.eye');
        const rect = monster.getBoundingClientRect();
        const monsterCenterX = rect.left + rect.width / 2;
        const monsterCenterY = rect.top + rect.height / 2;

        // Calculate angle from monster center to mouse
        const angle = Math.atan2(e.clientY - monsterCenterY, e.clientX - monsterCenterX);
        
        // Distance factor (limit eye movement)
        // Max pupil offset is around 3-4px
        const maxOffset = 3;
        const distance = Math.min(maxOffset, Math.hypot(e.clientX - monsterCenterX, e.clientY - monsterCenterY) / 15);
        
        const offsetX = Math.cos(angle) * distance;
        const offsetY = Math.sin(angle) * distance;

        eyes.forEach(eye => {
            const pupil = eye.querySelector('.pupil');
            if (pupil) {
                pupil.style.transform = `translate(calc(-50% + ${offsetX}px), calc(-50% + ${offsetY}px))`;
            }
        });
    });
});

function handleMonsterInteraction(card) {
    const isShowing = card.classList.contains('show-cn');
    
    // Determine Monster and Action
    // If NOT showing -> We want to SHOW -> Use MonsterShow (Green)
    // If SHOWING -> We want to HIDE -> Use MonsterHide (Purple)
    const monsterId = isShowing ? 'monsterHide' : 'monsterShow';
    const monster = document.getElementById(monsterId);
    
    if (!monster) {
        // Fallback if monsters not ready
        card.classList.toggle('show-cn');
        return;
    }

    // Visual Cue on Monster
    monster.classList.add('spitting');
    setTimeout(() => monster.classList.remove('spitting'), 200);

    // Animate Spit
    // If Showing -> We are hiding -> Purple spit
    // If Not Showing -> We are showing -> Green spit
    const spitColor = isShowing ? 'purple' : 'green';
    
    animateSpit(monster, card, spitColor, () => {
        // Toggle State on Impact
        if (isShowing) {
            card.classList.remove('show-cn');
        } else {
            card.classList.add('show-cn');
        }
        
        // Add Splash Effect
        const splash = document.createElement('div');
        splash.className = `spit-overlay ${isShowing ? 'purple-splash' : ''}`;
        card.querySelector('.card-content').appendChild(splash); // Append to content to stay inside
        
        // Clean up splash
        setTimeout(() => splash.remove(), 600);
    });
}

function animateSpit(sourceEl, targetEl, colorType, onComplete) {
    const projectile = document.getElementById('spit-projectile');
    const sourceRect = sourceEl.getBoundingClientRect();
    const targetRect = targetEl.getBoundingClientRect();

    // Start Position (Monster Mouth approx)
    const startX = sourceRect.left + sourceRect.width / 2;
    const startY = sourceRect.top + sourceRect.height * 0.7;

    // End Position (Card Center)
    const endX = targetRect.left + targetRect.width / 2;
    const endY = targetRect.top + targetRect.height / 2;

    // Reset Projectile
    projectile.style.left = `${startX}px`;
    projectile.style.top = `${startY}px`;
    projectile.className = `spit-projectile spit-${colorType}`;
    projectile.style.display = 'block';
    projectile.style.opacity = '1';
    projectile.style.transform = 'scale(1)';

    // Animate
    const startTime = performance.now();
    const duration = 200; // ms - Faster speed per user request

    function step(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing (ease-in for gravity feel?) -> Linear for spit is fine, maybe slight arc
        const ease = progress; 
        
        const currentX = startX + (endX - startX) * ease;
        const currentY = startY + (endY - startY) * ease;

        projectile.style.left = `${currentX}px`;
        projectile.style.top = `${currentY}px`;

        if (progress < 1) {
            requestAnimationFrame(step);
        } else {
            // Impact
            projectile.style.display = 'none';
            if (onComplete) onComplete();
        }
    }

    requestAnimationFrame(step);
}
