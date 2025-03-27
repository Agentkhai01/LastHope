import random

def get_random_tip():
    """
    Return a random humorous financial tip
    """
    tips = [
        "Remember, your wallet is like your heart - be careful who you open it for!",
        "Money doesn't grow on trees, but it does grow in mutual funds (usually)!",
        "Your budget is like a diet for your wallet - occasional treats are fine, just don't make it a habit!",
        "Investing is like planting trees - the best time was 20 years ago, the second best time is now!",
        "Credit cards are like fire - useful when controlled, dangerous when they control you!",
        "Saving money is like losing weight - everyone knows how to do it, few people actually do it!",
        "Compound interest is the 8th wonder of the world. It turns small chai money into big vacation funds!",
        "If you can't buy it twice, you can't afford it once! Unless it's college, then you can't afford it at all.",
        "A fool and his money are soon separated... usually by the latest smartphone release!",
        "If money doesn't make you happy, you're probably spending it on the wrong stuff!",
        "Being frugal doesn't mean being cheap - it means being smart with your money so you can be dumb with it later!",
        "Always save for a rainy day. In Mumbai, that's almost every day during monsoon!",
        "Your emergency fund should be like that friend who shows up at 3 AM - reliable and without judgment!",
        "Invest in yourself first. Your brain pays better dividends than any stock market!",
        "If you wait to invest until you 'have enough money,' you'll never invest. Start small, like your first apartment!",
        "Buy assets, not liabilities. If it eats, needs maintenance, or goes out of fashion - think twice!",
        "The stock market is the only place where people refuse to buy when there's a sale!",
        "Financial planning is like navigation - a small error in course now becomes a big miss later!",
        "The best way to save money is to tell everyone you're broke. It's surprisingly effective!",
        "Money can't buy happiness, but poverty can't buy anything. Choose wisely!",
        "The cheapest loan is the one you never take. Unless it's from your parents - that one's interest-free!",
        "The secret to financial freedom isn't earning more, it's wanting less... but earning more does help!",
        "Before making a purchase, convert the cost to 'hours worked.' That ₹5000 outfit might cost you two days of work!",
        "If your money isn't working for you while you sleep, you'll be working until you're too old to stay awake!",
        "Automate your savings like your Netflix subscription - set it and forget it until you get that surprise at the end!",
        "If you're paying more in bank fees than you are earning in interest, your money is in an abusive relationship!",
        "Financial maturity is when you stop buying things to impress people who don't care about you anyway!",
        "Your first investment should be a good pair of shoes and a quality mattress. If you're not in one, you're in the other!",
        "Pay yourself first, because your future self can't go back in time to yell at your present self!",
        "The best investment during uncertain times? Toilet paper, apparently!",
        "Your spending habits are just that - habits. And like all habits, they can be broken... especially the expensive ones!",
        "Investing in the stock market is like riding a roller coaster - it's scary at first, but you get used to the ups and downs!",
        "Money is like a good friend - it won't solve all your problems, but it makes solving them more comfortable!",
        "Budget like you breathe - regularly, consistently, and without thinking too much about it!",
        "The difference between being broke and being wealthy is often just patience and discipline... and a rich uncle helps too!",
        "Financial planning isn't about being rich, it's about being free to choose how you live your life!",
        "Saving is like exercise - painful in the short term, rewarding in the long term, and best done regularly!",
        "Rich people stay rich by living like they're poor. Poor people stay poor by living like they're rich!",
        "The best time to start saving was when you got your first pocket money. The second best time is NOW!",
        "Money is a great servant but a terrible master. Don't let it control your life, but don't ignore it either!"
    ]
    
    return random.choice(tips)

def get_category_tip(category):
    """
    Return a humorous financial tip based on expense category
    """
    category_tips = {
        "Food & Dining": [
            "Cooking at home isn't just healthier, it's cheaper too! Plus, you can blame yourself for the bad taste!",
            "Eating out every day is like setting your money on fire, but with more calories.",
            "Your stomach doesn't know the difference between a ₹500 meal and a ₹1500 meal, but your wallet certainly does!",
            "The most expensive ingredient in any restaurant dish is the ambiance. Mood lighting at home is much cheaper!"
        ],
        "Rent": [
            "Your rent should be like a good haircut - takes just enough off the top but still leaves you looking good!",
            "Finding affordable housing is like finding a perfect match - compromise is inevitable!",
            "A good roommate is worth their weight in gold, especially when they pay their share of rent on time!",
            "The smaller your living space, the bigger your savings account. But too small, and you'll spend it all on therapy!"
        ],
        "Transportation": [
            "Public transport: where your wallet gets fatter as you get to your destination!",
            "Walking isn't just good for your health, it's good for your wealth too!",
            "Car ownership is expensive. The real flex is having enough saved to buy a car but choosing not to!",
            "Every kilometer you walk is money in your pocket and years added to your life!"
        ],
        "Shopping": [
            "If you wouldn't buy it at full price, you don't really want it on sale either!",
            "Shopping with a list is like having a responsible adult supervising your inner child!",
            "The most stylish accessory is a healthy bank balance - it goes with everything!",
            "Fast fashion is like fast food - satisfying in the moment, regrettable in the long run!"
        ],
        "Education": [
            "Education expenses are not costs, they're investments - unless you're studying something no one will pay you for!",
            "Learning is the only investment that never depreciates. Unless it's learning how to use MySpace!",
            "Books are the cheapest tickets to anywhere in the universe, including financial freedom!",
            "The internet has made learning almost free - your grandmother would have traded her dowry for YouTube tutorials!"
        ],
        "Entertainment": [
            "The best entertainment often costs the least. When was the last time you played cards with friends?",
            "Netflix and chill is not just a date idea, it's a financial strategy compared to movie theaters!",
            "Expensive hobbies are fine if you can afford them. If not, discover the joy of people-watching - it's free!",
            "Your social media feed is full of people spending money they don't have on things they don't need. Don't join them!"
        ],
        "Others": [
            "Miscellaneous expenses are like ninjas - small individually but deadly in groups!",
            "If you can't categorize an expense, ask yourself if you really needed it in the first place!",
            "The 'Others' category should be small enough to ignore but tracked carefully enough not to explode!",
            "Mysterious expenses are like ghosts - they haunt your budget until you identify and exorcise them!"
        ]
    }
    
    tips = category_tips.get(category, [
        "Track every rupee - it's like having GPS for your money!",
        "A tracked expense is the first step to a reduced expense!",
        "Knowing where your money goes is half the battle in personal finance!",
        "If you're not tracking it, you're probably wasting it!"
    ])
    
    return random.choice(tips)

