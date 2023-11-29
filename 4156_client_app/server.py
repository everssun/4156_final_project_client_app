from flask import Flask, redirect, url_for, session
from flask import render_template
from flask import Response, request, jsonify

app = Flask(__name__)

admin_credentials = {'username': 'admin', 'password': '123456'}
app.secret_key = 'debugTeam'  

current_id = 10

data = {
	"1":{
		"id": "1",
		"name": "Lionel Messi",
		"image": "https://netstorage-legit.akamaized.net/images/3b7b5f5510d0bf96.jpg",
		"summary": "Lionel Andrés Messi, also known as Leo Messi, is an Argentine professional footballer who plays as a forward for Ligue 1 club Paris Saint-Germain and captains the Argentina national team. Often considered the best player in the world and widely regarded as one of the greatest players of all time, Messi has won a record seven Ballon d'Or awards, a record six European Golden Shoes, and in 2020 was named to the Ballon d'Or Dream Team. Until leaving the club in 2021, he had spent his entire professional career with Barcelona, where he won a club-record 35 trophies, including ten La Liga titles, seven Copa del Rey titles and four UEFA Champions Leagues. A prolific goalscorer and creative playmaker, Messi holds the records for most goals in La Liga, a La Liga and European league season, most hat-tricks in La Liga and the UEFA Champions League, and most assists in La Liga, a La Liga season and the Copa América. He also holds the record for most international goals by a South American male. Messi has scored over 750 senior career goals for club and country, and has the most goals by a player for a single club.",
		"rating": "93",
		"awards": ["Ballon d'Or/FIFA Ballon d'Or", "FIFA World Player of the Year", "The Best FIFA Men's Player", "European Golden Shoe", "FIFA World Cup Golden Ball", "La Liga Best Player", "Argentine Footballer of the Year"]
},
	"2":{
		"id": "2",
		"name": "Robert Lewandowski",
		"image": "https://bayernstrikes.com/wp-content/uploads/getty-images/2019/10/1168485252.jpeg",
		"summary": "Robert Lewandowski is a Polish professional footballer who plays as a striker for Bundesliga club Bayern Munich and is the captain of the Poland national team. Recognized for his positioning, technique and finishing, Lewandowski is considered one of the best strikers of all time, as well as one of the most successful players in Bundesliga history. He has scored over 600 senior career goals for club and country.",
		"rating": "92",
		"awards": ["Ballon d'Or Striker of the Year", "European Golden Shoe", "The Best FIFA Men's Player", "FIFA Club World Cup Golden Ball", "IFFHS World's Best Top Goal Scorer", "IFFHS World's Best Top Division Goal Scorer"]
},
	"3":{
                "id": "3",
		"name": "Cristiano Ronaldo",
		"image": "https://cdn-wp.thesportsrush.com/2017/04/cristiano-ronaldo-cristiano-ronaldo-cristiano-ronaldo-ronaldo-manchester-united-manchester-united-football-celebrity-star-football-sports.jpg",
		"summary": "Cristiano Ronaldo dos Santos Aveiro GOIH ComM is a Portuguese professional footballer who plays as a forward for Premier League club Manchester United and captains the Portugal national team. Often considered the best player in the world and widely regarded as one of the greatest players of all time, Ronaldo has won five Ballon d'Or awards and four European Golden Shoes, the most by a European player. He has won 32 trophies in his career, including seven league titles, five UEFA Champions Leagues, one UEFA European Championship, and one UEFA Nations League. Ronaldo holds the records for most appearances, most goals, and assists in the Champions League, most goals in the European Championship, most international goals by a male player, and most international appearances by a European male. He is one of the few players to have made over 1,100 professional career appearances, and has scored over 800 official senior career goals for club and country.",
		"rating": "91",
		"awards": ["FIFA Ballon d'Or/Ballon d'Or: 2008, 2013, 2014, 2016, 2017", "FIFA World Player of the Year: 2008", "The Best FIFA Men's Player: 2016, 2017", "European Golden Shoe: 2007–08, 2010–11, 2013–14, 2014–15"]
},
        "4":{
            "id": "4",
            "name": "Kylian Mbappe",
            "image": "https://datacdn.btimesonline.com/data/images/full/111772/friendly-le-havre-v-paris-st-germain.jpg",
            "summary": "Kylian Mbappé Lottin is a French professional footballer who plays as a forward for Ligue 1 club Paris Saint-Germain and the France national team. Considered one of the best players in the world, he is known for his dribbling, speed, and finishing.",
            "rating": "91",
            "awards": ["UEFA European Under-19 Championship Team of the Tournament: 2016", "UNFP Ligue 1 Player of the Year: 2018–19, 2020–21", "Golden Boy: 2017", "Kopa Trophy: 2018"],
            },
        "5":{
            "id": "5",
            "name": "Neymar Jr",
            "image": "https://d.newsweek.com/en/full/1512948/neymar-brazil.jpg",
            "summary": "Neymar da Silva Santos Júnior, known as Neymar, is a Brazilian professional footballer who plays as a forward for Ligue 1 club Paris Saint-Germain and the Brazil national team. He is widely regarded as one of the best players in the world.",
            "rating": "91",
            "awards": ["Copa América Team of the Tournament: 2021", "IFFHS Men's World Team: 2017", "ESM Team of the Year: 2017–18", "La Liga Best World Player: 2014–15"],
            },
        "6":{
            "id": "6",
            "name": "Kevin De Bruyne",
            "image": "https://mancitysquare.com/wp-content/uploads/getty-images/2018/06/874857730.jpeg",
            "summary": "Kevin De Bruyne is a Belgian professional footballer who plays as a midfielder for Premier League club Manchester City and the Belgium national team. De Bruyne is widely regarded as one of the best players in the world, and has often been described as a complete footballer.",
            "rating": "91",
            "awards": ["IFFHS All Time Belgium XI", "IFFHS World's Best Playmaker: 2020, 2021", "IFFHS UEFA Team of the Decade: 2011–2020", "UEFA Champions League Midfielder of the Season: 2019–20"],
            },
        "8":{
            "id": "8",
            "name": "Harry Kane",
            "image": "https://hotspurhq.com/wp-content/uploads/getty-images/2017/10/857967384-england-v-slovenia-fifa-2018-world-cup-qualifier.jpg.jpg",
            "summary": "Harry Edward Kane MBE is an English professional footballer who plays as a striker for Premier League club Tottenham Hotspur and captains the England national team. Regarded as one of the best strikers in the world, Kane is known for his prolific goalscoring record and ability to link play.",
            "rating": "90",
            "awards": ["FIFA World Cup Golden Boot: 2018", "IFFHS World's Best Top Goal Scorer: 2017", "England Player of the Year Award: 2017, 2018", "PFA Fans' Player of the Year: 2016–17"],
            },
        "9":{
            "id": "9",
            "name": "Kante",
            "image": "https://images.alphacoders.com/113/1138489.jpg",
            "summary": "N'Golo Kanté is a French professional footballer who plays as a central midfielder for Premier League club Chelsea and the France national team. Considered by many to be one of the world's best midfielders, Kanté is widely praised for his work rate and defensive acumen.",
            "rating": "90",
            "awards": ["PFA Team of the Year: 2015–16 ", "UEFA Team of the Year: 2018", "French Player of the Year: 2017", "Premier League Player of the Season: 2016–17"],
            },
        "10":{
            "id": "10",
            "name": "Heung Min Son",
            "image": "https://images.performgroup.com/di/library/GOAL/f6/a2/son-heung-min-tottenham-2018-19_5munr0zd9qe816snz2hw8818y.jpg?t=749962002&quality=100",
            "summary": "Son Heung-min is a South Korean professional footballer who plays as a forward for the Premier League club Tottenham Hotspur and captains the South Korea national team. Widely regarded as one of the best wingers in the world, as well as one of the best Asian footballers in history, Son was the first Asian player to score more than 50 goals in the Premier League, and was nominated for the Ballon d'Or in 2019.",
            "rating": "89",
            "awards": ["FIFA Puskás Award: 2020", "PFA Premier League Team of the Year: 2020–21", "Tottenham Hotspur Player of the Season: 2018–19, 2019–20", "London Player of the Year (Premier League): 2018–19"],
            },
}

