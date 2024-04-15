#include <iostream>
#include <pqxx/pqxx>
#include <cmath>
#include <string>
#include <chrono>

struct DamageResult {
    int dph;
    int ddph;
    int bonushealing;
};

typedef struct DamageResult Struct;


int getCountForItem(const std::map<std::string, std::map<std::string, int>>& counts, const std::string& item) {
    auto it = counts.find(item);
    if (it != counts.end()) {
        int total = 0;
        for (const auto& pair : it->second) {
            total += pair.second;
        }
        return total;
    }
    return 0; // If item not found, return 0
}

int getCountForAllegiance(const std::map<std::string, std::map<std::string, int>>& counts, const std::string& allegiance) {
    int total = 0;
    for (const auto& pair : counts) {
        auto it = pair.second.find(allegiance);
        if (it != pair.second.end()) {
            total += it->second;
        }
    }
    return total;
}

int getAttackerAsWarTargetCount(const std::string& attacker) {
    try {
        pqxx::connection conn("user=esse password=96509035 host=localhost port=5432 dbname=goldcastle");

        if (!conn.is_open()) {
            std::cerr << "Error: Failed to connect to the database." << std::endl;
            return -1; // Return an error value
        }

        pqxx::work txn(conn);
        pqxx::result result = txn.exec(
            "SELECT COUNT(*) FROM nft_goldcastle_asia WHERE members > 10 AND wartarget = " + txn.quote(attacker)
        );
        txn.commit();

        int count = result[0][0].as<int>();
        return count;
    } catch (const std::exception &e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return -1; // Return an error value
    }
}

