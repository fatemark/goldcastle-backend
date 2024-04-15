import pkg from 'pg';
const { Pool } = pkg;
import axios from 'axios';
import { groupOfAddress, NodeProvider, web3, subContractId, addressFromContractId, binToHex, contractIdFromAddress, hexToString, stringToHex, encodeByteVec, toApiByteVec, encodeU256, hexToBinUnsafe, encodeHexSignature } from '@alephium/web3';

const pool = new Pool({
    user: 'esse',
    host: 'postgres',
    database: 'goldcastle',
    password: '96509035',
    port: 5432,
  });

// const nodeProvider = new NodeProvider('http://localhost:22973');

web3.setCurrentNodeProvider("https://lb.notrustverify.ch/");
const nodeProvider = web3.getCurrentNodeProvider()

const marketplaceid = '1049eaa6d1660be75b8dd960d9d852ec0f2e06a5fc58a8d8df78534d39ac1600';
const marketplaceaddress = addressFromContractId(marketplaceid);

(async () => {
    const client = await pool.connect();
    try {


        //////////////////////////////////////////////////////////////////////////////////////////////////////
        const highestNumberQuery = 'SELECT MAX(eventcheckstartnumber) AS max_number FROM marketplaceeventlisteningcheck;';
        const highestNumberResult = await client.query(highestNumberQuery); 
        const highestNumber = highestNumberResult.rows[0].max_number - 1 || 0;  
            ////////////////////////////////////////////////////////////////////////////////////////////////////// set to 0 first time and comment out

            const step = 5 //give as argument //////////////////////////////////////////////////////////////////////////////////////////////////////

            let startnumber =  0 // highestNumber; ////////////////////////////////// 0 first run



            while (step == step) {

            const result = await nodeProvider.events.getEventsContractContractaddress(
                marketplaceaddress, { start: startnumber, limit: step }
            );

            // log result optional
            // const expandedresult = JSON.stringify(result, null, 2);
            
            const events = result.events;

            if (result.events.length == 0) {
                const timenow = parseInt(Date.now() / 1000)
                const saveEndNumberQuery = 'INSERT INTO marketplaceeventlisteningcheck (eventcheckstartnumber, time) VALUES ($1, $2)';
                await client.query(saveEndNumberQuery, [startnumber, timenow]);
                console.log('Inserted new event check numbers successfully');
                return
            }

            for (let event of events) {
                const eventIndex = event.eventIndex;
                const byteVecFields = event.fields.filter(field => field.type === 'ByteVec');
                const U256 = event.fields.filter(field => field.type === 'U256');
                const Address = event.fields.filter(field => field.type === 'Address');


                if (eventIndex == 0) {

                    const listingId = byteVecFields[0].value;
                    const nftId = byteVecFields[1].value;
                    const price = U256[0].value
                    const lister = Address[0].value

                    try {

                        await addListingToDatabase(price, listingId, nftId, lister);

                    } catch (error) {
                        console.log('failed to register new listing')
                        return
                    }
                }

                if (eventIndex == 1) {

                    const nftId = byteVecFields[0].value;
                    const price = U256[0].value

                    try {

                        const query1 = `
                        UPDATE marketplacelistings
                        SET bought = True
                        WHERE nftId = $1 AND bought IS NOT False
                    `;
                    await client.query(query1, [nftId]);
            


                    } catch (error) {
                        console.log('failed to register new buy')
                        return
                    }
                }


                if (eventIndex == 2) {

                    const nftId = byteVecFields[0].value;

                    try {
                        const query1 = `
                            UPDATE marketplacelistings
                            SET bought = False
                            WHERE nftId = $1 AND bought IS NOT TRUE
                        `;
                        await client.query(query1, [nftId]);

                    } catch (error) {
                        console.log('failed to register listing revocation')
                        return
                    }
                }


            }



            // event NewListing(nftId: ByteVec, price: U256, nftId: ByteVec, lister: Address)
            // event NewBuyListing(nftId: ByteVec, price: U256)
            // event RevokedListing(nftId: ByteVec)
        






            console.log(result.events.length)
            if (result.events.length == step) {
                startnumber += step
            } else{
                startnumber = startnumber + result.events.length
            try {
                const timenow = parseInt(Date.now() / 1000)
                const saveEndNumberQuery = 'INSERT INTO marketplaceeventlisteningcheck (eventcheckstartnumber, time) VALUES ($1, $2)';
                await client.query(saveEndNumberQuery, [startnumber, timenow]);
                console.log('Inserted new event check numbers successfully');
    
                } catch (error) {
                console.error('Error inserting new event check numbers:', error);
                return
                }
                return;
            }
                
        
        }
                } catch (error) {
                    //console.error('Error executing SQL query:', error.message);
                } finally {
                    client.release();
                    pool.end();
                }
        
            
})();




