import pkg from 'pg';
const { Pool } = pkg;
import { groupOfAddress, NodeProvider, web3, subContractId, addressFromContractId, binToHex, contractIdFromAddress, hexToString, stringToHex, encodeByteVec, toApiByteVec, encodeU256, hexToBinUnsafe, encodeHexSignature } from '@alephium/web3';
import axios from 'axios';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const pool = new Pool({
    user: 'esse',
    host: 'postgres',
    database: 'goldcastle',
    password: '96509035',
    port: 5432,
});

web3.setCurrentNodeProvider("https://lb.notrustverify.ch/");
const nodeProvider = web3.getCurrentNodeProvider();



async function updateBalances(tokensymbols, tokenids, tokenamount, decimals) {
    const client = await pool.connect();
    try {
        // Select all addresses from the goldowners table
        const addressesQuery = await client.query('SELECT owner, discordid FROM goldowners');

        // Iterate over each address and update gold balance
        for (const row of addressesQuery.rows) {
            const address = row.owner;
            const discordid = row.discordid;

            try {
                const balanceResult = await nodeProvider.addresses.getAddressesAddressBalance(address);

                const balanceresults = []
                let n = tokenamount - 1

                while ( n >= 0) {

                const balanceQuery = balanceResult.tokenBalances.find(token => token.id === tokenids[n]);
                let amount = balanceQuery ? balanceQuery.amount : 0;
              
                if (decimals[n] == 0) {
                  amount = parseInt(amount)
                } else {
                  amount = parseInt( amount / (10 ** decimals[n]))
                }

                await client.query(`UPDATE goldowners SET "${tokensymbols[n]}" = $1 WHERE owner = $2`, [amount, address]);
                n -= 1
                }
                console.log(`Updated TOKEN balances for address ${address} }`);


                const idsWithAmountOne = balanceResult.tokenBalances?.filter(token => token.amount === '1').map(token => token.id);

                const nftlength = idsWithAmountOne.length;
                n = nftlength - 1
                while ( n >= 0) {
                    await client.query(`UPDATE allnfts SET owner = $1, discordid = $2 WHERE nftcontractid = $3`, [address, discordid, idsWithAmountOne[n]]);
                    n -= 1
                }

            } catch (error) {
                console.error("Error fetching balances:", error);
                return 0;
            }

        }
    } catch (error) {
        console.error("Error updating balances:", error);
    } finally {
        client.release(); // Release the client back to the pool
    }
}


async function checkcolumns(tokensymbols, tokenamount) {
    const client = await pool.connect();
    try {
        let n = tokenamount - 1;
        while (n >= 0) {
            // Check if the column exists in the goldowners table
            const existsResult = await client.query('SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = $1 AND column_name = $2)', ['goldowners', tokensymbols[n]]);
            const exists = existsResult.rows[0].exists;

            if (!exists) {
                // If the column doesn't exist, add it to the table
                await client.query(`ALTER TABLE goldowners ADD COLUMN "${tokensymbols[n]}" BIGINT`);
                console.log(`Added column "${tokensymbols[n]}" to goldowners table`);
            }
            n -= 1
        }
    } catch (error) {
        console.log("Could not check columns", error);
    } finally {
        // Make sure to release the client back to the pool
        client.release();
    }
}