Struct damage(std::string genderattacker, int attackerrarity, int attackerwarhp, double warstarted, std::string attacker, double warattack, int xcoordsattacker, int ycoordsattacker, int zcoordsattacker, int acoordsattacker, std::string allegianceattacker, std::string itemattacker, std::string continentattacker, std::string attackerwifeallegiance, int attackerlives,
            std::string wartarget, int xcoordstarget, int ycoordstarget, int zcoordstarget, int acoordstarget, std::string allegiancetarget, std::string itemtarget, int defendattack, std::string continenttarget, std::string targetwifeallegiance, int wartargetlives
               ) {

    double predistance = pow(xcoordsattacker - xcoordstarget, 2) + pow(ycoordsattacker - ycoordstarget, 2) + pow(zcoordsattacker - zcoordstarget, 2) + pow(acoordsattacker - acoordstarget, 2);
    double distance = sqrt(predistance);
    
    double defendratio = 0.04;

    double attackratio = 0.04;

    int bonushealing = 0;

    int attackerflanks = getAttackerAsWarTargetCount(attacker);
    if (attackerflanks == -1) {
        // Handle error condition
        Struct errorResult;
        errorResult.dph = -1;
        errorResult.ddph = -1;
        return errorResult; // Return an error struct
    }

    int targetflanks = getAttackerAsWarTargetCount(wartarget);
    if (targetflanks == -1) {
        // Handle error condition
        Struct errorResult;
        errorResult.dph = -1;
        errorResult.ddph = -1;
        return errorResult; // Return an error struct
    }


    try {
        pqxx::connection conn("user=esse password=96509035 host=localhost port=5432 dbname=goldcastle");

        if (!conn.is_open()) {
            std::cerr << "Error: Failed to connect to the database." << std::endl;
            Struct errorResult;
            errorResult.dph = -1;
            errorResult.ddph = -1;
            return errorResult; // Return an error struct
        }

        // Store counts for both attacker and wartarget
        std::map<std::string, std::map<std::string, int>> attacker_counts;
        std::map<std::string, std::map<std::string, int>> target_counts;
        std::map<std::string, int> all_counts;

        // Function to process result and update counts
        auto process_result = [&](const pqxx::result& result, std::map<std::string, std::map<std::string, int>>& counts) {
            for (const auto& row : result) {
                std::string item = row["item"].as<std::string>();
                std::string allegiance = row["allegiance"].as<std::string>();
                int count = row["count"].as<int>();

                // Increment count for the item and allegiance
                counts[item][allegiance] += count;
                
                all_counts[item] += count;
                all_counts[allegiance] += count;
            }
        };

        // Execute queries for attacker and wartarget
        pqxx::work txn(conn);
        pqxx::result attacker_result = txn.exec(
            "SELECT item, allegiance, COUNT(*) FROM nft_goldcastle_asia WHERE overlord = " + txn.quote(attacker) + " GROUP BY item, allegiance"
        );
        pqxx::result target_result = txn.exec(
            "SELECT item, allegiance, COUNT(*) FROM nft_goldcastle_asia WHERE overlord = " + txn.quote(wartarget) + " GROUP BY item, allegiance"
        );
        txn.commit();

        // Process results to update counts
        process_result(attacker_result, attacker_counts);
        process_result(target_result, target_counts);


        // std::cout << "All Counts:" << std::endl;
        // for (const auto& entry : all_counts) {
        //     std::cout << entry.first << " Count: " << entry.second << std::endl;
        // }



int coffee_atck = getCountForItem(attacker_counts, "Coffee");
int avengingbrothers_atck = getCountForItem(attacker_counts, "Vengeful younger brother");
int fleetofbusan_atck = getCountForItem(attacker_counts, "Fleet of Busan");
int wildbrownbears_atck = getCountForItem(attacker_counts, "Wild Brown Bear");
int goldenbuddha_atck = getCountForItem(attacker_counts, "Golden Buddha");
int thaibrothels_atck = getCountForItem(attacker_counts, "Thai brothel");
int tombofkaidu_atck = getCountForItem(attacker_counts, "Tomb of Kaidu Khan");
int angkorwats_atck = getCountForItem(attacker_counts, "Angkor Wat");
int thezodiacs_atck = getCountForItem(attacker_counts, "The Zodiac");
int royalflowers_atck = getCountForItem(attacker_counts, "Royal Flower");
int mongolcourts_atck = getCountForItem(attacker_counts, "The Mongol Court");
int timecomputer_atck = getCountForItem(attacker_counts, "Time Computer");
int revivalspheres_atck = getCountForItem(attacker_counts, "Revival sphere");
int venemoussnakes_atck = getCountForItem(attacker_counts, "Venemous snake");
int armyofthelady_atck = getCountForItem(attacker_counts, "Army of the Lady");
int mountfuji_atck = getCountForItem(attacker_counts, "Mount Fuji");
int sogdianrock_atck = getCountForItem(attacker_counts, "Sogdian Rock");
int dragondiadem_atck = getCountForItem(attacker_counts, "Dragon Diadem");
int mountararat_atck = getCountForItem(attacker_counts, "Mount Ararat");
int dragonthrones_atck = getCountForItem(attacker_counts, "Dragon Throne");
int edocastle_atck = getCountForItem(attacker_counts, "Edo Castle");
int chrysanthemum_atck = getCountForItem(attacker_counts, "The Chrysanthemum");
int imperialseal_atck = getCountForItem(attacker_counts, "Imperial seal");
int mongolhordes_atck = getCountForItem(attacker_counts, "The Mongol Horde");
int karnatakaboars_atck = getCountForItem(attacker_counts, "Karnataka Boar");
int sensojis_atck = getCountForItem(attacker_counts, "Sensō-ji");
int churchoftheeast_atck = getCountForItem(attacker_counts, "The Church of the East");
int jewishwarships_atck = getCountForItem(attacker_counts, "Jewish war ship");
int celestialrelic_atck = getCountForItem(attacker_counts, "Celestial relic");
int marseshields_atck = getCountForItem(attacker_counts, "Mars shield");
int stolenhorses_atck = getCountForItem(attacker_counts, "Stolen horse");
int rubys_atck = getCountForItem(attacker_counts, "Ruby") + getCountForItem(attacker_counts, "Stolen Ruby");
int goldendaggers_atck = getCountForItem(attacker_counts, "Golden dagger") + getCountForItem(attacker_counts, "Golden Dagger");
int goldentomes_atck = getCountForItem(attacker_counts, "Golden tome");
int beers_atck = getCountForItem(attacker_counts, "Beer");
int armoredstallions_atck = getCountForItem(attacker_counts, "Armored Stallion");
int castles_atck = getCountForItem(attacker_counts, "Castle");
int spears_atck = getCountForItem(attacker_counts, "Spear");
int knightsswords_atck = getCountForItem(attacker_counts, "Knight's Sword");
int goldencompasses_atck = getCountForItem(attacker_counts, "Golden compass") + getCountForItem(attacker_counts, "Stolen Golden compass");
int woodenshields_atck = getCountForItem(attacker_counts, "Wooden shield");
int dogs_atck = getCountForItem(attacker_counts, "Dog");
int goldenarmors_atck = getCountForItem(attacker_counts, "Golden armor");
int silveramulets_atck = getCountForItem(attacker_counts, "Silver amulet") + getCountForItem(attacker_counts, "Stolen Silver amulet");
int oxes_atck = getCountForItem(attacker_counts, "Ox");
int rustyswords_atck = getCountForItem(attacker_counts, "Rusty sword");
int chickens_atck = getCountForItem(attacker_counts, "Chicken");
int jadeamulets_atck = getCountForItem(attacker_counts, "Jade amulet");
int cats_atck = getCountForItem(attacker_counts, "Cat");
int goldenswords_atck = getCountForItem(attacker_counts, "Golden sword");
int summerswords_atck = getCountForItem(attacker_counts, "Summersword");
int goats_atck = getCountForItem(attacker_counts, "Goat");
int birds_atck = getCountForItem(attacker_counts, "Bird");
int asses_atck = getCountForItem(attacker_counts, "Ass");
int chosenswords_atck = getCountForItem(attacker_counts, "Chosen sword");
int goldenshields_atck = getCountForItem(attacker_counts, "Golden Shield") + getCountForItem(attacker_counts, "Golden shield");
int summerstones_atck = getCountForItem(attacker_counts, "Summerstone");
int stolenarmor_atck = getCountForItem(attacker_counts, "Stolen armor");
int glasses_atck = getCountForItem(attacker_counts, "Glasses");
int chosenwings_atck = getCountForItem(attacker_counts, "Chosen's wings");
int books_atck = getCountForItem(attacker_counts, "Book");
int racehorses_atck = getCountForItem(attacker_counts, "Race Horse");
int universities_atck = getCountForItem(attacker_counts, "University");
int goldenmaces_atck = getCountForItem(attacker_counts, "Stolen Golden mace") + getCountForItem(attacker_counts, "Golden mace");
int mansions_atck = getCountForItem(attacker_counts, "Mansion");
int brothels_atck = getCountForItem(attacker_counts, "Brothel");
int banks_atck = getCountForItem(attacker_counts, "Bank");
int gamblinghouses_atck = getCountForItem(attacker_counts, "Gambling house");
int stolenshields_atck = getCountForItem(attacker_counts, "Stolen Shield");
int countryestates_atck = getCountForItem(attacker_counts, "Country estate");
int bronzecoins_atck = getCountForItem(attacker_counts, "Bronze coin");



int coffee_def = getCountForItem(target_counts, "Coffee");
int avengingbrothers_def = getCountForItem(target_counts, "GVengeful younger brother");
int fleetofbusan_def = getCountForItem(target_counts, "Fleet of Busan");
int wildbrownbears_def = getCountForItem(target_counts, "Wild Brown Bear");
int goldenbuddha_def = getCountForItem(target_counts, "Golden Buddha");
int thaibrothels_def = getCountForItem(target_counts, "Thai brothel");
int tombofkaidu_def = getCountForItem(target_counts, "Tomb of Kaidu Khan");
int angkorwats_def = getCountForItem(target_counts, "Angkor Wat");
int thezodiacs_def = getCountForItem(target_counts, "The Zodiac");
int royalflowers_def = getCountForItem(target_counts, "Royal Flower");
int mongolcourts_def = getCountForItem(target_counts, "The Mongol Court");
int timecomputer_def = getCountForItem(target_counts, "Time Computer");
int revivalspheres_def = getCountForItem(target_counts, "Revival sphere");
int venemoussnakes_def = getCountForItem(target_counts, "Venemous snake");
int armyofthelady_def = getCountForItem(target_counts, "Army of the Lady");
int mountfuji_def = getCountForItem(target_counts, "Mount Fuji");
int sogdianrock_def = getCountForItem(target_counts, "Sogdian Rock");
int dragondiadem_def = getCountForItem(target_counts, "Dragon Diadem");
int mountararat_def = getCountForItem(target_counts, "Mount Ararat");
int dragonthrones_def = getCountForItem(target_counts, "Dragon Throne");
int edocastle_def = getCountForItem(target_counts, "Edo Castle");
int chrysanthemum_def = getCountForItem(target_counts, "The Chrysanthemum");
int imperialseal_def = getCountForItem(target_counts, "Imperial seal");
int mongolhordes_def = getCountForItem(target_counts, "The Mongol Horde");
int karnatakaboars_def = getCountForItem(target_counts, "Karnataka Boar");
int sensojis_def = getCountForItem(target_counts, "Sensō-ji");
int churchoftheeast_def = getCountForItem(target_counts, "The Church of the East");
int jewishwarships_def = getCountForItem(target_counts, "Jewish war ship");
int celestialrelic_def = getCountForItem(target_counts, "Celestial relic");
int marseshields_def = getCountForItem(target_counts, "Mars shield");
int stolenhorses_def = getCountForItem(target_counts, "Stolen horse");
int rubys_def = getCountForItem(target_counts, "Ruby") + getCountForItem(target_counts, "Stolen Ruby");
int goldendaggers_def = getCountForItem(target_counts, "Golden dagger") + getCountForItem(target_counts, "Golden Dagger");
int goldentomes_def = getCountForItem(target_counts, "Golden tome");
int beers_def = getCountForItem(target_counts, "Beer");
int armoredstallions_def = getCountForItem(target_counts, "Armored Stallion");
int castles_def = getCountForItem(target_counts, "Castle");
int spears_def = getCountForItem(target_counts, "Spear");
int knightsswords_def = getCountForItem(target_counts, "Knight's Sword");
int goldencompasses_def = getCountForItem(target_counts, "Golden compass") + getCountForItem(target_counts, "Stolen Golden compass");
int woodenshields_def = getCountForItem(target_counts, "Wooden shield");
int dogs_def = getCountForItem(target_counts, "Dog");
int goldenarmors_def = getCountForItem(target_counts, "Golden armor");
int silveramulets_def = getCountForItem(target_counts, "Silver amulet") + getCountForItem(target_counts, "Stolen Silver amulet");
int oxes_def = getCountForItem(target_counts, "Ox");
int rustyswords_def = getCountForItem(target_counts, "Rusty sword");
int chickens_def = getCountForItem(target_counts, "Chicken");
int jadeamulets_def = getCountForItem(target_counts, "Jade amulet");
int cats_def = getCountForItem(target_counts, "Cat");
int goldenswords_def = getCountForItem(target_counts, "Golden sword");
int summerswords_def = getCountForItem(target_counts, "Summersword");
int goats_def = getCountForItem(target_counts, "Goat");
int birds_def = getCountForItem(target_counts, "Bird");
int asses_def = getCountForItem(target_counts, "Ass");
int chosenswords_def = getCountForItem(target_counts, "Chosen sword");
int goldenshields_def = getCountForItem(target_counts, "Golden Shield") + getCountForItem(target_counts, "Golden shield");
int summerstones_def = getCountForItem(target_counts, "Summerstone");
int stolenarmor_def = getCountForItem(target_counts, "Stolen armor");
int glasses_def = getCountForItem(target_counts, "Glasses");
int chosenwings_def = getCountForItem(target_counts, "Chosen's wings");
int books_def = getCountForItem(target_counts, "Book");
int racehorses_def = getCountForItem(target_counts, "Race Horse");
int universities_def = getCountForItem(target_counts, "University");
int goldenmaces_def = getCountForItem(target_counts, "Stolen Golden mace") + getCountForItem(target_counts, "Golden mace");
int mansions_def = getCountForItem(target_counts, "Mansion");
int brothels_def = getCountForItem(target_counts, "Brothel");
int banks_def = getCountForItem(target_counts, "Bank");
int gamblinghouses_def = getCountForItem(target_counts, "Gambling house");
int stolenshields_def = getCountForItem(target_counts, "Stolen Shield");
int countryestates_def = getCountForItem(target_counts, "Country estate");
int bronzecoins_def = getCountForItem(target_counts, "Bronze coin");



// item bonuses:

    attackratio -= 0.04 * angkorwats_def + 0.04 * sensojis_def + 0.04 * edocastle_def + 0.05 * sogdianrock_def + 0.001 * stolenshields_def + 0.004 * goldenshields_def + 0.007 * chosenwings_def + 0.005 * stolenarmor_def + 0.004 * goldenshields_def + 0.005 * goldenarmors_def + 0.0009 * woodenshields_def + 0.003 * castles_def + 0.004 * armoredstallions_def;
    bonushealing += coffee_atck * 15 + thaibrothels_atck * 25 + churchoftheeast_atck * 8 + mountfuji_atck * 30 + gamblinghouses_atck * 5 + countryestates_atck * 7 + bronzecoins_atck * 1 + brothels_atck * 5 + mansions_atck * 4 + banks_atck * 3 + universities_atck * 4 + silveramulets_atck * 1 + rubys_atck * 1 + jadeamulets_atck * 2 + goldentomes_atck * 2 + cats_atck;
    attackratio += avengingbrothers_atck * 0.04 + fleetofbusan_atck * 0.03 + tombofkaidu_atck * 0.02 + chosenswords_atck * 0.02 + karnatakaboars_atck * 0.01 + jewishwarships_atck * 0.009 + goldendaggers_atck * 0.004 + goldenmaces_atck * 0.005 + goldenswords_atck * 0.005 + knightsswords_atck * 0.004 + spears_atck * 0.003 + rustyswords_atck * 0.001 + birds_atck * 0.003 + dogs_atck * 0.001;


    if (goldenbuddha_def >= 1 && continentattacker == "Asia"){
        attackratio -= 0.01;
    }

       if (mongolcourts_atck >= 1 && continentattacker == "Asia"){
        bonushealing += 50;
    } 

       if (venemoussnakes_def >= 1){
        bonushealing = 0;
    } 

       if (mongolhordes_atck >= 1 && continenttarget == "Asia"){
        attackratio += 0.018;
    } 

       if (imperialseal_def >= 1 && attackerrarity <= 8){
        attackratio = 0.005;
    } 

       if (chrysanthemum_def >= 1 && continentattacker != "Asia"){
        defendratio += 0.02;
    } 

    if (thezodiacs_atck >= 1){
        attackratio += oxes_atck * 0.001 + goats_atck * 0.001 + dogs_atck * 0.001;
    }

    if (royalflowers_atck >= 1){
        bonushealing += 44;
        if (genderattacker == "woman"){
            bonushealing += 44;
        }
    }

    if (revivalspheres_atck >= 1){
        bonushealing += 1000;
    }

    if (mountararat_def >= 1){
        defendratio += 0.1;
        if (wartargetlives == 1){
            defendratio += 0.02;
        }
    }
    if (armyofthelady_atck >= 1 && genderattacker == "woman"){
        attackratio += 0.018;
    }

    if (acoordsattacker > 200){
        attackratio += summerswords_atck * 0.025;
        defendratio += summerswords_def * 0.025;
    } else {
        attackratio += summerswords_atck * 0.01;
        defendratio += summerswords_def * 0.01;
    }

    attackratio += marseshields_atck * 0.008;
    defendratio += marseshields_def * 0.008;

    int summerstoneratio = summerstones_def - summerstones_atck;
    if (allegianceattacker != "Guardians of the Simulator"){
    attackerflanks += summerstoneratio;
    } 
    else if (allegianceattacker == "Guardians of the Simulator" && summerstoneratio < 0){
    attackerflanks += summerstoneratio;
    }

    attackratio += celestialrelic_atck * 0.01;
    defendratio += celestialrelic_def * 0.01;
    if (zcoordsattacker >= 100){
        attackratio += 0.025 * celestialrelic_atck;
    }
    if (zcoordstarget >= 100){
        defendratio += 0.025 * celestialrelic_def;
    }  

    int ancientrights = getCountForAllegiance(attacker_counts, "The Ancient Rights");
    int ancientrelics = getCountForItem(attacker_counts, "Ancient Relic");
    while(ancientrelics > 0){
        attackratio += 0.002 * ancientrights;
        ancientrelics -= 1;
    }


    double dragonbonus = 0;
    int dragonattackers = 4 * getCountForAllegiance(attacker_counts, "Chosen Dragon") + getCountForAllegiance(attacker_counts, "Dragon Order");
    if (continenttarget != "Asia"){
        if (allegianceattacker == "Chosen Dragon" && attackerwifeallegiance == "Chosen Unicorn"){
            dragonbonus = 0.005;
        }
        else if (allegianceattacker == "Chosen Dragon" && attackerwifeallegiance == "Unicorn Order"){
            dragonbonus = 0.003;
        }
        else if (allegianceattacker == "Dragon Order" && attackerwifeallegiance == "Chosen Unicorn"){
            dragonbonus = 0.002;
        }
        else if (allegianceattacker == "Dragon Order" && attackerwifeallegiance == "Unicorn Order"){
            dragonbonus = 0.001;
        }
        else {
            dragonbonus = 0.0005;
        }
        while(dragonattackers > 0){
            attackratio += dragonbonus * (dragonthrones_atck + 1);
            dragonattackers -= 1;
        }
    }

    double unicbonus = 0;
    int unicorndefenders = 4 * getCountForAllegiance(target_counts, "Chosen Unicorn") + getCountForAllegiance(attacker_counts, "Unicorn Order");
    if (continenttarget != "Asia"){
        if (targetwifeallegiance == "Chosen Dragon" && allegiancetarget == "Chosen Unicorn"){
            unicbonus = 0.005;
        }
        else if (targetwifeallegiance == "Chosen Dragon" && allegiancetarget == "Unicorn Order"){
            unicbonus = 0.003;
        }
        else if (targetwifeallegiance == "Dragon Order" && allegiancetarget == "Chosen Unicorn"){
            unicbonus = 0.002;
        }
        else if (targetwifeallegiance == "Dragon Order" && allegiancetarget == "Unicorn Order"){
            unicbonus = 0.001;
        }
        else {
            unicbonus = 0.0005;
        }
        while(unicorndefenders > 0){
            defendratio += unicbonus * (dragondiadem_def + 1);
            unicorndefenders -= 1;
        }
    }





    int thenewrichandcitydwellers = getCountForAllegiance(target_counts, "The New Rich") + getCountForAllegiance(target_counts, "Citydwellers");
    int newnobles = getCountForAllegiance(target_counts, "The new Nobility");
    while (thenewrichandcitydwellers >= 8 && newnobles >= 1) {
        thenewrichandcitydwellers -= 8;
        newnobles -= 1;
        attackratio -= 0.004;
    }

    int atckthenewrichandcitydwellers = getCountForAllegiance(attacker_counts, "The New Rich") + getCountForAllegiance(attacker_counts, "Citydwellers");
    int atcknewnobles = getCountForAllegiance(attacker_counts, "The new Nobility");
    while (atckthenewrichandcitydwellers >= 8 && atcknewnobles >= 1) {
        atckthenewrichandcitydwellers -= 8;
        atcknewnobles -= 1;
        attackratio += 0.004;
    }


    int oldricholdnobles = getCountForAllegiance(target_counts, "The Old Rich") + getCountForAllegiance(target_counts, "The Old Nobility");
    int templarorder = getCountForAllegiance(target_counts, "Templar Order");
    while (oldricholdnobles >= 4 && templarorder >= 1) {
        oldricholdnobles -= 4;
        templarorder -= 1;
        attackratio -= 0.005;
    }

    int atckoldricholdnobles = getCountForAllegiance(attacker_counts, "The Old Rich") + getCountForAllegiance(attacker_counts, "The Old Nobility");
    int atcktemplarorder = getCountForAllegiance(attacker_counts, "Templar Order");
    while (atckoldricholdnobles >= 4 && atcktemplarorder >= 1) {
        atckoldricholdnobles -= 4;
        atcktemplarorder -= 1;
        attackratio += 0.005;
    }



    int truesworn = getCountForAllegiance(target_counts, "Truesworn");
    int roundtables = getCountForAllegiance(target_counts, "The Round Table");
    while (truesworn >= 2 && roundtables >= 1) {
        truesworn -= 2;
        roundtables -= 1;
        attackratio -= 0.005;
    }


    int attackertruesworn = getCountForAllegiance(attacker_counts, "Truesworn");
    int attackerroundtables = getCountForAllegiance(attacker_counts, "The Round Table");
    while (attackertruesworn >= 2 && attackerroundtables >= 1) {
        attackertruesworn -= 2;
        attackerroundtables -= 1;
        attackratio += 0.005;
    }


    if (allegianceattacker == "Order of Fine Wine"){
        int richboys = getCountForAllegiance(attacker_counts, "Order of Silver") + getCountForAllegiance(attacker_counts, "Order of Fine Wine") + getCountForAllegiance(attacker_counts, "The Old Rich") + getCountForAllegiance(attacker_counts, "The New Rich");
        attackratio += richboys * 0.002;
    }

        if (allegiancetarget == "Order of Fine Wine"){
        int richboysdefence = getCountForAllegiance(target_counts, "Order of Silver") + getCountForAllegiance(target_counts, "Order of Fine Wine") + getCountForAllegiance(target_counts, "The Old Rich") + getCountForAllegiance(target_counts, "The New Rich");
        defendratio += richboysdefence * 0.002;
    }

    int oldguards = getCountForAllegiance(target_counts, "The Old Guard") + getCountForAllegiance(target_counts, " The Old Guard");
    while (oldguards >= 4) {
        targetflanks -= 1;
        oldguards -= 4;
    }


    int peasantorders = getCountForAllegiance(attacker_counts, "Peasant Order");
    while (peasantorders >= 7) {
        targetflanks += 1;
        peasantorders -= 7;
    }


    int farmersunions = getCountForAllegiance(target_counts, "Farmer's Union");
    while (farmersunions >= 7) {
        targetflanks -= 1;
        farmersunions -= 7;
    }

    int townsfolkvssupersoldier = getCountForAllegiance(target_counts, "Townsfolk") - 8 * getCountForAllegiance(attacker_counts, "Supersoldier");
    if (townsfolkvssupersoldier > 0) {
    attackratio -= 0.002 * townsfolkvssupersoldier;
    }

    if (allegiancetarget == "Order of Silver" || allegiancetarget == "The Old Rich" || allegiancetarget == "The New Rich" || allegiancetarget == "Order of Fine Wine") {
    int plunderingpeasantsvsknights = getCountForAllegiance(attacker_counts, "Plundering Peasants") - getCountForAllegiance(target_counts, "The Ancient Rights") - getCountForAllegiance(target_counts, "The Old Guard") - getCountForAllegiance(target_counts, " The Old Guard");
        if (plunderingpeasantsvsknights > 0) {
            attackratio += plunderingpeasantsvsknights * 0.002;
            }
    }


    if (continenttarget != continentattacker) {
        attackratio += 0.004 * getCountForAllegiance(attacker_counts, "Piratical Maniacs");
    }


    if(attackerlives == 1) {
    int attackersupersoldiers = getCountForAllegiance(attacker_counts, "Supersoldier");
    attackratio += 0.02 * attackersupersoldiers;
    }

    if(wartargetlives == 1) {
    int defendsupersoldiers = getCountForAllegiance(target_counts, "Supersoldier");
    defendratio += 0.02 * defendsupersoldiers;
    }

    if(wartargetlives == 1 && allegiancetarget == "Supersoldier"){
        defendratio += 0.04;
    }


   // The Planetator's Chosen, increased healing in combination with Chosen and Chosen Knights

    int planetatorschosen =  getCountForAllegiance(attacker_counts, "The Planetator's Chosen");
    int chosencount = getCountForAllegiance(attacker_counts, "Chosen");
    int chosenknights = getCountForAllegiance(attacker_counts, "Chosen knight");
    while (planetatorschosen > 0 && chosencount > 0 && chosenknights > 0){
        bonushealing += 40;
        planetatorschosen -= 1;
        chosencount -= 1;
        chosenknights -= 1;
    }
    while (chosencount > 0 && chosenknights > 0){
        bonushealing += 20;
        chosenknights -= 1;
        chosencount -= 1;
    }
    if (allegianceattacker == "The Planetator's Chosen"){
        bonushealing = bonushealing * 2;
    }



    distance -= goldencompasses_atck * 10 + asses_atck * 4 + goats_atck * 1 + chickens_atck * 2 + oxes_atck * 3 + beers_atck * 1 + stolenhorses_atck * 5;

    if (allegianceattacker == "Guardians of the Simulator"){
        distance = 0;
    }
    if (distance < 0) {
        distance = 0;
    }

    if (allegiancetarget == "Imperial family of Fa" && zcoordstarget > 500 && zcoordstarget < 1500){
        defendratio += 0.8;
    }

    if (allegianceattacker == "The gods") {
        attackratio += 0.5;
        bonushealing += 77;
        attackratio += marseshields_atck * 0.22;
    }

    if (allegiancetarget == "The gods") {
        defendratio += 0.5;
        defendratio += marseshields_def * 0.22;
    }

    if (allegianceattacker == "Knights of Rodrick") {
        bonushealing += bonushealing * ancientrelics;
    }
     if (allegiancetarget == "Knights of Rodrick" && wartargetlives == 1) {
        defendattack += attackerwarhp * 22;
        warattack += attackerwarhp * 22;
    }   
    if (allegianceattacker == "Knights of Rodrick" && wartargetlives == 1) {
        defendattack += attackerwarhp * 22;
        warattack += attackerwarhp * 22;
    }   

    if (allegianceattacker == "Crusading Order") {
    attackratio += distance * 0.002;
    }

    attackratio += getCountForAllegiance(attacker_counts, "Crusading Order") * distance * 0.00015 - getCountForAllegiance(target_counts, "Crusading Order") * distance * 0.00015;


    warattack = warattack * (1 - distance / 1500 );
    defendattack = defendattack;


    if (attackerflanks >= 5) {
        warattack = 0;
        defendattack = defendattack * 2;
    }
    else if (attackerflanks > 0){
        warattack = warattack * (1 - 0.2 * attackerflanks);
        defendattack = defendattack * (1 + attackerflanks * 0.2);
    }
    else {
        warattack = warattack;
        defendattack = defendattack;
    }

    if (targetflanks >= 5) {
        defendattack = 0;
        warattack = warattack * 2;
    }
    else if (targetflanks > 0){
        defendattack = defendattack * (1 - 0.2 * targetflanks);
        warattack = warattack * (1 + targetflanks * 0.2);
    }
    else {
        warattack = warattack;
        defendattack = defendattack;
    }


    double timeratio = 0.05;
    auto now = std::chrono::system_clock::now();
    // Convert the time point to milliseconds since Unix epoch
    auto timestamp = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count();
    std::cout << "Unix timestamp in milliseconds: " << timestamp << std::endl;
    double timedelta = timestamp - warstarted;
    std::cout << "Time Delta: " << timedelta << std::endl;

    if (timedelta > 2592000000){
        timeratio = 1;
    }
    else if (timedelta > 17000000){
        timeratio = (log(timedelta / 2592000000) / log(200)) + 1;
    }

    if (timecomputer_atck >= 1){
        timeratio = 1;
    }

    if (wartarget == attacker){
    warattack = 0;
    defendattack = 0;
    }
    else {
    warattack = warattack * attackratio * timeratio;
    defendattack = defendattack * defendratio;
    }


    } catch (const std::exception &e) {
        std::cerr << "Error: " << e.what() << std::endl;
        Struct errorResult;
        errorResult.dph = -1;
        errorResult.ddph = -1;
        return errorResult; // Return an error struct
    }


    Struct result; // Create a struct to return
    result.dph = warattack;
    result.ddph = defendattack;
    result.bonushealing = bonushealing;

    return result; // Return the result struct
}