async function addListingToDatabase(price, listingId, nftId, lister) {
    const client = await pool.connect();
    try {
        if (nftId) {
            const timelisted = Date.now()
            const contractaddress = addressFromContractId(nftId)
            // Check if a row with the same contractAddress already exists
            const checkQuery = 'SELECT * FROM marketplacelistings WHERE listingid = $1 AND bought IS NULL';
            const checkResult = await client.query(checkQuery, [listingId]);
            
            // If a row with the same contractAddress exists, delete it
            if (checkResult.rows.length > 0) {
                const deleteQuery = 'DELETE FROM marketplacelistings WHERE listingid = $1 AND bought IS NULL';
                await client.query(deleteQuery, [listingId]);
                console.log(`Deleted existing row with contract address ${listingId}`);
            }

            const nftQuery = 'SELECT nfturi, item, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, potentialmarriage, unique_trait, members, wartargetname, wife, gender FROM nft_goldcastle_asia WHERE nftcontractid = $1';
            const nftResult = await client.query(nftQuery, [nftId]);
            
            if (nftResult.rows.length === 1) {
                const nftData = nftResult.rows[0];
                const { nfturi, item, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, potentialmarriage, unique_trait, members, wartargetname, wife, gender } = nftData;
            
                const finalQuery = 'SELECT name, allegiance, collection, nftindex, members, votingpower, maxpowerpotential, maxdefensivepower, wartargetname, rarity FROM nft_goldcastle_asia WHERE nftselfcontractaddress = $1';
                const finalResult = await client.query(finalQuery, [overlord]);
            
                if (finalResult.rows.length > 0) {
                    const finalResultData = finalResult.rows[0];
                    const { name: overlordname, allegiance: overlordallegiance, collection: overlordcollection, nftindex: overlordnftindex, members: overlordmembers, votingpower: overlordvotingpower, maxpowerpotential: overlordmaxpowerpotential, maxdefensivepower: overlordmaxdefensivepower, wartargetname: overlordwartargetname, rarity: overlordrarity } = finalResultData;
                                
                    const query = 'INSERT INTO marketplacelistings (nfturi, item, listingid, price, timelisted, nftid, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, wife, overlordname, overlordallegiance, overlordcollection, overlordnftindex, unique_trait, members, overlordmembers, overlordvotingpower, overlordmaxpowerpotential, overlordmaxdefensivepower, wartargetname, overlordwartargetname, overlordrarity, gender, lister) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31)';
                    await client.query(query, [nfturi, item, listingId, price, timelisted, nftId, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, wife, overlordname, overlordallegiance, overlordcollection, overlordnftindex, unique_trait, members, overlordmembers, overlordvotingpower, overlordmaxpowerpotential, overlordmaxdefensivepower, wartargetname, overlordwartargetname, overlordrarity, gender, lister]);
                
                } else {
                    console.log('Error: No matching record found in nft_goldcastle_asia table for the overlord.');
                }
            } else {
                console.log('Error: No matching record found in nft_goldcastle_asia table.');
            }
    }
    } catch (error) {
        console.error('Error adding to database:', error.message);
    } finally {
        client.release();
    }
}