async function checknfttable() {
    const jsonFile = path.join(__dirname, '../jsondata/collections.json');
    let data = { tokens: [] };

    try {
        if (fs.existsSync(jsonFile)) {
            const fileContent = fs.readFileSync(jsonFile, 'utf8');
            data = JSON.parse(fileContent);
        }
    } catch (error) {
        console.error("Error reading or parsing collections.json:", error);
    }

    const collectionamount = data.collections.length;

    const supplies = []
    const collectionaddresses = []
    const collectionnames = []
    const baseuris = []

    let n = collectionamount - 1
    while (n >= 0) {

        collectionnames.push(data.collections[n].name)
        collectionaddresses.push(data.collections[n].address)
        supplies.push(data.collections[n].supply)
        baseuris.push(data.collections[n].baseuri)

        n -= 1
    }


    const client = await pool.connect();
    try {
        let n = collectionamount - 1;
        try {
            while (n >= 0) {
                // Check if the column exists in the goldowners table
                const existsResult = await client.query(`SELECT COUNT(*) AS count FROM allnfts WHERE collectionaddress = '${collectionaddresses[n]}'`);
                const count = existsResult.rows[0].count;
                
                console.log(count)
                if (count != supplies[n]) {
                    for (let index = 0; index < supplies[n]; index++) {
                        const indexResult = await client.query(
                            `SELECT COUNT(*) AS count FROM allnfts WHERE collectionaddress = $1 AND index = $2;`, 
                            [collectionaddresses[n], index]
                        );
                        const countforindex = indexResult.rows[0].count;
                        if (countforindex == 0) {
                            const attributetypes = []
                            const attributevalues = []
                            console.log(`${baseuris[n]}${index}`)
                            const response = await axios.get(`${baseuris[n]}${index}`);
                            const result = response.data;

                            const attributestobeaddedlength = result.attributes.length;
                            for (let attributecount = 0; attributecount < attributestobeaddedlength; attributecount++) {

                            attributetypes.push(result.attributes[attributecount].trait_type)
                            attributevalues.push(result.attributes[attributecount].value)
                            }

                            console.log(attributetypes)
                            console.log(attributevalues)
            
                            for (let uniques = 0; uniques < attributetypes.length; uniques++) {
                                const columnquery = `SELECT COUNT(*) FROM information_schema.columns WHERE table_name='allnfts' and column_name='${attributetypes[uniques]}'`;
                                const result = await client.query(columnquery);
                                const columncount = result.rows[0].count;                          
                                if (columncount == 0) {
                                const newcolumnquery = `ALTER TABLE allnfts ADD COLUMN "${attributetypes[uniques]}" VARCHAR(255);`;
                                await client.query(newcolumnquery);
                                }
                            }
                            

                            const trypath = encodeU256(index);
                            const group = 0;
                            const nftcontractid = subContractId(binToHex(contractIdFromAddress(collectionaddresses[n])), trypath, group);
                            
                            console.log(addressFromContractId(nftcontractid))

                            const query = `INSERT INTO allnfts (collectionaddress, collectionname, index, nftcontractid) VALUES ('${collectionaddresses[n]}', '${collectionnames[n]}', '${index}', '${nftcontractid}')`;
                            await client.query(query);
            
                            
                            for (let adds = 0; adds < attributestobeaddedlength; adds++) {
                                try {
                                await client.query(`UPDATE allnfts SET "${attributetypes[adds]}" = '${attributevalues[adds]}' WHERE index = '${index}' AND collectionaddress = '${collectionaddresses[n]}'`);
                                } catch {
                                    console.log("Failed to add trait: ", attributetypes[adds], " With value: ", attributevalues[adds], " For Collection: ", collectionnames[n])
                                }
                            }
                        }

                    }
                }
                n -= 1
            } 
        }   catch {
        console.log("Failed to add collection: ", collectionnames[n])
        }
    } catch (error) {
        console.log("Could not check columns", error);
    } finally {
        // Make sure to release the client back to the pool
        client.release();
    }

}


async function checkbalances() {
    const jsonFile = path.join(__dirname, '../jsondata/tokenlist.json');
    let data = { tokens: [] };

    try {
        if (fs.existsSync(jsonFile)) {
            const fileContent = fs.readFileSync(jsonFile, 'utf8');
            data = JSON.parse(fileContent);
        }
    } catch (error) {
        console.error("Error reading or parsing tokenlist.json:", error);
    }

    const tokenamount = data.tokens.length;
    const tokenids = []
    const tokensymbols = []
    const decimals = []

    let n = tokenamount - 1
    while (n >= 0) {

    tokensymbols.push(data.tokens[n].symbol)
    tokenids.push(data.tokens[n].id)
    decimals.push(data.tokens[n].decimals)
    n -= 1
    }

    await checkcolumns(tokensymbols, tokenamount);
    await checknfttable();

    updateBalances(tokensymbols, tokenids, tokenamount, decimals);
}


checkbalances();