int main() {
    // Establish a connection to the PostgreSQL database
    pqxx::connection conn("user=esse password=96509035 host=localhost port=5432 dbname=goldcastle");

    try {
        if (conn.is_open()) {
            std::cout << "Opened database successfully: " << conn.dbname() << std::endl;

            // Execute a query to select nftindex and warhp from nft_goldcastle_asia table
            pqxx::work txn(conn);
            pqxx::result result = txn.exec("SELECT * FROM nft_goldcastle_asia WHERE nftselfcontractaddress != wartarget AND nftselfcontractaddress = overlord AND killed = False ORDER BY nftindex DESC");


            // Iterate over the result and print nftindex and warhp for each row
            for (const auto& row : result) {
                std::cout << "NftIndex:" << row["nftindex"].as<int>() <<  "\n";

                int xcoordsattacker = row["xcoordinates"].as<int>(),
                    ycoordsattacker = row["ycoordinates"].as<int>(),
                    zcoordsattacker = row["zcoordinates"].as<int>(),
                    acoordsattacker = row["acoordinates"].as<int>();

                std::cout << "War HP: " << row["warhp"].as<int>() << std::endl;
                int warattack = row["warattack"].as<int>();

                std::string wartarget = row["wartarget"].as<std::string>();
                std::string attacker = row["nftselfcontractaddress"].as<std::string>();
                std::string allegianceattacker = row["allegiance"].as<std::string>();
                std::string itemattacker = row["item"].as<std::string>();
                std::string genderattacker = row["gender"].as<std::string>();

                std::string continentattacker = row["continent"].as<std::string>();

                std::string attackerwifeallegiance = row["wifeallegiance"].is_null() ? "" : row["wifeallegiance"].as<std::string>();

                int attackerlives = row["warlives"].as<int>();
                int attackerwarhp = row["warhp"].as<int>();

                double warstarted = row["warstarted"].as<double>();

                int attackerrarity = row["rarity"].as<int>();
                int magic = row["magic"].as<int>();

                pqxx::result target_result = txn.exec("SELECT * FROM nft_goldcastle_asia WHERE nftselfcontractaddress = " + txn.quote(wartarget));
            
                int xcoordstarget = target_result[0]["xcoordinates"].as<int>(),
                    ycoordstarget = target_result[0]["ycoordinates"].as<int>(),
                    zcoordstarget = target_result[0]["zcoordinates"].as<int>(),
                    acoordstarget = target_result[0]["acoordinates"].as<int>();

                std::string allegiancetarget = target_result[0]["allegiance"].as<std::string>();
                std::string itemtarget = target_result[0]["item"].as<std::string>();  
                std::string continenttarget = target_result[0]["continent"].as<std::string>();
                
                std::string targetwifeallegiance = target_result[0]["wifeallegiance"].is_null() ? "" : target_result[0]["wifeallegiance"].as<std::string>();

                int wartargetlives = target_result[0]["warlives"].as<int>();

                int defendattack = target_result[0]["warattack"].as<int>();



                Struct DamageResult = damage(genderattacker, attackerrarity, attackerwarhp, warstarted, attacker, warattack, xcoordsattacker, ycoordsattacker, zcoordsattacker, acoordsattacker, allegianceattacker, itemattacker, continentattacker, attackerwifeallegiance, attackerlives,
                                 wartarget, xcoordstarget, ycoordstarget, zcoordstarget, acoordstarget, allegiancetarget, itemtarget, defendattack, continenttarget, targetwifeallegiance, wartargetlives);
                
                int dph = DamageResult.dph;
                int ddph = DamageResult.ddph;
                int bonushealing = DamageResult.bonushealing;
                int totalhealing = (bonushealing + magic) * 44;

                std::cout << "Damage per Hour: " << dph << std::endl;
                std::cout << "Defending Damage per Hour: " << ddph << std::endl;
                std::cout << "Total Healing: " << totalhealing << std::endl;


                attackerwarhp += totalhealing - ddph;



                if (attackerwarhp < 0){
                    int newattackerlives = attackerlives;
                    int targetlivestaken = 1;
                    ddph -= attackerwarhp;
                    while(ddph > 0 && newattackerlives > 0) {
                        ddph -= attackerwarhp;
                        if (ddph >= 0){
                            targetlivestaken += 1;
                        }
                    newattackerlives = attackerlives - targetlivestaken;
                    }

                        int defenderkills = target_result[0]["kills"].as<int>();
                        // Increment kills by 1
                        defenderkills += targetlivestaken;
                        int newdefenderwarpower = ((warattack / 10) * targetlivestaken) + defendattack;



                            if (newattackerlives == 0) {
                                // Set killed to True for wartarget and decrement warlives
                                txn.exec("UPDATE nft_goldcastle_asia SET killed = true, warlives = " + txn.quote(newattackerlives) + " WHERE nftselfcontractaddress = " + txn.quote(row["nftselfcontractaddress"].as<std::string>()));
                                
                                xcoordsattacker = (xcoordsattacker + xcoordstarget) / 2;
                                ycoordsattacker = (ycoordsattacker + ycoordstarget) / 2;
                                zcoordsattacker = (zcoordsattacker + zcoordstarget) / 2;
                                acoordsattacker = (acoordsattacker + acoordstarget) / 2;

                                txn.exec("UPDATE nft_goldcastle_asia SET ycoordinates = " + txn.quote(ycoordsattacker) + ", xcoordinates = " + txn.quote(xcoordsattacker) + ", zcoordinates = " + txn.quote(zcoordsattacker) + ", acoordinates = " + txn.quote(acoordsattacker) + ", kills = " + txn.quote(defenderkills) + ", warattack = " + txn.quote(newdefenderwarpower) + " WHERE nftselfcontractaddress = " + txn.quote(wartarget));

                            } else {
                                txn.exec("UPDATE nft_goldcastle_asia SET warlives = " + txn.quote(newattackerlives) + " WHERE nftselfcontractaddress = " + txn.quote(row["nftselfcontractaddress"].as<std::string>()));
                                
                                txn.exec("UPDATE nft_goldcastle_asia SET kills = " + txn.quote(defenderkills) + ", warattack = " + txn.quote(newdefenderwarpower) + " WHERE nftselfcontractaddress = " + txn.quote(wartarget));
                            }



                        attackerwarhp = ddph * -1;
                }


                if (attacker != wartarget) {


                    /// Damage by attacker:
                    if (!target_result.empty()) {
                        pqxx::field warhp_field = target_result[0]["warhp"];
                        if (!warhp_field.is_null()) {
                            int warhp = warhp_field.as<int>();
                            int maxhp = target_result[0]["maxdefensivepower"].as<int>();
                            
                            if (warhp > 0) {
                                std::cout << "War HP for wartarget " << wartarget << ": " << warhp << std::endl;
                                                            
                                int newwarhp = warhp - dph;

                                    

                                    if (newwarhp <= 0) {
                                            int newwartargetlives = wartargetlives;
                                            int livestaken = 1;
                                            dph -= warhp;
                                            while(dph > 0 && newwartargetlives > 0) {
                                                dph -= maxhp;
                                                if (dph >= 0){
                                                    livestaken += 1;
                                                }
                                            newwartargetlives = wartargetlives - livestaken;
                                            }

                                            int kills = row["kills"].as<int>();
                                            // Increment kills by 1
                                            kills += livestaken;

                                            int defeatedwarpower = target_result[0]["warattack"].as<int>();
                                            int newwarpower = ((defeatedwarpower / 10) * livestaken) + warattack;


                                            if (newwartargetlives == 0) {
                                                // Set killed to True for wartarget and decrement warlives
                                                txn.exec("UPDATE nft_goldcastle_asia SET killed = true, warlives = " + txn.quote(newwartargetlives) + " WHERE nftselfcontractaddress = " + txn.quote(wartarget));
                                                
                                                xcoordsattacker = (xcoordsattacker + xcoordstarget) / 2;
                                                ycoordsattacker = (ycoordsattacker + ycoordstarget) / 2;
                                                zcoordsattacker = (zcoordsattacker + zcoordstarget) / 2;
                                                acoordsattacker = (acoordsattacker + acoordstarget) / 2;

                                                txn.exec("UPDATE nft_goldcastle_asia SET ycoordinates = " + txn.quote(ycoordsattacker) + ", xcoordinates = " + txn.quote(xcoordsattacker) + ", zcoordinates = " + txn.quote(zcoordsattacker) + ", acoordinates = " + txn.quote(acoordsattacker) + ", warhp = " + txn.quote(attackerwarhp) + ", kills = " + txn.quote(kills) + ", warattack = " + txn.quote(newwarpower) + " WHERE nftselfcontractaddress = " + txn.quote(row["nftselfcontractaddress"].as<std::string>()));

                                            } else {
                                                newwarhp = dph * -1;
                                                txn.exec("UPDATE nft_goldcastle_asia SET warhp = " + txn.quote(newwarhp) + ", warlives = " + txn.quote(newwartargetlives) + " WHERE nftselfcontractaddress = " + txn.quote(wartarget));
                                                
                                                txn.exec("UPDATE nft_goldcastle_asia SET warhp = " + txn.quote(attackerwarhp) + ", kills = " + txn.quote(kills) + ", warattack = " + txn.quote(newwarpower) + " WHERE nftselfcontractaddress = " + txn.quote(row["nftselfcontractaddress"].as<std::string>()));

                                            }

                                    } else {
                                    // Update the warhp in the database
                                    std::cout << "Attacking the wartarget " << row["nftselfcontractaddress"].as<std::string>() << std::endl;
                                    txn.exec("UPDATE nft_goldcastle_asia SET warhp = " + txn.quote(newwarhp) + " WHERE nftselfcontractaddress = " + txn.quote(wartarget));
                                    txn.exec("UPDATE nft_goldcastle_asia SET warhp = " + txn.quote(attackerwarhp) + " WHERE nftselfcontractaddress = " + txn.quote(row["nftselfcontractaddress"].as<std::string>()));
                                    }


                                

                            
                            } else {
                                std::cout << "Wartarget has already been killed" << wartarget << " HP is not greater than 0." << std::endl;
                                txn.exec("UPDATE nft_goldcastle_asia SET warhp = " + txn.quote(attackerwarhp) + " WHERE nftselfcontractaddress = " + txn.quote(row["nftselfcontractaddress"].as<std::string>()));
                            }

                            

                        } else {
                            std::cout << "Wartarget has been killed" << wartarget << "HP is NULL." << std::endl;
                            txn.exec("UPDATE nft_goldcastle_asia SET warhp = " + txn.quote(attackerwarhp) + " WHERE nftselfcontractaddress = " + txn.quote(row["nftselfcontractaddress"].as<std::string>()));

                        }
                    } else {
                        std::cout << "No matching warhp found for wartarget " << wartarget << std::endl;
                        txn.exec("UPDATE nft_goldcastle_asia SET warhp = " + txn.quote(attackerwarhp) + " WHERE nftselfcontractaddress = " + txn.quote(row["nftselfcontractaddress"].as<std::string>()));
                    }




                }
                else{
                txn.exec("UPDATE nft_goldcastle_asia SET warhp = " + txn.quote(attackerwarhp) + " WHERE nftselfcontractaddress = " + txn.quote(row["nftselfcontractaddress"].as<std::string>()));
                }


            }

            txn.commit();
            std::cout << "Transaction committed successfully." << std::endl;
        } else {
            std::cerr << "Failed to open database." << std::endl;
            return 1;
        }
    } catch (const std::exception &e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