def get_investment_tip():
    """
    Return a humorous investment tip
    """
    tips = [
        "Time in the market beats timing the market. But telling people you timed it perfectly makes better party conversation!",
        "Diversification means not putting all your eggs in one basket. It also means accepting that some baskets will inevitably contain rotten eggs!",
        "The stock market is like a roller coaster - it's the people who get off in the middle who get hurt!",
        "Mutual funds are like arranged marriages - professional management with generally acceptable results!",
        "Day trading is like gambling, except the casino sometimes closes for holidays and has circuit breakers!",
        "The best investment strategy is the one you can stick with through both bull and bear markets... and through your spouse's reactions to both!",
        "Checking your investments daily is like watching grass grow, except sometimes the grass spontaneously catches fire!",
        "Stock tips from friends are like free puppies - they seem great until you realize the ongoing costs!",
        "Investment risk and return are like a see-saw - you can't have one end go up without the other going down!",
        "The three most dangerous words in investing are 'This time is different.' The three most profitable are 'I don't know.'",
        "Your investment portfolio should be like your spice cabinet - diverse, balanced, and occasionally reviewed for expired items!",
        "Investing is simple, but not easy - like losing weight, raising children, or pretending to enjoy your in-laws' company!",
        "Low-cost index funds are like vanilla ice cream - they seem boring until you realize how reliable they are compared to exotic flavors!",
        "Compound interest is like a snowball rolling downhill - it starts slow but becomes unstoppable with time and patience!",
        "The best investment returns often come from boring companies that make everyday products people can't live without... like toilet paper!"
    ]
    
    return random.choice(tips)

def get_budget_tip():
    """
    Return a humorous budgeting tip
    """
    tips = [
        "A budget doesn't limit your freedom; it gives you freedom from worry. And from expensive coffee shops!",
        "Budget categories are like speed limits - guidelines that you occasionally exceed but generally try to respect!",
        "The 50/30/20 budget: 50% needs, 30% wants, 20% savings, and 100% wondering how everything got so expensive!",
        "Your budget is the grown-up version of 'playing house' - except now the money is real and so are the bills!",
        "Zero-based budgeting is like Tetris - you arrange your money blocks until everything fits perfectly!",
        "Budgeting apps are like having a tiny accountant in your pocket, except they don't charge by the hour!",
        "Having a budget is like having a personal trainer for your money - keeping it disciplined when you'd rather splurge!",
        "The envelope system works because cash has one amazing feature - when it's gone, it's gone! Unlike your credit limit!",
        "A good budget has built-in fun money. Even financial responsible adults need ice cream sometimes!",
        "Updating your budget is like flossing - everyone knows they should do it regularly, but few actually do!",
        "Budget reviews are like checking your weight - sometimes painful but necessary for long-term health!",
        "Emergency funds are like umbrellas - you don't need them until you really, REALLY need them!",
        "Making a budget is easy; sticking to it is the hard part. Kind of like diet plans!",
        "The first rule of budgeting: Be honest with yourself about your spending. The second rule: Stop crying about rule one!",
        "Budgets are like New Year's resolutions - most fail by February unless you build in realistic expectations!"
    ]
    
    return random.choice(tips)

def get_saving_tip():
    """
    Return a humorous saving tip
    """
    tips = [
        "Pay yourself first, because no one else is standing in line to do it for you!",
        "Automatic transfers to savings are like brushing your teeth - do it regularly without thinking and avoid painful consequences later!",
        "Saving money is like learning a language - a little every day adds up to fluency over time!",
        "The 24-hour rule for purchases works because most desires, like spicy food cravings, fade with time!",
        "Your savings account should be like that one friend who's hard to reach - out of sight and requiring effort to contact!",
        "Saving 10% of your income is good. Saving 20% is better. Convincing rich relatives to include you in their will is best!",
        "The difference between saving and hoarding is purpose. One builds wealth, the other builds weird collections!",
        "Small savings add up. Skip the daily fancy coffee for a year = a weekend getaway. Skip it for 40 years = retirement in Goa!",
        "An emergency fund should cover 3-6 months of expenses, or 1-2 relationship breakups, whichever costs more!",
        "Save like a pessimist, invest like an optimist. It's the financial version of 'hope for the best, prepare for the worst'!",
        "Finding money to save is like finding time to exercise - it's about priorities, not possibilities!",
        "The joy of saving comes not from having money, but from having options that money provides!",
        "Saving is more psychological than mathematical. It's not about spreadsheets; it's about habits!",
        "When you get a raise, raise your savings rate, not your lifestyle. Your future self will thank you... or buy you better gifts!",
        "Living below your means isn't deprivation; it's preparation for a future where you can live however you want!"
    ]
    
    return random.choice(tips)