# ROUTES

@app.route('/')
def hello_world():
    return render_template('welcome.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # Retrieve form data
        entered_username = request.form['username']
        entered_password = request.form['password']

        # Check if entered credentials match the dummy admin credentials
        if entered_username == admin_credentials['username'] and entered_password == admin_credentials['password']:
            session['authenticated'] = True
            return redirect(url_for('admin_center'))
        else:
            # Render the login page with an error message
            return render_template('admin_login.html', error='Invalid username or password')

    # Render the login page for GET requests
    return render_template('admin_login.html', error=None)
   
@app.route('/admin-center')
def admin_center():
    if not session.get('authenticated'):
        return redirect(url_for('admin_login'))
    return render_template('admin_center.html')

@app.route('/admin-logout')
def admin_logout():
    session.pop('authenticated', None)
    return redirect(url_for('admin_login'))

@app.route('/add_company')
def add_company():
    global data
    return render_template('add_company.html', d=data)

@app.route('/add_susbscription')
def add_susbcription():
    global data
    return render_template('add_subscription.html', d=data)

@app.route('/save_data', methods=['GET', 'POST'])
def save_data():
    global data
    global current_id
    
    json_data = request.get_json()
    name = json_data["name"]
    rate = json_data["rating"]
    image = json_data["image"]
    summary = json_data["summary"]
    string = json_data["awards"]

    awards=[]
    temp=""
    for i in string:
        if i == ";":
            awards.append(temp)
            temp=""
        else:
            temp+=i
    
    current_id += 1
    new_id = current_id
    new_name_entry = {
        "id": str(current_id),
        "name": name,
        "image": image,
        "summary": summary,
        "rating": rate,
        "awards": awards
    }
    data[str(current_id)]=new_name_entry

    # send back the WHOLE array of data, so the client can redisplay it
    return jsonify(data=data, id_add = str(current_id))

if __name__ == '__main__':
    app.run(debug=True)
    #print(add_name())

