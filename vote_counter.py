import csv

def SafeIntAndReturn(object): #extraccion de metodos, extraccion de clases y simplificacion de condicionales
    try: value = int(object)
    except: value = 0
    return value

def separationOfARow(row): #extraccion de metodos
    city = row[0]
    candidate = row[1]
    votes = SafeIntAndReturn(row[2]) # extraccion de clases y simplificacion de condicionales
    return city, candidate, votes

def addingVotes(candidate, result, votes): #extraccion de metodos
    if candidate in result:
        result[candidate]+=votes
    else: 
        result[candidate]=votes


def count_votes(file_path):
    results = {}
    
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # Skip the header

        for row in reader:
            city,candidate, votes = separationOfARow(row)
            addingVotes(candidate, results, votes)
            #eliminacion de codigo duplicado tras extraccion de metodos

    for candidate, total_votes in results.items():
        print(f"{candidate}: {total_votes} votes")

    sortedbyvotes = sorted(results.items(), key=lambda item:item[1], reverse=True)
    print(f"winner is {sortedbyvotes[0][0]}")

# Example usage
count_votes('votes.csv')
